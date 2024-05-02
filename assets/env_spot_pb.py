from cmath import e
from copy import deepcopy
import numpy as np
import pybullet as p
import time
from gym import spaces
from collections import deque
import cv2
from mpi4py import MPI
comm = MPI.COMM_WORLD
import torch

from assets.env_base_pb import EnvBasePB

class Env(EnvBasePB):
    # Terrain size and image size are the same
    terrain_size = im_size = [1,100,100]
    timeStep = 1/50
    simStep = 1/200
    def __init__(self, PATH=None, args=None, writer=None):

        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True 
        
        super().__init__(PATH)

        self.ac_size = 12
        self.ob_size = 55
        self.Kp = 400
        self.initial_Kp = self.Kp
        self.ROBOT_HEIGHT = 0.5
        self.best_return = 0
        self.action_multiplier = 30


        if self.args.with_initial_cmd:
            self.use_vx_reward = True
            self.use_vy_reward = True
            self.use_yaw_vel_reward = True

                
            self.max_vx = 1.0
            self.max_vy = 0.5
            self.max_yaw_vel = 1.5

            self.min_vx = -0.5
            self.min_vy = -0.5
            self.min_yaw_vel = -1.5


        else:        
            self.use_vx_reward = True
            self.use_vy_reward = False
            self.use_yaw_vel_reward = False


            self.max_vx = 0.5
            self.max_vy = 0.0
            self.max_yaw_vel = 0.0

            self.min_vx = 0.5
            self.min_vy = -0.0
            self.min_yaw_vel = -0.0

        self.target_max_vx = 1.0
        self.target_max_vy = 0.5
        self.target_max_yaw_vel = 1.5

        self.target_min_vx = -0.5
        self.target_min_vy = -0.5
        self.target_min_yaw_vel = -1.5
        self.cmd_cur = True

        self.w_cont = 0.1

        self.cmd_update_rate = 100
        self.cmd_vel = np.array([0.0, 0.0, 0.0])
        self.action_scale = 0.5

        self.kp = 20.0
        self.kd = 0.5

        self.default_joints = np.array([0.0, 1.2, -2.0]*4)

        self.steps = 0

        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        
        self.episodes = -1
        
        self.target_yaw = 0.0
        self.sign = 1

        self.cur_success = deque([0.0], maxlen=5)

        if self.args.add_terrain:
            self.terrain_difficulty = self.args.initial_terrain_difficulty
        else:
            self.terrain_difficulty = 0
            self.terrain = None

        self.max_disturbance = 250
        self.final_disturbance = 1600

        self.states_to_restore = ["joints", "pos", "orn", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "episodes", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

        self.log_things = {"Kp": self.Kp, "Success": self.cur_success, "Dist": self.max_disturbance, "Difficulty": self.terrain_difficulty}

        self.reward_names = ["Reward/lin_vel", "Reward/ang_vel", "Reward/orien", "Reward/height", "Reward/joints", "Reward/contacts", "Reward/rate", "Reward/avg"]
        self.cmd_names = ["Cmd/self.max_vx",
                        "Cmd/self.max_vy",
                        "Cmd/self.max_yaw_vel",
                        "Cmd/self.args.yaw_cmd_dif",
                        "Cmd/self.min_vx",
                        "Cmd/self.min_vy",
                        "Cmd/self.w_cont",
                        "Cmd/self.min_yaw_vel"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names + self.cmd_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        self.load_robot()   


    def load_specific_robot(self):
        
        self.load_urdf_robot("./assets/urdfs/spot/urdf/spot.urdf")

        self.jdict = {}
        self.feet_dict = {}
        self.leg_dict = {}
        self.body_dict = {}
        self.feet = ["rear_left_lower_leg", "rear_right_lower_leg", "front_left_lower_leg", "front_right_lower_leg"]
        self.legs = ["rear_left_upper_leg", "rear_right_upper_leg", "front_left_upper_leg", "front_right_upper_leg"]
        self.feet_contact = {f:True for f in self.feet}
        self.ordered_joints = []
        self.ordered_joint_indices = []
        self.shin_dict = {}
        self.arm_dict = {}
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            link_name = info[12].decode("ascii")
            if link_name in self.feet: self.feet_dict[link_name] = j
            if link_name in self.legs: self.leg_dict[link_name] = j
            if link_name=="pelvis": self.body_dict["body_link"] = j
            self.ordered_joint_indices.append(j)
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            # print(jname)

            lower, upper = (info[8], info[9])
            self.ordered_joints.append( (j, lower, upper) )
            self.jdict[jname] = j
        
        # exit()

        # Do not change this order!! Else joint postions will be wrong
        self.motor_names = ["front_left_hip_x"]
        self.motor_names += ["front_left_hip_y"]
        self.motor_names += ["front_left_knee"]
        self.motor_names += ["front_right_hip_x"]
        self.motor_names += ["front_right_hip_y"]
        self.motor_names += ["front_right_knee"]
        self.motor_names += ["rear_left_hip_x"]
        self.motor_names += ["rear_left_hip_y"]
        self.motor_names += ["rear_left_knee"]
        self.motor_names += ["rear_right_hip_x"]
        self.motor_names += ["rear_right_hip_y"]
        self.motor_names += ["rear_right_knee"]
        self.motor_power =  [20]*len(self.motor_names)       

        self.motors = [self.jdict[n] for n in self.motor_names]
            
        forces = np.ones(len(self.motors))*240
        # self.actions =
        #  {key:0.0 for key in self.motor_names}

        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(self.motor_names))

        for key in self.feet_dict:
            p.changeDynamics(self.Id, self.feet_dict[key],lateralFriction=0.9, spinningFriction=0.9)


    def check_for_success(self):
        return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()

    def get_success(self):
        if self.steps == 0:
            return False
        return self.ep_reward_dict["Reward/avg"]/self.steps > self.args.cur_thres and self.steps > 300

    def reset(self, terrain=None, test=False, restore_state=None):

        # Wait until both feet are on the ground before starting walking
        self.paused = True

        if self.episodes > -1:
            self.ep_success = self.get_success()
            self.cur_success.append(self.ep_success)  

        if self.steps > 0:
            for key in self.reward_names:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        if self.rank == 0 and self.args.record_sim and self.episodes > -1:
            self.record_sim_state(best=self.total_return > self.best_return, additional_arguments=self.terrain, test=test)
            if self.total_return > self.best_return:
                self.best_return = self.total_return
        self.total_return = 0
        
        # Three curriculum stages, can swap the order of the first two
        # Stage 1
        if self.args.terrain_first:
            if self.args.add_terrain and self.terrain_difficulty < self.args.final_terrain_difficulty and self.check_for_success():
                self.terrain_difficulty += 0.05
                self.cur_success = deque([0.0], maxlen=5)

        if self.args.cur and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
            self.cur_success = deque([0.0], maxlen=5)

        if self.w_cont < 0.1 and self.check_for_success():
            self.w_cont += 0.01
            self.cur_success = deque([0.0], maxlen=5)

        if self.args.yaw_cmd_dif <= self.target_max_yaw_vel and self.check_for_success():
            self.args.yaw_cmd_dif += 0.1
            self.cur_success = deque([0.0], maxlen=5)

        # Command curriculum
        if self.cmd_cur and self.check_for_success():
            if self.max_vx < self.target_max_vx or self.min_vx > self.target_min_vx:
                self.use_vx_reward = True
                if self.max_vx < self.target_max_vx:
                    self.max_vx = min(self.max_vx + 0.1, self.target_max_vx)
                elif self.min_vx > self.target_min_vx:
                    self.min_vx = max(self.min_vx - 0.1, self.target_min_vx)
            elif self.max_yaw_vel < self.target_max_yaw_vel or self.min_yaw_vel > self.target_min_yaw_vel:
                self.use_yaw_vel_reward = True
                self.max_yaw_vel = min(self.max_yaw_vel + 0.1, self.target_max_yaw_vel)
                self.min_yaw_vel = max(self.min_yaw_vel - 0.1, self.target_min_yaw_vel)
            elif self.max_vy < self.target_max_vy or self.min_vy > self.target_min_vy:
                self.use_vy_reward = True
                self.max_vy = min(self.max_vy + 0.1, self.target_max_vy)
                self.min_vy = max(self.min_vy - 0.1, self.target_min_vy)
            else:
                self.cmd_cur = False
        
            self.cur_success = deque([0.0], maxlen=5)
        
        
        # Stage 2
        if not self.args.terrain_first:
            if self.args.add_terrain and self.terrain_difficulty < self.args.final_terrain_difficulty and self.check_for_success():
                self.terrain_difficulty += 0.05
                self.cur_success = deque([0.0], maxlen=5)

        # Stage 3
        if self.args.apply_disturbances and self.max_disturbance < self.final_disturbance and self.check_for_success():
            self.max_disturbance += 250
            self.cur_success = deque([0.0], maxlen=5)

        
        self.reward_dict["Cmd/self.max_vx"].append(self.max_vx)
        self.reward_dict["Cmd/self.max_vy"].append(self.max_vy)
        self.reward_dict["Cmd/self.max_yaw_vel"].append(self.max_yaw_vel)
        self.reward_dict["Cmd/self.args.yaw_cmd_dif"].append(self.args.yaw_cmd_dif)
        self.reward_dict["Cmd/self.min_vx"].append(self.min_vx)
        self.reward_dict["Cmd/self.min_vy"].append(self.min_vy)
        self.reward_dict["Cmd/self.min_yaw_vel"].append(self.min_yaw_vel)
        self.reward_dict["Cmd/self.w_cont"].append(self.w_cont)


        self.exp_joints = self.default_joints

        if terrain is not None:
            self.load_terrain(terrain)
        elif self.args.add_terrain:
            template = (np.random.random([int(self.terrain_size[2]/4),int(self.terrain_size[2]/4)]) + 1.0) * self.terrain_difficulty 
            # Make the edges smooth
            template[:, 0] = 0.0
            template[:, -1] = 0.0
            template[0, :] = 0.0
            template[-1, :] = 0.0
            terrain = cv2.resize(template, dsize=(self.terrain_size[1], self.terrain_size[2])).reshape(self.terrain_size)
            self.load_terrain(terrain)

        self.steps = 0
        self.episodes += 1

        self.ob_dict = {}
        for foot in self.feet_dict:
            self.ob_dict[foot] = False
            self.ob_dict["prev_" + foot] = False

        self.z_offset = 0

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            rand_scale = self.max_disturbance / self.final_disturbance
            pos = [0,0,0.5 + np.random.uniform(-0.05, 0.05)]
            self.roll, self.pitch, self.yaw = [np.random.uniform(-0.05, 0.05), np.random.uniform(-0.05, 0.05), np.random.uniform(-0.05, 0.05)] 
            orn = p.getQuaternionFromEuler([self.roll, self.pitch, self.yaw])
            base_vel = [0,0,0]
            joints = []
            for j in self.ordered_joints:
                joints.append(np.clip(np.random.random() * rand_scale * 0.25 , j[1], j[2]))
            joints = self.default_joints + (np.random.random(self.ac_size)*0.2 - 0.1)
            joint_vel = [0]*len(self.motors)
            self.set_position(pos, orn, joints, base_vel, joint_vel)

        self.actions = np.zeros(self.ac_size)
        self.prev_actions = self.actions
        
        self.commands = np.zeros(3)
        self.target_yaw = self.yaw
        self.sign = 1

        self.get_observation()

        self.step_count = 0

        # Experimental for symmetry:
        # self.all_actions = np.zeros([self.env_exp.sample_size, 6])
        self.indicies = [5,6,7,11,12,13]

        return self.obs_buf

    def compute_torques(self, actions):
        # print(actions.shape, self.default_joints.shape, sel)
        return self.kp*(self.action_scale*actions + self.default_joints - np.array(self.joints)) - self.kd*(np.array(self.joint_vel))


    def step(self, actions):

        self.actions = actions

        for _ in range(int(self.timeStep/self.simStep)):
            jointStates = p.getJointStates(self.Id,self.ordered_joint_indices)
            self.joints = list(np.array([jointStates[j[0]][0] for j in self.ordered_joints[:int(self.ac_size)]]))
            
            # Scale vels 
            self.joint_vel = list(np.array([jointStates[j[0]][1] for j in self.ordered_joints[:int(self.ac_size)]]) / 10) 

            forces = self.compute_torques(actions)

            if self.args.cur:
                if self.Kp > 0:
                    exp_forces = self.apply_forces()

                    hips = [0,3,6,9]
                    exp_forces[hips] = 0.0
                    forces = forces + (self.Kp/self.initial_Kp) * exp_forces
            forces = forces.reshape(-1)
            p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.TORQUE_CONTROL, forces=forces)

            p.stepSimulation()

        if self.args.render:
            time.sleep(self.timeStep)
        
        if (self.steps % int(4 / self.timeStep) == 0 and self.steps != 0) or (self.paused and self.steps > 100):
            self.paused = False
            # if True:
                # self.commands = np.array([0,0,np.random.choice([-1.5, 1.5])])
            # else:
            self.commands = np.random.uniform([self.min_vx, self.min_vy, self.min_yaw_vel],[self.max_vx, self.max_vy, self.max_yaw_vel])
            self.commands[2] = np.random.choice([-1,1]) * np.random.uniform(self.target_max_yaw_vel - self.args.yaw_cmd_dif, self.target_max_yaw_vel)
            # Set low lin velocities to zeros
            self.commands[0] *= abs(self.commands[0])>0.1
            self.commands[1] *= abs(self.commands[1])>0.1
            self.commands[2] *= abs(self.commands[2])>0.1
            self.target_yaw = self.yaw        

        self.get_observation()
        self.save_sim_state()
        reward, done = self.get_reward()
        self.total_return += reward
        self.steps += 1

        return self.obs_buf, reward, done, None

    def get_reward(self):
        
        tracking_sigma = 0.1
        ang_vel_tracking_sigma = self.args.ang_vel_tracking_sigma
        
        _reward_tracking_lin_vel = 0.0
        _reward_tracking_ang_vel = 0.0
        orientation = 0.0
        rate = 0
        contacts = 0.0
        height = 0.0
        joints = 0.0
        rate = 0.0

        if self.args.scale_yaw_cmds:
            command_scales = np.clip(abs(self.commands), a_min=0.3, a_max=1.5) 
        else:
            command_scales = [1.0]*3

        # ang_vel_error = np.sum(np.square(np.array([self.target_yaw - self.yaw, self.commands[2] - self.base_ang_vel[2] ])))
        ang_vel_error = np.sum(np.square(np.array([self.commands[2] - self.base_ang_vel[2] ])))

        _reward_tracking_ang_vel = 1.0*command_scales[2]*np.exp(-ang_vel_error/ang_vel_tracking_sigma)

        if True:

            lin_vx_error = np.sum(np.square(self.commands[0] - self.base_lin_vel[0]))
            _reward_tracking_lin_vel = 0.5*command_scales[0]*np.exp(-lin_vx_error/tracking_sigma)

            lin_vy_error = np.sum(np.square(self.commands[1] - self.base_lin_vel[1]))
                
            _reward_tracking_lin_vel += 0.5*command_scales[1]*np.exp(-lin_vy_error/tracking_sigma)

            orientation = -1.2*np.sum(np.square([self.roll, self.pitch]))
            # orientation += -0.0005*np.sum(np.square([self.roll_vel, self.pitch_vel]))

            height = -0.5 * abs(self.body_xyz[2] - 0.5)

            not_hips = [1,2,4,5,7,8,10,11]
            joints = -0.2*self.w_cont * np.sum(np.square(self.default_joints[not_hips] - np.array(self.joints)[not_hips]))

            if abs(self.commands[1]) < 0.1 and abs(self.commands[2]) < 0.1:
                 # More emphasis on hip joints being zero when not needed
                hips = [0,3,6,9]
                joints += -0.2*self.w_cont * np.sum(np.square(np.array(self.joints)[hips]))

            if (self.commands == 0).all():
                contacts = -self.w_cont*((1 - self.ob_dict["rear_left_lower_leg"]) + (1-self.ob_dict["rear_right_lower_leg"]) + (1-self.ob_dict["front_right_lower_leg"]) + (1-self.ob_dict["front_left_lower_leg"])) 
            else:
                # Foot pairs should be the same
                contacts = -self.w_cont*(abs(self.ob_dict["rear_left_lower_leg"] - self.ob_dict["front_right_lower_leg"]))
                contacts += -self.w_cont*(abs(self.ob_dict["rear_right_lower_leg"] - self.ob_dict["front_left_lower_leg"]))
                
                # If a pair is off the ground, the other pair should be on the ground, but ok if all on the ground
                if not self.ob_dict["rear_left_lower_leg"]:
                    contacts += -self.w_cont*((1 - self.ob_dict["rear_right_lower_leg"]) + (1 - self.ob_dict["front_left_lower_leg"]))
                if not self.ob_dict["front_right_lower_leg"]:
                    contacts += -self.w_cont*((1 - self.ob_dict["rear_right_lower_leg"]) + (1 - self.ob_dict["front_left_lower_leg"]))
                if not self.ob_dict["rear_right_lower_leg"]:
                    contacts += -self.w_cont*((1 - self.ob_dict["rear_left_lower_leg"]) + (1 - self.ob_dict["front_right_lower_leg"]))
                if not self.ob_dict["front_left_lower_leg"]:
                    contacts += -self.w_cont*((1 - self.ob_dict["rear_left_lower_leg"]) + (1 - self.ob_dict["front_right_lower_leg"]))
                    
                # No foot pair should be in contact at the same time, doesn't like standing still
                # contacts = -self.w_cont*(abs(self.ob_dict["rear_left_lower_leg"] - self.ob_dict["front_right_lower_leg"]) + abs(self.ob_dict["rear_left_lower_leg"] - (1 - self.ob_dict["front_left_lower_leg"])) + abs(self.ob_dict["rear_left_lower_leg"] - (1 - self.ob_dict["rear_right_lower_leg"])))      
                # contacts += -self.w_cont*(abs(self.ob_dict["rear_right_lower_leg"] - self.ob_dict["front_left_lower_leg"]) + abs(self.ob_dict["rear_right_lower_leg"] - (1 - self.ob_dict["front_right_lower_leg"])) + abs(self.ob_dict["rear_right_lower_leg"] - (1 - self.ob_dict["rear_left_lower_leg"])))      
                # contacts += -self.w_cont*(abs(self.ob_dict["front_right_lower_leg"] - (1 - self.ob_dict["front_left_lower_leg"])) + abs(self.ob_dict["front_right_lower_leg"] - (1 - self.ob_dict["rear_right_lower_leg"])))      
                # contacts += -self.w_cont*(abs(self.ob_dict["front_left_lower_leg"] - (1 - self.ob_dict["front_right_lower_leg"])) + abs(self.ob_dict["front_left_lower_leg"] - (1 - self.ob_dict["rear_left_lower_leg"])))    

            rate = -0.0001 * np.sum(np.square(self.actions - self.prev_actions))
            self.prev_actions = self.actions

        reward = 1.*_reward_tracking_lin_vel + _reward_tracking_ang_vel + orientation + height + joints + contacts + rate

        self.ep_reward_dict["Reward/lin_vel"] += _reward_tracking_lin_vel
        self.ep_reward_dict["Reward/ang_vel"] += _reward_tracking_ang_vel
        self.ep_reward_dict["Reward/orien"] += orientation
        self.ep_reward_dict["Reward/height"] += height
        self.ep_reward_dict["Reward/joints"] += joints
        self.ep_reward_dict["Reward/contacts"] += contacts
        self.ep_reward_dict["Reward/rate"] += rate
        self.ep_reward_dict["Reward/avg"] += reward

        done = False
        if self.body_xyz[2] < 0.2 or (abs(np.array([self.pitch, self.roll])) > 1.0).any() or (np.array(self.leg_contacts)).any():
            done = True
            print("fallen")
        return reward, done

    def get_observation(self):
        jointStates = p.getJointStates(self.Id,self.ordered_joint_indices)
        self.joints = list(np.array([jointStates[j[0]][0] for j in self.ordered_joints[:int(self.ac_size)]]))
        
        # Scale vels 
        if self.args.load_path != "":
            # Used an additionally scaling for training translation.pt
            self.joint_vel = list(np.array([jointStates[j[0]][1] for j in self.ordered_joints[:int(self.ac_size)]]) / 10) 
        else:
            self.joint_vel = list(np.array([jointStates[j[0]][1] for j in self.ordered_joints[:int(self.ac_size)]])) 
        
        self.ob_dict.update({n + '_pos':j for n,j in zip(self.motor_names, self.joints)})


        self.body_xyz, (self.qx, self.qy, self.qz, self.qw) = p.getBasePositionAndOrientation(self.Id)
        self.pos = self.body_xyz
        self.orn = [self.qx, self.qy, self.qz, self.qw]
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion([self.qx, self.qy, self.qz, self.qw])

        self.body_vxyz, self.base_rot_vel = p.getBaseVelocity(self.Id)
        
        self.roll_vel = self.base_rot_vel[0]
        self.pitch_vel = self.base_rot_vel[1]
        self.yaw_vel = self.base_rot_vel[2]

        rot_speed = np.array(
        [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
            [np.sin(-self.yaw), np.cos(-self.yaw), 0],
            [		0,			 0, 1]]
        )

        self.vx, self.vy, self.vz = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        
        # Policy shouldn't know yaw
        self.body = [self.vx, self.vy, self.vz, self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel, self.body_xyz[2] - self.z_offset]

        self.leg_contacts = []
        for leg in self.leg_dict:
            self.ob_dict[leg] = len(p.getContactPoints(self.Id, -1, self.leg_dict[leg], -1))>0
            self.leg_contacts += [self.ob_dict[leg]]


        self.contacts = []
        for foot in self.feet_dict:
            self.ob_dict["prev_" + foot] = self.ob_dict[foot]
            self.ob_dict[foot] = len(p.getContactPoints(self.Id, -1, self.feet_dict[foot], -1))>0
            self.contacts += [self.ob_dict[foot], self.ob_dict["prev_" + foot]]

        self.target_yaw += self.commands[2] * self.timeStep 
        
        self.base_lin_vel = np.array([self.vx, self.vy, self.vz])
        self.base_ang_vel = np.array([self.roll_vel, self.pitch_vel, self.yaw_vel])
        self.dof_pos = np.array(self.joints)
        self.dof_vel = np.array(self.joint_vel)
        lin_vel = 1.0
        ang_vel = 1.0
        commands_scale = np.array([1.0, 1.0, 1.0])
        dof_pos = 1.0
        dof_vel = 0.05
     
        self.obs_buf = np.concatenate((  (self.base_lin_vel * lin_vel).reshape([1,3]),
                                (self.base_ang_vel  * ang_vel).reshape([1,3]),
                                np.array([[self.roll, self.pitch]]),
                                (self.commands[:3] * commands_scale).reshape([1,3]),
                                ((self.dof_pos - self.default_joints) * dof_pos).reshape([1,self.ac_size]),
                                (self.dof_vel * dof_vel).reshape([1,self.ac_size]),
                                (np.array(self.contacts)).reshape([1,8]),
                                self.actions.reshape([1,self.ac_size])
                                ),axis=-1)

    def apply_forces_yaw(self):
        yaw_force = 1.5*self.Kp*(self.commands[2] - self.yaw_vel)
        roll_force = 0.0
        pitch_force = 0.0
        # p.applyExternalTorque(self.Id,-1,[roll_force,pitch_force,yaw_force],p.WORLD_FRAME)
        p.applyExternalTorque(self.Id,-1,[roll_force,pitch_force,yaw_force],p.LINK_FRAME)


    def apply_forces(self):
        z_force = 1.0*(self.Kp * ((self.ROBOT_HEIGHT + self.z_offset)-self.body_xyz[2]) + 0.1*self.Kp * self.vz * -1)
        x_force = 10.0*self.Kp * (self.commands[0] - self.vx) 
        y_force = 10.0*self.Kp * (self.commands[1] - self.vy)
        p.applyExternalForce(self.Id,-1,[x_force,y_force,z_force],[0,0,0],p.LINK_FRAME)

        yaw_force = 1.5*self.Kp*(self.commands[2] - self.yaw_vel)
        roll_force = -0.1*self.Kp * self.roll        - 0.01*self.Kp*self.roll_vel
        pitch_force = -0.1*self.Kp * self.pitch    - 0.01*self.Kp*self.pitch_vel

        # p.applyExternalTorque(self.Id,-1,[roll_force,pitch_force,yaw_force],p.WORLD_FRAME)
        p.applyExternalTorque(self.Id,-1,[roll_force,pitch_force,yaw_force],p.LINK_FRAME)
        
        return 240*(np.array(self.exp_joints) - np.array(self.joints)) + 0.5*(np.zeros(self.ac_size) - np.array(self.joint_vel))

    def add_disturbance(self, max_dist=None, forward_only=False):
        if forward_only:
            force_x = np.random.random()*max_dist/2
        else:
            force_x = (np.random.random() - 0.5)*max_dist
        force_y = (np.random.random() - 0.5)*max_dist
        force_z = (np.random.random() - 0.5)*(max_dist/4)
        p.applyExternalForce(self.Id,-1,[force_x,force_y,force_z],[0,0,0],p.LINK_FRAME)
        force_roll = (np.random.random() - 0.5)*max_dist/2
        force_pitch = (np.random.random() - 0.5)*max_dist/2
        force_yaw = (np.random.random() - 0.5)*(max_dist/2)
        p.applyExternalTorque(self.Id,-1,[force_roll,force_pitch,force_yaw],p.LINK_FRAME)

        forces = 20.0*(max_dist/self.final_disturbance)*np.random.random(self.ac_size)
        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.TORQUE_CONTROL, forces=forces)

    def get_image(self):
        return self.terrain
    
    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        return_dict = {"Kp": self.Kp, "Success": self.cur_success, "Cur": self.args.cur}
        return_dict.update(self.reward_dict)
        return return_dict
    
# =========================================
# Rewards from IsaacGym, not used, just for inspiration
# =========================================
    def _reward_lin_vel_z(self):
        # Penalize z axis base linear velocity
        return torch.square(self.base_lin_vel[:, 2])
    
    def _reward_ang_vel_xy(self):
        # Penalize xy axes base angular velocity
        return torch.sum(torch.square(self.base_ang_vel[:, :2]), dim=1)
    
    def _reward_orientation(self):
        # Penalize non flat base orientation
        return torch.sum(torch.square(self.projected_gravity[:, :2]), dim=1)

    def _reward_base_height(self):
        # Penalize base height away from target
        # print(self.root_states[:10, 2].unsqueeze(1))
        base_height = torch.mean(self.root_states[:, 2].unsqueeze(1) - self.measured_heights, dim=1)
        return torch.square(base_height - self.cfg.rewards.base_height_target)
    
    def _reward_torques(self):
        # Penalize torques
        return torch.sum(torch.square(self.torques), dim=1)

    def _reward_ankle_torques(self):
        # Penalize ankle torques more
        return torch.sum(torch.square(self.torques[:, [2,5]]), dim=1)


    def _reward_dof_vel(self):
        # Penalize dof velocities
        return torch.sum(torch.square(self.dof_vel), dim=1)
    
    def _reward_dof_acc(self):
        # Penalize dof accelerations
        return torch.sum(torch.square((self.last_dof_vel - self.dof_vel) / self.dt), dim=1)
    
    def _reward_action_rate(self):
        # Penalize changes in actions
        return torch.sum(torch.square(self.last_actions - self.actions), dim=1)
    
    def _reward_collision(self):
        # Penalize collisions on selected bodies
        return torch.sum(1.*(torch.norm(self.contact_forces[:, self.penalised_contact_indices, :], dim=-1) > 0.1), dim=1)
    
    def _reward_termination(self):
        # Terminal reward / penalty
        return self.reset_buf * ~self.time_out_buf
    
    def _reward_dof_pos_limits(self):
        # Penalize dof positions too close to the limit
        out_of_limits = -(self.dof_pos - self.dof_pos_limits[:, 0]).clip(max=0.) # lower limit
        out_of_limits += (self.dof_pos - self.dof_pos_limits[:, 1]).clip(min=0.)
        return torch.sum(out_of_limits, dim=1)

    def _reward_dof_vel_limits(self):
        # Penalize dof velocities too close to the limit
        # clip to max error = 1 rad/s per joint to avoid huge penalties
        # print(self.dof_vel[:10])
        return torch.sum((torch.abs(self.dof_vel) - self.dof_vel_limits*self.cfg.rewards.soft_dof_vel_limit).clip(min=0., max=1.), dim=1)


    def _reward_heading(self):
        # Penalize dof velocities too close to the limit
        # clip to max error = 1 rad/s per joint to avoid huge penalties
        forward = quat_apply(self.base_quat, self.forward_vec)
        heading = torch.atan2(forward[:, 1], forward[:, 0])
        return torch.abs(heading)


    def _reward_torque_limits(self):
        # penalize torques too close to the limit
        return torch.sum((torch.abs(self.torques) - self.torque_limits*self.cfg.rewards.soft_torque_limit).clip(min=0.), dim=1)

    def _reward_tracking_lin_vel(self):
        # Tracking of linear velocity commands (xy axes)
        lin_vel_error = torch.sum(torch.square(self.commands[:, :2] - self.base_lin_vel[:, :2]), dim=1)
        return torch.exp(-lin_vel_error/self.cfg.rewards.tracking_sigma)
    
    def _reward_tracking_ang_vel(self):
        # Tracking of angular velocity commands (yaw) 
        ang_vel_error = torch.square(self.commands[:, 2] - self.base_ang_vel[:, 2])
        return torch.exp(-ang_vel_error/self.cfg.rewards.tracking_sigma)

    def _reward_feet_air_time(self):
        # Reward long steps
        # Need to filter the contacts because the contact reporting of PhysX is unreliable on meshes
        contact = self.contact_forces[:, self.feet_indices, 2] > 1.
        contact_filt = torch.logical_or(contact, self.last_contacts) 
        self.last_contacts = contact
        first_contact = (self.feet_air_time > 0.) * contact_filt
        self.feet_air_time += self.dt
        rew_airTime = torch.sum((self.feet_air_time - 0.5) * first_contact, dim=1) # reward only on first contact with the ground
        rew_airTime *= torch.norm(self.commands[:, :2], dim=1) > 0.1 #no reward for zero command
        self.feet_air_time *= ~contact_filt
        return rew_airTime

    def _reward_stumble(self):
        # Penalize feet hitting vertical surfaces
        return torch.any(torch.norm(self.contact_forces[:, self.feet_indices, :2], dim=2) >\
             5 *torch.abs(self.contact_forces[:, self.feet_indices, 2]), dim=1)
        
    def _reward_stand_still(self):
        # Penalize motion at zero commands
        return torch.sum(torch.abs(self.dof_pos - self.default_dof_pos), dim=1) * (torch.norm(self.commands[:, :2], dim=1) < 0.1)

    def _reward_feet_contact_forces(self):
        # penalize high contact forces
        return torch.sum((torch.norm(self.contact_forces[:, self.feet_indices, :], dim=-1) -  self.cfg.rewards.max_contact_force).clip(min=0.), dim=1)

    def _reward_jumping(self):
        # encourage both feet to be in the air or on the ground
        contact = self.contact_forces[:, self.feet_indices, 2] > 1.
        contacts = torch.logical_or(contact, self.last_contacts) 
        return torch.logical_and(contacts[:,0], contacts[:,1])
    
    def _reward_joints(self):
        # Penalise joints (for standing still)
        return torch.sum(torch.abs(self.dof_pos - self.default_dof_pos), dim=1)

    def _reward_exp_joints(self):
        # Encourage tracking expert joints
        if self.cfg.env.cur:
            exp_joint_error = torch.sum(torch.square(self.dof_pos[:,:6] - self.exp_joints[:,:6]), dim=1)
            return torch.exp(-exp_joint_error/self.cfg.rewards.exp_joint_sigma)
        else:
            return torch.zeros(self.num_envs, device=self.device, requires_grad=False)

    def _reward_ankles_and_hips(self):
        # penalize torques too close to the limit
        return torch.sum((torch.abs(self.dof_pos[:,[0,3]]) - self.dof_pos[:,[2,5]]), dim=1)

    def _reward_stand(self):
        # Standing still
        error =  torch.sum(torch.abs(self.dof_pos - self.standing_dof_pos), dim=1)
        return torch.exp(-error/self.cfg.rewards.stand_sigma)
    
    def _reward_spot_sym(self):
        # Symmetry for quadruped

        # "front_left_hip_x": 0.0,
        # "front_left_hip_y": 1.2,
        # "front_left_knee": -2.0,
        # "front_right_hip_x": 0.0,
        # "front_right_hip_y": 1.2,
        # "front_right_knee": -2.0,
        # "rear_left_hip_x": 0.0,
        # "rear_left_hip_y": 1.2,
        # "rear_left_knee": -2.0,
        # "rear_right_hip_x": 0.0,
        # "rear_right_hip_y": 1.2,
        # "rear_right_knee": -2.0

        # e.g. left front should match rear right
        front = [0,1,2,3,4,5]
        back = [9,10,11,6,7,8]
        return torch.sum(torch.square(self.actions[:,front] - self.actions[:,back]), dim=1)
    