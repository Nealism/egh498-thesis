import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
import numpy as np
import pybullet as p
from collections import deque
from pathlib import Path
home = str(Path.home())
from mpi4py import MPI
comm = MPI.COMM_WORLD
import time
import cv2
import random
import copy
np.set_printoptions(precision=3, suppress=True)
from utils.utils import display_images

from assets.env_base_pb import EnvBasePB

class Env(EnvBasePB):
    rank = comm.Get_rank()
    simStep = 1/120
    timeStep = 1/120
    ob_size = (12*2 + 8 + 7 + 8 + 2 + 4)
    ac_size = 12
    total_steps = 0
    steps = 0
    Kp = 400
    prev_local_Kp = local_Kp = 400
    initial_Kp = Kp
    Kd = 0.1
    height_coeff = 0.011
    max_yaw = 0.0
    episodes = 0
    iters_so_far = 0
    rew_Kp = 1
    max_v = 1.5
    min_v = 0.5
    max_yaw = 1.25
    # Strafe max velocity
    # max_vy = 0.75
    max_vy = 0.4
    pause_time = 50
    replace_Id = None
    grid_size = 0.025  
    eval = False
    dist_difficulty = 0
    max_action = 3
    def __init__(self, PATH=None, args=None):

        self.PATH = PATH
        self.args = args
        self.max_disturbance = self.args.initial_disturbance

        super().__init__(PATH)
        
        if self.args.multi_robots:
            self.robots = {}
            self.robot_num = 0
        self.stopped_start = True
        self.box_nums = [-1,0,1,2,3]
        self.num_boxes = len(self.box_nums)
        self.box_dim = 5
        
        if self.args.vis_type == 'hm':
            self.im_size = [60,40,1]
        elif self.args.vis_type == 'state':
            self.im_size = [self.num_boxes*self.box_dim]
        elif self.args.vis_type == 'rgbd':
            self.im_size = [48, 48, 4]
        elif self.args.vis_type == 'depth':
            self.im_size = [48, 48, 1]
        # self.im_size = [980, 980, 1]
        elif self.args.vis_type == 'state':
            self.im_size = [self.num_boxes*self.box_dim]

        self.reward_breakdown = {'goal':deque(maxlen=100), 'pos':deque(maxlen=100), 'vel':deque(maxlen=100),  'neg':deque(maxlen=100), 'tip':deque(maxlen=100), 'com':deque(maxlen=100), 'sym':deque(maxlen=100), 'act':deque(maxlen=100)}
    
        if self.args.render and self.args.MASTER:
            self.physicsClientId = p.connect(p.GUI)
        else:
            self.physicsClientId = p.connect(p.DIRECT) #DIRECT is much faster, but GUI shows the robot

        self.sim_data = []
        self.im_data = []
        self.load()
        self.box_info = None
        self.world_map = None
        self.z_offset = 0
        try:
            from assets.obstacles import Obstacles
        except:
            from obstacles import Obstacles
        self.obstacles = Obstacles()
        self.still_pos = np.array([0.0,0.0,-0.1,-0.2,0.0,-0.1,0.0,0.0,-0.1,-0.2,0.0,-0.1])
        self.target_joints = self.still_pos
        
        # if self.args.obstacle_type in ['hard_high_jumps', 'high_jumps']:
        #   self.args.num_artifacts = 1

        self.order = None
        self.args.cur_count = 0
        self.args.cur_len = self.args.cur_len
        if self.args.obstacle_type == 'mix':
            self.max_steps = 4047
            self.args.cur_len = 2000
        elif self.args.run_state in ["train_setup", "run_setup", "train_switch", "run_switch", "train_admis", "train_q", "run_admis"]:  
            if self.args.obstacle_type in ["stairs", "steps","up_stairs","down_stairs"]:
                self.max_steps = 400 + self.args.num_artifacts*500
                self.args.cur_len = 300 + self.args.num_artifacts*500
            else:
                self.max_steps = 300 + self.args.num_artifacts*400
                self.args.cur_len = 200 + self.args.num_artifacts*400 
        else:
            # if self.args.obstacle_type == "flat":
                # self.args.num_artifacts = 2
                # self.max_steps = 1200
                # self.args.cur_len = 1000
            if self.args.obstacle_type in ["flat","stairs", "steps","up_stairs","down_stairs"]:
                # self.max_steps = 400 + self.args.num_artifacts*500
                # self.args.cur_len = 300 + self.args.num_artifacts*500
                self.max_steps = 300 + self.args.num_artifacts*400
                self.args.cur_len = 200 + self.args.num_artifacts*400
            else:
                # self.max_steps = 300 + self.args.num_artifacts*400
                # self.args.cur_len = 200 + self.args.num_artifacts*400
                self.max_steps = 300 + self.args.num_artifacts*200
                self.args.cur_len = 200 + self.args.num_artifacts*200

        # self.order = None
        # self.args.cur_count = 0
        # self.args.cur_len = self.args.cur_len
        # if self.args.obstacle_type == 'mix' or self.args.run_state == "multi":
        #     self.max_steps = 4047
        #     self.args.cur_len = 2000        
        # elif self.args.num_artifacts > 2:
        #     self.max_steps = 2047
        #     self.args.cur_len = 1200
        # elif self.args.num_artifacts == 2:
        #     if self.args.obstacle_type == 'hard_steps':
        #         self.max_steps = 1700
        #     else:
        #         self.max_steps = 1200
        #     self.args.cur_len = 900
        # elif self.args.dqn:
        #     self.max_steps = 1200
        #     self.args.cur_len = 1000  
        # elif self.args.single_pol:
        #     self.max_steps = 1000
        #     self.args.cur_len = 700  
        # else:
        #     if self.args.obstacle_type in ['steps']:
        #         self.max_steps = 1000
        #         self.args.cur_len = 700  
        #     elif self.args.obstacle_type in ['gaps', 'jumps', 'hard_high_jumps']:
        #         self.max_steps = 700
        #         self.args.cur_len = 500
        #     elif self.args.obstacle_type in ['stairs', 'flat']:
        #         self.max_steps = 1000
        #         self.args.cur_len = 700
        #     elif self.args.obstacle_type in ['high_jumps']:
        #         self.max_steps = 500
        #         self.args.cur_len = 400
        #     else:
        #         self.max_steps = 1000
        #         self.args.cur_len = 700  
            
        self.iters_since_starting = 0
        self.avg_reward = 0
        self.best_reward = 1
        self.adapts = [0.9]
        self.min_difficulty = self.args.difficulty
        self.prev_cur = self.args.cur
        self.collect_data = False
        self.current_pol = self.args.obstacle_type
        if self.args.debug or args.render:
            # if self.replace_Id is not None:
            #     p.removeUserDebugItem(self.replace_Id)
            self.replace_Id = p.addUserDebugText(self.current_pol,[0,0,0],[0,0,1],textSize=3)
        self.success = deque([0],maxlen=self.args.cur_num)

    def load(self):
        if self.args.MASTER:
            p.loadMJCF(currentdir + "/xmls/ground.xml")
            objs = p.loadURDF(currentdir + "/urdfs/biped.urdf",flags = p.URDF_USE_SELF_COLLISION | p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS)
            self.Id = objs
        else:
            self.Id = 1
        
        p.setTimeStep(self.simStep)
        p.setGravity(0,0,-9.8)
        # ======================================================================

        numJoints = p.getNumJoints(self.Id)
        # Camera following robot:
        # body_xyz, (qx, qy, qz, qw) = p.getBasePositionAndOrientation(self.Id)
        # p.resetDebugVisualizerCamera(2.0, self.camera_rotation, -10.0, body_xyz)
        # p.resetDebugVisualizerCamera(2.0, 50, -10.0, body_xyz)

        self.jdict = {}
        self.feet_dict = {}
        self.leg_dict = {}
        self.body_dict = {}
        self.feet = ["left_heel1", "left_heel2", "left_toe1", "left_toe2", "right_heel1", "right_heel2", "right_toe1", "right_toe2"]
        self.feet_contact = {f:True for f in self.feet}
        self.ordered_joints = []
        self.ordered_joint_indices = []
        self.shin_dict = {}
        self.shins = ["left_shin", "right_shin", "left_thigh_link", "right_thigh_link", "base_link", "torso_link2"]
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            link_name = info[12].decode("ascii")
            if link_name in self.feet: self.feet_dict[link_name] = j
            if link_name in self.shins: self.shin_dict[link_name] = j
            if link_name=="base_link": self.body_dict["body_link"] = j
            self.ordered_joint_indices.append(j)
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            lower, upper = (info[8], info[9])
            self.ordered_joints.append( (j, lower, upper) )
            self.jdict[jname] = j
            
        self.motor_names = ["right_hip_z", "right_hip_x", "right_hip_y", "right_knee"]
        self.motor_names += ["right_ankle_x", "right_ankle_y"]
        self.motor_names += ["left_hip_z", "left_hip_x", "left_hip_y", "left_knee"]
        self.motor_names += ["left_ankle_x", "left_ankle_y"]
        self.motor_power = [300, 300, 900, 600]
        self.motor_power += [150, 300]
        self.motor_power += [300, 300, 900, 600]
        self.motor_power += [150, 300]

        self.motors = [self.jdict[n] for n in self.motor_names]
        
        forces = np.ones(len(self.motors))*240
        self.actions = {key:0.0 for key in self.motor_names}

        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(self.motor_names))

        for key in self.feet_dict:
            p.changeDynamics(self.Id, self.feet_dict[key],lateralFriction=0.9, spinningFriction=0.9)

        self.ep_lens = deque(maxlen=5)

        self.ep_speeds = deque(maxlen=5)
        self.speeds = [0]

        # self.terrain_cur_num = 2
        self.terrain_cur_num = self.args.cur_num

        # if self.args.terrain_first:
        #     self.ep_rewards = deque(maxlen=self.terrain_cur_num)
        #     self.success = deque(maxlen=self.args.cur_num)
        # else:
        self.ep_rewards = deque(maxlen=self.args.cur_num)
        self.success = deque(maxlen=self.args.cur_num)
        self.total_reward = 0

        self.pos_error = deque(maxlen=5)
        self.pos_errors = [0.0]
        self.step_time = {'right':deque(maxlen=100), 'left':deque(maxlen=100)}
        self.box_num = 0
        # self.replace_Id = None
        self.args.cur_history = []
        self.time_of_last_decay = 0
        self.ready_to_stop = False
        self.all_ready_to_stop = False
        self.start_box = 0
        self.all_difficulties = [0]

    def get_success(self):
        success = False
        if self.args.run_state in ["train_single"]:
        # if self.box_info is not None and ((self.box_num >= len(self.box_info[1]) - 1) or (self.steps >= self.max_steps - 2)):
            if (self.steps >= self.max_steps - 2):
                success = True
        else:
            if self.box_info is not None:
                # print(self.order)
                if (self.box_num >= self.target_index):
                    success = True
        return success

    def reset(self, params=None, base_before=False, box_info=None, cur_params=None, set_position=None, test=False, restore_state=None):
        if self.args.multi_robots and self.robot_num > 0:
            for r in range(1, self.robot_num+1):
                p.removeBody(self.robots[r]['Id'])
            self.robot_num = 0
            self.robots = {}

        if self.replace_Id is not None:
            p.removeUserDebugItem(self.replace_Id)
        
        self.foot_on_box = {'left':0,'right':0}   
        self.desired_box = {'left':0,'right':0}
        self.touchdown_pens = {0:[0], 1:[0]}
        self.touchdown_dists = {'left':0, 'right':0}
        self.touchdown_box = {'left':set(), 'right':set()}

        self.foot_box = {'right':{0}, 'left':{0}}
        self.args.current_foot_box = {'right':0, 'left':0}
        self.desired_box = {'right':0, 'left':0}
        self.step_sign = 0
        self.swing_on_ground_time = 0
        self.prev_thing = 0
        if self.args.obstacle_type in ['high_jumps','hard_high_jumps']:
            self.first_jump = True
            self.stage = '1'

        self.right_boxes = []
        self.left_boxes = []

        self.ep_lens.append(self.steps)

        # ===========================================================================================================
        # This is where we see if the previous episode was successful.
        # ===========================================================================================================
        if self.args.obstacle_type == 'mix':
            self.ep_rewards.append(self.steps)
        elif self.args.num_artifacts in [1,2,3] and self.box_info is not None:
            if self.steps >= self.max_steps - 2 and self.box_num > 1:
                self.ep_rewards.append(self.args.cur_len + 1)
            else: 
                self.ep_rewards.append(0)
        else:
            self.ep_rewards.append(self.total_reward)
            
        self.success.append(self.get_success())
        # ===========================================================================================================

        if self.args.early_stop and not self.args.cur and self.args.difficulty >= 10 and len(self.ep_rewards) >= self.terrain_cur_num and (np.array(self.ep_rewards)[-self.terrain_cur_num:] > self.args.cur_len).all():  
            self.ready_to_stop = True

        self.ep_speeds.append(np.mean(self.speeds))
        self.speeds = [0]

        self.pos_error.append(np.mean(self.pos_errors))
        self.pos_errors = []

        if self.prev_cur != self.args.cur:
            self.save_sim_data(tag="cur")
        self.prev_cur = self.args.cur

        if self.episodes > 0 and self.args.record_step:
            self.save_sim_data()
        self.sim_data = []
        self.im_data = []
        # ===========================================================================================================
        # Perturbation curriculum (After self.args.cur is set to False)
        # ===========================================================================================================
        if cur_params is not None:
            self.max_disturbance = np.clip(cur_params[2], 50, 2000)
        # elif not self.args.cur and self.args.comparison != 'no_stage3' and not self.eval and self.args.disturbances and (self.max_disturbance < self.args.final_disturbance ) and (self.height_coeff >= 0.07 or self.args.difficulty >= 10) and len(self.ep_rewards) == self.args.cur_num and (np.array(self.ep_rewards) > self.args.cur_len).all():
        elif not self.args.cur and self.args.comparison != 'no_stage3' and not self.eval and self.args.disturbances and (self.max_disturbance < self.args.final_disturbance ) and (self.height_coeff >= 0.07 or self.args.difficulty >= 10) and len(self.success) >= self.args.cur_num and (np.array(self.success) > 0).all():
            self.ep_rewards = deque(maxlen=self.args.cur_num)
            self.max_disturbance = self.args.final_disturbance
        # ===========================================================================================================
        
        if box_info is not None:
            self.obstacles.remove_obstacles()
            self.box_info = box_info
            for pos, size, colour in zip(self.box_info[1], self.box_info[2], self.box_info[3]):
                self.obstacles.add_box(pos=pos[:3], orn=pos[3:], size=size, colour=colour)
        elif self.args.obstacle_type != 'None':  
            # ===========================================================================================================
            # Terrain curriculum (Default is to run terrain curriculum first)
            # ===========================================================================================================
            if cur_params is not None:
                self.difficulty = np.clip(cur_params[1], 1, 10)
            # elif (not self.args.cur or self.args.terrain_first) and self.args.difficulty < 10 and len(self.ep_rewards) >= self.terrain_cur_num and (np.array(self.ep_rewards) > self.args.cur_len).all():  
            elif (not self.args.cur or self.args.terrain_first) and self.args.difficulty < 10 and len(self.success) >= self.args.cur_num and (np.array(self.success) > 0).all():  
                    
                if self.args.difficulty < 10:
                    self.args.difficulty += 1*self.args.inc
                if self.args.difficulty == 10:
                    self.ep_rewards = deque(maxlen=self.args.cur_num)
                    self.success = deque(maxlen=self.args.cur_num)
                    self.best_reward = self.avg_reward
                    self.save_sim_data(tag="terrain")
                else:
                    self.ep_rewards = deque(maxlen=self.terrain_cur_num)
                    self.success = deque(maxlen=self.terrain_cur_num)
                self.success.append(0)
                self.iters_since_starting = self.iters_so_far
            # ===========================================================================================================

            self.obstacles.remove_obstacles()
            # Terrains if using --obstacle_type mix:
            if self.args.run_state == 'mix':
                self.obstacle_types = ['flat','jumps','gaps','stairs','steps', 'high_jumps']
            else:
                self.obstacle_types = None
            if self.args.ood:
                self.difficulty = np.random.uniform(self.args.difficulty - 3, self.args.difficulty + 3)
                # self.difficulty = self.args.difficulty + 5
                # print("difficulty", self.difficulty)
            else:
                self.difficulty = self.args.difficulty
            self.order, self.ob_first_step, self.last_artifact_box = self.obstacles.add_straight_world(difficulty=self.difficulty, height_coeff=self.height_coeff, terrain_type=self.args.obstacle_type, num_artifacts=self.args.num_artifacts, args=self.args, obstacle_types=self.obstacle_types, dqn=self.args.dqn)

            self.box_info = self.obstacles.get_box_info()
            self.world_map = self.get_world_map(self.box_info)    
            self.box_num = 0

        # ===========================================================================================================
        # Guide force curriculum - default cur_decay is 'exp'. Terrain_first is True by default. Also see def log_stuff below for when self.args.cur is set to False
        # ===========================================================================================================
        if cur_params is not None:
            self.local_Kp = self.Kp = np.clip(cur_params[0], 0, 400)
        # elif len(self.ep_rewards) == self.args.cur_num and (np.array(self.ep_rewards) > self.args.cur_len).all():
        elif len(self.success) == self.args.cur_num and (np.array(self.success) > 0).all() and (np.array(self.all_difficulties) > 9).all():
            if self.args.cur_decay == 'exp':
                self.local_Kp = self.local_Kp*self.args.decay   
            elif self.args.cur_decay == 'linear':
                self.local_Kp = max(self.local_Kp - self.args.decay, 0)
            elif self.args.cur_decay == 'sigmoid':
                self.local_Kp = self.initial_Kp*(1 - 1/(1+np.exp(-(self.args.cur_count - 5))))
                self.args.cur_count += 1
            # Reset ep_rewards buffer
            self.ep_rewards = deque(maxlen=self.args.cur_num)
            self.success = deque(maxlen=self.args.cur_num)
            self.success.append(0)
        # ===========================================================================================================
        # Find out where target box is in self.order
        if self.order is not None:
            self.target_list = [n for n,i in enumerate(self.order) if i == self.args.obstacle_type]
            if len(self.target_list) > 0:
                self.target_index = self.target_list[-1] + 2
        else:
            self.target_index = 0
        
        start_rot = [0.0,0.0,0.0]
        start_orn = p.getQuaternionFromEuler(start_rot)
        
        self.body_xyz, self.yaw = [0.0, 0.0, 0.0 + 0.95], start_rot[2]
        self.boxes = np.zeros(self.im_size)
        
        self.ob_dict = {'prev_right_foot_left_ground':False,'prev_left_foot_left_ground':False,'left_foot_left_ground':False,'right_foot_left_ground':False}
        
        self.ob_dict['prev_right_heel1'] = self.ob_dict['right_heel1'] = False
        self.ob_dict['prev_right_heel2'] = self.ob_dict['right_heel2'] = False
        self.ob_dict['prev_right_toe2']  = self.ob_dict['right_toe2']  = False
        self.ob_dict['prev_right_toe1']  = self.ob_dict['right_toe1']  = False
        self.ob_dict['prev_left_heel1']  = self.ob_dict['left_heel1']  = False
        self.ob_dict['prev_left_heel2']  = self.ob_dict['left_heel2']  = False
        self.ob_dict['prev_left_toe2']   = self.ob_dict['left_toe2']   = False
        self.ob_dict['prev_left_toe1']   = self.ob_dict['left_toe1']   = False
        
        if self.args.obstacle_type == 'one_leg_hop':
            self.initial_swing_foot = self.ob_first_step > 0
        else:
            self.initial_swing_foot = np.random.randint(2)
        if self.initial_swing_foot:
            self.ob_dict['swing_foot'] = True
        else: 
            self.ob_dict['swing_foot'] = False
        self.ob_dict['cur_swing_foot'] = self.ob_dict['swing_foot']

        self.ob_dict['right_foot_swing'] = False
        self.ob_dict['left_foot_swing'] = False
        self.first_step = True
        self.step_count = 0

        # ===========================================================================================================
        # Starting position (different if training single policies or training switch/setup)
        # ===========================================================================================================
        if self.args.run_state in ["run_setup", "train_setup", "run_switch", "train_switch", "run_admis", "train_admis", "train_q"]:
            self.hj_steps = None
            # rand_box = np.random.randint(1,5)

            # if self.collect_data and self.args.obstacle_type == 'high_jumps':
            #     pos = [self.box_info[1][5][0] + np.random.uniform(0,0), np.random.uniform(-0.1,0.1), 0.95+self.z_offset] 
            #     orn, joints, base_vel, joint_vel = list(p.getQuaternionFromEuler([0,0,np.random.uniform(-0.1,0.1)])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)
            # elif self.args.obstacle_type == 'flat':
            #     pos = [self.box_info[1][rand_box][0] + np.random.uniform(0,0), self.box_info[1][rand_box][1] + np.random.uniform(-0.1,0.1), 0.95+self.z_offset] 
            #     orn, joints, base_vel, joint_vel = list(p.getQuaternionFromEuler([0,0,np.random.uniform(-0.3,0.3)])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)
            #     for i,j in enumerate(joints):
            #         if i in [0,1,2,6,7,8]:
            #             if (i in [7,8]):
            #                 if (i == 7 and joints[1] > 0) or (i == 8 and joints[2] < 0):
            #                     joints[i] = np.random.uniform(low=0.0, high=0.5)
            #                 else:
            #                     joints[i] = np.random.uniform(low=-0.5, high=0.0)
            #             else:
            #                 joints[i] = np.random.uniform(low=-0.5, high=0.5)
            #         elif i in [3,9]:
            #             joints[i] = np.random.uniform(low=-0.5, high=0.0)

            # else:
            # y_extents = self.box_info[2][0][1] - 0.17
            # y_extents = self.box_info[2][0][1] - 0.3
            y_extents = 0.1
            x = np.random.uniform(self.box_info[1][0][0], self.box_info[1][4][0]+self.box_info[2][4][0])
            pos = [x, np.random.uniform(-y_extents,y_extents), 0.95+self.z_offset] 
            orn, joints, base_vel, joint_vel = list(p.getQuaternionFromEuler([0,0,np.random.uniform(-0.3,0.3)])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)
        
        # elif self.args.doa or self.args.multi or self.args.obstacle_type in ['turn','mix']:
        #     pos, orn, joints, base_vel, joint_vel = [self.box_info[1][0][0],self.box_info[1][0][1],0.95 + self.z_offset], list(p.getQuaternionFromEuler([0,0,self.box_info[1][0][5]])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)

        else:
            # if self.args.obstacle_type in ['high_jumps']:
                # if self.args.num_artifacts == 1:
                #     self.start_box = 0
                # else:
            self.start_box = 0
            if self.box_info is not None:
                # y_extents = self.box_info[2][0][1] - 0.17
                y_extents = 0.2
                pos = [self.box_info[1][0][0] + np.random.uniform(-0.25,0.0), np.random.uniform(-y_extents,y_extents), 0.95+self.z_offset] 
            else:
                pos = [0 + np.random.uniform(-0.25,0.0), np.random.uniform(-0.3,0.3), 0.95+self.z_offset] 
            orn, joints, base_vel, joint_vel = list(p.getQuaternionFromEuler([0,0,np.random.uniform(-0.2,0.2)])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)
            # orn, joints, base_vel, joint_vel = list(p.getQuaternionFromEuler([0,0,np.random.uniform(-0.5,0.5)])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)

            # if self.start_box == 0:
                # pos = [self.box_info[1][0][0] + np.random.uniform(-0.23,-0.18), np.random.uniform(-0.15,0.15), 0.95+self.z_offset] 
            # else:
            #     pos = [self.box_info[1][1][0], np.random.uniform(-0.15,0.15), 0.95+self.z_offset] 

            # elif self.args.obstacle_type in ['hard_high_jumps','one_leg_hop']:
            #     if self.args.obstacle_type in ['hard_high_jumps']:
            #         if self.args.num_artifacts == 1:
            #             self.start_box = np.random.choice([0,2], p=[0.8,0.2])
            #         else:
            #             self.start_box = np.random.choice([0,2,4,6], p=[0.7,0.1,0.1,0.1])
            #         pos = [self.box_info[1][self.start_box][0], np.random.uniform(-0.15,0.15), 0.95+self.z_offset] 
            #     else:
            #         pos = [self.box_info[1][0][0] + np.random.uniform(0,0.1), np.random.uniform(-0.15,0.15), 0.95+self.z_offset] 
            
            # else:
            #     pos = [np.random.uniform(-0.05,0.1), np.random.uniform(-0.15,0.15), 0.95+self.z_offset] 
            
            # if self.eval:
            #     if self.args.obstacle_type in ['high_jumps']:
            #         pos = [self.box_info[1][0][0] + np.random.uniform(-0.23,-0.18), 0, 0.95+self.z_offset] 
            #     elif self.args.obstacle_type in ['hard_high_jumps','one_leg_hop']:
            #         pos = [self.box_info[1][0][0] + np.random.uniform(0,0.1), 0, 0.95+self.z_offset] 
            #     else:
            #         pos = [np.random.uniform(-0.05,0.1), 0, 0.95+self.z_offset] 
            #     orn, joints, base_vel, joint_vel = list(p.getQuaternionFromEuler([0,0,0])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)
            # else:
            # orn, joints, base_vel, joint_vel = list(p.getQuaternionFromEuler([0,0,np.random.uniform(-0.3,0.3)])), [0.]*len(self.motor_names), [[0,0,0],[0,0,0]], [0.]*len(self.motor_names)
        
            # base_vel = [[0,0,0],[0,0,0]]    
            # joints, joint_vel = [0.]*len(self.motor_names), [0.]*len(self.motor_names)

        if self.args.obstacle_type in ['hard_high_jumps','high_jumps']:
            mult = 1
            if self.args.obstacle_type == 'hard_high_jumps':
                mult = 2
            self.high_jump_first_left_ground = False
            self.high_jump_step = False
            self.high_jump_second_on_ground = False
            self.high_jump_second_left_ground = False
            self.second_high_jump_step = False

            if self.start_box >= 1*mult:
                self.high_jump_first_left_ground = True
                self.high_jump_step = True
            if self.start_box >= 2*mult:
                self.high_jump_second_on_ground = True
            if self.start_box >= 3*mult:
                self.high_jump_second_left_ground = True
                self.second_high_jump_step = True

        self.body_xyz[0] = pos[0]
        self.body_xyz[1] = pos[1]
        self.get_z_offset()
        # print(pos)
        pos = [pos[0], pos[1], 0.95+self.z_offset]

        self.target_pos = [pos[0], 0, pos[2]]
        if set_position is not None:
            self.set_position(set_position[0], set_position[1], set_position[2], set_position[3], set_position[4])
        else:
            self.set_position(pos, orn, joints, base_vel, joint_vel)

        self.prev_speed = self.speed = self.original_speed = self.prev_yaw_speed = self.yaw_speed = self.original_yaw_speed = self.prev_y_speed = self.y_speed = self.original_y_speed = 0.0
        self.prev_time_of_step = self.time_of_step = 0

        self.total_reward = 0
        self.steps = 0
        self.step_count = 0
        self.episodes += 1
        self.prev_artifact = None
        self.get_observation()
        self.prev_state = self.joints + self.joint_vel
        self.prev_joints = self.joints 
        self.prev_joint_vel = self.joint_vel

        # self.action_store = deque(maxlen=self.time_of_step)
        self.action_store = np.zeros([self.time_of_step, 4])
        
        # Work out hip angle needed to evenly walk over blocks
        if self.box_info is None:
            self.x_dist = 0.45
        else:
            self.x_dist = self.box_info[2][0][0]*2
        self.thigh_length = 0.29
        self.shin_length = 0.31
        standing_leg_length = np.sqrt(self.thigh_length**2 + self.shin_length**2 - 2*self.thigh_length*self.shin_length*np.cos(np.pi-0.2))
        angle = np.arccos((self.x_dist/2)/standing_leg_length)
        self.hip_y_total_angle = np.pi - 2*angle 
        self.hip_x_total_angle = 0.05
        self.hip_z_total_angle = 1.49

        self.state = self.joints + self.joint_vel + self.body + self.contacts + [0,0]
        return np.array(self.state)

    def stopped(self):
        return (self.ob_dict['left_foot_on_ground'] and self.ob_dict['right_foot_on_ground']) and (self.body_xyz[2] > self.z_offset + 0.9)

    def stop_pol(self):
        # return ((not self.ob_dict['left_foot_left_ground'] and not self.ob_dict['right_foot_left_ground']) and self.x_min > (self.box_info[1][self.target_list[-1]][0] + self.box_info[2][self.target_list[-1]][0])) or self.box_num == len(self.box_info[1]) - 2
        # print((self.box_num > self.target_list[-1] and self.x_min > (self.box_info[1][self.target_list[-1]][0] - self.box_info[2][self.target_list[-1]][0])) , self.box_num == len(self.box_info[1]) - 2)
        return (self.box_num > self.target_list[-1] and self.x_min > (self.box_info[1][self.target_list[-1]][0] - self.box_info[2][self.target_list[-1]][0])) or self.box_num == len(self.box_info[1]) - 2

    def step(self, actions=np.zeros(12), freeze_robot=False, frozen=False, set_position=None):
        # print(self.order)
        # if self.original_speed == 1 and (self.args.run_state in ["train_single"] and self.order[self.box_num] != self.args.obstacle_type and self.box_num > 1) or self.box_num == len(self.box_info[1]) - 1: 
        #     if self.args.obstacle_type not in ["high_jumps"] or (self.args.obstacle_type == "high_jumps" and self.x_min > (self.box_info[1][self.box_num][0] - self.box_info[2][self.box_num][0]) and self.ob_dict['left_foot_on_ground'] and self.ob_dict['right_foot_on_ground']):

        # if self.original_speed == 1 and (self.args.run_state in ["train_single", "run_single"] and self.x_min > (self.box_info[1][self.last_artifact_box][0] + self.box_info[2][self.last_artifact_box][0])) or self.box_num == len(self.box_info[1]) - 1:    
        if set_position is None:
            if self.stop_pol():
                # print("no speed due to ", self.box_num, self.target_list)
                self.original_speed = self.speed = 0
                self.time_of_step = 0
            elif self.original_speed == 0 and self.box_num < len(self.box_info[1]) - 1 and self.stopped():
                # If both feet in contact with the ground and body velcity stable, and height above thres:
                # print(np.sqrt(self.vx*self.vx + self.vy*self.vy + self.vz*self.vz), self.body_xyz[2] , self.z_offset + 0.9)
                # if (self.ob_dict['left_foot_on_ground'] and self.ob_dict['right_foot_on_ground']) and (self.body_xyz[2] > self.z_offset + 0.9) and np.sqrt(self.vx*self.vx + self.vy*self.vy + self.vz*self.vz) < 0.05:
                self.original_speed = self.speed = 1
                self.time_of_step = 60

                # print("setting speed")
            
        # if (not self.args.obstacle_type == 'mix' and not self.args.multi and (((self.steps*self.timeStep) % 3) == 0 and self.steps != 0)) or self.steps == self.pause_time:
        #     if not self.args.speed_cur:        
        #         if self.args.obstacle_type == 'run':
        #             self.original_speed = 4.0
        #         else:
        #             self.original_speed = 1.0 
        #     else:
        #         self.original_speed = np.random.uniform(low=self.min_v,high=self.max_v)           
        
        #     if random.random() < 0.05 or not self.args.speed_cur:
        #         self.yaw_speed = 0
        #     else:
        #         self.yaw_speed = np.random.uniform(low=-self.max_yaw,high=self.max_yaw)           
        
        #     if abs(self.original_speed) >= 0.2:
        #         self.time_of_step = int(60/abs(self.original_speed))
        #         self.dsp_time = int(20/abs(self.original_speed))
        #         self.action_store = np.zeros([self.time_of_step, 4])
        #     else:
        #         self.time_of_step = 0

        # speeds = np.array([self.original_speed, self.original_y_speed, self.original_yaw_speed])
        # if (speeds != 0).any():
        #     self.time_of_step = int(60/np.max(abs(speeds)))
        # # self.speed = np.clip(self.original_speed, self.prev_speed - 0.01, self.prev_speed + 0.01)
        # self.yaw_speed = 0
        # self.y_speed = 0.0


        # if self.time_of_step != 0 and (np.array([self.original_speed, self.original_y_speed, self.original_yaw_speed]) == 0).all() and (np.abs([self.speed, self.y_speed, self.yaw_speed]) < 0.01).all():
        #     self.time_of_step = 0

        if self.args.dist_off_ground:
            if self.args.disturbances and random.random() < 0.02:
                self.add_disturbance(self.max_disturbance)
        else:
            if self.args.disturbances and random.random() < 0.02 and (not self.ob_dict['left_foot_left_ground'] or not self.ob_dict['right_foot_left_ground']):
                self.add_disturbance(self.max_disturbance)
            
        self.prev_state = self.joints + self.joint_vel
        self.prev_joints = self.joints  
        self.prev_joint_vel = self.joint_vel
        self.actions = actions
        
        # if self.args.obstacle_type != 'None' and self.speed != 0:    
        #     if self.args.obstacle_type not in ['flat','mix']:
        #         if self.x_min > (self.box_info[1][-1][0] - self.box_info[2][-1][0]):
        #             if self.args.obstacle_type not in ['high_jumps', 'hard_high_jumps']:
        #                 self.speed = self.original_speed = 0
        #             elif self.args.obstacle_type in ['high_jumps', 'hard_high_jumps'] and (not self.ob_dict['left_foot_left_ground'] or not self.ob_dict['right_foot_left_ground']):
        #                 self.speed = self.original_speed = 0
        #     elif self.box_num >= (len(self.box_info[1]) - 1):
        #         self.speed = self.original_speed = 0

        # Calculate desired positions
        if self.args.obstacle_type == 'None':
            self.target_yaw = 0
        else:
            if self.box_num >= len(self.box_info[1]) - 1:
                self.target_yaw = self.box_info[1][self.box_num][5]
            else:
                self.target_yaw = self.box_info[1][self.box_num+1][5]

        self.get_expert()

        if self.args.cur:
            exp_forces = self.apply_forces(actions)
        else:
            exp_forces = np.zeros(self.ac_size)
        power_mult = 0.082*self.args.more_power

        if self.args.comparison in ['no_exp', 'no_link_no_exp']:
            forces = np.array(self.motor_power)*np.array(actions)*power_mult
        else:
            forces = np.array(self.motor_power)*np.array(actions)*power_mult + exp_forces

        if set_position is not None:
            self.set_position(pos=set_position[0], orn=set_position[1], joints=set_position[2])
            try:
                self.current_pol = set_position[3]
            except:
                pass                
        else:
            if self.args.expert:
                forces = exp_forces
                p.setJointMotorControlArray(self.Id, self.motors,controlMode=p.POSITION_CONTROL, targetPositions=self.target_joints)
            else:
                p.setJointMotorControlArray(self.Id, self.motors,controlMode=p.TORQUE_CONTROL, forces=forces)


        if self.args.multi_robots:
            if freeze_robot:
                # print("freezing at ", self.body_xyz)
                self.robot_num += 1
                self.robots[self.robot_num] = {}
                self.robots[self.robot_num]['Id'] = p.loadURDF(currentdir + "/robot.urdf",flags = p.URDF_USE_SELF_COLLISION | p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS)
                self.robots[self.robot_num]['pos'] = self.body_xyz
                self.robots[self.robot_num]['orn'] = [self.qx, self.qy, self.qz, self.qw]
                self.robots[self.robot_num]['joints'] = self.joints
                
            if frozen:
                self.set_position([0,0,-2], [0,0,0,1], robot_id=self.Id)   
            for i in range(1,self.robot_num+1):
                if self.body_xyz[0]  > self.robots[i]['pos'][0] + 0.4 or frozen:
                    self.set_position(self.robots[i]['pos'], self.robots[i]['orn'], joints=self.robots[i]['joints'], robot_id=self.robots[i]['Id'])   

        for _ in range(int(self.timeStep/self.simStep)):
            p.stepSimulation()

        if self.args.render:
            time.sleep(self.args.sleep)
        self.get_observation()
        self.prev_speed = self.speed
        self.prev_yaw_speed = self.yaw_speed
        self.prev_time_of_step = self.time_of_step
        self.prev_box_num = self.box_num

        if self.args.record_step: 
            self.record_sim_data()
        reward, done = self.get_reward()
        # print("removed reward")
        # reward, done = 0,0
        self.prev_actions = self.actions
        self.total_reward += reward
        self.steps += 1
        self.total_steps += 1
        
        if self.args.debug or self.args.render:
            try:
                self.replace_Id = p.addUserDebugText(self.current_pol,[self.body_xyz[0], self.body_xyz[1], self.body_xyz[2]+0.5],[0,0,1],textSize=3,replaceItemUniqueId=self.replace_Id)
            except Exception as e:
                print("error printing current pol", e)
                self.replace_Id = p.addUserDebugText("None",[self.body_xyz[0], self.body_xyz[1], self.body_xyz[2]+0.5],[0,0,1],textSize=3,replaceItemUniqueId=self.replace_Id)

        # self.state = self.joints + self.joint_vel + self.body + self.contacts + [self.original_speed, self.original_yaw_speed]
        self.state = self.joints + self.joint_vel + self.body + self.contacts + [0,0]
        return np.array(self.state), reward, done, None

    def get_reward(self):

        reward = 0
        done = False
        goal, pos, neg, vel, com, sym, tip = 0, 0, 0, 0, 0, 0, 0
        
        act = -0.0001*np.sum(self.actions**2)

        if sum([self.ob_dict[w] for w in self.shin_dict]) > 0 and not self.args.expert:
            done = True

        if self.args.obstacle_type in ['high_jumps', 'hard_high_jumps'] or (self.args.e2e and not self.args.flat_e2e):
            if not self.args.old_rew:
                if self.stage in ['1','2']:
                    goal = 0.0
                else:
                    goal = np.exp(-2.5*max(0, self.speed - self.vx)**2)

                pos = 0.65*np.exp(-2.0*np.sum((np.array(self.target_joints) - np.array(self.joints))**2))      
                com = 0.2*np.exp(-10*np.sum((np.array([self.roll, self.pitch, self.body_xyz[2], self.body_xyz[1], self.yaw]) - np.array([0.0, 0.0, self.target_pos[2], 0.0, 0.0]))**2))
                
                joints = np.array(self.joints)
                neg -= 0.01*np.sum((joints[:6] - joints[6:])**2)
                neg -= 0.05*(not (self.ob_dict['right_foot_left_ground'] == self.ob_dict['left_foot_left_ground']))
                
                if self.time_of_step > 0 and self.stage in ["3","4"] and not (self.ob_dict['right_foot_left_ground'] and self.ob_dict['left_foot_left_ground']):
                    neg -= 0.5
                if self.time_of_step > 0 and self.stage in ["1","2"] and (self.ob_dict['right_foot_left_ground'] or self.ob_dict['left_foot_left_ground']):
                    neg -= 0.2
            else:
                if self.args.train_multi:
                    if self.body_xyz[0] < self.box_info[1][5][0]:
                        target_x = self.box_info[1][5][0]
                        goal = np.exp(-1.0*(target_x - self.body_xyz[0])**2)
                    else:
                        if not self.hj_steps:
                            self.hj_steps = 0
                        else:
                            self.hj_steps += 1
                        if not self.high_jump_step:
                            target_x = self.box_info[1][6][0]
                        else:
                            target_x = self.box_info[1][7][0]
                        if self.hj_steps < 200 or (self.hj_steps > 200 and self.high_jump_step):
                            goal = np.exp(-2.5*(target_x - self.body_xyz[0])**2)
                        if not self.high_jump_step:
                            z_height = (self.box_info[1][6][2] + self.box_info[2][6][2])
                            if (not self.ob_dict['right_foot_left_ground'] and self.foot_pos['right'][2] > z_height) and (not self.ob_dict['left_foot_left_ground'] and self.foot_pos['left'][2] > z_height) and self.box_num == 7:
                                self.high_jump_step = True
                else:
                    mult = 1
                    if not self.high_jump_step:
                        target_x = self.box_info[1][mult*1][0]
                    else:
                        target_x = self.box_info[1][mult*2][0]
                    if self.steps < 200 or (self.steps > 200 and self.high_jump_step) or (self.steps > 400 and self.high_jump_second_on_ground) or (self.steps > 600 and self.second_high_jump_step):
                        goal = np.exp(-2.5*(target_x - self.body_xyz[0])**2)

                pos = 0.65*np.exp(-2.0*np.sum((np.array(self.target_joints) - np.array(self.joints))**2))      
                vel = 0.05*np.exp(-0.1*np.sum((np.zeros(self.ac_size) - np.array(self.joint_vel))**2))
            
                if self.stage == '1' and self.vx < 0.1:
                    neg -= self.vx

                if not self.high_jump_step and not self.args.train_multi:
                    z_height = (self.box_info[1][mult*1][2] + self.box_info[2][mult*1][2])
                    if (not self.ob_dict['right_foot_left_ground'] and self.foot_pos['right'][2] > z_height) and (not self.ob_dict['left_foot_left_ground'] and self.foot_pos['left'][2] > z_height) and self.box_num == mult*1:
                        self.high_jump_step = True

            com = 0.2*np.exp(-10*np.sum((np.array([self.roll, self.pitch, self.body_xyz[2], self.body_xyz[1], self.yaw]) - np.array([0.0, 0.0, self.target_pos[2], 0.0, 0.0]))**2))

            neg -= 0.01*np.sum((self.actions[:6] - self.actions[6:])**2)
            joints = np.array(self.joints)
            neg -= 0.01*np.sum((joints[:6] - joints[6:])**2)
            neg -= 0.05*(not (self.ob_dict['right_foot_left_ground'] == self.ob_dict['left_foot_left_ground']))
            if self.time_of_step > 0 and self.stage in ["3","4"] and (not self.ob_dict['right_foot_left_ground'] or not self.ob_dict['left_foot_left_ground']):
                neg -= 0.2
            
            if self.time_of_step > 0 and self.stage in ["1","2"] and (self.ob_dict['right_foot_left_ground'] or self.ob_dict['left_foot_left_ground']):
                neg -= 0.2
        
        else:
            goal = np.exp(-2.5*max(0, self.speed - self.vx)**2)
            pos = 0.65*np.exp(-2.0*np.sum((np.array(self.target_joints) - np.array(self.joints))**2))      
            vel = 0.05*np.exp(-0.1*np.sum((np.zeros(self.ac_size) - np.array(self.joint_vel))**2))
            
            if self.args.obstacle_type != 'None':
                if self.args.obstacle_type == 'flat':
                    com = 0.2*np.exp(-10*np.sum((np.array([self.roll, self.pitch, self.body_xyz[2], self.yaw]) - np.array([0.0, 0.0, 0.95+self.z_offset, self.target_yaw]))**2))
                else:
                    com = 0.2*np.exp(-10*np.sum((np.array([self.roll, self.pitch, self.body_xyz[2], self.body_xyz[1], self.yaw]) - np.array([0.0, 0.0, 0.95+self.z_offset, 0.0,self.box_info[1][self.box_num][5]]))**2))

            if self.ob_dict['right_foot_left_ground'] and self.ob_dict['left_foot_left_ground'] and (self.args.obstacle_type in ['flat','stairs','up_stairs','down_stairs','steps'] or (self.args.obstacle_type in ['gaps', 'jumps'] and self.args.cur)):
                neg -= 0.1      

            

            if self.step_count > 2 and self.time_of_step > 0:
                if min(self.touchdown_pen/5, 5.0) > 0:
                    neg -= min(self.touchdown_pen/5, 5.0)  
                    self.touchdown_pens[self.ob_dict['cur_swing_foot']].append(min(self.touchdown_pen/5, 5.0))
                    if self.ob_dict['cur_swing_foot']:
                        swing = 'right'
                        stance = 'left'
                    else:
                        stance = 'right'
                        swing = 'left'

        if self.args.run_state == "train_single" and self.args.obstacle_type not in ["gaps", "jumps", "steps"] and np.linalg.norm(self.foot_pos["left"] - self.foot_pos["right"]) > 0.4:
            done = True

        sym = 0.0
        # if self.time_of_step != 0 and self.step_count > 2:
        #     if self.args.cur_time < self.time_of_step:
        #         if self.ob_dict['cur_swing_foot']:
        #             swing = 'right'
        #             stance = 'left'
        #         else:
        #             swing = 'left'
        #             stance = 'right'
        #     current_hip_y = np.array([self.ob_dict[swing + '_hip_y_pos'], self.ob_dict[swing + '_knee_pos'], self.ob_dict[stance + '_hip_y_pos'], self.ob_dict[stance + '_knee_pos']])
        #     sym = sym_fact*np.exp(-5*np.sum((self.action_store[self.args.cur_time,:] - current_hip_y)**2))      
            
        #     self.action_store[self.args.cur_time, :] = current_hip_y

        reward = goal + pos + com + neg + sym + act + vel + tip
        self.pos_errors.append(pos)

        self.reward_breakdown['goal'].append(goal)
        self.reward_breakdown['pos'].append(pos)
        self.reward_breakdown['vel'].append(vel)
        self.reward_breakdown['neg'].append(neg)
        self.reward_breakdown['tip'].append(tip)
        self.reward_breakdown['com'].append(com)
        self.reward_breakdown['sym'].append(sym)
        self.reward_breakdown['act'].append(act)
        
        if self.args.doa or self.args.obstacle_type == 'mix':
            if self.body_xyz[2] < (0.6 + self.z_min) or self.box_num == len(self.box_info[1]) - 1 or (self.steps > self.max_steps):
                done = True
        else:
            if self.args.advantage2:
                if (self.steps > self.max_steps):
                    done = 2
                if self.args.obstacle_type == 'None':
                    if (self.body_xyz[2] < (0.7 + self.z_min)):   
                        done = 1
                elif (self.order[self.box_num] not in ['high_jumps', 'hard_high_jumps'] and self.body_xyz[2] < (0.7 + self.z_min)) or (self.order[self.box_num] in ['high_jumps', 'hard_high_jumps'] and self.body_xyz[2] < (0.6 + self.z_min)):   
                    done = 1
            else:
                if sum([self.ob_dict[w] for w in self.shin_dict]) > 0:
                    done = True
                if (self.steps > self.max_steps) or (self.order[self.box_num] not in ['high_jumps', 'hard_high_jumps'] and self.body_xyz[2] < (0.7 + self.z_min)) or (self.order[self.box_num] in ['high_jumps','hard_high_jumps'] and self.body_xyz[2] < (0.6 + self.z_min)):     
                    done = True
                if self.eval and self.args.obstacle_type not in ['high_jumps', 'hard_high_jumps']:
                    if self.args.obstacle_type == 'flat':
                        if self.box_num == len(self.box_info[1]) - 1:
                            done = True
                    else:
                        if self.x_min > (self.box_info[1][-1][0] - self.box_info[2][-1][0]):
                            done = True
        return reward, done

    def get_observation(self):
        jointStates = p.getJointStates(self.Id,self.ordered_joint_indices)
        self.joints = list(np.array([jointStates[j[0]][0] for j in self.ordered_joints[:int(self.ac_size)]]))
        # self.joint_vel = list(np.array([jointStates[j[0]][1] for j in self.ordered_joints[:int(self.ac_size)]]) + np.random.uniform(-0.5,0.5,self.ac_size))
        self.joint_vel = list(np.array([jointStates[j[0]][1] for j in self.ordered_joints[:int(self.ac_size)]]))
        
        self.ob_dict.update({n + '_pos':j for n,j in zip(self.motor_names, self.joints)})


        self.body_xyz, (self.qx, self.qy, self.qz, self.qw) = p.getBasePositionAndOrientation(self.Id)
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion([self.qx, self.qy, self.qz, self.qw])
        self.pos = list(self.body_xyz)
        self.orn = [self.qx, self.qy, self.qz, self.qw]
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

        self.ob_dict['prev_right_heel1']  = self.ob_dict['right_heel1'] 
        self.ob_dict['prev_right_heel2']  = self.ob_dict['right_heel2'] 
        self.ob_dict['prev_right_toe1']   = self.ob_dict['right_toe1']   
        self.ob_dict['prev_right_toe2']   = self.ob_dict['right_toe2']   
        self.ob_dict['prev_left_heel1']   = self.ob_dict['left_heel1'] 
        self.ob_dict['prev_left_heel2']   = self.ob_dict['left_heel2'] 
        self.ob_dict['prev_left_toe1']    = self.ob_dict['left_toe1']   
        self.ob_dict['prev_left_toe2']    = self.ob_dict['left_toe2']   

        self.ob_dict['right_heel1'] = len(p.getContactPoints(self.Id, -1, self.feet_dict['right_heel1'], -1))>0
        self.ob_dict['right_heel2'] = len(p.getContactPoints(self.Id, -1, self.feet_dict['right_heel2'], -1))>0
        self.ob_dict['right_toe1']  = len(p.getContactPoints(self.Id, -1, self.feet_dict['right_toe1'], -1))>0
        self.ob_dict['right_toe2']  = len(p.getContactPoints(self.Id, -1, self.feet_dict['right_toe2'], -1))>0
        self.ob_dict['left_heel1']  = len(p.getContactPoints(self.Id, -1, self.feet_dict['left_heel1'], -1))>0
        self.ob_dict['left_heel2']  = len(p.getContactPoints(self.Id, -1, self.feet_dict['left_heel2'], -1))>0
        self.ob_dict['left_toe1']   = len(p.getContactPoints(self.Id, -1, self.feet_dict['left_toe1'], -1))>0
        self.ob_dict['left_toe2']   = len(p.getContactPoints(self.Id, -1, self.feet_dict['left_toe2'], -1))>0

        for w in self.shin_dict:
            self.ob_dict[w] = len(p.getContactPoints(self.Id, -1, self.shin_dict[w], -1))>0

        # Update feet that have left the ground.
        self.ob_dict['prev_right_foot_left_ground'] = self.ob_dict['right_foot_left_ground']
        self.ob_dict['prev_left_foot_left_ground'] = self.ob_dict['left_foot_left_ground']
        self.ob_dict['right_foot_left_ground'] = not self.ob_dict['right_heel1'] and not self.ob_dict['right_heel2'] and not self.ob_dict['right_toe2'] and not self.ob_dict['right_toe1']
        self.ob_dict['left_foot_left_ground'] = not self.ob_dict['left_heel1'] and not self.ob_dict['left_heel2'] and not self.ob_dict['left_toe2'] and not self.ob_dict['left_toe1']
        
        self.ob_dict['right_full_foot_on_ground'] = self.ob_dict['right_heel1'] and self.ob_dict['right_heel2'] and self.ob_dict['right_toe2'] and self.ob_dict['right_toe1']    
        self.ob_dict['left_full_foot_on_ground'] = self.ob_dict['left_heel1'] and self.ob_dict['left_heel2'] and self.ob_dict['left_toe2'] and self.ob_dict['left_toe1']    
        
        self.ob_dict['right_foot_on_ground'] = not self.ob_dict['right_foot_left_ground']
        self.ob_dict['left_foot_on_ground'] = not self.ob_dict['left_foot_left_ground']
        
        right_contacts = [self.ob_dict['right_heel1'],self.ob_dict['right_heel2'],self.ob_dict['right_toe2'],self.ob_dict['right_toe1']]
        left_contacts = [self.ob_dict['left_heel1'],self.ob_dict['left_heel2'],self.ob_dict['left_toe2'],self.ob_dict['left_toe1']]
        prev_right_contacts = [self.ob_dict['prev_right_heel1'],self.ob_dict['prev_right_heel2'],self.ob_dict['prev_right_toe2'],self.ob_dict['prev_right_toe1']]
        prev_left_contacts = [self.ob_dict['prev_left_heel1'],self.ob_dict['prev_left_heel2'],self.ob_dict['prev_left_toe2'],self.ob_dict['prev_left_toe1']]

        self.foot_pos = {}
        self.foot_pos['left'] = np.array(p.getLinkState(self.Id, self.feet_dict['left_heel1'])[0])
        self.foot_pos['right'] = np.array(p.getLinkState(self.Id, self.feet_dict['right_heel1'])[0])

        self.local_foot_pos = {}
        self.local_foot_pos['left'] = self.global_to_local_2d(self.body_xyz, self.yaw, self.foot_pos['left'])
        self.local_foot_pos['right'] = self.global_to_local_2d(self.body_xyz, self.yaw, self.foot_pos['right'])
        self.x_min = min(self.body_xyz[0], self.foot_pos['left'][0], self.foot_pos['right'][0])
        self.x_max = max(self.body_xyz[0], self.foot_pos['left'][0], self.foot_pos['right'][0])

        if self.ob_dict['right_foot_swing']:
            swing = 'right'
            stance = 'left'
        else: 
            swing = 'left'
            stance = 'right'

        if self.time_of_step == 0:
            self.ob_dict['right_foot_swing'] = 0
            self.ob_dict['left_foot_swing'] = 0
            if self.box_info is not None:
                for foot in ['right', 'left']:
                    for i in range(self.box_num-2, self.box_num+2):
                        if i < 0 or i > (len(self.box_info[0]) - 1): continue
                        x, y = self.foot_pos[foot][0], self.foot_pos[foot][1]
                        length, width = self.box_info[2][i][0], self.box_info[2][i][1]
                        box_yaw = self.box_info[1][i][5] 
                        diag = np.sqrt(length**2 + width**2)
                        x1 = self.box_info[1][i][0] + diag*np.cos(box_yaw+np.arctan2( width,  length))
                        y1 = self.box_info[1][i][1] + diag*np.sin(box_yaw+np.arctan2( width,  length))
                        x2 = self.box_info[1][i][0] + diag*np.cos(box_yaw+np.arctan2(-width, -length))
                        y2 = self.box_info[1][i][1] + diag*np.sin(box_yaw+np.arctan2(-width, -length))
                        if x1 > x2:
                            x_temp = x1
                            x1 = x2
                            x2 = x_temp
                        if y1 > y2:
                            y_temp = y1
                            y1 = y2
                            y2 = y_temp
                        if x1 < x < x2 and y1 < y < y2:
                            self.desired_box[foot] = i
                            break
        else:

            if self.ob_dict['prev_' + swing + '_foot_left_ground'] and not self.ob_dict[swing + '_foot_left_ground']:
                self.swing_on_ground_time = self.steps

        self.swing_stance = [self.ob_dict['right_foot_swing'], self.ob_dict['left_foot_swing']]

        self.contacts = right_contacts + left_contacts + prev_right_contacts + prev_left_contacts + self.swing_stance
        # self.contacts = right_contacts + left_contacts + prev_right_contacts + prev_left_contacts + [self.initial_swing_foot]

        # Find current box number (under com)
        if self.box_info is not None:
            if self.box_num == None:
                self.box_num = 0
            i = self.box_num
            total_i = 0
            while True:
                x, y = self.body_xyz[0], self.body_xyz[1]

                x1, y1 = self.box_info[1][i][0] - self.box_info[2][i][0], self.box_info[1][i][1] - self.box_info[2][i][1]
                x2, y2 = self.box_info[1][i][0] + self.box_info[2][i][0], self.box_info[1][i][1] + self.box_info[2][i][1]
                
                if x1 > x2:
                    x_temp = x1
                    x1 = x2
                    x2 = x_temp
                elif y1 > y2:
                    y_temp = y1
                    y1 = y2
                    y2 = y_temp
                if x1 < x < x2 and y1 < y < y2:
                    self.box_num = i
                    break
                i += 1
                total_i += 1
                if i > (len(self.box_info[0]) - 1):
                    i = 0
                if total_i > (len(self.box_info[0]) - 1):
                    # ("com not over box, box number frozen"), box number will remain the last box number
                    break
            
            for foot in ['left','right']:
                # foot_pos = p.getLinkState(self.Id, self.feet_dict[foot +'_heel1'])[0]
                for i in range(self.box_num-1, self.box_num+2):
                    if i < 0 or i > (len(self.box_info[0]) - 1): continue
                    x, y = self.foot_pos[foot][0], self.foot_pos[foot][1]
                    x1, y1 = self.box_info[1][i][0] - self.box_info[2][i][0], self.box_info[1][i][1] - self.box_info[2][i][1]
                    x2, y2 = self.box_info[1][i][0] + self.box_info[2][i][0], self.box_info[1][i][1] + self.box_info[2][i][1]
                    if x1 > x2:
                        x_temp = x1
                        x1 = x2
                        x2 = x_temp
                    elif y1 > y2:
                        y_temp = y1
                        y1 = y2
                        y2 = y_temp
                    if x1 < x < x2 and y1 < y < y2:
                        self.foot_on_box[foot] = i
                        break

            # Need to play with this
            self.boxes = []
            self.null_box = [0]*self.box_dim
            for box in self.box_nums:
                if (self.box_num + box < 1) or (self.box_num + box > len(self.box_info[0]) - 1):
                    self.boxes.extend(self.null_box)
                else:

                    length, width = self.box_info[2][self.box_num+box][0], self.box_info[2][self.box_num+box][1]

                    box_yaw = self.box_info[1][self.box_num+box][5] 
                    
                    diag = np.sqrt(length**2 + width**2)
                    self.world_box_x1 = self.box_info[1][self.box_num+box][0] + diag*np.cos(box_yaw+np.arctan2( width,  length))
                    self.world_box_y1 = self.box_info[1][self.box_num+box][1] + diag*np.sin(box_yaw+np.arctan2( width,  length))
                    self.world_box_x2 = self.box_info[1][self.box_num+box][0] + diag*np.cos(box_yaw+np.arctan2( width, -length))
                    self.world_box_y2 = self.box_info[1][self.box_num+box][1] + diag*np.sin(box_yaw+np.arctan2( width, -length))
                    self.world_box_x3 = self.box_info[1][self.box_num+box][0] + diag*np.cos(box_yaw+np.arctan2(-width,  length))
                    self.world_box_y3 = self.box_info[1][self.box_num+box][1] + diag*np.sin(box_yaw+np.arctan2(-width,  length))
                    self.world_box_x4 = self.box_info[1][self.box_num+box][0] + diag*np.cos(box_yaw+np.arctan2(-width, -length))
                    self.world_box_y4 = self.box_info[1][self.box_num+box][1] + diag*np.sin(box_yaw+np.arctan2(-width, -length))

                    box_x1, box_y1 = self.global_to_local_2d(self.body_xyz, self.yaw, [self.world_box_x1, self.world_box_y1])
                    box_x2, box_y2 = self.global_to_local_2d(self.body_xyz, self.yaw, [self.world_box_x4, self.world_box_y4])

                    z  = self.body_xyz[2] - (self.box_info[1][self.box_num+box][2] + self.box_info[2][self.box_num+box][2])
                    # z  = self.body_xyz[2] - (self.box_info[1][self.box_num+box][2]*2)
                    self.boxes.extend([box_x1,box_y1,box_x2,box_y2,z])
        else:
            self.boxes = [0.0]*self.box_dim*self.num_boxes
        
        if self.box_num is None or self.box_info is None:
            self.z_min = 0
        else:
            zs = []
            zs.append(self.box_info[1][self.box_num][2] + self.box_info[2][self.box_num][2])
            if self.box_num - 1 > 0:
                zs.append(self.box_info[1][self.box_num - 1][2] + self.box_info[2][self.box_num - 1][2])
            if self.box_num + 1 < len(self.box_info[0]) - 1:
                zs.append(self.box_info[1][self.box_num + 1][2] + self.box_info[2][self.box_num + 1][2])
            self.z_min = min(zs)
            if self.z_min < 0.1:
                zs.remove(self.z_min)
                self.z_min = min(zs)

    def get_terrain(self, box_tense="current"):
        if box_tense == "current":
            num = 0
        elif box_tense == "previous":
            num = -1
        elif box_tense == "next":   
            num = 1
        if self.order[self.box_num + num] == "zero":
            return "flat"
        else:
            return self.order[self.box_num + num]

    def get_expert(self):
        if (np.abs([self.speed, self.y_speed, self.yaw_speed]) < 0.1).all():
            self.target_joints = copy.copy(self.still_pos)
            self.args.cur_time = 0
            self.ob_dict['right_foot_swing'] = 0
            self.ob_dict['left_foot_swing'] = 0
            self.stage = '1'
            self.phase = 0
            if self.args.obstacle_type == 'None':
                self.target_pos = [self.body_xyz[0], self.body_xyz[1], self.z_offset + 0.95]
            else:
                self.target_pos = [self.body_xyz[0], self.body_xyz[1], self.z_offset + 0.95]
                # self.target_pos = [self.box_info[1][self.box_num][0], self.box_info[1][self.box_num][1], self.z_offset + 0.95]
        else:
            if self.args.obstacle_type in ['high_jumps','hard_high_jumps']:
                if (self.args.e2e and self.args.flat_e2e):
                    self.get_walking_expert()
                else:
                    self.get_jumping_expert()
            else:
                self.get_walking_expert()

    def get_jumping_expert(self):
        '''
        upright, lower, jump, pull in legs, land (upright)
        vertical velocity
        '''
        dy = 0.0
        self.target_orn = [0,0,0,1]

        if self.stage == '1' and not (self.ob_dict['left_foot_left_ground'] and self.ob_dict['right_foot_left_ground']) and (np.array([self.vx, self.vy, self.vz ])< 0.1).all() and (self.body_xyz[2] > self.foot_pos['left'][2] + 0.8) and (self.body_xyz[2] > self.foot_pos['right'][2] + 0.8):
            self.stage = '2'
            self.phase = 0

        # Lower
        if self.stage == '2' and (((self.body_xyz[2] < self.foot_pos['left'][2] + 0.6) and (self.body_xyz[2] < self.foot_pos['right'][2] + 0.6)) or (self.phase > 50)):
            self.stage = '3'
            self.phase = 0
        
        # Jump
        if self.stage == '3' and (self.phase > 25 ):
            self.stage = '4'
            self.phase = 0
      
        # Lift legs
        if self.stage == '4' and (self.phase > 25 or (not self.ob_dict['left_foot_left_ground'] and not self.ob_dict['right_foot_left_ground'])):
            self.stage = '1'
            self.phase = 0

        # if self.stage in ['2','3','4']:
        self.phase += 1
        
        if self.stage in ['1','2']:
            self.speed = 0.15
        else:
            self.speed = 1.2

        dx = self.speed * self.timeStep

        if self.stage == '1':
            if self.target_joints[self.motor_names.index("left_hip_y")] < 0.0:
                self.target_joints[self.motor_names.index("left_hip_y")]   += 0.03
            if self.target_joints[self.motor_names.index("left_knee")]  < 0.0:
                self.target_joints[self.motor_names.index("left_knee")]    += 0.06
            if self.target_joints[self.motor_names.index("left_ankle_y")] > 0.5:
                self.target_joints[self.motor_names.index("left_ankle_y")] -= 0.03
            if self.body_xyz[2] > (self.z_offset + 0.95):
            # dz = -0.01
                dz = -0.02
            else:
                dz = 0

        # lower
        if self.stage == '2':
            if self.target_joints[self.motor_names.index("left_hip_y")] > -1.0:
                self.target_joints[self.motor_names.index("left_hip_y")]   -= 0.03
            if self.target_joints[self.motor_names.index("left_knee")]  > -2.0:
                self.target_joints[self.motor_names.index("left_knee")]    -= 0.06
            if self.target_joints[self.motor_names.index("left_ankle_y")] > -0.5:
                self.target_joints[self.motor_names.index("left_ankle_y")] -= 0.03
        dz = -0.005

        # Jump
        if self.stage == '3':
            if self.target_joints[self.motor_names.index("left_hip_y")] < 0.0:
                self.target_joints[self.motor_names.index("left_hip_y")]   += 0.08
            if self.target_joints[self.motor_names.index("left_knee")]  < 0.0:
                self.target_joints[self.motor_names.index("left_knee")]    += 0.15
            if self.target_joints[self.motor_names.index("left_ankle_y")] < 0.5:
                self.target_joints[self.motor_names.index("left_ankle_y")] += 0.08
            # dz = 0.01
            dz = 0.0225
            # dx = 0.01

        # pull in legs
        if self.stage == '4':
            if self.target_joints[self.motor_names.index("left_hip_y")] > -1.0:
                self.target_joints[self.motor_names.index("left_hip_y")]   -= 0.3
            if self.target_joints[self.motor_names.index("left_knee")]  > -2.0:
                self.target_joints[self.motor_names.index("left_knee")]    -= 0.6
            if self.target_joints[self.motor_names.index("left_ankle_y")] > -0.5:
                self.target_joints[self.motor_names.index("left_ankle_y")] -= 0.08
            dz = 0.01

        self.ob_dict['right_foot_swing'] = True
        self.ob_dict['left_foot_swing']  = True

        self.target_joints[self.motor_names.index("right_hip_y")]   = self.target_joints[self.motor_names.index("left_hip_y")]   
        self.target_joints[self.motor_names.index("right_knee")]    = self.target_joints[self.motor_names.index("left_knee")]    
        self.target_joints[self.motor_names.index("right_ankle_y")] = self.target_joints[self.motor_names.index("left_ankle_y")] 

        self.target_pos = [self.target_pos[0]+dx,self.target_pos[1]+dy,self.target_pos[2]+dz]

    def get_walking_expert(self):
        # Was previously stopped, now need to select a swing foot
        if self.prev_time_of_step == 0 and self.time_of_step != 0:
            if self.args.obstacle_type == 'one_leg_hop':
                self.ob_dict['swing_foot'] = self.ob_first_step
            else:
                self.ob_dict['swing_foot'] = self.ob_dict['cur_swing_foot'] = np.random.randint(2)
            self.ob_dict['right_foot_swing'] = self.ob_dict['swing_foot']
            self.ob_dict['left_foot_swing'] = not self.ob_dict['right_foot_swing']

        if self.ob_dict['cur_swing_foot']:
            swing = 'right'
            stance = 'left'
        else:
            swing = 'left'
            stance = 'right'
        self.touchdown_pen = 0
        
        # if self.time_of_step > 0.0 and ((self.args.expert or self.args.comparison in ['no_link','no_link_no_exp']) and (self.steps-self.pause_time) % self.time_of_step == 0) or (not (self.args.expert or self.args.comparison in ['no_link','no_link_no_exp']) and self.ob_dict['prev_' + swing + '_foot_left_ground'] and not self.ob_dict[swing + '_foot_left_ground']):
        if self.original_speed > 0 and self.ob_dict['prev_' + swing + '_foot_left_ground'] and not self.ob_dict[swing + '_foot_left_ground']:
    
            self.touchdown_pen = abs(self.args.cur_time - self.time_of_step)
            self.touchdown_dists[swing] = (self.local_foot_pos[swing][0])
            
            if len(self.touchdown_box[swing]) > 0:
                max_box = max(self.touchdown_box[swing])
                if (max_box - self.foot_on_box[swing]) != 2:
                    self.single_step = True
                else:
                    self.single_step = False

            if self.foot_on_box[swing] not in self.touchdown_box[stance]:
                if len(self.touchdown_box[swing]) > 0 and abs(max_box - self.foot_on_box[swing]) > 1:
                    self.touchdown_box[swing].add(self.foot_on_box[swing])
                elif len(self.touchdown_box[swing]) < 1:
                    self.touchdown_box[swing].add(self.foot_on_box[swing])
                self.double_feet = False
            else:
                self.double_feet = True

            self.args.cur_time = 0
            self.ob_dict['cur_swing_foot'] = not self.ob_dict['cur_swing_foot']
            self.step_count += 1
            
            if self.box_info is not None:
                if self.ob_dict['cur_swing_foot']:
                    swing = 'right'
                    stance = 'left'
                else:
                    swing = 'left'
                    stance = 'right'

                if self.foot_on_box[stance] + 1 < len(self.box_info[1]):
                    self.desired_box[swing] = self.foot_on_box[stance] + 1
    
        self.ob_dict['swing_foot'] = self.ob_dict['cur_swing_foot']
        if self.ob_dict['swing_foot']:
            self.ob_dict['right_foot_swing'] = True
        else:
            self.ob_dict['right_foot_swing'] = False
        self.ob_dict['left_foot_swing'] = not self.ob_dict['right_foot_swing']

        step_type = 'flat'
        step_fact = 0
        swing_fact = 2.5
        # if self.steps - self.pause_time < self.time_of_step:
        if self.original_speed == 0:
            stance_hip = self.hip_y_total_angle/4
            swing_hip  = -self.hip_y_total_angle/4
            if self.args.cur_time < 2*self.time_of_step/4:
                swing_knee = -0.4
            else:
                swing_knee = -0.2
            stance_knee = -0.2
        else:
            stance_hip = 2*self.hip_y_total_angle/5 
            swing_hip  = -3*self.hip_y_total_angle/5 
            if self.args.cur_time < swing_fact*self.time_of_step/4:
                swing_knee = -1.3
            else:
                swing_knee = -0.2
            stance_knee = -0.2
                    
        delta = 1.2*(0.015*(1.0*abs(self.speed)) + 0.1*step_fact)
        knee_delta = 1.2*(0.04*(1.0* abs(self.speed))+ 0.1*step_fact)

        stance_hip_x = 0.05
        take_off_ankle_y = 0.3
        if self.speed < 0:
            if swing == 'right':
                # Swing
                self.target_joints[2] = min(self.target_joints[2] + delta, -swing_hip)
                if self.args.cur_time < swing_fact*self.time_of_step/4:
                    self.target_joints[3] = max(self.target_joints[3] - knee_delta, swing_knee)
                else:
                    self.target_joints[3] = min(self.target_joints[3] + knee_delta, swing_knee)
                # Stance
                self.target_joints[8] = max(self.target_joints[8] - delta, -stance_hip)
                self.target_joints[9] = min(self.target_joints[9] + knee_delta, stance_knee)
            else:
                # Swing
                self.target_joints[8] = min(self.target_joints[8] + delta, -swing_hip)
                if self.args.cur_time < swing_fact*self.time_of_step/4:
                    self.target_joints[9] = max(self.target_joints[9] - knee_delta, swing_knee)
                else:
                    self.target_joints[9] = min(self.target_joints[9] + knee_delta, swing_knee)
                # Stance
                self.target_joints[2] = max(self.target_joints[2] - delta, -stance_hip)
                self.target_joints[3] = min(self.target_joints[3] + knee_delta, stance_knee)
        elif self.speed == 0 and (self.yaw_speed or self.y_speed):
            y_dt = 40*0.02/self.time_of_step
            if swing == 'right':
                if self.args.cur_time < swing_fact*self.time_of_step/4:
                    self.target_joints[2] = max(self.target_joints[2] - y_dt, -0.3)
                    self.target_joints[3] = max(self.target_joints[3] - y_dt, -0.7)
                else:
                    self.target_joints[2] = min(self.target_joints[2] + y_dt, -0.1)
                    self.target_joints[3] = min(self.target_joints[3] + y_dt, -0.2)
            else:
                if self.args.cur_time < swing_fact*self.time_of_step/4:
                    self.target_joints[8] = max(self.target_joints[8] - y_dt, -0.3)
                    self.target_joints[9] = max(self.target_joints[9] - y_dt, -0.6)
                else:
                    self.target_joints[8] = min(self.target_joints[8] + y_dt, -0.1)
                    self.target_joints[9] = min(self.target_joints[9] + y_dt, -0.2)

        else:
            if swing == 'right':
                # Swing
                self.target_joints[2] = max(self.target_joints[2] - delta, swing_hip)
                if self.args.cur_time < swing_fact*self.time_of_step/4:
                    self.target_joints[3] = max(self.target_joints[3] - knee_delta, swing_knee)
                else:
                    self.target_joints[3] = min(self.target_joints[3] + knee_delta, swing_knee)
                # Stance
                self.target_joints[8] = min(self.target_joints[8] + delta, stance_hip)
                self.target_joints[9] = min(self.target_joints[9] + knee_delta, stance_knee)
            else:
                # Swing
                self.target_joints[8] = max(self.target_joints[8] - delta, swing_hip)
                if self.args.cur_time < swing_fact*self.time_of_step/4:
                    self.target_joints[9] = max(self.target_joints[9] - knee_delta, swing_knee)
                else:
                    self.target_joints[9] = min(self.target_joints[9] + knee_delta, swing_knee)
                # Stance
                self.target_joints[2] = min(self.target_joints[2] + delta, stance_hip)
                self.target_joints[3] = min(self.target_joints[3] + knee_delta, stance_knee)

        # right z
        if self.yaw_speed == 0:
            self.target_joints[0] = self.still_pos[0]
            self.target_joints[6] = self.still_pos[6]
        else:
            z_dt = 40*0.02/self.time_of_step
            if swing == 'right':
                if self.yaw_speed < 0:
                    self.target_joints[0] = max(self.target_joints[0] - z_dt, -self.hip_z_total_angle)
                    self.target_joints[6] = max(self.target_joints[6] - z_dt, -self.hip_z_total_angle)
                else:
                    self.target_joints[0] = min(self.target_joints[0] + z_dt, self.hip_z_total_angle)
                self.target_joints[6] = min(self.target_joints[6] + z_dt, self.hip_z_total_angle)
            else:
                if self.yaw_speed < 0:
                    self.target_joints[0] = min(self.target_joints[0] + z_dt, self.hip_z_total_angle)
                    self.target_joints[6] = min(self.target_joints[6] + z_dt, self.hip_z_total_angle)
                else:
                    self.target_joints[0] = max(self.target_joints[0] - z_dt, -self.hip_z_total_angle)
                    self.target_joints[6] = max(self.target_joints[6] - z_dt, -self.hip_z_total_angle)
            
        if self.y_speed == 0:
            self.target_joints[1] = self.still_pos[1]
            self.target_joints[7] = self.still_pos[7]
        else:
            x_dt = 120*0.002/self.time_of_step
            if swing == 'right':
                if self.y_speed < 0:            
                    self.target_joints[1] = max(self.target_joints[1] - x_dt, -self.hip_x_total_angle*4)
                    self.target_joints[7] = max(self.target_joints[7] - x_dt, -self.hip_x_total_angle*4)
                else:            
                    self.target_joints[1] = min(self.target_joints[1] + x_dt, self.hip_x_total_angle)
                    self.target_joints[7] = min(self.target_joints[7] + x_dt, self.hip_x_total_angle)
            else:
                if self.y_speed < 0:            
                    self.target_joints[1] = min(self.target_joints[1] + x_dt, self.hip_x_total_angle)
                    self.target_joints[7] = min(self.target_joints[7] + x_dt, self.hip_x_total_angle)
                else:            
                    self.target_joints[1] = max(self.target_joints[1] - x_dt, -self.hip_x_total_angle*4)
                    self.target_joints[7] = max(self.target_joints[7] - x_dt, -self.hip_x_total_angle*4)
                
        # Ankles
        self.target_joints[4] = self.target_joints[1]

        self.target_joints[10] = self.target_joints[7]

        if swing == 'right' and self.joints[2] < 0:
            self.target_joints[5] = self.still_pos[5] + self.target_joints[2]/2
        else:
            self.target_joints[5] = self.still_pos[5] - self.target_joints[2]/2

        if swing == 'left' and self.joints[8] < 0:
            self.target_joints[11] = self.still_pos[11] + self.target_joints[8]/2
        else:
            self.target_joints[11] = self.still_pos[11] - self.target_joints[8]/2

        self.args.cur_time += 1
        
        if self.args.obstacle_type in ['one_leg_hop', 'hard_steps']:
            if self.args.obstacle_type == 'one_leg_hop':
                dx = self.speed*self.timeStep
            else:
                dx = self.speed*self.timeStep
            dy = 0
            target_z =  self.z_offset + 0.95

        else:
            dx = self.speed*self.timeStep
            dy = dz = 0
            target_z =  self.target_pos[2] + dz
        if self.args.obstacle_type != 'None':
            self.target_pos = [self.target_pos[0]+dx*np.cos(self.box_info[1][self.box_num][5]),self.target_pos[1]+dx*np.sin(self.box_info[1][self.box_num][5]),target_z]
        else:
            self.target_pos = [self.target_pos[0]+dx,self.target_pos[1],target_z]

    def apply_forces(self, actions=None):
        # z_force = 1.5*(self.Kp * ((0.95+self.z_offset)-self.body_xyz[2]) + 0.1*self.Kp * self.vz * -1)
        # x_force = 1.0*self.Kp * (self.speed - self.vx)
        # if self.args.obstacle_type in ['flat', 'hard_steps'] and self.steps > 200:
        #     y_force = self.Kp*(0.0 - self.vy)
        # else:
            # y_force = 1.0*self.Kp*(0 - self.body_xyz[1]) + self.Kp*(0.0 - self.vy)
        # y_force = self.Kp*(0.0 - self.vy)

        if self.args.obstacle_type in ["gaps","stairs","up_stairs","down_stairs","steps","high_jumps","jumps"]:
            if self.args.obstacle_type == "high_jumps":
                if self.stage == '2':
                    z_force = 0
                else:
                    if self.vz < 0:
                        z_force = 0.5*self.Kp * (0.0 - self.body_vxyz[2])
                    else:
                        z_force = 0
            else:
                if self.vz < 0:
                    z_force = 0.5*self.Kp * (0.0 - self.body_vxyz[2])
                else:
                    z_force = 0
            foot_max_x = max(self.foot_pos['left'][0], self.foot_pos['right'][0])
            if self.args.obstacle_type in ["down_stairs"]:
                x_force = 0.5*self.Kp * (self.speed - self.body_vxyz[0]) + 2.0*self.Kp*(foot_max_x - self.body_xyz[0])
            else:
                x_force = 0.5*self.Kp * (self.speed - self.body_vxyz[0]) + 1.5*self.Kp*(foot_max_x - self.body_xyz[0])
            y_force = 1.0*self.Kp*(0 - self.body_xyz[1]) + self.Kp*(0.0 - self.body_vxyz[1])
            # y_force = 0
            # p.applyExternalForce(self.Id,-1,[x_force,y_force,z_force],[0,0,0],p.WORLD_FRAME)
            # print(x_force, y_force, z_force)
            p.applyExternalForce(self.Id,-1,[x_force,y_force,z_force],[0,0,0],p.LINK_FRAME)
        else:
            if self.vz < 0:
                z_force = 0.5*self.Kp * (0.0 - self.vz)
            else:
                z_force = 0
            foot_max_x = max(self.foot_pos['left'][0], self.foot_pos['right'][0])
            x_force = 0.1*self.Kp * (self.speed - self.vx) + 1.0*self.Kp*(foot_max_x - self.body_xyz[0])
            y_force = self.Kp*(0.0 - self.vy)
            p.applyExternalForce(self.Id,-1,[x_force,y_force,z_force],[0,0,0],p.LINK_FRAME)

        if self.speed < 0.3:
            if self.args.expert:
                yaw_force = 0.0
            else:
                yaw_force = 1.0*self.Kp*(self.target_yaw - self.yaw) - 0.1*self.Kp*self.yaw_vel
            roll_force = -1.0*self.Kp * self.roll    - 0.1*self.Kp*self.roll_vel
            pitch_force = -2.0*self.Kp * self.pitch  - 0.1*self.Kp*self.pitch_vel
        else:
            if self.args.expert:
                yaw_force = 0.0
            else:
                yaw_force = 1.0*self.Kp*(self.target_yaw - self.yaw) - 0.1*self.Kp*self.yaw_vel
            roll_force = -1.0*self.Kp * self.roll    - 0.1*self.Kp*self.roll_vel
            pitch_force = -2.0*self.Kp * self.pitch  - 0.1*self.Kp*self.pitch_vel
        p.applyExternalTorque(self.Id,-1,[roll_force,pitch_force,yaw_force],p.WORLD_FRAME)
    
        return (self.Kp/self.initial_Kp)*(80*(self.target_joints - np.array(self.joints)) + 0.5*(np.zeros(self.ac_size) - np.array(self.joint_vel)))

    def set_current_pol(self, current_pol):
        self.current_pol = current_pol

    def set_position(self, pos=[0,0,0], orn=[0,0,0,1], joints=None, velocities=None, joint_vel=None, robot_id=None):
        if robot_id is None:
            robot_id = self.Id
        pos = [pos[0], pos[1], pos[2]]
        p.resetBasePositionAndOrientation(robot_id, pos, orn)
        if joints is not None:
            if joint_vel is not None:
                for j, jv, m in zip(joints, joint_vel, self.motors):
                    p.resetJointState(robot_id, m, targetValue=j, targetVelocity=jv)
            else:
                for j, m in zip(joints, self.motors):
                    p.resetJointState(robot_id, m, targetValue=j)
        if velocities is not None:
            p.resetBaseVelocity(robot_id, velocities[0], velocities[1])

    def save_sim_data(self, PATH=None, last_steps=False, tag='', evaluate=False, force=False):
        if tag != '':
            tail = '_' + tag
        else:
            tail = tag
        if self.sim_data and (self.rank == 0 or force) or last_steps:
            if PATH is not None:
                path = PATH
            else:
                path = self.PATH
            try:
                if last_steps:
                    np.save(path + 'sim_data.npy', np.array(self.sim_data, dtype=object)[-300:,:])     
                else:
                    if self.eval or evaluate:
                        np.save(path + 'sim_data_eval' + tail + '.npy', np.array(self.sim_data, dtype=object))     
                    else:
                        np.save(path + 'sim_data' + tail + '.npy', np.array(self.sim_data, dtype=object))     
                try:
                    if self.box_info is not None:
                        if self.eval or evaluate:
                            np.save(path + 'box_info_eval' + tail + '.npy', np.array(self.box_info, dtype=object))
                        else:
                            np.save(path + 'box_info' + tail + '.npy', np.array(self.box_info, dtype=object))
                except Exception as e:
                    print("trying to save box info", e)
                if tag == '':
                    self.sim_data = []
            except Exception as e:
                    print("Save sim data error:")
                    print(e)
            np.save(path + 'im_data' + tail + '.npy', np.array(self.im_data, dtype=object))     

    def set_images(self, orig_im, recon_im):
        self.orig_im = orig_im
        self.recon_im = recon_im

    def record_sim_data(self):
        if len(self.sim_data) > 100000: return
        pos, orn = p.getBasePositionAndOrientation(self.Id)
        data = [pos, orn]
        joints = p.getJointStates(self.Id, self.motors)
        data.append([i[0] for i in joints])
        data.append(self.current_pol)
        self.sim_data.append(data)
        self.im_data.append(np.concatenate([self.orig_im, self.recon_im]))

    def get_robot_state(self):
        pos, orn = p.getBasePositionAndOrientation(self.Id)
        data = [pos, orn]
        joints = p.getJointStates(self.Id, self.motors)
        data.append([i[0] for i in joints])
        data.append(self.current_pol)      
        return data

    def to_grid(self, y, x):
        x = int(x/self.grid_size +(-self.min_x+1)/self.grid_size)
        y = int(y/self.grid_size + (-self.min_y+1)/self.grid_size)
        return (y, x) 

    def project_to_segment(self, p, v, w):
        l2 = (v[0] - w[0])**2 + (v[1] - w[1])**2
        if l2 == 0: 
            return v[0], v[1]
        t = ((p[0] - v[0]) * (w[0] - v[0]) + (p[1] - v[1]) * (w[1] - v[1])) / l2
        t = max(0, min(1, t))
        return [v[0] + t * (w[0] - v[0]), v[1] + t * (w[1] - v[1])] 

    def dist_to_segment(self, p, v, w):
        p_on_line = self.project_to_segment(p, v, w)
        return np.sqrt((p_on_line[0] - p[0])**2 + (p_on_line[1] - p[1])**2)

    def global_to_local_2d(self, robot_pos, robot_yaw, global_point):
        x1 = global_point[0] - robot_pos[0]
        y1 = global_point[1] - robot_pos[1]
        new_x_point = np.cos(-robot_yaw) * x1 - np.sin(-robot_yaw) * y1
        new_y_point = np.cos(-robot_yaw) * y1 + np.sin(-robot_yaw) * x1
        return new_x_point, new_y_point
  
    def transform_rot(self, yaw, pos, point):
        rot_mat = np.array(
        [[np.cos(-yaw), np.sin(-yaw), 0],
            [-np.sin(-yaw), np.cos(-yaw), 0],
            [		0,			 0, 1]] )
        x,y,z = np.dot(rot_mat,[point[0],point[1],point[2]])
        return pos[0] + x, pos[1] + y, pos[2] + z
  
    def transform_rot3d(self, euler_orn, pos, point):
        roll, pitch, yaw = euler_orn
        yaw_rot_mat = np.array(
        [[np.cos(yaw), -np.sin(yaw), 0.0],
            [np.sin(yaw), np.cos(yaw), 0.0],
            [0.0,0.0,1.0]] )
        pitch_rot_mat = np.array(
        [[np.cos(pitch), 0.0, np.sin(pitch)],
            [0.0,1.0,0.0],
            [-np.sin(pitch), 0.0, np.cos(pitch)]] )
        roll_rot_mat = np.array(
        [[1.0, 0.0, 0.0],
            [0.0, np.cos(roll), -np.sin(roll)],
            [0.0, np.sin(roll), np.cos(roll)]] )
        
        # x,y,z = np.dot(np.dot(np.dot(yaw_rot_mat, pitch_rot_mat), roll_rot_mat),[point[0],point[1],point[2]])
        x,y,z = np.dot(np.dot(np.dot(roll_rot_mat, pitch_rot_mat), yaw_rot_mat),[point[0],point[1],point[2]])
        return pos[0] + x, pos[1] + y, pos[2] + z
    

    def get_z_offset(self):
        x,y,yaw = np.nan_to_num(self.body_xyz[0]/self.grid_size), np.nan_to_num(self.body_xyz[1]/self.grid_size), np.nan_to_num(self.yaw)
        try:
            x_pix = int(x+(-self.min_x+1)/self.grid_size)
            y_pix = int(y+(-self.min_y+1)/self.grid_size)
            ordered_pix = np.sort(self.world_map[x_pix-10:x_pix+10, y_pix-10:y_pix+10], axis=None)
            self.z_offset = max(ordered_pix[-1], 0.5)
        except Exception as e:
            self.z_offset = 0.0

    def get_hm(self, im_size=[60,40,1]):
        x,y,yaw = self.body_xyz[0]/self.grid_size, self.body_xyz[1]/self.grid_size, self.yaw
        if self.world_map is not None:

            # t1 = time.time()
            hm_pts = self.transform_rot_and_add(1*yaw, [x+(-self.min_x+1)/self.grid_size, y+(-self.min_y+1)/self.grid_size], self.ij)
            hm_pts[:,0] = np.clip(hm_pts[:,0], 0, self.world_map.shape[0]-1)
            hm_pts[:,1] = np.clip(hm_pts[:,1], 0, self.world_map.shape[1]-1)
            self.hm[self.hm_ij[:,0],self.hm_ij[:,1]] = self.world_map[hm_pts[:,0],hm_pts[:,1]]
            # Clip to -1, 1 meters
            # print(self.z_offset)
            
            # Constant height
            # hm = np.clip(self.hm - self.z_offset, -1, 1).reshape(im_size)
            # hm = (hm+1)/2

            # White is lowest
            # hm = np.clip(self.body_xyz[2] - self.hm, 0, 2).reshape(im_size)
            # hm = (hm)/2

            # Black is lowest
            hm = np.clip(self.hm-self.body_xyz[2], -2, 0).reshape(im_size)
            hm = (hm+2)/2
    
        else:
            print("No world map")
            hm = np.zeros(im_size)
        return hm

    def normalise_q(self, v, tolerance=0.00001):
        mag2 = sum(n * n for n in v)
        if mag2 > tolerance:
            mag = np.sqrt(mag2)
            v = tuple(n / mag for n in v)
        return np.array(v)

    def q_mult(self, q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
        return w, x, y, z
        
    def rotate_vector_by_q(self, v, q, pos):
        q = self.normalise_q(q)
        q1 = (q[3], q[0], q[1], q[2])
        q2 = (0, v[0], v[1], v[2])
        # q1_conj = (self.qw, -self.qx, -self.qy, -self.qz)
        q1_conj = (q[3], -q[0], -q[1], -q[2])
        v_out = self.q_mult(self.q_mult(q1, q2), q1_conj)[1:] 
        return v_out[0] + pos[0], v_out[1] + pos[1], v_out[2] + pos[2]

    def get_rgbd(self, cam_pos='lower'):
        camTargetPos = [0.,0.,0.]
        # This is to stop a weird pitch inversion that happens at 0.422? 
        # if self.pitch < 0.422:
        cameraUp = [0,0,1]
        # else:
        #     cameraUp = [0,0,-1]
        cameraPos = [1,1,1]
        # yaw = 40
        # pitch = 10.0
        # roll=0

        upAxisIndex = 2
        camDistance = 4
        # new ===================
        pixelWidth = self.im_size[0]
        pixelHeight = self.im_size[1]
        pos = self.body_xyz
        roll, pitch, yaw = self.roll, self.pitch, self.yaw
        # pos, orn = p.getBasePositionAndOrientation(self.Id)
        # roll, pitch, yaw = p.getEulerFromQuaternion(orn)
        if cam_pos == 'lower':
            dx = 0.6
            dy = 0
            dz = -1
            # cam_dx = 0.2
            cam_dx = 0.1
            cam_dy = 0
            cam_dz = 0.2
            fov = 60
            nearPlane = 0.25
            farPlane = 2
        
        elif cam_pos == 'lower2':
            # dx = 1.0
            # dy = 0
            # dz = -1
            # cam_dx = 0.1
            # cam_dy = 0
            # cam_dz = 0.2
            # dx = 0.75
            dx = 0.4
            dy = 0
            dz = -1
            cam_dx = 0.2
            cam_dy = 0
            cam_dz = 0.2
            fov = 60
            nearPlane = 0.5
            farPlane = 3

        elif cam_pos == 'upper':
            dx = 3.0
            dy = 0
            dz = -1
            cam_dx = 0.0
            cam_dy = 0
            cam_dz = 0.4
            fov = 80
            nearPlane = 0.5
            farPlane = 2

        elif cam_pos == 'back':
            dx = -0.15
            dy = 0
            dz = -1
            # cam_dx = 0.2
            cam_dx = 0.0
            cam_dy = 0
            cam_dz = -0.0
            fov = 60
            pixelWidth = self.im_size[0]
            pixelHeight = self.im_size[1]
            nearPlane = 0.5
            farPlane = 2

        lightDirection = [pos[0]+cam_dx,pos[1],pos[2]]
        shadow = 1
        
        lightColor = [1,1,1]#optional argument
        
        # Before you go trying to get the image to move with pitch and roll, there is an issue with the pitch inverting with a small pitch (~0.42) and issue with roll. I have tried to get these to work with euler and quaternions, i don't think it is just gimbel lock. Just leave as yaw

        # p_x, p_y, p_z = self.transform_rot(yaw, pos, [dx,dy,dz])
        # cam_x, cam_y, cam_z = self.transform_rot(yaw, pos, [cam_dx, cam_dy, cam_dz])
        # p_x, p_y, p_z = self.rotate_vector_by_q([pos[0] + dx, pos[1] + dy, pos[2] + dz])
        # cam_x, cam_y, cam_z = self.rotate_vector_by_q([pos[0] + cam_dx, pos[1] + cam_dy, pos[2] + cam_dz])
        # cam_x, cam_y, cam_z = self.rotate_vector_by_q([cam_dx,cam_dy, cam_dz], [self.qx, self.qy, self.qz, self.qw], pos)
        # p_x, p_y, p_z = self.rotate_vector_by_q([dx,dy, dz], [self.qx, self.qy, self.qz, self.qw], pos)
        # print("q rotation")
        p_x, p_y, p_z = self.transform_rot3d([roll, pitch, yaw], pos, [dx,dy,dz])
        cam_x, cam_y, cam_z = self.transform_rot3d([roll, pitch, yaw], pos, [cam_dx,cam_dy,cam_dz])

        aspect = 1
        
        projectionMatrix = p.computeProjectionMatrixFOV(fov, aspect, nearPlane, farPlane)
        viewMatrix = p.computeViewMatrix([cam_x,cam_y,cam_z], [p_x, p_y, p_z], cameraUp)
        try:
            image = p.getCameraImage(pixelWidth, pixelHeight, viewMatrix, projectionMatrix=projectionMatrix, lightDirection=lightDirection,lightColor=lightColor, shadow=shadow, renderer = p.ER_TINY_RENDERER)
            
            depth = copy.deepcopy(image[3]).reshape([pixelHeight, pixelWidth, 1])
            if self.args.vis_type == 'depth':
                return depth

            rgb = np.array(copy.deepcopy(image[2])).reshape([pixelHeight, pixelWidth, 4])[:,:,:3]/255.0
            return np.nan_to_num(np.concatenate((rgb,depth), axis=2))

        except Exception as e:
            print("get_rgb exception", e)
            return np.zeros([pixelWidth, pixelHeight, 4])

    def get_im(self):
        self.get_z_offset()
        if self.args.vis_type == 'hm':
            self.im = self.get_hm()
        elif self.args.vis_type == 'state':
            self.im = np.array(self.boxes).reshape(self.im_size)
        elif self.args.vis_type in ['rgbd','depth']:
            if self.steps % self.args.camera_rate == 0:
                if self.args.run_state == "train_setup":
                    self.im = self.get_rgbd("lower")
                else:
                    self.im = self.get_rgbd("lower2")
                self.orig_im = self.im
                self.recon_im = self.im
                # up = self.get_rgbd("upper")
                # if self.args.run_state == "train_q":
                #     self.im1 = self.get_rgbd("lower2")
                    # self.im2 = self.get_rgbd("back")
                if self.args.render:
                    display_images(self.im)
        if self.args.display_im:
            self.display()        
        return self.im

    def display(self):
        cv2.imshow("image", self.im)
        cv2.waitKey(1)
  
    def get_world_map(self, box_info=None):
        gz = False
        if gz:
            self.min_x = np.min(np.array(box_info[1])[:,0] - np.array(box_info[2])[:,0]/2)
            self.min_y = np.min(np.array(box_info[1])[:,1] - np.array(box_info[2])[:,1]/2)
            self.max_x = np.max(np.array(box_info[1])[:,0] + np.array(box_info[2])[:,0]/2)
            self.max_y = np.max(np.array(box_info[1])[:,1] + np.array(box_info[2])[:,1]/2)
        else:
            self.min_x = np.min(np.array(box_info[1])[:,0] - np.array(box_info[2])[:,0])
            self.min_y = np.min(np.array(box_info[1])[:,1] - np.array(box_info[2])[:,1])
            self.max_x = np.max(np.array(box_info[1])[:,0] + np.array(box_info[2])[:,0])
            self.max_y = np.max(np.array(box_info[1])[:,1] + np.array(box_info[2])[:,1])
        world_shape = [int((self.max_x - self.min_x + 2)/self.grid_size), int((self.max_y - self.min_y + 2)/self.grid_size)]

        hm = np.ones([world_shape[0], world_shape[1]]).astype(np.float32)*-1
        if box_info is not None:
            positions = box_info[1]
            sizes = box_info[2]
            for pos, size in zip(positions, sizes):
                x, y, z = pos[0]/self.grid_size, pos[1]/self.grid_size, pos[2]
                if gz:
                    x_size, y_size, z_size = (size[0]/2)/self.grid_size, (size[1]/2)/self.grid_size, size[2]/2
                else:
                    x_size, y_size, z_size = (size[0])/self.grid_size, (size[1])/self.grid_size, size[2]
                
                ij = np.array([[i,j,1] for i in range(int(0-x_size), int(0+x_size)) for j in range(int(0-y_size), int(0+y_size))])

                hm_pts = self.transform_rot_and_add(1*pos[5], [x+(-self.min_x+1)/self.grid_size, y+(-self.min_y+1)/self.grid_size], ij)
                for pt in hm_pts:
                    try:
                        # Not sure why this doesn't work for larger z heights? Should be box z pos + box z size (half extent). It's because I wasn't copying a list properly..
                        if hm[pt[0], pt[1]] < (z * 2):
                            hm[pt[0], pt[1]] = (z * 2)
                    except Exception as e:
                        print(e)
                        print(pt)
        self.dx_forward, self.dx_back, self.dy = 36, 24, 20        
        self.ij = np.array([[i,j,1] for i in range(-self.dx_back, self.dx_forward) for j in range(-self.dy, self.dy)])
        self.hm_ij = np.array([[i,j] for i in range(0, self.dx_back + self.dx_forward) for j in range(0, self.dy + self.dy)])
        self.hm = np.ones([self.dx_back+self.dx_forward, 2*self.dy], dtype=np.float32)*-1
        return hm

    def transform_rot_and_add(self, yaw, pos, points):
        rot_mat = np.array(
                [[np.cos(yaw), -np.sin(yaw), pos[0]],
                [np.sin(yaw), np.cos(yaw), pos[1]],
                [0, 0, 1]])
        return np.dot(rot_mat,points.T).T.astype(np.int32)

    def add_disturbance(self, max_dist=None, forward_only=False):
        if forward_only:
            force_x = random.random()*max_dist/2
        else:
            force_x = (random.random() - 0.5)*max_dist
        force_y = (random.random() - 0.5)*max_dist
        force_z = (random.random() - 0.5)*(max_dist/4)
        # print("applying forces", force_x, force_y, force_z)
        p.applyExternalForce(self.Id,-1,[force_x,force_y,force_z],[0,0,0],p.LINK_FRAME)
        force_roll = (random.random() - 0.5)*max_dist/2
        force_pitch = (random.random() - 0.5)*max_dist/2
        force_yaw = (random.random() - 0.5)*(max_dist/2)
        p.applyExternalTorque(self.Id,-1,[force_roll,force_pitch,force_yaw],p.LINK_FRAME)

    def log_stuff(self, logger, writer, iters_so_far, log=True):
        self.all_difficulties = MPI.COMM_WORLD.allgather(self.args.difficulty)
        dist_difficulty = MPI.COMM_WORLD.allgather(self.args.dist_difficulty)
        self.min_difficulty = np.min(self.all_difficulties)
        disturbances = MPI.COMM_WORLD.allgather(self.max_disturbance)
        success = MPI.COMM_WORLD.allgather(np.mean(self.success))
        Kp = MPI.COMM_WORLD.allgather(self.local_Kp) 

        # ==================================================================================================================
        # This is where self.args.cur is set to False when self.local_Kp is below 5, this function synced with all processes, so we can choose to use the local_Kp or take the max of all processes
        # ==================================================================================================================
        if self.args.cur:
            if not self.args.yu:
                if not self.args.cur_local:
                    self.Kp = np.max(Kp)
                else:
                    self.Kp = self.local_Kp
            if self.local_Kp < 5:
                self.prev_local_Kp = self.local_Kp = self.Kp = 0
                self.args.cur = False
        # ==================================================================================================================
        
        self.iters_so_far = iters_so_far

        if self.rank == 0 and log:

            writer.add_scalar("Success", np.mean(success), self.iters_so_far)
            logger.record_tabular("Success", np.mean(success))

            print("success", np.array(success))

            if self.args.run_state in ["train_single"]:
                print("disturbances", disturbances, self.max_disturbance)
                print("difficulty", self.all_difficulties, self.args.difficulty)

                print("gains", Kp, self.Kp, self.prev_local_Kp, self.local_Kp)
                print("dist_difficulty", dist_difficulty, self.args.dist_difficulty)

                writer.add_scalar("breakdown/goal", np.mean(self.reward_breakdown['goal']), self.iters_so_far)        
                writer.add_scalar("breakdown/pos", np.mean(self.reward_breakdown['pos']), self.iters_so_far)        
                writer.add_scalar("breakdown/vel", np.mean(self.reward_breakdown['vel']), self.iters_so_far)   
                writer.add_scalar("breakdown/tip", np.mean(self.reward_breakdown['tip']), self.iters_so_far)   
                writer.add_scalar("breakdown/com", np.mean(self.reward_breakdown['com']), self.iters_so_far)   
                writer.add_scalar("breakdown/neg", np.mean(self.reward_breakdown['neg']), self.iters_so_far)   
                writer.add_scalar("breakdown/sym", np.mean(self.reward_breakdown['sym']), self.iters_so_far)   
                writer.add_scalar("breakdown/act", np.mean(self.reward_breakdown['act']), self.iters_so_far)   
                writer.add_scalar("difficulty", self.min_difficulty, self.iters_so_far)   
                writer.add_scalar("dist_difficulty", self.args.dist_difficulty, self.iters_so_far)   
                writer.add_scalar("height", self.height_coeff, self.iters_so_far)   

                writer.add_scalar("Best reward", self.best_reward, self.iters_so_far)
                logger.record_tabular("Best reward", self.best_reward)

                writer.add_scalar("Kp", np.mean(Kp), self.iters_so_far)
                logger.record_tabular("Kp", np.mean(Kp))
                logger.record_tabular("max yaw", self.max_yaw)
                logger.record_tabular("pos error", np.mean(self.pos_error))
                # if self.args.obstacle_type == 'path':
                logger.record_tabular("difficulty", self.min_difficulty)
                logger.record_tabular("dist_difficulty", self.args.dist_difficulty)
                # elif self.args.obstacle_type == 'stairs':
                logger.record_tabular("height_coeff", self.height_coeff)

                writer.add_scalar("cur_num", self.args.cur_num, self.iters_so_far)   
                logger.record_tabular("cur_num", self.args.cur_num)

                writer.add_scalar("touchdown/left", np.mean(self.touchdown_pens[0]), self.iters_so_far)   
                writer.add_scalar("touchdown/right", np.mean(self.touchdown_pens[1]), self.iters_so_far)   

                writer.add_scalar("touchdown_dists/left", np.mean(self.touchdown_dists['left']), self.iters_so_far)   
                writer.add_scalar("touchdown_dists/right", np.mean(self.touchdown_dists['right']), self.iters_so_far)   

                logger.record_tabular("touchdown_left", np.mean(self.touchdown_pens[0]))
                logger.record_tabular("touchdown_right", np.mean(self.touchdown_pens[1]))

                logger.record_tabular("touchdown_dists_left", np.mean(self.touchdown_dists['left']))
                logger.record_tabular("touchdown_dists_right", np.mean(self.touchdown_dists['right']))

                writer.add_scalar("max_disturbance", self.max_disturbance, self.iters_so_far)   
                logger.record_tabular("max_disturbance", self.max_disturbance)