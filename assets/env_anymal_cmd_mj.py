import numpy as np
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation
import mujoco_viewer
from pyquaternion import Quaternion
import os

from .env_base_mj import EnvBaseMJ
from utils.terrain import Terrain, TerrainGen
from utils.xml_helper import indent_xml
from lxml import etree
import shutil


## CONSTANTS ##
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

        # dimensions of entire ground truth 
        self.ground_truth_dim = (500, 500) # image - (i, j)
        self.mj_ground_truth_dim = (10, 10) # mj - x_rad, y_rad

        #dimensions of the height map sub-section the robot 'sees'
        self.sub_sec_dim = (80, 80) 
        self.mj_sub_sec_dim = (self.mj_ground_truth_dim[0] / (self.ground_truth_dim[0] / self.sub_sec_dim[0]),  
                               self.mj_ground_truth_dim[1] / (self.ground_truth_dim[1] / self.sub_sec_dim[1]))
        
        # current waypoint position
        self.waypoint_pos = None
        self.mj_waypoint_pos = None
        
        # array of Terrain objects loaded into the environment
        self.terrains = []
        # self.setup_terrain_xmls("test_terr.xml")

        if self.args.add_terrain:
            self.terrain_generator = TerrainGen()
            self.load_terrain_images()
        
        self.load_robot()
    
        self.taking_cmds = True # just if I want to use brendan's waking gate (remove when done)

        if self.taking_cmds:
            self.ob_size = 54
        else:
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

        self.map_count = 0

        # States that we want to restore, for resuming training after running a test
        # self.states_to_restore = ["pos", "orn", "joints", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

    def load_terrain_images(self):
        """
        Generates any images we want to load into mujoco as terrain for the 
        robot to traverse.
        """
        # generate and load ground truth image
        gt_arr = self.terrain_generator.gen_rand_ground_truth(0, 255, self.ground_truth_dim)
        self.ground_truth = Terrain(gt_arr, self.mesh_dir, "ground_truth.png")
        self.terrains.append(self.ground_truth)

        # generate and load other curves
        fn = self.terrain_generator.hump_func
        curve = self.terrain_generator.gen_curve(-5, 5, 5, 5, 500, fn)
        self.curve1 = Terrain(curve, self.mesh_dir, "curve1.png")
        self.terrains.append(self.curve1)
    
    def show_map(self, show_waypoint=True):
        """
        Displays a birds-eye map of the ground truth the robot is traversing.
        Also draws a bounding box around the robot's sub-section (image
        the policy is fed)
        """
        img_copy = self.ground_truth.terr_img.copy()
        box_centre = self.ground_truth.rob_to_img_pos(self.pos, 10, 10) 
        Terrain.draw_bounding_box(img_copy, box_centre, self.sub_sec_dim[0], self.sub_sec_dim[1])
        if show_waypoint:
            Terrain.draw_dot(img_copy, self.mj_waypoint_pos)
        Terrain.display_img(img_copy)
    
    def gen_new_waypoint(self):
        """
        Generates a random waypoint within the robot's sub-section
        """
        rand_x = np.random.uniform(low=self.pos[0]-self.mj_sub_sec_dim[0], high=self.pos[0]+self.mj_sub_sec_dim[0])
        rand_y = np.random.uniform(low=self.pos[1]-self.mj_sub_sec_dim[1], high=self.pos[1]+self.mj_sub_sec_dim[1])
        self.waypoint_pos = (rand_x, rand_y)
        self.mj_waypoint_pos = self.ground_truth.rob_to_img_pos(self.waypoint_pos, 10, 10)
    
    def setup_terrain_xmls(self, file_name):
        """
        Creates and populates a terrain xml file
        """
        # set up mujoco xml backbone
        boiler_plate = os.path.join(self.general_xml_path, "empty.xml")
        file = os.path.join(self.general_xml_path, file_name)
        shutil.copy(boiler_plate, file)

        xml = etree.parse(file)
        root = xml.getroot()
        compiler = etree.SubElement(root, "compiler", attrib={
            "assetdir":"assets"
        })

        # define assets
        asset = etree.SubElement(root, "asset")
        gt = etree.SubElement(asset, "hfield", attrib={
            "name":"ground_truth"
        })

        # define worldbody stuff
        wb = etree.SubElement(root, "worldbody")
        gt = etree.SubElement(wb, "geom", attrib={
            "name":"gt"
        })

        indent_xml(root)
        xml.write(file)
    
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
        # Success is time spent above a target goal
        return len(self.goal) > 100 and np.mean(self.goal) > 1.0


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
            # self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), np.pi], degrees=False)
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

        self.command_ranges = np.array([1,1,1.5])
        self.commands = list(np.random.uniform(-self.command_ranges, self.command_ranges))
        self.time_at_speed = 0
        self.goal = []

        self.prev_actions = self.joints
        if self.taking_cmds:
            state = self.imu + self.commands + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        else:
            state = self.imu + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        return state

    def step(self, actions=None, replay_state=None, additional_stuff=None, cmds=None):
        """
        TODO: make a self.args.show_map argument
        we want to be able to show the map, bounding boxes and waypoints even if 
        person is not using ground truth

        -means we need a map to show people if they haven't loaded in any terrain
        (empty image)
        -which in turn means we need the auto xml load thing
        """
        if self.args.add_terrain:
            if self.steps % 100 == 0:
                self.gen_new_waypoint()
            self.show_map(show_waypoint=True)
            
        if cmds is not None:
            self.commands = cmds
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
            if self.traj_i < self.traj_size - 1:
                self.traj_i += 1

        if actions is not None:
            self.actions = list(np.array(self.initial_joints) + np.array(actions))
        else:
            self.actions = self.initial_joints

        if self.args.cur:
            # Sample every 4 seconds
            if self.steps > 0 and self.steps % int(4 / self.timeStep)==0:
                self.commands = list(np.random.uniform(-self.command_ranges, self.command_ranges))
                self.success.append(self.get_success())
                self.time_at_speed = 0
                self.goal = []

            world_to_robot_rot_mat = np.array(
            [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
                [np.sin(-self.yaw), np.cos(-self.yaw), 0],
                [		0,			 0, 1]]
            )

            # Need to convert robot frame velocities and commands to world frame to apply forces
            robot_to_world_rot_mat = np.array(
            [[np.cos(-self.yaw), np.sin(-self.yaw), 0],
                [-np.sin(-self.yaw), np.cos(-self.yaw), 0],
                [		0,			 0, 1]]
            )

            vx_cmd, vy_cmd, _ = np.dot(robot_to_world_rot_mat, (self.commands[0], self.commands[1],0))
            vx, vy, _ = np.dot(robot_to_world_rot_mat, (self.vx, self.vy, self.vz))
            
            forces = np.zeros(6)
            error = np.abs(np.array(self.commands) - np.array([self.vx, self.vy, self.yaw_vel]))
            
            # This doesn't seem to work, instead using average goal reward
            if (error < 0.3).all():
                self.time_at_speed += 1
            gain = 50
            z_gain = 200
            forces[0] = gain * (self.Kp / self.initial_Kp) * np.clip((vx_cmd - vx), -1, 1)
            forces[1] = gain * (self.Kp / self.initial_Kp) * np.clip((vy_cmd - vy), -1, 1)
            forces[2] = z_gain * (self.Kp / self.initial_Kp) * np.clip((0.5 - self.pos[2]), -1, 1)
            forces[5] = gain * (self.Kp / self.initial_Kp) * np.clip((self.commands[2] - self.yaw_vel), -1, 1)
            self.data.xfrc_applied = forces

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

        if self.taking_cmds:
            state = self.imu + self.commands + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        else:
            state = self.imu + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        return np.array(state), reward, done, None
    
    def get_reward(self):
        done = False
        if self.pos[2] < 0.35 or abs(self.pitch) > 0.5 or abs(self.roll) > 0.5:
            done = True
        
        goal = 1.0*np.exp(-5.0*np.sum(np.array(self.commands[:2]) - np.array([self.vx, self.vy]) )**2)            
        goal += 0.5*np.exp(-2.5*np.sum(np.array(self.commands[2]) - np.array(self.yaw_vel) )**2)     
        self.goal.append(goal)

        joints = np.exp(-0.5*np.sum((np.array(self.joints) - np.array(self.initial_joints))**2))
        orn = np.exp(-10.0 * np.sum((np.array([self.roll, self.pitch]) - np.zeros(2))**2))
        
        # Contacts should match pair-wise. both front's should be off the ground, both backs shouldn't
        contacts = 0.25*(self.contacts["left_front"] - self.contacts["right_back"])**2 
        contacts += 0.25*(self.contacts["right_front"] - self.contacts["left_back"])**2 
        contacts += 0.25*((1 - self.contacts["left_front"]) - self.contacts["right_front"])**2 
        contacts += 0.25*((1 - self.contacts["left_back"]) - self.contacts["right_back"])**2 

        # reward = 1.5*goal + 0.5*joints + 0.25*orn - 0.25*contacts
        reward = 1.5*goal + 0.5*joints + 0.1*orn - 0.25*contacts
        
        # old
        # reward = 1.5*goal + 0.1*joints + 0.1*orn - 0.1*contacts

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
        self.vx, self.vy, self.vz = self.data.sensordata[3:6]
        self.yaw_vel = self.data.sensordata[2]

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