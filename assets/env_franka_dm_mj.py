import numpy as np
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation
from pyquaternion import Quaternion

from .env_base_mj import EnvBaseMJ

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
        if self.args.control_type == "torque":
            self.model = mujoco.MjModel.from_xml_path("assets/xmls/franka_emika_panda/scene_torque.xml")
            self.action_multiplier = 10.0
        else:
            self.model = mujoco.MjModel.from_xml_path("assets/xmls/franka_emika_panda/scene.xml")
            self.action_multiplier = 1.0
        self.data = mujoco.MjData(self.model)
        
        # Mujoco_viewer doesn't work on the hpc, shouldn't render there anyway
        if not args.training_on_hpc:
            import mujoco_viewer
            if self.render:
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data)
            else:
                # Offscreen might help getting images?
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data, 'offscreen')
        else:
            self.viewer = None
            print("Can't view mujoco on the HPC.")

        self.ob_size = 36
        self.ac_size = 7

        self.motor_names = ['joint' + str(n + 1) for n in range(self.ac_size)]
        
        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

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

        # Name of the base link in the xml, for setting the robot position on reset
        self.base_link = "link0"

        # States that we want to restore, for resuming training after running a test
        self.states_to_restore = ["pos", "orn", "joints", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        return {"Kp": self.Kp, "Success": self.success, "Cur": self.args.cur}

    def get_success(self):
        return np.sqrt(np.sum((np.array(self.end_effector[:3]) - np.array(self.target_point))**2)) < 0.1 and \
               Quaternion.absolute_distance(Quaternion(self.end_effector[3:]), Quaternion(self.target_orn)) < 0.1

    def check_for_success(self):
        return len(self.success) == 5 and (np.array(self.success) == True).all()

    def reset(self, test=False):

        if self.episodes > -1:
            self.success.append(self.get_success())
            target = self.target + self.target_point 
            self.record_sim_state(best=self.total_return > self.best_return, test=test, additional_arguments=target)
            if self.total_return > self.best_return:
                self.best_return = self.total_return
        self.total_return = 0

        if self.args.cur and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
                self.args.cur = False
            self.success = deque([0.0], maxlen=5)

        mujoco.mj_resetData(self.model, self.data)

        # Same as the titan
        self.initial_joints = [0.0, -1.3439, 0.0,  -2.8100, 0.0, 1.4835, 0.785, 0.0] 

        # Rotate the base of the robot to simulate being on the back of a titan
        rot_range = 0.2
        # rot_range = 0.0
        self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), 0.0], degrees=False)
        self.orn = self.rot.as_quat()
        self.pos = [0,0,0]
        self.set_position(pos=self.pos, orn=self.orn, joints=self.initial_joints)
        
        self.steps = 0
        self.episodes += 1

        # Step the simulation once to get the initial state
        mujoco.mj_forward(self.model, self.data)
        
        self.get_observation()
        self.initial_end_effector = self.end_effector
        self.get_target()
        self.prev_actions = self.joints + [0]
        self.expert = self.get_expert()

        # On the real robot everything will be in base link frame, need to rotate end effector and target points by the initial base rotation
        new_target_rot = list((Rotation.from_quat(self.target_orn) * self.rot).as_quat())
        new_end_effector_rot = Rotation.from_quat(self.end_effector[-4:]) * self.rot
        new_end_effector = list(self.rot.apply(self.end_effector[:3])) + list(new_end_effector_rot.as_quat())
        new_target_point = list(self.rot.apply(self.target_point)) 
        state = self.joints + self.joint_vel + self.joint_force + new_end_effector + new_target_point + new_target_rot
        return state

    def step(self, actions=None, replay_state=None, target=None, target_point=None, target_point2=None):
        if actions is not None:
            self.actions = list(actions) + [0]
        else:
            self.actions = [0]*(self.ac_size + 1)

        self.exp_joints = self.expert_traj[self.traj_i]
        self.exp_end_effector = self.expert_end_effector_traj[self.traj_i]

        if replay_state is not None:
            if not self.args.use_ball:
                self.set_target(target, target_point)
            self.set_position(joints=replay_state[2])
        else:
            if self.render:
                if not self.args.use_ball:
                    self.set_target(self.target, self.target_point)
            
            if self.args.cur: 
                if self.args.control_type == "torque":
                    expert = 80 * (np.array(self.exp_joints + [0]) - np.array(self.joints + [0])) - 2.0 * np.array(self.joint_vel + [0])
                elif self.args.control_type == "position":
                    expert = np.array(self.exp_joints + [0])
               
                if self.args.just_expert:
                    self.data.ctrl[:] = ((self.Kp / self.initial_Kp ) * expert)[:]
                else:
                    self.data.ctrl[:] = self.action_multiplier*np.array(self.actions) +  (self.Kp / self.initial_Kp) * expert
                    
                if self.traj_i < self.traj_size - 1:
                    self.traj_i += 1
            else:
                self.data.ctrl[:] = self.action_multiplier*np.array(self.actions)
        
        if self.render:
            self.viewer.render()
        for _ in range(int(np.rint(self.timeStep/self.simStep))):
            mujoco.mj_step(self.model, self.data)

        # self.data.ncon == 0
        self.get_observation()

        self.save_sim_state()
        reward, done = self.get_reward()
        self.prev_actions = self.actions
        self.total_return += reward
        self.steps += 1

        # Rotate end effector and targets to be in base_link frame
        new_target_rot = list((Rotation.from_quat(self.target_orn) * self.rot).as_quat())
        new_end_effector_rot = Rotation.from_quat(self.end_effector[-4:]) * self.rot
        new_end_effector = list(self.rot.apply(self.end_effector[:3])) + list(new_end_effector_rot.as_quat())
        new_target_point = list(self.rot.apply(self.target_point)) 
        state = self.joints + self.joint_vel + self.joint_force + new_end_effector + new_target_point + new_target_rot
        return np.array(state), reward, done, None
    
    def get_reward(self):
        done = False
        if self.args.use_ball:
            reward = 1.0
            if self.target[2] < 0.3:
                done = True
        else:
            end_effector = np.exp(-5.0*np.sum((np.array(self.end_effector[:3]) - np.array(self.exp_end_effector))**2))
            orn = np.exp(-5.0 * Quaternion.absolute_distance(Quaternion(self.end_effector[3:]), Quaternion(self.target_orn)))
            # Probably don't need to try and copy the expert joints
            joints = np.exp(-2.0*np.sum((np.array(self.joints) - np.array(self.exp_joints))**2))
            joint_vel = 0.05 * np.exp(-0.1*np.sum(np.array(self.joint_vel)**2))
            action = -0.02 * np.sum((np.array(self.actions) - np.array(self.prev_actions))**2)
            reward = end_effector + orn + action + joint_vel 
        return reward, done

    def close(self):
        self.viewer.close()
    
    def get_observation(self):
        # Keep an eye on these to make sure they are getting what you think
        self.end_effector = list(self.data.body('hand').xipos) 
        rot = Rotation.from_matrix(np.array(self.data.body('hand').ximat).reshape(3,3))
        self.end_effector += list(rot.as_quat())

        self.joints = [self.data.joint(name).qpos[0] for name in self.motor_names]
        self.joint_vel = [self.data.joint(name).qvel[0] for name in self.motor_names]
        self.joint_force = list(self.data.actuator_force)

    def get_target(self):
        if self.args.use_ball:
            dist, angle = np.random.uniform(0.2, 0.4), np.random.uniform(-0.5, 0.5)
            self.target = [dist*np.cos(angle), dist*np.sin(angle), 2.0]
            self.target_point = [0,0,0] 
            self.data.set_joint_qpos("ball", self.target + [1.0, 0, 0, 0])
        else: 
            # Get the target position from the reach centre (same parameters as refarm)
            self.dist = np.random.uniform(self.dist_min, self.dist_max)
            self.reach_theta = np.random.uniform(self.reach_theta_min, self.reach_theta_max)
            # self.reach_theta = np.pi/2
            self.reach_pitch = np.random.uniform(self.reach_pitch_min, self.reach_pitch_max)

            self.target = [0] * 3
            self.target[0] = self.reach_centre[0] + self.dist * np.cos(self.reach_theta) * np.sin(self.reach_pitch)
            self.target[1] = self.reach_centre[1] + self.dist * np.sin(self.reach_theta) * np.sin(self.reach_pitch)
            self.target[2] = self.reach_centre[2] + self.dist * np.cos(self.reach_pitch)    

            # This is the rotation from reach centre to an effector pose with a horizontal camera (from refarm/moveit_interface)
            # Eigen::Quaterniond q_orig = Eigen::AngleAxisd(yaw, Eigen::Vector3d::UnitZ()) *
            #                             Eigen::AngleAxisd(-((M_PI / 2) - inv_pitch), Eigen::Vector3d::UnitY()) *
            #                             Eigen::AngleAxisd(0.0, Eigen::Vector3d::UnitX());

            # Eigen::Quaterniond q_rot = Eigen::AngleAxisd(M_PI, Eigen::Vector3d::UnitX()) *
            #                             Eigen::AngleAxisd(0.5 * M_PI, Eigen::Vector3d::UnitY()) *
            #                             Eigen::AngleAxisd(0.25 * M_PI, Eigen::Vector3d::UnitZ());

            # q_orig = (q_orig * q_rot).normalized();


            self.q_rot = Rotation.from_euler('xyz', [0, np.pi, 0], degrees=False)

            # Get the target point in rotation link (same as reach centre, with x back on rotation joint)
            base_point = [0.0, 0.0, self.reach_centre[2]]
            dist_from_base = np.sqrt((self.target[0] - base_point[0])**2 +
                                     (self.target[1] - base_point[1])**2 +
                                     (self.target[2] - base_point[2])**2)
            self.base_pitch = np.arccos((self.target[2] - base_point[2]) / dist_from_base)
            self.base_theta = np.arctan2(self.target[1] - base_point[1], self.target[0] - base_point[0]) 
            dist2 = (dist_from_base - self.target_radius)
            self.target_point = [0] * 3
            self.target_point[0] = base_point[0] + dist2 * np.cos(self.base_theta) * np.sin(self.base_pitch)
            self.target_point[1] = base_point[1] + dist2 * np.sin(self.base_theta) * np.sin(self.base_pitch)
            self.target_point[2] = base_point[2] + dist2 * np.cos(self.base_pitch)    


            # TODO: vary the rotation by a little
            self.q_rot = Rotation.from_euler('xyz', [0, 0, np.pi], degrees=False)
            self.q_orig = Rotation.from_euler('xyz', [0.0, self.base_pitch, self.base_theta], degrees=False)
            self.target_rot = self.q_orig * self.q_rot
            self.target_orn = self.target_rot.as_quat()

    def set_target(self, target=[0.5,0,0.5], target_point=[0.1, 0.1, 0.1], target_point2=None):        
        self.add_shape(pos=target,        size=0.05,               rgba=[0.0, 0.0, 1.0, 1.0])
        self.add_shape(pos=target,        size=self.target_radius, rgba=[0.0, 1.0, 0.0, 0.2])
        self.add_shape(pos=target_point,  size=0.01,               rgba=[1.0, 0.0, 0.0, 1.0])
        # self.add_shape(pos=target_point2, size=0.01,               rgba=[1.0, 0.0, 0.0, 1.0])        

        # orn = Rotation.from_euler('xyz', [-np.pi/2 - self.reach_pitch, self.reach_theta, 0], degrees=False)
        # orn = Rotation.from_euler('zxy', [-np.pi/2 - self.reach_pitch, self.reach_theta, 0], degrees=False)
        # self.add_shape(pos=target_point2, orn=orn, size=0.3, rgba=[1.0, 0.0, 0.0, 1.0], shape="line")        
        # self.add_shape(pos=target_point, orn=self.target_orn, size=0.3, rgba=[1.0, 0.0, 0.0, 1.0], shape="line")        
        
        self.add_axis(pos=self.end_effector[:3], orn=self.end_effector[3:])
        self.add_axis(pos=self.exp_end_effector[:3], orn=self.target_orn)

    def get_expert(self):
        expert = np.array(self.initial_joints)
        rot1 = np.arctan2(self.target_point[1], self.target_point[0])
        
        # Rotate the first joint towards point
        expert[0] = rot1

        link1 = 0.333
        link2 = 0.316 
        link3 = 0.384
        delta = np.sqrt((self.target_point[0])**2 + 
                        (self.target_point[1])**2 +   
                        (self.target_point[2] - link1)**2)  
        
        # Cosine rule to find joint 2 and 4
        gamma = np.arccos(np.clip((link2**2 + link3**2 - delta**2) / (2*link2*link3), -1, 1))
        alpha = np.arccos(np.clip((link2**2 + delta**2 - link3**2) / (2*link2*delta), -1, 1))
        beta = np.arcsin(np.clip( (self.target_point[2] - link1) / delta, -1, 1))
        expert[1] = np.pi/2 - alpha - beta
        expert[3] = -np.pi + gamma

        # Set the pitch of joint 6
        expert[5] = np.pi + (np.pi/2 - self.base_pitch)

        # Extrapolate trajectory based on max_joint_vel
        self.get_trajectory(expert)
    
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
        
        # Also find the end effector trajectory, assuming constant velocity in each direction
        # TODO: find slerp between the inital rotation and target_orn
        self.expert_end_effector_traj = []
        for i in range(self.traj_size):
            points =[]
            for j in range(3):
                point = i * ((self.target_point[j] - self.end_effector[j]) / self.traj_size) + self.end_effector[j]
                points.append(point)
            self.expert_end_effector_traj.append(points)

        # See if we can stop the episode early
        if not self.args.render:
            self.args.max_ep_len = self.traj_size + 10