import numpy as np
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation, Slerp
from pyquaternion import Quaternion
import mujoco_viewer
import roboticstoolbox as rtb
from spatialmath import SE3

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

        super().__init__(PATH)
        
        self.robot_name = "panda"
        self.mesh_dir = "assets/xmls/franka_emika_panda/assets"

        if self.args.control_type == "torque":
            self.model_path = "assets/xmls/franka_emika_panda/scene_torque.xml"
            self.action_multiplier = np.array([21, 21, 21, 21, 3, 3, 3, 0])*self.args.action_multiplier
        else:
            self.model_path = "assets/xmls/franka_emika_panda/scene.xml"
            self.action_multiplier = np.array([1, 1, 1, 1, 1, 1, 1, 0])
        
        if self.args.tree_type:
            self.set_up_xmls()
        
        self.viewer = None
        self.load_robot()
        
        self.ob_size = 40
        self.ac_size = 7

        self.panda = rtb.models.DH.Panda() 
        # print(self.panda)
            
        self.motor_names = ['joint' + str(n + 1) for n in range(self.ac_size)]
        
        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        self.episodes = -1
        self.success = deque([0.0], maxlen=5)
        self.target_radius = 0.12
        self.sim_data = []
        self.best_return = 0
        self.steps = 0
        self.total_steps = 0

        # Reachibility parameters
        self.reach_centre = [0.174, 0, 0.501]
        self.dist_max = 0.55
        self.dist_min = 0.3
        self.reach_theta_max = 1.5
        self.reach_theta_min = -1.5
        # self.reach_pitch_max = 1.5
        self.reach_pitch_max = 1.0
        self.reach_pitch_min = 0

        self.success_dist = 0.15
        self.success_orn = 0.5
        self.jitter_scalar = 0
        self.steps_before_cur = 0
        self.actions = [0.0] * self.ac_size
        # Name of the base link in the xml, for setting the robot position on reset
        self.base_link = "link0"

        self.ob_dict = {}

        self.reward_names = ["Reward/goal", "Reward/joint", "Reward/orn", "Reward/joint_vel", "Reward/action", "Reward/jitter"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

    def load_robot(self):
        if not self.args.replay and self.args.tree_type and not self.args.cur:
            self.generate_tree(radius=0.02, height=1.5, damping=1, stiffness=10, pos=[0,0,0],rot=[0,1,0,0], num=20, spread=[[-0.2, 0.5],[-0.3, 0.3]], z_height=1.6, segs_per_branch=8)

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
            print("Why is this happening just for the tree? ", self.args.tree_type, " hpc: ", self.args.training_on_hpc, " rank ", self.rank)
            print("Can't view mujoco on the HPC.")

    def get_log_things(self):   
        # Things we want to log each training step (print and add to tensorboard)
        return_dict = {"Kp": self.Kp, "Success": self.success, "Cur": self.args.cur, "Jitter Scalar": self.jitter_scalar}
        return_dict.update(self.reward_dict)
        return return_dict

    def get_success(self):
        if "delay" in self.args.goal:
            if self.args.cur:
                return np.sqrt(np.sum((np.array(self.end_effector[:3]) - np.array(self.target))**2)) < self.success_dist
            else:
                return np.sqrt(np.sum((np.array(self.end_effector[:3]) - np.array(self.target))**2)) < self.success_dist and \
                Quaternion.absolute_distance(Quaternion(self.end_effector[3:]), Quaternion(self.target_orn)) < self.success_orn
        elif "end_effector" in self.args.goal:
            return np.sqrt(np.sum((np.array(self.end_effector[:3]) - np.array(self.target))**2)) < self.success_dist and \
                Quaternion.absolute_distance(Quaternion(self.end_effector[3:]), Quaternion(self.target_orn)) < self.success_orn
        elif self.args.goal == "joint":
            return (abs(np.array(self.joints[:self.ac_size]) - np.array(self.target_joints[:self.ac_size])) < self.success_dist).all()              

    def check_for_success(self):
        return len(self.success) == 5 and (np.array(self.success) == True).all()

    def reset(self, test=False, model_path=None, restore_state=None):

        if self.steps > 0:
            for key in self.reward_dict:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        if self.episodes > -1:

            # self.success.append(self.get_success())
            target = self.target + self.target_point + self.target_orn
            if self.args.tree_type and not self.args.cur:
                self.save_tree(best=self.total_return > self.best_return, test=test)
            self.record_sim_state(best=self.total_return > self.best_return, test=test, additional_arguments=target)
            if self.total_return > self.best_return:
                self.best_return = self.total_return
        self.total_return = 0
        
        if self.args.cur and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
                self.args.cur = False
                self.steps_before_cur = self.total_steps
            self.success = deque([0.0], maxlen=5)

        self.jitter_scalar = self.args.jitter_scalar * (not self.args.cur) * (self.total_steps - self.steps_before_cur) / (self.args.local_epoch_len * self.args.epochs)

        if model_path is not None:
            self.model_path = model_path 
        if (self.args.tree_type and not self.args.cur) or model_path is not None:
            self.load_robot()

        mujoco.mj_resetData(self.model, self.data)

        # Same as the titan
        self.initial_joints = [0.0, -1.3439, 0.0,  -2.8100, 0.0, 1.4835, 0.785, 0.0] 

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            # Rotate the base of the robot to simulate being on the back of a titan
            if self.args.rand_rot:
                rot_range = 0.2
            else:
                rot_range = 0.0
            self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), 0.0], degrees=False)
            self.orn = list(self.rot.as_quat())
            self.pos = [0,0,0]    
            self.set_position(pos=self.pos, orn=self.orn, joints=self.initial_joints)
        
        self.steps = 0
        self.episodes += 1

        # Step the simulation once to get the initial state
        mujoco.mj_forward(self.model, self.data)
        
        self.get_observation()
        self.goto_goal = True
        self.initial_end_effector = self.end_effector
        self.get_target()
        self.expert = self.get_expert()
        self.tar_end_effector = list(self.end_effector_traj[self.traj_i])
        self.tar_orn = list(self.slerp_rots[self.traj_i].as_quat())
        self.exp_joints = self.expert_traj[self.traj_i]
        self.prev_actions = self.joints + [0]
        self.prev_joints = self.joints 

        # On the real robot everything will be in base link frame, need to rotate end effector and target points by the initial base rotation
        # new_target_rot = list((Rotation.from_quat(self.target_orn) * self.rot).as_quat())
        # new_end_effector_rot = Rotation.from_quat(self.end_effector[-4:]) * self.rot
        # new_end_effector = list(self.rot.apply(self.end_effector[:3])) + list(new_end_effector_rot.as_quat())
        # new_target_point = list(self.rot.apply(self.target_point)) 
        # state = self.joints + self.joint_vel + self.joint_force + new_end_effector + new_target_point + new_target_rot
        if "end_effector" in self.args.goal:
            if "intermediate" in self.args.goal:
                goal = self.tar_end_effector + self.tar_orn
            else:
                # goal = self.target_point + self.target_orn
                goal = self.target + self.target_orn
        elif self.args.goal == "joint":
            goal = self.exp_joints

        state = self.orn + self.joints + self.joint_vel + self.joint_force + self.end_effector + goal
        return state

    def step(self, actions=None, replay_state=None):
        # print(self.get_success())

        if self.ep_len < self.steps:
            if self.goto_goal:
                self.success.append(self.get_success())
            # Periodically go back to start position (not goto_goal)
            # self.goto_goal = np.random.random() > 0.3
            self.goto_goal = not self.goto_goal
            self.get_target()
            self.expert = self.get_expert()

        if actions is not None:
            self.actions = list(actions) + [0]
        else:
            self.actions = [0]*(self.ac_size + 1)

        self.exp_joints = self.expert_traj[self.traj_i]
        self.tar_end_effector = list(self.end_effector_traj[self.traj_i])
        if self.traj_i < len(self.slerp_rots):
            self.tar_orn = list(self.slerp_rots[self.traj_i].as_quat())
        else:
            self.tar_orn = self.target_orn
        if self.traj_i < self.traj_size - 1:
            self.traj_i += 1

        if replay_state is not None:
            try:
                self.set_targets(replay_state[3])
                # print(replay_state[3][0][0], replay_state[3][2][0])
                self.target = replay_state[3][0][0]
                self.target_point = replay_state[3][2][0]
                self.target_orn = replay_state[3][3][1]
                self.set_position(pos=replay_state[0], orn=replay_state[1], joints=replay_state[2])
            except Exception as e:
                print(e)
        else:
            if self.render:
                # self.set_target(self.target, self.target_point)
                self.set_targets(self.targets + [[self.end_effector[:3], self.end_effector[3:]], [self.wrist, 0.07, [0.1, 0.2, 0.3, 1.0]]])

            if self.args.cur: 
                if self.args.control_type == "torque":
                    # expert = 80 * (np.array(self.exp_joints + [0]) - np.array(self.joints + [0])) - 2.0 * np.array(self.joint_vel + [0])
                    expert = 200 * (np.array(self.exp_joints + [0]) - np.array(self.joints + [0])) - 5.0 * np.array(self.joint_vel + [0])
                elif self.args.control_type == "position":
                    expert = np.array(self.exp_joints + [0])
               
                if self.args.just_expert:
                    self.data.ctrl[:self.ac_size+1] = ((self.Kp / self.initial_Kp ) * expert)[:]
                else:
                    self.data.ctrl[:self.ac_size+1] = self.action_multiplier*np.array(self.actions) +  (self.Kp / self.initial_Kp) * expert
            else:
                self.data.ctrl[:self.ac_size+1] = self.action_multiplier*np.array(self.actions)

        for _ in range(int(np.rint(self.timeStep/self.simStep))):
            mujoco.mj_step(self.model, self.data)
        
        if self.render:
            self.viewer.render()

        # self.data.ncon == 0
        self.get_observation()
        # print(self.targets[0][0], self.targets[2][0])
        self.save_sim_state(self.targets + [[self.end_effector[:3], self.end_effector[3:]]])
        reward, done = self.get_reward()
        self.prev_actions = self.joints + [0]
        self.prev_joints = self.joints
        self.total_return += reward
        self.steps += 1
        self.total_steps += 1

        # Rotate end effector and targets to be in base_link frame
        # new_target_rot = list((Rotation.from_quat(self.target_orn) * self.rot).as_quat())
        # new_end_effector_rot = Rotation.from_quat(self.end_effector[-4:]) * self.rot
        # new_end_effector = list(self.rot.apply(self.end_effector[:3])) + list(new_end_effector_rot.as_quat())
        # new_target_point = list(self.rot.apply(self.target_point)) 
        # state = self.joints + self.joint_vel + self.joint_force + new_end_effector + new_target_point + new_target_rot
        if "end_effector" in self.args.goal:
            if "intermediate" in self.args.goal:
                goal = self.tar_end_effector + self.tar_orn
            else:
                # goal = self.target_point + self.target_orn
                goal = self.target + self.target_orn
        elif self.args.goal == "joint":
            goal = self.exp_joints

        state = self.orn + self.joints + self.joint_vel + self.joint_force + self.end_effector + goal
        return np.array(state), reward, done, None
    
    def get_reward(self):
        done = False
        
        end_effector = np.exp(-10.0*np.sum(abs(np.array(self.end_effector[:3]) - np.array(self.target))))
        wrist = np.exp(-10.0*np.sum(abs(np.array(self.wrist) - np.array(self.target_point))))
        goal = 0.5*end_effector + 0.5*wrist

        # Unsure if we want distance or absolute distance
        # orn = np.exp(-10.0 * Quaternion.absolute_distance(Quaternion(self.end_effector[3:]), Quaternion(self.tar_orn)))
        # orn = np.exp(-10.0 * Quaternion.distance(Quaternion(self.end_effector[3:]), Quaternion(self.tar_orn)))
        orn = np.exp(-5.0 * Quaternion.distance(Quaternion(self.end_effector[3:]), Quaternion(self.tar_orn)))

        # Probably don't need to try and copy the expert joints
        # joints = np.exp(-2.0*np.sum((np.array(self.joints) - np.array(self.exp_joints))**2))
        
        # joints = np.exp(-5.0*np.sum((np.array(self.joints) - np.array(self.exp_joints))**2))
        joints = np.exp(-2.5*np.sum(abs((np.array(self.joints) - np.array(self.exp_joints)))))
        
        # joint_vel = 0.05 * np.exp(-0.1*np.sum(np.array(self.joint_vel)**2))
        joint_vel = -0.2 * (np.sum((np.array(self.joints) - np.array(self.prev_joints))**2) / self.timeStep)
        action = -0.002 * np.sum((np.array(self.actions) - np.array(self.prev_actions))**2)

        if "end_effector" in self.args.goal:
            if "delay" in self.args.goal:
                if not self.args.cur:
                    reward = 1.5*goal + 0.5*orn + self.jitter_scalar*(joint_vel + action)
                else:
                    reward = 1.5*goal + 0.0*orn + self.jitter_scalar*(joint_vel + action)
            else:
                reward = 1.5*goal + 0.5*orn + self.jitter_scalar*(joint_vel + action)
        elif self.args.goal == "joint":
            reward = 1.0*joints + joint_vel + action
        if self.contact:
            done = True

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/joint"] += joints
        self.ep_reward_dict["Reward/orn"] += orn
        self.ep_reward_dict["Reward/joint_vel"] += joint_vel
        self.ep_reward_dict["Reward/action"] += action
        self.ep_reward_dict["Reward/jitter"] += self.jitter_scalar*(joint_vel + action)
            
        return reward, done

    def close(self):
        self.viewer.close()
    
    def get_observation(self):
        # Keep an eye on these to make sure they are getting what you think
        self.wrist = list(self.data.body('link5').xipos) 
        self.end_effector = list(self.data.body('hand').xipos) 
        rot = Rotation.from_matrix(np.array(self.data.body('hand').ximat).reshape(3,3))
        self.end_effector += list(rot.as_quat())

        self.joints = [self.data.joint(name).qpos[0] for name in self.motor_names]
        self.joint_vel = [self.data.joint(name).qvel[0] for name in self.motor_names]
        self.joint_force = list(self.data.actuator_force[:self.ac_size+1])

        for i in range(self.ac_size):
            self.ob_dict["joint_pos" + str(i)] = self.joints[i]
            self.ob_dict["joint_vel" + str(i)] = self.joint_vel[i]
            self.ob_dict["joint_effort" + str(i)] = self.joint_force[i]
            self.ob_dict["joint_cmd" + str(i)] = self.action_multiplier*self.actions[i]

        # Check if contacted the ground or
        # contact_list = self.data.contact
        self.contact = False
        # self.print_contacts()
        # print(self.data.ncon)
        # for dim, contact1, contact2 in zip(contact_list.dim, contact_list.geom1, contact_list.geom2):
        #     if dim:
        #         geom_name1 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact1)
        #         geom_name2 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact2)
        #         if (geom_name1 == "floor" and geom_name2 is None) or (geom_name2 == "floor" and geom_name1 is None):
        #             self.contact = True
        #         if (geom_name1 is None and geom_name2 is None) or (geom_name2 is None and geom_name1 is None):
        #             self.contact = True

    def get_target(self):
        if not self.goto_goal:
            self.target_joints = self.initial_joints
            self.target = self.initial_end_effector[:3]
            inv_pitch = np.arctan2(0.088, 0.107)
            inv_yaw = np.pi
            self.target_point[0] = self.target[0] + self.target_radius * np.cos(inv_yaw) * np.sin(inv_pitch)
            self.target_point[1] = self.target[1] + self.target_radius * np.sin(inv_yaw) * np.sin(inv_pitch)
            self.target_point[2] = self.target[2] + self.target_radius * np.cos(inv_pitch)  

            # self.target_point = self.initial_end_effector[:3]
            self.target_orn = self.initial_end_effector[3:]
        elif "end_effector" in self.args.goal:
            # Get the target position, on a sphere from the reach centre (same parameters as refarm)
            self.dist = np.random.uniform(self.dist_min, self.dist_max)
            self.reach_theta = np.random.uniform(self.reach_theta_min, self.reach_theta_max)
            # self.reach_theta = self.reach_theta_min 
            self.reach_pitch = np.random.uniform(self.reach_pitch_min, self.reach_pitch_max)

            self.target = [0] * 3
            self.target[0] = self.reach_centre[0] + self.dist * np.cos(self.reach_theta) * np.sin(self.reach_pitch)
            self.target[1] = self.reach_centre[1] + self.dist * np.sin(self.reach_theta) * np.sin(self.reach_pitch)
            self.target[2] = self.reach_centre[2] + self.dist * np.cos(self.reach_pitch)    

            # This is the rotation from reach centre to an effector pose with a horizontal camera (from refarm/moveit_interface)
            # Just left here for reference. Given the rotation is slight different, not sure if this will transfer to the robot
            # Eigen::Quaterniond q_orig = Eigen::AngleAxisd(yaw, Eigen::Vector3d::UnitZ()) *
            #                             Eigen::AngleAxisd(-((M_PI / 2) - inv_pitch), Eigen::Vector3d::UnitY()) *
            #                             Eigen::AngleAxisd(0.0, Eigen::Vector3d::UnitX());

            # Eigen::Quaterniond q_rot = Eigen::AngleAxisd(M_PI, Eigen::Vector3d::UnitX()) *
            #                             Eigen::AngleAxisd(0.5 * M_PI, Eigen::Vector3d::UnitY()) *
            #                             Eigen::AngleAxisd(0.25 * M_PI, Eigen::Vector3d::UnitZ());

            # q_orig = (q_orig * q_rot).normalized();


            base_point = [0.0, 0.0, self.reach_centre[2]]
            rand_range = 0.1
            # base_point = [np.random.uniform(-rand_range, rand_range), np.random.uniform(-rand_range, rand_range), self.reach_centre[2] + np.random.uniform(-rand_range, rand_range)]
            dist_from_base = np.sqrt((self.target[0] - base_point[0])**2 +
                                        (self.target[1] - base_point[1])**2 +
                                        (self.target[2] - base_point[2])**2)
            self.base_pitch = np.arccos((self.target[2] - base_point[2]) / dist_from_base)
            self.base_theta = np.arctan2(self.target[1] - base_point[1], self.target[0] - base_point[0])

            # print(self.target[2])
            if self.target[2] < 0.9:
               self.base_pitch = np.random.uniform(self.base_pitch, np.pi - 0.05)
            
            # self.base_pitch = np.pi - 0.2
            # self.base_pitch = np.pi/2 - 0.2
            # self.base_pitch = 0.2

            # TODO: vary the rotation by a little
            self.q_rot = Rotation.from_euler('xyz', [0, 0, np.pi], degrees=False)
            # self.q_rot2 = Rotation.from_euler('xyz', [0, np.pi, np.pi], degrees=False)
            # self.q_orig = Rotation.from_euler('xyz', [0.0, self.base_pitch, self.base_theta], degrees=False)

            # self.q_orig = Rotation.from_euler('xyz', [0.0, self.base_pitch, self.base_theta + np.random.uniform(-0.2, 0.2)], degrees=False)
            self.q_orig = Rotation.from_euler('xyz', [0.0, self.base_pitch, self.base_theta], degrees=False)
            # self.q_orig_inv = Rotation.from_euler('xyz', [0.0, self.base_pitch, np.pi - self.base_theta], degrees=False)
            # self.q_orig = Rotation.from_euler('xyz', [0.0, np.pi, self.base_theta + np.random.uniform(-0.2, 0.2)], degrees=False)
            self.target_rot = self.q_orig * self.q_rot
            # self.target_rot2 = self.q_orig * self.q_rot2
            self.target_orn = list(self.target_rot.as_quat())


            # def angle(x,y,z,w,a):
            #     factor = np.sin( a / 2.0 )

            #     # Calculate the x, y and z of the quaternion
            #     x = x * factor
            #     y = y * factor
            #     z = z * factor

            #     # // Calcualte the w value by cos( theta / 2 )
            #     w = np.cos( a / 2.0 )

            #     # return Quaternion(x, y, z, w).normalize()
            #     return Rotation.from_quat([x, y, z, w])
            # self.q_rot2 = Rotation.from_euler('xyz', [0,-np.pi,0], degrees=False)
            self.q_rot2 = Rotation.from_euler('xyz', [0,0,np.pi], degrees=False)
            # self.q_rot2 = Rotation.from_euler('xyz', [np.pi,0,0], degrees=False)

            # print(self.q_rot2.as_quat())
            # print(angle(0,1,0,0,np.pi).as_quat())
            # print()


            # self.q_rot2 = Rotation.from_euler('xyz', [0,0,np.pi], degrees=False)
            # self.q_rot2 = Rotation.from_euler('xyz', [np.pi,0,0], degrees=False)


            self.target_radius = np.sqrt(0.107**2 + 0.088**2)
            # # # print(np.sqrt(0.107**2 + 0.088**2))
            self.target_point = [0] * 3
            # # self.base_pitch += np.arctan2(0.088, 0.107)
            # _, pitch, yaw = self.target_rot.inv().as_euler('xyz')
            # roll, pitch, yaw = self.target_rot.inv().as_euler('xyz')
            # targ = self.target_rot.as_quat()
            # print(targ)
            # targ[0] = -targ[0]
            # targ[2] = -targ[2]
            # print(targ)
            # inv_target_roll = Rotation.from_quat(targ)
            # roll, pitch, yaw = self.target_rot.as_euler('xyz')
            # roll, pitch, yaw = inv_target_roll.as_euler('xyz')
            # rot3 = (self.target_rot * self.q_rot2)
            # rot3 = self.target_rot 
            # print(rot3.as_quat())
            # print(self.target_rot.as_quat())
            # roll, pitch, yaw = rot3.as_euler('xyz')
            # rollt, pitcht, yawt = self.target_rot.as_euler('xyz')
            # print(rollt, pitcht, yawt)
            # print(inv_target_roll.as_quat())
            # roll, pitch, yaw = inv_target_roll.as_euler('xyz')

            # roll, pitch, yaw = (self.q_rot2*self.target_rot).as_euler('xyz')


            # inv_pitch = -np.pi + pitch
            inv_pitch = np.pi - self.base_pitch + np.arctan2(0.088, 0.107)

            # inv_yaw = -yaw
            # inv_yaw = roll
            if self.base_theta > 0:
                inv_yaw = -np.pi + self.base_theta
            else:
                inv_yaw = np.pi + self.base_theta

            
            # print(inv_pitch, inv_yaw, self.base_pitch, self.base_theta)
            # print(roll, pitch, yaw, self.base_pitch, self.base_theta)
            # print()

            self.target_point[0] = self.target[0] + self.target_radius * np.cos(inv_yaw) * np.sin(inv_pitch)
            self.target_point[1] = self.target[1] + self.target_radius * np.sin(inv_yaw) * np.sin(inv_pitch)
            self.target_point[2] = self.target[2] + self.target_radius * np.cos(inv_pitch)   


            # self.q_rot = Rotation.from_euler('xyz', [0, np.pi, 0], degrees=False)

            # # Get the target point in rotation link (same as reach centre, with x back on rotation joint)
            # base_point = [0.0, 0.0, self.reach_centre[2]]
            # rand_range = 0.1
            # # base_point = [np.random.uniform(-rand_range, rand_range), np.random.uniform(-rand_range, rand_range), self.reach_centre[2] + np.random.uniform(-rand_range, rand_range)]
            # dist_from_base = np.sqrt((self.target[0] - base_point[0])**2 +
            #                             (self.target[1] - base_point[1])**2 +
            #                             (self.target[2] - base_point[2])**2)
            # self.base_pitch = np.arccos((self.target[2] - base_point[2]) / dist_from_base)
            # self.base_theta = np.arctan2(self.target[1] - base_point[1], self.target[0] - base_point[0])
            # dist2 = (dist_from_base - self.target_radius)
            # self.target_point = [0] * 3
            # self.target_point[0] = base_point[0] + dist2 * np.cos(self.base_theta) * np.sin(self.base_pitch)
            # self.target_point[1] = base_point[1] + dist2 * np.sin(self.base_theta) * np.sin(self.base_pitch)
            # self.target_point[2] = base_point[2] + dist2 * np.cos(self.base_pitch)    


            # # dist3 = (dist_from_base - self.target_radius - np.sqrt(0.107**2 + 0.088**2))
            # # # print(np.sqrt(0.107**2 + 0.088**2))
            # # self.target_point2 = [0] * 3
            # # # self.base_pitch += np.arctan2(0.088, 0.107)

            # # # if not self.args.cur:
            # # #     self.base_pitch = np.random.uniform(self.base_pitch, np.pi)
            # # self.base_pitch = np.pi
            # # # self.base_pitch = np.pi/2
            # # # base_pitch = self.base_pitch + np.arctan2(0.088, 0.107)
            # # base_pitch = self.base_pitch 
            # # # print(self.base_pitch, np.arctan2(0.088, 0.107))
            # # # self.base_pitch =
            # # self.target_point2[0] = base_point[0] + dist3 * np.cos(self.base_theta) * np.sin(base_pitch)
            # # self.target_point2[1] = base_point[1] + dist3 * np.sin(self.base_theta) * np.sin(base_pitch)
            # # self.target_point2[2] = base_point[2] + dist3 * np.cos(base_pitch)    

            # # TODO: vary the rotation by a little
            # self.q_rot = Rotation.from_euler('xyz', [0, 0, np.pi], degrees=False)
            # # self.q_orig = Rotation.from_euler('xyz', [0.0, self.base_pitch, self.base_theta], degrees=False)

            # self.q_orig = Rotation.from_euler('xyz', [0.0, self.base_pitch, self.base_theta + np.random.uniform(-0.2, 0.2)], degrees=False)
            # # self.q_orig = Rotation.from_euler('xyz', [0.0, np.pi, self.base_theta + np.random.uniform(-0.2, 0.2)], degrees=False)
            # self.target_rot = self.q_orig * self.q_rot
            # self.target_orn = list(self.target_rot.as_quat())
            
            # # Inverse kinematics might be hard to learn, not always the shortest joint positions to target
            # # # Make a 4x4 transformation matrix
            # # T = np.identity(4)
            # # T[:3, 3] = self.target_point
            # # T[:3,:3] = Rotation.from_quat(self.target_orn).as_matrix()
            # # self.target_joints = self.panda.ik_lm_chan(SE3(T))[0]
        elif self.args.goal == "joint":
            # Set a target joint space goal within the joint range of the Panda
            mins = [-np.pi, -1.7628, -np.pi, -3.0718, -np.pi, -0.0175, -np.pi]
            maxs = [np.pi, 1.7628, np.pi, -0.0698, np.pi, 3.7525, np.pi]
            self.target_joints = np.random.uniform(mins, maxs)
            T = np.array(self.panda.fkine(self.target_joints))
            self.target = self.target_point = list(T[:3,3])
            # It's possible to reach into the ground
            while self.target[2] < 0.3:
                self.target_joints = np.random.uniform(mins, maxs)
                T = np.array(self.panda.fkine(self.target_joints))
                self.target = self.target_point = list(T[:3,3])
            self.target_orn = list(Rotation.from_matrix(T[:3, :3]).as_quat())

        self.targets = [[self.target, self.success_dist, [0.0, 0.0, 1.0, 0.2]], 
                #    [self.target, 0.1, [0.0, 0.5, 0.5, 0.3]], 
                   [self.target, self.target_radius, [0.0, 1.0, 0.0, 0.4]], 
                   [self.target_point, 0.01, [1.0, 0.0, 0.0, 1.0]]]
                #    [self.target_point2, 0.01, [1.0, 0.0, 0.0, 1.0]]]
                #    [self.end_effector[:3], self.end_effector[3:]]

        if (self.target_orn is None or len(self.target_orn) != 4) and "end_effector" in self.args.goal:
            self.targets.append([self.tar_end_effector[:3], self.target_orn])
        else:
            # self.targets.append([self.target_point, self.target_orn])
            self.targets.append([self.target, self.target_orn])

    def set_targets(self, targets):
        if isinstance(targets, list):
            for target in targets:
                if len(target) == 3:
                    self.add_shape(pos=target[0], size=target[1], rgba=target[2])
                else:
                    self.add_axis(pos=target[0], orn=target[1])

    def get_expert(self):
        if not self.goto_goal:
            expert = np.array(self.initial_joints)
        elif "end_effector" in self.args.goal:
            # expert = self.target_joints

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

            # expert[1] = (np.pi*2)/7 - alpha - beta
            # expert[3] = -((np.pi*9)/7) + gamma

            # Set the pitch of joint 6
            expert[5] = np.pi + (np.pi/2 - self.base_pitch) - (gamma - (np.pi - alpha - beta))
            # print((gamma - (np.pi - alpha - beta)))
            # expert[5] = np.pi/2
        elif self.args.goal == "joint":
            expert = self.target_joints


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
        self.end_effector_traj = []
        for i in range(self.traj_size):
            points =[]
            for j in range(3):
                point = i * ((self.target_point[j] - self.end_effector[j]) / self.traj_size) + self.end_effector[j]
                points.append(point)
            self.end_effector_traj.append(points)

        # Constant number of rotations

        # Get to the desired rotation in 1 second, take 1/10th of a second to get there, play with these..
        key_rots = Rotation.from_quat([self.end_effector[3:], self.target_orn])
        key_times = [0,1]
        slerp = Slerp(key_times, key_rots)
        times = np.linspace(0,1,10)
        self.slerp_rots = slerp(times)

        # See if we can stop the episode early (single target)
        # if not self.args.render:
            # self.args.max_ep_len 

        self.ep_len = self.steps + self.traj_size + 200