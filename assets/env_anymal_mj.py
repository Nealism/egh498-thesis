import numpy as np
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation
import mujoco_viewer
from pyquaternion import Quaternion
import glfw

from .env_base_mj import EnvBaseMJ
from utils.terrain_gen import TerrainGen

class Env(EnvBaseMJ):
    # Timestep for mujoco is set in the .xml, and shows up under self.model.opt.timestep
    # Default is 0.002, changing this might affect the contact model. 
    simStep = 1/500
    timeStep = 1/100
    rank = comm.Get_rank()
    Kp = 400
    initial_Kp = Kp
    def __init__(self, PATH=None, args=None, writer=None):

        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True 

        super().__init__(PATH)

        self.general_xml_path = "assets/xmls/anybotics_anymal_c/"

        # Name of the base link in the xml, for setting the robot position on reset
        self.base_link = "base"
        if self.args.control_type == "torque":
            self.model_path = self.general_xml_path + "scene_torque.xml"
            self.action_multiplier = 20
        elif self.args.control_type == "position":
            self.model_path = self.general_xml_path + "scene.xml"
            self.action_multiplier = 0.2

        self.robot_name = "anymal_c"
        self.mesh_dir = self.general_xml_path + "assets/"
        # self.action_multiplier = 0.0
        
        if self.args.tree_type:
            self.set_up_xmls()
        
        self.viewer = None

        self.terrain_gen = TerrainGen()
        self.load_terrain_images()
        self.load_robot()
        
        self.ob_size = 51
        self.ac_size = 12

        self.motor_names = ['LF_HAA', 'LF_HFE', 'LF_KFE', 'RF_HAA', 'RF_HFE', 'RF_KFE', 'LH_HAA', 'LH_HFE', 'LH_KFE', 'RH_HAA', 'RH_HFE', 'RH_KFE']
        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        # left front, right front, left back, right back
        self.initial_joints = [-0.2,0.6,-1.0, 0.2,0.6,-1.0, -0.2,-0.6,1.0, 0.2,-0.6,1.0]
        self.right_swing = [-0.2,0.0,-0.8, 0.2,1.0,-1.0, -0.2,-0.4,1.0, 0.2,-1.0,0.0]
        self.left_swing = [-0.2,1.0,-1.0, 0.2,0.0,-0.8, -0.2,-1.0,0.0, 0.2,-0.4,1.0]

        self.initial_z = 0.7

        self.episodes = -1
        self.success = deque([0.0], maxlen=5)
        self.target_radius = 0.12
        self.sim_data = []
        self.best_return = 0

        # Reachibility parameters
        self.reach_centre = [0.174, 0, 0.501]
        self.dist_max = 0.55
        self.dist_min = 0.3
        self.reach_theta_max = 1.5
        self.reach_theta_min = -1.5
        self.reach_pitch_max = 1.5
        self.reach_pitch_min = 0
        self.steps = 0

        self.reward_names = ["Reward/goal", "Reward/joint", "Reward/orn", "Reward/contacts"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        # States that we want to restore, for resuming training after running a test
        # self.states_to_restore = ["pos", "orn", "joints", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

    def load_terrain_images(self):
        # generate and load ground truth image
        dim = (100, 100)
        gt = self.terrain_gen.gen_rand_ground_truth(0, 255, dim)
        # gt = np.ones(dim)
        # gt[60:80, 75] = 2
        self.terrain_gen.load_im_from_arr_2(gt, self.mesh_dir, "test.png", "PNG")

        # generate and load other curves
        fn = self.terrain_gen.hump_func
        # fn = self.terrain_gen.gaussian
        curve = self.terrain_gen.gen_curve(0, 5, 0, 5, 500, fn)
        self.terrain_gen.load_im_from_arr_2(curve, self.mesh_dir, "smooth.png", "PNG")

    def load_robot(self):
        if not self.args.replay and self.args.tree_type:
            if self.args.tree_type == "grass":
                self.generate_tree(radius=0.02, height=0.4, damping=1, stiffness=2, pos=[0,0,0],rot=[1,0,0,0], num=200, segs_per_branch=4, spread=[[1.0, 7.0],[-1, 1]], z_height=-0.05)
            elif self.args.tree_type == "tree":
                self.generate_tree(spread=[[1.0, 2.0],[-0.2, 0.2]])

        self.model = mujoco.MjModel.from_xml_path(self.model_path)
        self.data = mujoco.MjData(self.model)

        # Mujoco_viewer doesn't work on the hpc, shouldn't render there anyway
        if not self.args.training_on_hpc:
            if isinstance(self.viewer, mujoco_viewer.MujocoViewer):
                # Replace model and data of an existing viewer
                self.viewer.model = self.model
                self.viewer.data = self.data
            elif self.render:
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data)
            else:
                # Offscreen might help getting images?
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data, 'offscreen')
        else:
            print("Can't view mujoco on the HPC.")
        
    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        return_dict = {"Kp": self.Kp, "Success": self.success, "Cur": self.args.cur}
        return_dict.update(self.reward_dict)
        return return_dict

    def get_success(self):
        return self.pos[0] > 10

    def check_for_success(self):
        return len(self.success) == 5 and (np.array(self.success) == True).all()

    def reset(self, test=False, model_path=None, restore_state=None):

        if self.steps > 0:
            for key in self.reward_dict:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        if self.episodes > -1:
            self.success.append(self.get_success())
            target = None
            if self.args.tree_type:
                self.save_tree(best=self.total_return > self.best_return, test=test)
            self.record_sim_state(best=self.total_return > self.best_return, test=test, additional_arguments=target)
            if self.total_return > self.best_return:
                self.best_return = self.total_return
        self.total_return = 0
        self.paused = True

        if self.args.cur and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
                self.args.cur = False
            self.success = deque([0.0], maxlen=5)
        
        if model_path is not None:
            self.model_path = model_path 
        if self.args.tree_type or model_path is not None:
            self.load_robot()

        mujoco.mj_resetData(self.model, self.data)

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            # Rotate the base of the robot to simulate being on the back of a titan
            rot_range = 0.2
            # rot_range = 0.0
            self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), 0], degrees=False)
            self.orn = self.rot.as_quat()
            self.pos = [0,0,self.initial_z]
            self.set_position(pos=self.pos, orn=self.orn, joints=self.initial_joints)

        self.steps = 0
        self.episodes += 1

        # Step the simulation once to get the initial state
        mujoco.mj_forward(self.model, self.data)
        self.get_observation()

        # Maybe randomise which legs swing first?
        self.current_swing = "right"
        self.expert_target = self.right_swing if self.current_swing == "right" else self.left_swing
        self.get_trajectory(self.expert_target)

        self.prev_actions = self.joints
        state = self.imu + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        return state

    def step(self, actions=None, replay_state=None, additional_stuff=None):
        print(self.pos)
        if self.paused:
            self.target_vx = 0.0
            expert = self.initial_joints    
        else:
            self.target_vx = 1.0
            if self.steps % self.traj_size == 0:
                self.current_swing = "right" if self.current_swing == "left" else "left"
                self.expert_target = self.right_swing if self.current_swing == "right" else self.left_swing
                self.get_trajectory(self.expert_target)
            expert = self.expert_traj[self.traj_i]
            # expert = self.expert_target
            if self.traj_i < self.traj_size - 1:
                self.traj_i += 1

        if actions is not None:
            self.actions = list(actions)
        else:
            self.actions = [0]*(self.ac_size)

        # This might do something weird with mujoco contacts, and other things in the sim.
        for _ in range(int(np.rint(self.timeStep/self.simStep))):

            # self.set_position(pos=[0,0,0.5], orn=[0,0,0,1])

            if replay_state is not None:
                self.set_position(pos=replay_state[0], orn=replay_state[1])
            else:            
                if self.args.cur:
                    if self.args.just_expert:
                        self.data.ctrl[:self.ac_size] = (self.Kp / self.initial_Kp)*np.array(expert)
                    else:
                        self.data.ctrl[:self.ac_size] = self.action_multiplier*np.array(self.actions) + (self.Kp / self.initial_Kp) * np.array(expert)
                else:
                    self.data.ctrl[:self.ac_size] = self.action_multiplier*np.array(self.actions)
                            
            mujoco.mj_step(self.model, self.data)
        
        if self.render:
            self.viewer.render()

        self.get_observation()

        self.save_sim_state()
        reward, done = self.get_reward()
        self.prev_actions = self.actions
        self.total_return += reward
        self.steps += 1

        state = self.imu + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        return np.array(state), reward, done, None
    
    def get_reward(self):
        done = False
        # done if: below 0.3m, 'pitching' more than 0.7 rads, 'rolling' more than 0.7 rads
        if self.pos[2] < 0.3 or abs(self.pitch) > 0.7 or abs(self.roll) > 0.7:
            done = True

        # error in forward velocity (this is main component of reward function)
        goal = np.exp(-2.5*max(0, self.target_vx - self.data.joint("free").qvel[0])**2)
        # sum of squared errors in joint positions w.r.t to initial positions 
        joints = np.exp(-0.5*np.sum((np.array(self.joints) - np.array(self.initial_joints))**2))
        # error in rotation w.r.t. to upright quaternion
        orn = np.exp(-10.0 * Quaternion.absolute_distance(Quaternion(self.orn), Quaternion([0,0,0,1])))
        
        # Contacts should match pair-wise. both front's should be off the ground, both backs shouldn't
        contacts = 0.25*(self.contacts["left_front"] - self.contacts["right_back"])**2 
        contacts += 0.25*(self.contacts["right_front"] - self.contacts["left_back"])**2 
        contacts += 0.25*((1 - self.contacts["left_front"]) - self.contacts["right_front"])**2 
        contacts += 0.25*((1 - self.contacts["left_back"]) - self.contacts["right_back"])**2 
                
        # orn = 0.1*np.exp(-5*np.sum((np.array(self.orn) - np.array([0,0,0,1]))**2))

        # NOTE: all components of rew. func. are negative (just doesn't look like it here, SEE ABOVE)
        reward = 1.5*goal + 0.5*joints + 0.25*orn - 0.25*contacts
        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/joint"] += joints
        self.ep_reward_dict["Reward/orn"] += orn
        self.ep_reward_dict["Reward/contacts"] += contacts
        return reward, done

    def get_observation(self):
        # Keep an eye on these to make sure they are getting what you think)
        self.pos = self.data.body(self.base_link).xpos.copy()
        orn = self.data.body(self.base_link).xquat.copy()
        self.orn = [orn[1],orn[2],orn[3],orn[0]]

        rot = Rotation(self.orn)
        self.roll, self.pitch, self.yaw = rot.as_euler('xyz', degrees=False)
        self.imu = [self.roll, self.pitch] + list(self.data.sensordata) 
        self.joints = [self.data.joint(name).qpos[0] for name in self.motor_names]
        self.joint_vel = [self.data.joint(name).qvel[0] for name in self.motor_names]
        self.joint_force = list(self.data.actuator_force[:self.ac_size])

        # Should be an easier way to get a specific contact?
        self.feet = ["left_front", "right_front", "left_back", "right_back"]
        contact_list = self.data.contact
        # self.contacts = [0] * len(self.feet)
        self.contacts = {foot:0 for foot in self.feet}
        for dim, contact1, contact2 in zip(contact_list.dim, contact_list.geom1, contact_list.geom2):
            if dim:
                geom_name1 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact1)
                geom_name2 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact2)
                if geom_name1 in self.feet:
                    # self.contacts[self.feet.index(geom_name1)] = 1
                    self.contacts[geom_name1] = 1
                elif geom_name2 in self.feet: 
                    # self.contacts[self.feet.index(geom_name2)] = 1
                    self.contacts[geom_name2] = 1

        if self.steps > 20 and np.array(self.contacts).all():
            # For some reason all feet are in contact on reset even when not touching the ground
            self.paused = False

    def get_trajectory(self, expert):
        # Extrapolate trajectory based on max_joint_vel
        max_joint_difference = 0  
        for joint, expert_joint in zip(self.joints, expert):
            if abs(joint - expert_joint) > max_joint_difference:
                max_joint_difference = abs(joint - expert_joint)
       
        # What number of trajectory points do we need to travel the max distance at a set velocity
        self.traj_size = int(np.rint(max_joint_difference / self.args.max_joint_vel / self.timeStep))
        self.expert_traj = []
        for i in range(self.traj_size):
            points = []            
            for j in range(len(self.joints)):
                point = i * ( (expert[j] - self.joints[j]) / self.traj_size ) + self.joints[j]
                points.append(point)
            self.expert_traj.append(points)
        self.traj_i = 0    