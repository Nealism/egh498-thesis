from cmath import e
from copy import deepcopy
import numpy as np
import pandas as pd

import pybullet as p
import time
from gym import spaces
from collections import deque

from mpi4py import MPI
comm = MPI.COMM_WORLD
import math
from heapq import nsmallest
import random
import copy

from assets.env_base_pb import EnvBasePB
from statistics import mean



#Currently, we are commenting our work on inlation radius. We will consider our inflation radius work before testing phase.
#Inflation radious code are specified some in reset, some in reward function and mostly in observation.

class Env(EnvBasePB):
    
    def __init__(self, PATH=None, args=None, writer=None,posi=None):

        #Initiations like CPU parallelisation rank, arguments, render, path, writer for tensorboard plot, 
        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        # self.master = True
        Initial_distance_to_goal=0
        self.number_Goal_Reached=0
        self.trial=0
        
        self.prev_dist_to_goal= Initial_distance_to_goal

        
        
    
        super().__init__(PATH)
        # Setting arguments to change functions (reward,reset,step) based on arguments
        self.reward_fn_name = f'get_reward_{self.args.reward_fn}'
        self.reset_fn_name = f'reset_{self.args.reset_fn}'
        self.step_fn_name = f'step_{self.args.step_fn}'

        
        #Action Size and Obs Size (Also setting input types using arguments)
        if "pumpkin" in self.args.env:
            self.ac_size = 2
            self.ob_size = 7
        else:
            self.ac_size = 2
            if self.args.static_robots > 1:
                self.ob_size = 18
            elif self.args.obstacle_avoidance:
            
                self.ob_size = 16+2*(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_0 and  self.args.occupancy_map and self.args.use_perception:
                
                #print("owch")
                self.ob_size = 4#+2 *(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_1 and  self.args.occupancy_map and self.args.use_perception:
                
                #print("owch")
                self.ob_size = 6#+2 *(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_2 and self.args.occupancy_map and self.args.use_perception:
                
                #print("owch")
                self.ob_size = 6+2 *(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_3 and self.args.occupancy_map and self.args.use_perception:
                
                #print("owch")
                self.ob_size = 7+5 *(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_3:

                self.ob_size = 27+5*(self.args.num_robots-1)
                
            elif self.args.gap_avoidance:
                
                self.ob_size = 26+2*(self.args.num_robots-1)
            
            else:
                #print("nowch")
                self.ob_size = 6+2*(self.args.num_robots-1)

        #Initialising KP for bootstrap curr, time to goal, 
        # opposite angle to set goal position opposide side of wall if needed (not needed).
        #Start Timer
        # self.Kp = 400
        self.Kp = self.args.initial_kp
        self.w = self.args.clone_value
        self.initial_Kp = self.Kp
        self.time_to_goal=0
        self.time_to_gapwp1=0
        self.time_to_gapwp2=0
        
        self.opposite_angle=0

        self.start_time = time.time() 

        self.gap_list=[]


        
        #initialising single robot collision likelihood curr (Not Needed)
        if self.args.obstacle_avoidance and self.args.static_robots > 1 and self.args.single_collision_curr or self.args.cur:
            self.a=5.0
            self.b=0.5
        else:

            self.a=0.0
            self.b=0.0

        #initialising collision likelihood curr (Not Needed) but else command is needed
        if self.args.gap_avoidance and self.args.num_robots>1 and self.args.collision_likelihood_curr:
            # self.increase_collision_rate=-2
            self.increase_collision_rate=0
        else:
            self.increase_collision_rate=0
            
            
        #Initialising Gap cur and Tunnel Cur Parameters for Single Robot
        if self.args.num_robots==1: 
                   
            if self.args.gap_avoidance  and self.args.gap_curr or self.args.cur:
                #parameters for gap curr
                self.max_gap_width=self.args.starting_gap_width
                self.decrease_gap_width=0
                self.final_gap_width=self.args.final_gap_width
                #parameters for tunnel curr
                self.max_tunnel_depth = 0.1
                self.increase_tunnel_depth = 0.1
                self.max_gap_among_all_robots_individual_gap_width=self.max_gap_width
                
                
                
            elif self.args.gap_avoidance and not self.args.gap_curr:
                self.max_gap_width=1
                self.decrease_gap_width=0
                self.max_tunnel_depth = 0.2
                self.increase_tunnel_depth = 0.1
                self.max_gap_among_all_robots_individual_gap_width=self.max_gap_width
        
        #Initialising Gap cur and Tunnel Cur Parameters for Multi Robot
        elif self.args.num_robots>1:
            
            if self.args.gap_avoidance  and self.args.gap_curr or self.args.cur:
                #parameters for gap curr
                self.max_gap_width=self.args.starting_gap_width
                # self.max_gap_width=np.random.uniform(2,0,1)
                self.decrease_gap_width=0
                self.final_gap_width=self.args.final_gap_width
                #parameters for tunnel curr
                self.max_tunnel_depth = 0.2
                self.increase_tunnel_depth = 0.1
                self.max_gap_among_all_robots_individual_gap_width=self.max_gap_width
                
                
            elif self.args.gap_avoidance and not self.args.gap_curr:
                self.max_gap_width=3
                self.decrease_gap_width=0
                self.max_tunnel_depth = 0.1
                self.increase_tunnel_depth = 0.1
                self.max_gap_among_all_robots_individual_gap_width=self.max_gap_width
            




   
        
        #Initialising Region Cur Parameters
        if self.args.cur or self.args.region_curr:
            self.initial_goal_dist=6	
            self.max_goal_dist=12
        else:
            self.initial_goal_dist=8
   
            self.max_goal_dist=8
        

        self.action_multiplier = 1
  
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        self.steps = -1
   
        
        self.reward_names = ["Reward/goal", "Reward/heading", "Reward/heading_obs", "Reward/neg", "Reward/MA_colision", "Reward/collision","Reward/reach"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names}

        # if self.args.gap_random:
        #     self.gap_names = ["Gap_per_Reset"]
        #     self.gap_dict = {gap:deque(maxlen=100) for gap in self.gap_names} 
        #     self.ep_gap_dict = {gap:0 for gap in self.gap_names}

        # if self.args.expert_curr or self.args.cur:
        #     self.action_names = ["Action/Linear", "Action/Angular", "Prior_Action/Linear", "Prior_Action/Angular", "Policy_Action/Linear", "Policy_Action/Angular"]
        # else:
        #     self.action_names = ["Action/Linear", "Action/Angular", "Policy_Action/Linear", "Policy_Action/Angular"]
        # self.action_dict = {action:deque(maxlen=100) for action in self.action_names} 
        # self.ep_action_dict = {action:0 for action in self.action_names}

        
    
        self.env_exp = None

        
        self.initial_joints = [0.0] * 15 + [ 0.5, -0.5, -1.5707] + [-0.5, 0.5, -1.5707]
        self.cur_success = deque([0.0], maxlen=5)
        self.success = deque([0.0], maxlen=1)
        self.ep_goal_success = 0.0
        self.ep_success = False

        if self.args.add_terrain:
            self.terrain_difficulty = self.args.initial_terrain_difficulty
        else:
            self.terrain_difficulty = 0
            self.terrain = None

        self.max_disturbance = 250
        self.final_disturbance = 1600
        self.episodes = -1
        self.total_steps = 0
        self.ob_dict = {}
        
        self.states_to_restore = ["pos", "orn", "joints", "base_vel", "joint_vel", "args", "episodes", "steps", "total_steps"]

        
        self.load_robot()

        

    def load_specific_robot(self):

        if "pumpkin" in self.args.env:
            self.load_urdf_robot("./assets/urdfs/pumpkin.urdf")
            self.contact_list = ['pumpkin_chassis', 'pumpkin_lower_chassis']
        
        else:
            if self.args.turtle_titan:
                robot1=self.load_urdf_robot("./assets/urdfs/turtlebot_boxy_original.urdf")
            else:
                #state_object= [random.uniform(-4,4),random.uniform(4,1),0.00]
                robot1=self.load_urdf_robot("./assets/urdfs/dynamic_titan.urdf")
                # robot1=self.load_urdf_robot("./assets/urdfs/turtlebot_boxy.urdf")
                # robot1=self.load_urdf_robot("/home/kom018/pybullet_robots/data/turtlebot.urdf")
                # robot1=self.load_urdf_robot("/home/kom018/pybullet_robots/data/turtlebot_boxy.urdf")
                # robot1=self.load_urdf_robot("/home/kom018/pybullet_robots/data/r2d2.urdf")
                # robot1=self.load_urdf_robot("/home/kom018/behaviour_rl/assets/turtlebot_titan2.urdf")
            
            self.contact_list = ['titan_chassis', 'left_11_wheel', 'right_11_wheel','left_1_wheel', 'right_1_wheel']
            if self.args.static_robots > 1 and self.args.insert_robot2:
                robot2=self.load_urdf_robot2("./assets/urdfs/dynamic_titan.urdf")
            if self.args.insert_box:
                wall_dir= "Wall_URDF/"
                self.square = p.loadURDF(wall_dir + "square.urdf", [0,2,0.5], useFixedBase=True)

            
            #robot2=self.load_urdf_robot("./assets/urdfs/dynamic_titan.urdf")
            self.contact_list2 = ['titan_chassis', 'left_11_wheel', 'right_11_wheel','left_1_wheel', 'right_1_wheel']
            wall_dir= "Wall_URDF/"
            #self.square = p.loadURDF(wall_dir + "square.urdf", [0,2,0.5], useFixedBase=True)

            # wallA = p.loadURDF(wall_dir + "Wall.urdf", [11.25,0,0], useFixedBase=True)
            # wallB = p.loadURDF(wall_dir + "Wall.urdf", [-11.25,0,0], useFixedBase=True)
            # wall2A = p.loadURDF(wall_dir + "Wall2.urdf", [0,11.25,0], useFixedBase=True)
            # wall2A = p.loadURDF(wall_dir + "Wall2.urdf", [0,-11.25,0], useFixedBase=True)
            #wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [-2,0,0], useFixedBase=True)
            #wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [-2,1,0], useFixedBase=True)
            #wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [2,0,0], useFixedBase=True)
            #wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [2,1,0], useFixedBase=True)
            # wall2A = p.loadURDF("/home/komol/00_STUDY_DRIVE/Codes/mobile_robot/Wall_URDF/Wall2_small.urdf", [2,-1,0], useFixedBase=True)
            #wall2A = p.loadURDF("/home/komol/00_STUDY_DRIVE/Codes/mobile_robot/Wall_URDF/Wall2_small.urdf", [-2,1,0], useFixedBase=True)
            #state_object= [random.uniform(-4,4),random.uniform(-4,1),0.00]
            #state_object=[-2,-3,0.00]
            state_object=[np.random.uniform(-2, 2),np.random.uniform(-3, -3.5),0.00]
            wall_dir= "Wall_URDF/"
            self.Goal = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=state_object)
            
            
            
            
            #p.setCollisionFilterPair(self.Id, self.Id2, -1, -1, 0)
            
            #print(aabbMin)

        self.left_track = []
        self.right_track = []
        self.contact_dict = {}
        self.wheel_dict = {}
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            link_name = info[12].decode("ascii")
            if "wheel" in link_name: self.wheel_dict[link_name] = j
            if link_name in self.contact_list: self.contact_dict[link_name] = j
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            if "left" in jname:
                self.left_track.append(j)
            elif "right" in jname:
                self.right_track.append(j)
        self.motors = []
        # Works much better if using husky wheel interias in the URDF
        # for key in self.wheel_dict:
        # 	p.changeDynamics(self.Id, self.wheel_dict[key], lateralFriction=0.9, spinningFriction=0.01, rollingFriction=0.01)


    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        # print("What the ", self.ep_goal_success); exit()
        
        if self.args.obstacle_avoidance and self.args.gap_avoidance:
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "RC_Initial Distance to Goal": self.initial_goal_dist, "GC: Gap Width":self.max_gap_among_all_robots_individual_gap_width, "TC: Tunnel Width":self.increase_tunnel_depth,"CLC: distance between obstacle and path": self.a-self.b, "EC: Kp": self.Kp }
        elif self.args.gap_avoidance:
            # print("self.max_gap_among_all_robots_individual_gap_width",self.max_gap_among_all_robots_individual_gap_width);exit()
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "EC: Kp": self.Kp, "GC: Gap Width":self.max_gap_among_all_robots_individual_gap_width, "TC: Tunnel Width":self.increase_tunnel_depth,"Time_to_Goal":self.time_to_goal,"Time_to_gapwp1":self.time_to_gapwp1,"Time_gapwp1_gapwp2":self.time_to_gapwp2-self.time_to_gapwp1,"Time_gapwp2_goal":self.time_to_goal-self.time_to_gapwp2, "Collision_likelihood": self.increase_collision_rate}
        else:
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "RC_Initial Distance to Goal": self.initial_goal_dist, "EC: Kp": self.Kp }

        return_dict.update(self.reward_dict)
        # print("self.reward_dict",self.reward_dict)
        # if self.args.gap_random:
        #     return_dict.update(self.gap_dict)
        #     print("self.gap_dict",self.gap_dict)
        # return_dict.update(self.action_dict)
        return return_dict

    

    def get_success(self):
        # dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        
        if self.args.cur_succ==0:
            #print("self.distance_to_goal",dist_to_goal,self.distance_to_goal)
            return self.distance_to_goal == True
        

    def check_for_success(self):
        return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()
    
    def check_both_for_success(self):
        return len(self.All_Robot_ID[0].cur_success) == 3 and len(self.All_Robot_ID[1].cur_success) == 3 and (np.array(self.All_Robot_ID[0].cur_success) == True).all() and (np.array(self.All_Robot_ID[1].cur_success) == True).all()

    def reset(self, terrain=None, test=False, restore_state=None):
        #print("self.max_gap_among_all_robots_individual_gap_width",self.max_gap_among_all_robots_individual_gap_width)
        #self.load_simulator()
        #p.resetDebugVisualizerCamera(cameraDistance=10, cameraYaw=0, cameraPitch=-40, cameraTargetPosition=[0.55,-0.35,0.2])
        self.intersection_r1_box= False
        self.intersection_r1_r= False
        self.robot1_near_robot2=False
        self.goal_moved=False
        Initial_distance_to_goal=0
        
        self.prev_dist_to_goal= Initial_distance_to_goal

        if self.steps > 0:
            for key in self.reward_dict:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 


        # if self.args.gap_random:
        #     if self.steps > 0:
        #         for key in self.gap_dict:
        #             self.gap_dict[key].append(self.ep_gap_dict[key])
        #     self.ep_gap_dict = {gap:0 for gap in self.gap_names} 

        # if self.steps > 0:
        #     for key in self.action_dict:
        #         self.action_dict[key].append(self.ep_action_dict[key])
        # self.ep_action_dict = {action:0 for action in self.action_names} 

        if self.episodes > -1:

            self.success.append(self.get_success())
            #print("SUCCESS________________________________________",self.success)
            # print("distanc-to_wp", self.dist_to_wp)

            self.ep_success = self.get_success()
            #print("Episdoe_Succ", self.ep_success)			
            self.cur_success.append(self.ep_success)
            self.ep_goal_success = np.mean(self.goal_success) if self.goal_success else 0.0

        self.goal_success = []
        # print("GOAL", self.ep_goal_success)
        # print("cur",self.cur_success,self)
        #print(self.body_xyz)
        

        #pos, orn = p.getBasePositionAndOrientation(self.Id)
        
        
        #Uncomment this part for static inflation radius. Not for dynamic inflation radius.
        #For dynamic inflation radious, this part is added in observation section. 

        # m=0.075 #value of inflation radius
        # x=(1.4/2)+m
        # y=(0.78/2)+m
        # z=0.235
        # # get the self.corners of the bounding box
        # self.corners1 = [(x, y, z),
        #   		(x,-y,z),
        #   		(-x,-y,z),
        #   		(-x,y,z),
        #   		(x,y,z)]
        
        # self.corners2 = [(x, y, z),
        #   		(x,-y,z),
        #   		(-x,-y,z),
        #   		(-x,y,z),
        #   		(x,y,z)]
        
        
        # self.lineId1 = [-1]*4  # initialize with an invalid ID for lines around robots
        # self.lineId2 = [-1]*4 
        
        p.removeAllUserDebugItems()		





        p.removeBody(self.Goal)
        
        # p.removeBody(self.Goal2)
        # p.removeBody(self.Goal3)
        
        #state_object= [random.uniform(-4,4),random.uniform(-4,0),0.00]
        #state_object=[-2,-3,0.00]


        # Goal
        # state_object=[np.random.uniform(-3, 3), np.random.uniform(-3, -3.5), 0.00]
        state_object=[np.random.uniform(-4, 4), np.random.uniform(-4, 4), 0.00]
        wall_dir= "Wall_URDF/"
        self.Goal = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=state_object)
        p.setCollisionFilterGroupMask(self.Goal, -1, collisionFilterGroup=0, collisionFilterMask=0)
        
        
        
        if self.rank == 0 and self.args.record_sim and self.episodes > 0:
            self.record_sim_state(best=self.check_for_success(), test=test)
        
        # if terrain is not None:
        #     self.load_terrain(terrain)
        # elif self.args.add_terrain:
        #     template = (np.random.random([int(self.terrain_size[2]/4),int(self.terrain_size[2]/4)]) + 1.0) * self.terrain_difficulty 
        #     # Make the edges smooth
            
        #     df = pd.DataFrame(template)
        #     df.to_csv("template.csv")
        #     #dj=pd.read_csv("template.csv")
        #     #template=dj.to_numpy()
        #     template[:, 0] = 0.0
        #     #print(type(template))
        #     template[:, -1] = 0.0
        #     template[0, :] = 1.0
        #     template[-1, :] = 0.0
        #     #print(self.terrain_size[1])
        #     terrain = cv2.resize(template, dsize=(self.terrain_size[1], self.terrain_size[2])).reshape(self.terrain_size)
        #     #print(template)
        #     #print(template[:, 0])
        #     self.load_terrain(terrain)


        self.steps = 0
        self.st=time.time()
        #Robot1
        # initial_x, initial_y = np.random.uniform(-3, 3), np.random.uniform(3, 3.5) 
        initial_x, initial_y = np.random.uniform(0,4), np.random.uniform(0, 4) 
        #initial_x, initial_y = -2, -2 
        # self.initial_yaw = np.random.uniform(-np.pi, np.pi) 
        self.initial_yaw = 0.0#np.random.uniform(-np.pi, np.pi) 
        # self.initial_yaw = np.random.uniform(-0.5, 0.5) #np.random.uniform(-np.pi, np.pi) 
        # self.initial_yaw = 0.5 #np.random.uniform(-np.pi, np.pi) 
        # self.initial_yaw = np.random.uniform(-np.pi, np.pi) 
        # print("self.initial_yaw",self.initial_yaw)
        self.initial_orn = p.getQuaternionFromEuler([0,0,self.initial_yaw])
        # print("self.initial_orn",self.initial_orn)
        self.z_offset = 0



        # if not self.args.region_curr:  #to set random distances to goal
        #     self.initial_goal_dist=self.random_robot_init
        #     self.max_goal_dist=self.initial_goal_dist

    
        ######___________ALL CURRICULUM STAGES ARE HERE__________________##################################################
        
        #########____EXPERT/GUIDED_CURRICULUM__########   
        
        

        if (self.args.cur or self.args.expert_curr) and self.Kp > 0 and self.check_for_success():

            if self.args.cloning:
                self.Kp = 0.75*self.Kp
                self.cur_success = deque([0.0], maxlen=5) 
            else:
                self.Kp = 0.75*self.Kp
                if self.Kp < 5:
                    self.Kp = 0
                self.cur_success = deque([0.0], maxlen=5) 
            
                # print(self.Kp)

        
               

        if self.args.gap_avoidance and self.increase_collision_rate <3 and (self.args.cur or self.args.collision_likelihood_curr) and self.args.num_robots>1 and self.check_for_success():    
            self.increase_collision_rate += 1
            self.cur_success = deque([0.0], maxlen=5)
        
        elif self.args.gap_avoidance and self.increase_collision_rate >= 3 and self.args.collision_likelihood_curr:
            self.increase_collision_rate=3

        elif self.args.gap_avoidance and not self.args.collision_likelihood_curr:
            self.increase_collision_rate=-1
        
        
        for robot, angles in self.robottogoal_angles:
            if robot == self:
                # Assuming there's only one value in the angles list for simplicity
                self.robottogoal_angle = angles#[0]
                
                break
            # else:
            #     # If the robot_name is not found, handle it accordingly
            #     print(f"Robot {self} not found in robottogoal_angles.")
        
        # print("4th self.increase_rate",self.increase_collision_rate)
        
        self.robottogoal_angle *=  -self.increase_collision_rate
        # print("after self.robottogoal_angle",self.robottogoal_angle)
        # print("outside self.robottogoal_angle",self.robottogoal_angle)

        
        #REGION_CUrriculum: Increasing Distance to Goal Gradually
        if (self.args.cur or self.args.region_curr) and self.check_for_success() and self.initial_goal_dist <= self.max_goal_dist:
            #self.initial_goal_dist=self.initial_goal_dist+self.increase_goal_dist
            #print(self.initial_goal_dist,self.max_goal_dist)
            # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
            self.initial_goal_dist +=1 # = 0
            self.cur_success = deque([0.0], maxlen=5)
                #print("cur_success", self.cur_success)			
        
        
        #GAP_CUrriculum: Reducing Gap Width Gradually
        if self.args.gap_avoidance and (self.args.cur or self.args.gap_curr):
            #if self.max_gap_width-self.decrease_gap_width - self.final_gap_width == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                #self.decrease_gap_width = self.max_gap_width
            
            # if self.args.num_robots>1 and self.check_both_for_success():
            if self.args.num_robots>1 and self.check_for_success():
                # print("BUJH",self.max_gap_width,self.decrease_gap_width,self.final_gap_width)
                if self.max_gap_width-self.decrease_gap_width > self.final_gap_width :         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                    #self.decrease_gap_width = self.max_gap_width-self.final_gap_width
                    #self.decrease_gap_width = 0
                    # self.All_Robot_ID[0].decrease_gap_width=0
                    # self.All_Robot_ID[1].decrease_gap_width=0
                    #self.cur_success = deque([0.0], maxlen=5)
                    #print("cur_success", self.cur_success)			
                # else:
                    # self.All_Robot_ID[0].decrease_gap_width += self.All_Robot_ID[0].args.gap_decrease			
                    # self.All_Robot_ID[1].decrease_gap_width += self.All_Robot_ID[1].args.gap_decrease
                    if self.args.rand_gap_cur:
                        self.decrease_gap_width += np.random.choice([0,self.args.gap_decrease])   
                    else:
                        self.decrease_gap_width += self.args.gap_decrease			
                    #print("TOTTOOTOTOTO")

                    self.cur_success = deque([0.0], maxlen=5)
                    # self.All_Robot_ID[0].cur_success = deque([0.0], maxlen=5)
                    # self.All_Robot_ID[1].cur_success = deque([0.0], maxlen=5)
                    

            elif self.args.num_robots==1 and self.check_for_success():
                # if self.max_gap_width-self.decrease_gap_width == self.final_gap_width:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                if self.max_gap_width-self.decrease_gap_width > self.final_gap_width:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                    self.decrease_gap_width += self.args.gap_decrease			
                    self.cur_success = deque([0.0], maxlen=5)
                    
                
                #     #self.decrease_gap_width = self.max_gap_width-self.final_gap_width
                #     self.decrease_gap_width = 0
                #     #self.cur_success = deque([0.0], maxlen=5)
                #     #print("cur_success", self.cur_success)			
                # else:
                #     self.decrease_gap_width += self.args.gap_decrease			
                    
                #     self.cur_success = deque([0.0], maxlen=5)
        
               
        #Tunnel_CUrriculum: Increasing the Tunnel/Gap length Gradually
        if self.args.gap_avoidance and (self.args.cur or self.args.tunnel_curr) and self.check_for_success():
            if self.max_tunnel_depth-self.increase_tunnel_depth == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                self.increase_tunnel_depth = self.max_tunnel_depth
                #self.cur_success = deque([0.0], maxlen=5)
                #print("cur_success", self.cur_success)			
            else:
                self.increase_tunnel_depth += 0.2			
                
                self.cur_success = deque([0.0], maxlen=5)

        
                
        
    
        
        #########____OBSTACLE_AVOIDANCE_CURRICULUM/Collision_likelihood_Curriculum__########
        # self.a is the fixed value of unit ( how far from the line) and self.b is the step size ( Here, step size is 0.5 unit)
        #print("static robot distance from trajectory",self.a-self.b,"and cur_success", self.cur_success)
        #print("cur_success", self.cur_success)	

        if (self.args.static_robots > 1 or self.args.obstacle_avoidance) and (self.args.cur or self.args.collision_likelihood_curr) and self.check_for_success():
            if self.a-self.b == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                self.b = self.a
                self.cur_success = deque([0.0], maxlen=5)
                #print("cur_success", self.cur_success)			
            else:
                self.b +=0.1			
                
                self.cur_success = deque([0.0], maxlen=5)

        #print(self.cur_success)

        
        
        
        
        

        #x = (np.random.uniform(1, 5) if np.random.randint(2) else np.random.uniform(-1, -5))
        #y = (np.random.uniform(1, 5) if np.random.randint(2) else np.random.uniform(-1, -5))
        #self.goal = (x, y)
        
        #print("Curriculum Success", self.cur_success, "Goal Success", self.ep_goal_success, "RC_Initial Distance to Goal", self.max_goal_dist - self.increase_goal_dist, "GC: Gap Width", self.max_gap_width-self.decrease_gap_width, "TC: Tunnel Width", self.increase_tunnel_depth,"CLC: distance between obstacle and path", self.a-self.b, "EC: Kp", self.Kp)
        # Visual element of the goal
        #Goal(self.goal)
        

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1])
            
        else:
            pos, orn, self.joints, self.base_vel, self.joint_vel = [initial_x, initial_y, self.z_offset+0.31],self.initial_orn, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
            #print("external",self.external_robots_pos)
            self.robot_own_pos=None
            for robot, own_pos in self.external_robots_pos:
                if robot == self:
                    # Assuming there's only one value in the angles list for simplicity
                    self.robot_own_pos = own_pos
                    break
                # else:
                #     # If the robot_name is not found, handle it accordingly
                #     print(f"Robot {self} not found in pos.")
            #print("Externally_set",self.robot_own_pos)
            
            pos=self.robot_own_pos
            # pos2, orn2, self.joints, self.base_vel, self.joint_vel = [initial_x2, initial_y2, self.z_offset+0.31],self.initial_orn2, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
            self.set_position(pos, orn, robot_id=self.Id)
            #self.h=0

        # self.robottogoal_angle=None
        self.external_goals_states=[]
        self.external_robots_states=[]
        
        for robot,goal in self.external_goals_states_with_IDx:
            self.external_goals_states.append(goal)
        
        for robot,r_position in self.external_robots_pos:
            self.external_robots_states.append(r_position)

        self.mid_point_of_goals=self.calculate_midpoint(self.external_goals_states[0],self.external_goals_states[-1])
        # self.mid_point_of_goals=(self.mid_point_of_goals[0],self.mid_point_of_goals[1],self.mid_point_of_goals[2])
        # print(self.mid_point_of_goals)
        # self.mid_point_of_goals= (self.mid_point_of_goals[0],self.mid_point_of_goals[1])

        self.mid_point_of_robots=self.calculate_midpoint(self.external_robots_states[0],self.external_robots_states[-1])
        # self.mid_point_of_robots_offsetting=(self.mid_point_of_robots[0],self.mid_point_of_robots[1]+np.random.uniform(-1.2,1.2))
        # self.mid_point_of_robots=(self.mid_point_of_robots[0],self.mid_point_of_robots[1]-1.2)
        # self.mid_point_of_robots=(self.mid_point_of_robots[0],self.mid_point_of_robots[1]+np.random.uniform(-3,3))

        # Function to move the goal and the static robot
        
        
    

        



        if self.args.gap_avoidance:
            

            #print("reset self.robottogoal_angle",self.robottogoal_angle)
            
            self.move_goal_and_static_robot(initial_x=pos[0], initial_y=pos[1], yaw=self.initial_yaw,robottogoal_angle=self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)
        else:
            self.move_goal_and_static_robot(initial_x=pos[0], initial_y=pos[1], yaw=self.initial_yaw,robottogoal_angle=self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)
        
        
        # print("robot_positions", pos2)
        # print("robot_state")
        # print(self.state_robot2)
        self.reset_time=self.timeStep_10Hz*self.steps
        # print("RESET_TIME",self.reset_time)
        self.lineId_wp1_wp2=-1
        self.lineId_heading = -1
        self.lineId_side1 = -1
        self.lineId_side2 = -1
        self.lineId_heading_MA = -1
        self.lineId_side1_MA = -1
        self.lineId_side2_MA = -1
        self.lineId = [-1]
        self.lineId_object= -1
        self.lineId_r2_big = [-1]*4 
        self.lineId1 = [-1]*4  # initialize with an invalid ID for lines around robots
        self.lineId1bonus = [-1]*4  # initialize with an invalid ID for lines around robots
        self.lineId12 = [-1]*4
        self.lineId12_static = [-1]*4
        self.lineId2 = [-1]*4 
        self.lineId_box1 = [-1]*4
        self.lineId_box1_safety = [-1]*4
        self.lineId_box1big = [-1]*4
        self.ray_line = [-1]*2
        #gap line ids
        
        self.hit = False
        self.h=0
        self.poshit_x=None
        self.poshit_y=None
        self.poshit_z=None
        self.ornhit_a=None
        self.ornhit_b=None 
        self.ornhit_c=None
        self.ornhit_d=None

        self.wp1_reach=0
        self.wp2_reach=0
        self.wp3_reach=0
        self.wp4_reach=0

        self.gapwp1_reach=False
        self.gapwp2_reach=False

        self.counter=0

        self.lineIdgap=[-1]*4
        self.lineIdA=[-1]*4
        self.lineIdB=[-1]*4
        self.lineIdWall=[-1]*4

        self.trial=self.trial+1
        # print("Trial",self.trial)

        self.goal_reaching=False

        # start_time=time.time()
        self.time_saving=[]
        self.velocity_saving1=[]
        self.velocity_saving2=[]
        self.action_saving1=[]
        self.action_saving2=[]
        self.scale_f_linear=[]
        self.scale_f_angular=[]
        

        self.wall_length=1.7

        self.k=0

        if self.args.gap_random:
            # self.max_gap_width=np.random.uniform(2,0.8,1)
            # self.max_gap_width=np.random.uniform(2,0.85,0.1)
            self.max_gap_width=np.random.uniform(self.args.starting_gap_width,self.args.final_gap_width,1)
            self.max_gap_width = (self.max_gap_width /0.05) * 0.05
            # self.max_gap_width = np.round(self.max_gap_width / 1) * 1
            # print('t_w',self.max_gap_width)
            # self.gap_list.append(self.max_gap_width)

            # with open('self.gap_list.txt', 'w') as file:
            #     for item in self.gap_list:
            #         file.write(f"{item}\n")
            

        # if self.args.gap_random:
        #     self.max_gap_width=np.random.uniform(2,1,1)
        #     self.max_gap_width = np.round(self.max_gap_width / 0.05) * 0.05

        #     self.gap_list.append(self.max_gap_width)

        #     with open('self.gap_list.txt', 'w') as file:
        #         for item in self.gap_list:
        #             file.write(f"{item}\n")
        # print("self.gap_list",self.gap_list)
        #     self.ep_gap_dict["Gap_per_Reset"] = self.max_gap_width
        # print("self.max_gap_width",self.max_gap_width)
        # print("self.ep_gap_dict",self.ep_gap_dict)
        # print("self.max_gap_among_all_robots_individual_gap_width",self.max_gap_among_all_robots_individual_gap_width)
        

        


        
        if self.args.gap_avoidance:
            #THIS PART IS NEEDED FOR SETTING ORIENTATION OF GAP WITH THE MID LINE
            # self.line1_start=(pos[0], pos[1])
            # self.line1_end=(self.state_goal[0], self.state_goal[1])
            # self.line1_angle=self.perpendicular_angle(self.line1_start,self.line1_end)
            # #print("angle",self.line1_angle)
            # self.line_orn=(0.0,0.0, self.line1_angle,0.1)
            
            #Set the Gap width taken from the gap curriculum in reset
            self.All_Robot_ID[0].gap_width=self.All_Robot_ID[0].max_gap_width-self.All_Robot_ID[0].decrease_gap_width

            if self.args.num_robots>1:
                self.All_Robot_ID[1].gap_width=self.All_Robot_ID[1].max_gap_width-self.All_Robot_ID[1].decrease_gap_width

            # max_gap_width_robots=max(self.All_Robot_ID[0].gap_width,self.All_Robot_ID[1].gap_width)
            # # if self==self.All_Robot_ID[0]:
            # print("self.gap_width",max_gap_width_robots,self.All_Robot_ID[0].gap_width,self.All_Robot_ID[1].gap_width,self.max_gap_width,self.All_Robot_ID[0].decrease_gap_width,self.All_Robot_ID[1].decrease_gap_width)
            #print("Gap_Width",self.gap_width,"Decrease_gap",self.decrease_gap_width)
            
            #Set the Tunnel/Gap Depth from the Tunnel Curriculum in reset
            self.tunnel_depth= self.increase_tunnel_depth

            #self.each_wall_length=10-(self.gap_width/2)
            #print("self.robots_bbox",self.robots_bbox)
            # print("All",self.All_Robot_ID,"self",self)
            # print(self.max_gap_among_all_robots_individual_gap_width)
            # side_wall_moving_rate=self.max_gap_among_all_robots_individual_gap_width-17
            # print("self.max_gap_among_all_robots_individual_gap_width,",self.max_gap_among_all_robots_individual_gap_width)
            # side_wall_moving_rate=self.max_gap_among_all_robots_individual_gap_width-21
            # side_wall_moving_rate=-np.random.choice([20,21])
            side_wall_moving_rate=-21
            # print("self.All_Robot_ID[0].mid_point_of_goals",self.All_Robot_ID[0].mid_point_of_goals)
            # self.gap=self.gap_generator(width=self.max_gap_among_all_robots_individual_gap_width, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = self.wall_length,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)
            self.gap=self.gap_generator(width=self.max_gap_among_all_robots_individual_gap_width, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = self.wall_length,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)
            self.sidewalls=self.gap_generator(width=side_wall_moving_rate, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = 25,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)
            # self.sidewall_left=self.gap_generator(width=0.1, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = 15,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)

            #print("gap",self,self.gap[0],self.gap[1])

            self.gap_point1,self.gap_point2=self.gap[2],self.gap[3]

            self.gap_orn=self.gap[4]
            # print(self.gap_orn)

            wall_1_length = max(np.linalg.norm(np.array(self.gap[0][0]) - np.array(self.gap[0][2])), np.linalg.norm(np.array(self.gap[0][1]) - np.array(self.gap[0][3])))
            #print("wall_1_length",wall_1_length)

            self.dist_gapwp1 = self.distance(pos, self.gap[2])
            self.dist_gapwp2 = self.distance(pos, self.gap[3])

            self.rectangle1_centre = [(self.gap[0][0][i] + self.gap[0][2][i]) / 2 for i in range(3)]
            self.rectangle2_centre = [(self.gap[1][0][i] + self.gap[1][2][i]) / 2 for i in range(3)]
            # print("r1",self.rectangle1_centre,"r2",self.rectangle2_centre)
            self.rectangle3_centre = [(self.sidewalls[0][0][i] + self.sidewalls[0][2][i]) / 2 for i in range(3)]
            self.rectangle4_centre = [(self.sidewalls[1][0][i] + self.sidewalls[1][2][i]) / 2 for i in range(3)]
            # print("r3",self.rectangle3_centre,"r4",self.rectangle4_centre)
            
            
            self.Boolian=False
            self.Boolian2=False

            
            # self.gap_point_moving = self.gap[2]
            # self.dist_gapwp_mv = self.distance(pos, self.gap[2])

            

            

        # if self.args.gap_avoidance and self.args.insert_wall:
        #     p.removeBody(self.rectangle_id1)
        #     p.removeBody(self.rectangle_id2)

        
            

        self.get_observation()

        
        

        # if self.args.obstacle_avoidance:
        #     self.corner_robot1 = [(tuple(self.robot1_bbox[0])),(tuple(self.robot1_bbox[1]))]
        #     self.corner_square_bigbox= [(tuple(self.safety_square_bbox[0])),(tuple(self.safety_square_bbox[1])),(tuple(self.safety_square_bbox[2])),(tuple(self.safety_square_bbox[3]))]
        #     self.way_point1,self.way_point2,self.way_point3,self.way_point4,_,_,_,_= self.min_fourth_min_distances(self.corner_robot1 , self.corner_square_bigbox)
        #     print(self.way_point1)
        #     self.Goal2 = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=self.way_point1[1])

        #     pm,om=p.getBasePositionAndOrientation(self.Id)
        #     print(pm)
        
        #self.Goal2 = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=self.waypoint)
        # self.Goal3 = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=self.way_point2)
        self.episodes += 1

        self.cur_time = 0
        self.total_reward = 0
        self.distance_to_goal=0
        

        # Time to take single step
        #print(list(self.pos))
        postuple= tuple(self.pos)
        allowance = 0.05 # allowance for flexibility in avoiding robot2
        if self.args.static_robots > 1:
            self.Initial_robot2_avoid_angle=self.robot2_avoid_angle + allowance #Set Robot 2 avoid angle in reset
        #print("Self_Robot2Ang",self.Initial_robot2_avoid_angle)
        #print("goal",_)
        #print(type(self.joint_vel))
        #return np.array(self.robot1_bbox[0] +self.robot1_bbox[1] +self.robot1_bbox[2] +self.robot1_bbox[3] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3] + self.contacts + self.contacts2+ list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+  list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped])
        # return np.array(list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped])
        return self.return_state()


    def move_goal_and_static_robot(self, initial_x, initial_y, yaw,robottogoal_angle,mid_point_goals,mid_point_robots):

        # Get a new goal position, make sure it is far enough away from the robot. 
        #state_object=[np.random.uniform(-7, 7), np.random.uniform(-8, -6), 0.00]
        #print("self.external_goals_states",self.external_goals_states)
        robot1_pos=(initial_x, initial_y)
        
        
        # if self.args.gap_avoidance:
        #     for self.robottogoal_angle in self.robottogoal_angles:
        #         state_object=self.find_position_B(robot1_pos, self.initial_goal_dist, self.robottogoal_angle)
        # else:
        # state_object=self.find_position_B(robot1_pos, self.initial_goal_dist, random.randint(0, 360))
        if self.args.gap_avoidance:
            
            state_object=self.find_position_B(robot1_pos, self.initial_goal_dist, robottogoal_angle)
            #print(self.robottogoal_angle);exit()
            # print("goal_pos",state_object)
            dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)
            #print(dist)
            # print(self.initial_goal_dist)
            while dist < 3:
                state_object=self.find_position_B(robot1_pos, self.initial_goal_dist, robottogoal_angle)
                dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)
        else:
            state_object=self.find_position_B(robot1_pos, self.initial_goal_dist, random.randint(0, 360))
            #print(self.robottogoal_angle);exit()
            dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)
            #print(dist)
            # print(self.initial_goal_dist)
            while dist < 3:
                state_object=self.find_position_B(robot1_pos, self.initial_goal_dist, random.randint(0, 360))
                dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)

        # Estimate time to target, velocity in steps + time to turn + current steps + buffer for going around a robot / acceleration
        # Keep an eye on this, need to make sure there's enough time to get to the goal
        self.heading_error, _ = self.calc_angle_error(state_object, [initial_x, initial_y], yaw)
        self.time_to_target = dist / self.timeStep_10Hz + abs(self.heading_error) / self.timeStep_10Hz + self.steps + 500000
        #print(self.time_to_target)
        
        if self.args.gap_avoidance:
                #Equation of the line trajectory from moving robot to goal
            if (mid_point_robots[0]-mid_point_goals[0])==0:
                mid_point_robots[0]=mid_point_goals[0]+0.01
                #print("DENOM_ZERO")

            #Slope
            M = (mid_point_robots[1]-mid_point_goals[1])/(mid_point_robots[0]-mid_point_goals[0])

            #Y-Intercept
            C = mid_point_robots[1] - (M * mid_point_robots[0])
            
            #Robot2

            # initial_y2 = np.random.uniform(-2.5, 2.5)  # y position of static robot

            # Start from the midpoint:
            rand_x = (mid_point_robots[0] + mid_point_goals[0]) / 2
            rand_y = (mid_point_robots[1] + mid_point_goals[1]) / 2
            
        
        else:
            #Equation of the line trajectory from moving robot to goal
            if (initial_x-state_object[0])==0:
                initial_x=state_object[0]+0.01
                #print("DENOM_ZERO")

            #Slope
            M = (initial_y-state_object[1])/(initial_x-state_object[0])

            #Y-Intercept
            C = initial_y - (M * initial_x)
            
            #Robot2

            # initial_y2 = np.random.uniform(-2.5, 2.5)  # y position of static robot

            # Start from the midpoint:
            rand_x = (initial_x + state_object[0]) / 2
            rand_y = (initial_y + state_object[1]) / 2

        target_dist = self.a-self.b
        # print("g",self.Goals_pos)
        # mid_point_goals=self.calculate_midpoint(self.Goals_pos[0],self.Goals_pos[1])

        # if self.args.gap_avoidance:
        #     angle = np.arctan2((initial_y-mid_point_goals[1]), (initial_x-mid_point_goals[0]))
        # else:
        #print("state_obj",state_object)
        if self.args.gap_avoidance:
            angle = np.arctan2((mid_point_robots[1]-mid_point_goals[1]), (mid_point_robots[0]-mid_point_goals[0]))
        
        else:
            angle = np.arctan2((initial_y-state_object[1]), (initial_x-state_object[0]))
        # target_angle = angle - 90 
        target_angle = random.choice([90 + angle, angle - 90 ])
        initial_x2 = target_dist * np.cos(target_angle) + rand_x
        initial_y2 = target_dist * np.sin(target_angle) + rand_y

        if self.args.debug:
            self.lineId=p.addUserDebugLine((initial_x, initial_y, 0), (state_object[0], state_object[1], 0), lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=5)
            p.addUserDebugLine((rand_x, rand_y, 0), (initial_x2, initial_y2, 0), lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=5)

        #initial_y2 = np.random.uniform(0, 0.5)   
        #initial_x2, initial_y2 = 0,0
        
        # self.initial_yaw2 = 0.0 # np.random.uniform(-1, 1)
        self.initial_yaw2 = -0.5 # np.random.uniform(-1, 1)
        self.initial_orn2 = p.getQuaternionFromEuler([0,0,self.initial_yaw2])
        self.z_offset = 0
        self.pos2, self.orn2 = [initial_x2, initial_y2, self.z_offset+0.31],self.initial_orn2
        #print("self.pos2",self.pos2)
        
        self.state_robot2 = self.pos2
        self.orn_robot2 = self.orn2
        self.roll2, self.pitch2, self.yaw2 = p.getEulerFromQuaternion(self.orn2)

        # Move the goal
        self.set_position(state_object, robot_id=self.Goal)
        self.state_goal, self.orn_goal = p.getBasePositionAndOrientation(self.Goal)

        # Move the static robot
        if self.args.static_robots > 1 and self.args.insert_robot2:
            self.set_position(self.pos2, self.orn2, robot_id=self.Id2)
            self.state_robot2, self.orn_robot2 = p.getBasePositionAndOrientation(self.Id2)

        # Move the square box
        if self.args.insert_box:
            self.set_position(self.pos2, self.orn2, robot_id=self.square)
            self.state_box, self.orn_box = p.getBasePositionAndOrientation(self.square)

        
        
            

    
    # FOR TURTLEBOT
    def twist_to_tracks(self, actions):
        # print(actions)
        if self.args.turtle_titan: 
            # print("check");exit()
            radius = 0.14
            width = 0.78/2
            # print(actions)
            lin_vel = actions[0]*3.9#*0.50
            ang_vel = np.clip(actions[1], -0.75, 0.75) #*0.48#*2.5/2
            # print(lin_vel,np.clip(ang_vel, -0.65, 0.65))
            # ang_vel = actions[1] #*3/2
            w_r = (lin_vel + ang_vel*width)/radius
            w_l = (lin_vel - ang_vel*width)/radius
            # print("action",actions,"wl",w_l,"w_r",w_r,self)
        else:
            radius = 0.14
            width = 0.78/2
            # print(actions)
            lin_vel = actions[0]#*3.9#*0.50
            ang_vel = np.clip(actions[1], -1, 1)#*2.5/2
            # ang_vel = actions[1] *0.6#*2.5/2
            # ang_vel = actions[1] #*3/2
            w_r = (lin_vel + ang_vel*width)/radius
            w_l = (lin_vel - ang_vel*width)/radius
            # print("action",actions,"wl",w_l,"w_r",w_r,self)
            return [w_l, w_r]

        return [w_l, w_r]
    

    # #FOR TITAN
    # def twist_to_tracks(self, actions):
    #     radius = 0.14
    #     width = 0.78/2
    #     # print(actions)
    #     lin_vel = actions[0]#*3.9#*0.50
    #     ang_vel = actions[1] *0.6#*2.5/2
    #     # ang_vel = actions[1] #*3/2
    #     w_r = (lin_vel + ang_vel*width)/radius
    #     w_l = (lin_vel - ang_vel*width)/radius
    #     # print("action",actions,"wl",w_l,"w_r",w_r,self)
    #     return [w_l, w_r]
    
    #def step(self, actions):
        #print("AAA",actions)
        #print(self)
        # actions=[2.5,5]
   
        # actions = 0.5*actions
        # ===========================
        # This is an expert functionexper
        # ===========================
    def motor_action(self,actions,expert_ac):
        # print("Action",actions)
        # print("expert_ac",expert_ac)
        # print("KP",self.Kp,self.Kp/self.initial_Kp)
        # print("titanaction",actions)
        # actions=[0.0,1.5]
        # actions=np.array([0,1.5])
        # print("motor action",actions,self)
        
        
        # print(self.max_gap_width-self.decrease_gap_width,self.final_gap_width)
        # self.ep_action_dict["Policy_Action/Linear"] += abs(actions[0])
        # self.ep_action_dict["Policy_Action/Angular"] += abs(actions[1])
        self.exp_actions = [0.0]*2

        if self.args.gap_avoidance and self.args.Pretrained_cur:
            # obs = MUL.reset()
            # im = MUL.get_image()
            # pol=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt")
            # sp_ac = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
            
            self.exp_actions[1] =expert_ac[1]
            self.exp_actions[0] = expert_ac[0]
            
            # print("self.exp_actions_immediate",self.exp_actions[0],self.exp_actions[1])
            
            for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                if str(robot_bbox[0]) != str(self):
                    self.robot1_near_robot2=False
                    self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                    self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                    self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                    # self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                    # self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox]
                    self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox, self.intersection_s1line_rbbox ]
                    #print(self.int_check_lines_vs_rbbox,self)
                    #print(num,robot_bbox[0]);exit()
                    # print("checking",self.turn_both)

                    if any(self.int_check_lines_vs_rbbox):
                        self.robot1_near_robot2=True
                        # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                        self.exp_actions[0] = expert_ac[0]*0.2
                        self.exp_actions[1] = expert_ac[0]*0.25
            
            # for robot_bbox in self.robots_bbox:
            # #print("k",robot_bbox,"whole",self.robots_bbox)
            #     # if str(robot_bbox[0])==str(self):
            #     #     #print(str(robot_bbox[0]),str(self))
            #     #     self.robot1_near_robot2=False
            #     if str(robot_bbox[0]) != str(self):
            #         self.robot1_near_robot2=False
            #         self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
            #         self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
            #         self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
            #         self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
            #         #print(self.int_check_lines_vs_rbbox,self)
            #         #print(num,robot_bbox[0]);exit()
            #         # print("checking",self.turn_both)

            #         if any(self.int_check_lines_vs_rbbox):
            #             self.robot1_near_robot2=True
            #             # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
            #             self.exp_actions[0] = -0.01
            #             self.exp_actions[1] = 0
            #             if self.turn_both and self==self.All_Robot_ID[0]:
            #                 self.exp_actions[0] = 0
            #                 self.exp_actions[1] = 0
            #             elif self.turn_both and self==self.All_Robot_ID[1]:
            #                 self.exp_actions[0] = 0
            #                 self.exp_actions[1] = 0


                
            #     # if self==self.All_Robot_ID[1]:    
            #     #     print(self.robot1_near_robot2,self)
            #             #break

            # # if self.intersection_r1_r:
            # #     print("TRRRRRRUUEEE")
            # #     self.exp_actions[0] = 0
            # #     self.exp_actions[1] = 0

        
            # if self.gapwp1_reach:
            #     # self.exp_actions[1] = 1.5*np.clip(self.heading_error_gapwp2, -1.5, 1.5)
            #     # # self.exp_actions[0] = 0.025
            #     # self.exp_actions[0] = 0.05
                
            #     for robot_bbox in self.robots_bbox:
            # #print("k",robot_bbox,"whole",self.robots_bbox)
            #     # if str(robot_bbox[0])==str(self):
            #     #     #print(str(robot_bbox[0]),str(self))
            #     #     self.robot1_near_robot2=False
            #         if str(robot_bbox[0]) != str(self):
            #             self.robot1_near_robot2=False
            #             self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
            #             self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
            #             self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
            #             self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
            #             #print(self.int_check_lines_vs_rbbox,self)
            #             #print(num,robot_bbox[0]);exit()
            #             # print("checking",self.turn_both)

            #             if any(self.int_check_lines_vs_rbbox):
            #                 self.robot1_near_robot2=True
            #                 # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
            #                 self.exp_actions[0] = -0.03
            #                 self.exp_actions[1] = -0.02
            #                 # if self.turn_both and self==self.All_Robot_ID[0]:
            #                 #     self.exp_actions[0] = 0.0
            #                 #     self.exp_actions[1] = 0.5
            #                 # elif self.turn_both and self==self.All_Robot_ID[1]:
            #                 #     self.exp_actions[0] = 0.0
            #                 #     self.exp_actions[1] = 0.0
                

            
            #     if self.gapwp2_reach:
            #         # self.exp_actions[1] = 1.5*np.clip(self.heading_error, -1, 1)

            #         # # self.exp_actions[0] = 1000
            #         # self.exp_actions[0] = 0.15
            #         for robot_bbox in self.robots_bbox:
            # #print("k",robot_bbox,"whole",self.robots_bbox)
            #     # if str(robot_bbox[0])==str(self):
            #     #     #print(str(robot_bbox[0]),str(self))
            #     #     self.robot1_near_robot2=False
            #             if str(robot_bbox[0]) != str(self):
            #                 self.robot1_near_robot2=False
            #                 self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
            #                 self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
            #                 self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
            #                 self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
            #                 #print(self.int_check_lines_vs_rbbox,self)
            
        # ##########################__RAY_LINE___###################
        #if self.args.num_robots > 1:
        # 	if self.hit[0] == True:
        # 		self.exp_actions[0] = 0.0
        # 		self.exp_actions[1] = -0.5
        # 	elif self.hit[1] == True:
        # 		self.exp_actions[0] = 0.0
        # 		self.exp_actions[1] = 0.5
        # 	elif abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
        # 		self.exp_actions[0] = 0.25
        # 		self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        # 	else:	
        # 		self.exp_actions[0] = 0.0
        # 		self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        # if self.args.gap_avoidance:
        # ####################_______WAY_POINT_ATTEMPT_FAILED______######################
        #     if (self.intersection_line_gap_wall1== True or self.intersection_line_gap_wall2==True) and abs(self.heading_error) < 1.6: 
                
        #         self.exp_actions[0] = 0.1
        #         self.exp_actions[1] = 0.5#*np.clip(self.heading_error_wp1, -1, 1)
                
        #     elif (self.intersection_headingcorner1_gap_wall1 == True or self.intersection_headingcorner1_gap_wall2 == True) and abs(self.heading_error) < 1.6:
        #         self.exp_actions[0] = 0.05
        #         self.exp_actions[1] = -0.5	
        #     elif (self.intersection_headingcorner2_gap_wall1 == True or self.intersection_headingcorner2_gap_wall2 == True) and abs(self.heading_error) < 1.6:
        #         self.exp_actions[0] = 0.05
        #         self.exp_actions[1] = 0.5
        #     elif abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
        #         self.exp_actions[0] = 0.25
        #         self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        #     else:	
        #         self.exp_actions[0] = 0.0
        #         self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)


        # if self.args.gap_avoidance and self.args.MA_bootstrap_extreme:
        # # ####################_______WAY_POINT_SYSTEM______#####
        #     #make sure to uncomment it when remove wall
        #     # if self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2 or self.intersection_r1_r:
        #     #     self.exp_actions[0] = 0
        #     #     self.exp_actions[1] = 0
        #     # else:
        #     #print(self.heading_error_gapwp1,self.heading_error_gapwp2,self.heading_error)

            

        #     # else:
            
        #     self.exp_actions[0] = 0.08
        #     self.exp_actions[1] = 0.5*np.clip(self.heading_error_gapwp1, -1, 1)
            
        #     for robot_bbox in self.robots_bbox:
        #     #print("k",robot_bbox,"whole",self.robots_bbox)
        #         # if str(robot_bbox[0])==str(self):
        #         #     #print(str(robot_bbox[0]),str(self))
        #         #     self.robot1_near_robot2=False
        #         if str(robot_bbox[0]) != str(self):
        #             self.robot1_near_robot2=False
        #             self.intersection_hline_rbbox,_= self.intersection_check(self.head_line,robot_bbox[1])
        #             self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g,robot_bbox[1])
        #             self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g,robot_bbox[1])
        #             self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
        #             #print(self.int_check_lines_vs_rbbox,self)
        #             #print(num,robot_bbox[0]);exit()
        #             # print("checking",self.turn_both)

        #             if any(self.int_check_lines_vs_rbbox):
        #                 self.robot1_near_robot2=True
        #                 # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
        #                 self.exp_actions[0] = 0
        #                 self.exp_actions[1] = 1*np.clip(self.heading_error_gapwp1, -1, 1)
        #                 if self.turn_both and self==self.All_Robot_ID[0]:
        #                         self.exp_actions[0] = -0.2
        #                         self.exp_actions[1] = 0.1
        #                 elif self.turn_both and self==self.All_Robot_ID[1]:
        #                     self.exp_actions[0] = 0.05
        #                     self.exp_actions[1] = 0.5*np.clip(self.heading_error_gapwp1, -1, 1)


                
        #         # if self==self.All_Robot_ID[1]:    
        #         #     print(self.robot1_near_robot2,self)
        #                 #break

        #     # if self.intersection_r1_r:
        #     #     print("TRRRRRRUUEEE")
        #     #     self.exp_actions[0] = 0
        #     #     self.exp_actions[1] = 0

        
        #     if self.gapwp1_reach:
        #         self.exp_actions[0] = 0.15
        #         self.exp_actions[1] = 1*np.clip(self.heading_error_gapwp2, -1, 1)
        #         for robot_bbox in self.robots_bbox:
        #     #print("k",robot_bbox,"whole",self.robots_bbox)
        #         # if str(robot_bbox[0])==str(self):
        #         #     #print(str(robot_bbox[0]),str(self))
        #         #     self.robot1_near_robot2=False
        #             if str(robot_bbox[0]) != str(self):
        #                 self.robot1_near_robot2=False
        #                 self.intersection_hline_rbbox,_= self.intersection_check(self.head_line,robot_bbox[1])
        #                 self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g,robot_bbox[1])
        #                 self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g,robot_bbox[1])
        #                 self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
        #                 #print(self.int_check_lines_vs_rbbox,self)
        #                 #print(num,robot_bbox[0]);exit()
        #                 # print("checking",self.turn_both)

        #                 if any(self.int_check_lines_vs_rbbox):
        #                     self.robot1_near_robot2=True
        #                     # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
        #                     self.exp_actions[0] = 0
        #                     self.exp_actions[1] = 0.7*np.clip(self.heading_error_gapwp2, -1, 1)
        #                     if self.turn_both and self==self.All_Robot_ID[0]:
        #                         self.exp_actions[0] = -0.2
        #                         self.exp_actions[1] = 0.1
        #                     elif self.turn_both and self==self.All_Robot_ID[1]:
        #                         self.exp_actions[0] = -0.1
        #                         self.exp_actions[1] = -0.1
                

            
        #         if self.gapwp2_reach:
        #             self.exp_actions[0] = 0.2
        #             self.exp_actions[1] = 2*np.clip(self.heading_error, -1, 1)
        #             for robot_bbox in self.robots_bbox:
        #     #print("k",robot_bbox,"whole",self.robots_bbox)
        #         # if str(robot_bbox[0])==str(self):
        #         #     #print(str(robot_bbox[0]),str(self))
        #         #     self.robot1_near_robot2=False
        #                 if str(robot_bbox[0]) != str(self):
        #                     self.robot1_near_robot2=False
        #                     self.intersection_hline_rbbox,_= self.intersection_check(self.head_line,robot_bbox[1])
        #                     self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g,robot_bbox[1])
        #                     self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g,robot_bbox[1])
        #                     self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
        #                     #print(self.int_check_lines_vs_rbbox,self)
        #                     #print(num,robot_bbox[0]);exit()
        #                     # print("checking",self.turn_both)

        #                     if any(self.int_check_lines_vs_rbbox):
        #                         self.robot1_near_robot2=True
        #                         # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
        #                         self.exp_actions[0] = 0
        #                         self.exp_actions[1] = 2*np.clip(self.heading_error_gapwp2, -1, 1)
        #                     if self.turn_both and self==self.All_Robot_ID[0]:
        #                         self.exp_actions[0] = -0.2
        #                         self.exp_actions[1] = 0.1
        #                     elif self.turn_both and self==self.All_Robot_ID[1]:
        #                         self.exp_actions[0] = -0.1
        #                         self.exp_actions[1] = -0.1
        #     #print(self.exp_actions,self)

        elif self.args.gap_avoidance and self.args.RIPG:
        # ####################_______WAY_POINT_SYSTEM______#####
            #make sure to uncomment it when remove wall
            # if self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2 or self.intersection_r1_r:
            #     self.exp_actions[0] = 0
            #     self.exp_actions[1] = 0
            # else:
            #print(self.heading_error_gapwp1,self.heading_error_gapwp2,self.heading_error)

            

            # else:
            
            
            # self.exp_actions[1] = 1.5*np.clip(self.heading_error_gapwp1, -1, 1)
            # self.exp_actions[0] = 0.05
            self.exp_actions=actions
            for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                if str(robot_bbox[0]) != str(self):
                    self.robot1_near_robot2=False
                    self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                    self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                    self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                    self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                    #print(self.int_check_lines_vs_rbbox,self)
                    #print(num,robot_bbox[0]);exit()
                    # print("checking",self.turn_both)

                    if any(self.int_check_lines_vs_rbbox):
                        self.robot1_near_robot2=True
                        # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                        # self.exp_actions[0] = -0.02
                        
                        # print("time",self.timeStep_10Hz*self.steps)
                        # reverse_time=0.5
                        # self.exp_actions[0] = -0.75
                        # self.exp_actions[1] = 0
                        self.reset_time+=self.timeStep_10Hz
                        # print("New_TIME",self.reset_time)
                        if self.turn_both and self==self.All_Robot_ID[0]:
                            # print("New_TIME",self.reset_time);exit()
                            if self.reset_time<0.5:
                                self.exp_actions[0] = -0.75#0.02
                                self.exp_actions[1] = 0
                            elif self.reset_time<np.random.uniform(0.5, 6):
                                self.exp_actions[0] = 0#0.02
                                self.exp_actions[1] = 0
                        elif self.turn_both and self==self.All_Robot_ID[1]:
                            # print("New_TIME",self.reset_time);exit()
                            if self.reset_time<0.5:
                                self.exp_actions[0] = -0.75#0.02
                                self.exp_actions[1] = 0
                            elif self.reset_time<np.random.uniform(0.5, 6):
                                self.exp_actions[0] = 0#0.02
                                self.exp_actions[1] = 0
                        else:
                            # if self.reset_time<2:
                            # if self.args.randomness==1:
                            if self.reset_time<0.5:
                                self.exp_actions[0] = -0.75#0.02
                                self.exp_actions[1] = 0
                            elif self.reset_time<np.random.uniform(0.5, 6):
                                self.exp_actions[0] = 0#0.02
                                self.exp_actions[1] = 0
                            # if self.args.randomness==3:
                            #     self.exp_actions[0] = -0.75#0.02
                            #     self.exp_actions[1] = 0
                            # self.exp_actions[0] = -0.75#0.02
                            # self.exp_actions[1] = 0
                            # elif self.reset_time<np.random.uniform(0.5, 6):
                            #     self.exp_actions[0] = 0#0.02
                            #     self.exp_actions[1] = 0
                            # self.exp_actions[0] = -0.75#0.02
                            # self.exp_actions[1] = 0


        elif self.args.gap_avoidance and self.args.Road_rule:
        # ####################_______WAY_POINT_SYSTEM______#####
            #make sure to uncomment it when remove wall
            # if self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2 or self.intersection_r1_r:
            #     self.exp_actions[0] = 0
            #     self.exp_actions[1] = 0
            # else:
            #print(self.heading_error_gapwp1,self.heading_error_gapwp2,self.heading_error)

            

            # else:
            
            
            # self.exp_actions[1] = 1.5*np.clip(self.heading_error_gapwp1, -1, 1)
            # self.exp_actions[0] = 0.05
            self.exp_actions=actions
            for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                if str(robot_bbox[0]) != str(self):
                    self.robot1_near_robot2=False
                    self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                    self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                    self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                    # self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                    # self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox]
                    self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox, self.intersection_s1line_rbbox ]
                    #print(self.int_check_lines_vs_rbbox,self)
                    #print(num,robot_bbox[0]);exit()
                    # print("checking",self.turn_both)

                    if any(self.int_check_lines_vs_rbbox):
                        self.robot1_near_robot2=True
                        # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                        self.exp_actions[0] = -0.75
                        self.exp_actions[1] = 0
                        # if self.turn_both and self==self.All_Robot_ID[0]:
                        #     self.exp_actions[0] = -0.02
                        #     self.exp_actions[1] = 0
                        # elif self.turn_both and self==self.All_Robot_ID[1]:
                        #     self.exp_actions[0] = -0.02
                        #     self.exp_actions[1] = 0

        ##THIS MA BOOTSTRAP IS THE BEST AND SAVED############################
        elif self.args.gap_avoidance and self.args.MA_bootstrap:
        # elif self.args.gap_avoidance and self.args.MA_bootstrap :
        # ####################_______WAY_POINT_SYSTEM______#####
            #make sure to uncomment it when remove wall
            # if self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2 or self.intersection_r1_r:
            #     self.exp_actions[0] = 0
            #     self.exp_actions[1] = 0
            # else:
            #print(self.heading_error_gapwp1,self.heading_error_gapwp2,self.heading_error)

            

            # else:
            
            
            self.exp_actions[1] = 1.5*np.clip(self.heading_error_gapwp1, -1, 1)
            self.exp_actions[0] = 0.05
            # print(actions,self)
            for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                if str(robot_bbox[0]) != str(self):
                    self.robot1_near_robot2=False
                    self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                    self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                    self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                    self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                    #print(self.int_check_lines_vs_rbbox,self)
                    #print(num,robot_bbox[0]);exit()
                    # print("checking",self.turn_both)

                    if any(self.int_check_lines_vs_rbbox):
                        self.robot1_near_robot2=True
                        # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                        self.exp_actions[0] = -0.01
                        self.exp_actions[1] = 0
                        if self.turn_both and self==self.All_Robot_ID[0]:
                            self.exp_actions[0] = 0
                            self.exp_actions[1] = 0
                        elif self.turn_both and self==self.All_Robot_ID[1]:
                            self.exp_actions[0] = 0
                            self.exp_actions[1] = 0


                
                # if self==self.All_Robot_ID[1]:    
                #     print(self.robot1_near_robot2,self)
                        #break

            # if self.intersection_r1_r:
            #     print("TRRRRRRUUEEE")
            #     self.exp_actions[0] = 0
            #     self.exp_actions[1] = 0

        
            if self.gapwp1_reach:
                self.exp_actions[1] = 1.5*np.clip(self.heading_error_gapwp2, -1.5, 1.5)
                # self.exp_actions[0] = 0.025
                self.exp_actions[0] = 0.05
                
                for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                    if str(robot_bbox[0]) != str(self):
                        self.robot1_near_robot2=False
                        self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                        self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                        self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                        self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                        #print(self.int_check_lines_vs_rbbox,self)
                        #print(num,robot_bbox[0]);exit()
                        # print("checking",self.turn_both)

                        if any(self.int_check_lines_vs_rbbox):
                            self.robot1_near_robot2=True
                            # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                            self.exp_actions[0] = -0.03
                            self.exp_actions[1] = -0.02
                            # if self.turn_both and self==self.All_Robot_ID[0]:
                            #     self.exp_actions[0] = 0.0
                            #     self.exp_actions[1] = 0.5
                            # elif self.turn_both and self==self.All_Robot_ID[1]:
                            #     self.exp_actions[0] = 0.0
                            #     self.exp_actions[1] = 0.0
                

            
                if self.gapwp2_reach:
                    self.exp_actions[1] = 1.5*np.clip(self.heading_error, -1, 1)

                    # self.exp_actions[0] = 1000
                    self.exp_actions[0] = 0.15
                    for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
                # if str(robot_bbox[0])==str(self):
                #     #print(str(robot_bbox[0]),str(self))
                #     self.robot1_near_robot2=False
                        if str(robot_bbox[0]) != str(self):
                            self.robot1_near_robot2=False
                            self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                            self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                            self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                            self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                            #print(self.int_check_lines_vs_rbbox,self)
                            #print(num,robot_bbox[0]);exit()
                            # print("checking",self.turn_both)

                            # if any(self.int_check_lines_vs_rbbox):
                            #     self.robot1_near_robot2=True
                            #     # print("self.robot1_near_robot2",self.robot1_near_robot2,self)
                            #     self.exp_actions[0] = 0
                            #     self.exp_actions[1] = 0
                                # if self.turn_both and self==self.All_Robot_ID[0]:
                                #     self.exp_actions[0] = 0.0
                                #     self.exp_actions[1] = 0.5
                                # elif self.turn_both and self==self.All_Robot_ID[1]:
                                #     self.exp_actions[0] = 0.0
                                #     self.exp_actions[1] = 0.0
            #print(self.exp_actions,self)
            

        elif self.args.gap_avoidance and (self.args.regular_bootstrap):

            self.exp_actions[0] = 0.08
            self.exp_actions[1] = 0.5*np.clip(self.heading_error_gapwp1, -1, 1)
            # print(self.heading_error_gapwp1)  #heading_error_gapwp1
            if self.gapwp1_reach:
                self.exp_actions[0] = 0.08
                self.exp_actions[1] = 0.2*np.clip(self.heading_error_gapwp2, -1, 1)
                #print("wp2")
                if self.gapwp2_reach:
                    self.exp_actions[0] = 0.08
                    self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                    #print("Goal")

        elif self.args.gap_avoidance and (self.args.num_robots == 1)  and not self.Kp<5:

            self.exp_actions[0] = 0.06
            self.exp_actions[1] = 0.5*np.clip(self.heading_error_gapwp1, -1, 1)
            #print("wp1")
            if self.gapwp1_reach:
                self.exp_actions[0] = 0.06
                self.exp_actions[1] = 0.5*np.clip(self.heading_error_gapwp2, -1, 1)
                #print("wp2")
                if self.gapwp2_reach:
                    self.exp_actions[0] = 0.1
                    self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                    #print("Goal")

    
        elif self.args.obstacle_avoidance  and not self.Kp<5:
        # ####################_______WayPoint System Inspired by Bug 2 algorithm______######################
            if self.intersection_r1_box or self.intersection_r1_r:
                self.exp_actions[0] = 0
                self.exp_actions[1] = 0
                #print("MAMMMMAAAAAAAAAAAAAAAAAAAAAAA",self.exp_actions[0],self.exp_actions[1])

            elif self.intersection_wp2G_obs == None or self.intersection_wp3G_obs == None or self.dist_R12G == None or self.dist_R13G == None or self.dist_R124G==None or self.dist_R134G==None:
                if abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
                    self.exp_actions[0] = 0.15
                else:	
                    self.exp_actions[0] = 0.0
                self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)

            elif (self.intersection_wp2G_obs == True and self.intersection_wp3G_obs == False) or (self.intersection_wp2G_obs == False and self.intersection_wp3G_obs == False and self.dist_R13G<self.dist_R12G):
                self.exp_actions[0] = 0.1
                self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    self.exp_actions[0] = 0.1
                    self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp3, -1, 1)
                    if self.wp3_reach>0:
                        self.exp_actions[0] = 0.1
                        self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                
                    


            elif (self.intersection_wp3G_obs == True and self.intersection_wp2G_obs == False) or (self.intersection_wp2G_obs == False and self.intersection_wp3G_obs == False and self.dist_R12G<self.dist_R13G):
                self.exp_actions[0] = 0.1
                self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    self.exp_actions[0] = 0.1
                    self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp2, -1, 1)
                    if self.wp2_reach>0:
                        self.exp_actions[0] = 0.1
                        self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                
                    

            elif self.intersection_wp2G_obs == True and self.intersection_wp3G_obs == True and self.dist_R124G<self.dist_R134G:
                self.exp_actions[0] = 0.1
                self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    self.exp_actions[0] = 0.1
                    self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp2, -1, 1)
                    if self.wp2_reach>0:
                        self.exp_actions[0] = 0.1
                        self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp4, -1, 1)
                        if self.wp4_reach>0:
                            self.exp_actions[0] = 0.1
                            self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                
                    


            elif self.intersection_wp2G_obs == True and self.intersection_wp3G_obs == True and self.dist_R134G<self.dist_R124G:
                self.exp_actions[0] = 0.1
                self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    self.exp_actions[0] = 0.1
                    self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp3, -1, 1)
                    if self.wp3_reach>0:
                        self.exp_actions[0] = 0.1
                        self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp4, -1, 1)
                        if self.wp4_reach>0:
                            self.exp_actions[0] = 0.1
                            self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)

            
                
                    


        # ####################_______BUG_1_intersection_only______######################
            # if self.intersection_line_square== True and abs(self.heading_error) < 1.6: 
            #     # self.square_bigbox=self.bbox_generator_box(3,0.035,self.pos2,self.orn2,self.lineId_box1big)
            #     # self.square_bigbox.append(self.square_bigbox[0])
            #     # self.corner_robot1 = [(tuple(self.robot1_bbox[0])),(tuple(self.robot1_bbox[1]))]
            #     # self.corner_square_bigbox= [(tuple(self.square_bigbox[0])),(tuple(self.square_bigbox[1])),(tuple(self.square_bigbox[2])),(tuple(self.square_bigbox[3]))]
            #     # _,_,self.way_point1,self.way_point2= self.min_distance_corners(self.corner_robot1 , self.corner_square_bigbox)
            #     # self.heading_error_wp1, _ = self.calc_angle_error(self.way_point1, self.pos, self.yaw)
            #     # self.heading_error_wp2, _ = self.calc_angle_error(self.way_point2, self.pos, self.yaw)
            #     self.exp_actions[0] = 0.1
            #     self.exp_actions[1] = 0.5#*np.clip(self.heading_error_wp1, -1, 1)
            #     # if self.args.obstacle_avoidance:
            #     # 	self.exp_actions[0] = 0.2
            #     # 	self.exp_actions[1] = 0.5*np.clip(self.heading_error_wp2, -1, 1)
            # elif self.intersection_corner1_square == True and abs(self.heading_error) < 1.6:
            #     self.exp_actions[0] = 0.05
            #     self.exp_actions[1] = -0.5	
            # elif self.intersection_corner2_square ==True and abs(self.heading_error) < 1.6:
            #     self.exp_actions[0] = 0.05
            #     self.exp_actions[1] = 0.5
            # elif abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
            #     self.exp_actions[0] = 0.25
            #     self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
            # else:	
            #     self.exp_actions[0] = 0.0
            #     self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)

        ######################____OLD_IS_GOLD___#################################

        # 	if abs(self.heading_error) < 0.5 and self.dist_r1_r2 >1.5 and self.dist_to_wp > 1.0:
        # 		self.exp_actions[0] = 0.25
        # 		self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
            
        # 	elif abs(self.heading_error) < 1.5 and self.dist_r1_r2 <1.5 and self.dist_to_wp > 1.0:
        # 		self.exp_actions[0] = 0.04
        # 		self.exp_actions[1] = -0.5*np.clip(self.heading_error_obs, -1, 1)
        # 	else:	
        # 		self.exp_actions[0] = 0.0
        # 		self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        # elif self.Kp<5:
        #     # print("checking")
        #     self.exp_actions[0] = 0
        #     self.exp_actions[1] = 0
        # elif self.max_gap_width-self.decrease_gap_width == self.final_gap_width:
        #     self.exp_actions[0] = 0
        #     self.exp_actions[1] = 0
        else:
            if abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
                self.exp_actions[0] = 0.25
            else:	
                self.exp_actions[0] = 0.0
            self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        
        # print("actions",actions,self)
        # self.dd +=actions[0]
        # print('dd',self.dd)
        # print("actions",actions,self)
        # self.exp_actions = [0.0]*2
        # print("self.exp_actions",self.exp_actions)
        if self.args.unclipped_vel:
            self.exp_actions=self.exp_actions*np.array([10,16])

        elif self.args.Pretrained_cur:
            self.exp_actions=self.exp_actions
            
        else:
            self.exp_actions=self.exp_actions*np.array([35,70])
            self.expertise_actions=self.exp_actions.tolist()
        # print("self.exp_actions_afer",self.exp_actions)
        # print("expeeee",type(self.exp_actions),type(actions))

        
        # actions=[0.1,0.1]
        if self.args.just_expert or (self.args.cur or self.args.expert_curr) and self.goal_moved==False:
            # print(self.goal_moved,"goal_moved")
            #Make sure to uncomment it when freezing robot when hitting wall lines to work with multi robot
            # if (self.args.reward_fn == 25 or self.args.reward_fn == 26 or self.args.reward_fn == 27 or self.args.reward_fn == 28 ) and (np.array(self.contacts) == True).any() and (self.applied_actions[0]>0):
            # #if self.intersection_r1_r:
            # # if self.args.num_robots >1 and self.robot1_near_robot2 and not self.turn_both:
            #     self.applied_actions=[0]*2
            # if (self.args.reward_fn == 25 or self.args.reward_fn == 26 or self.args.reward_fn == 27 or self.args.reward_fn == 28 ) and (np.array(self.contacts) == True).any() and (self.applied_actions[0]>-0.2):
            # #if self.intersection_r1_r:
            # # if self.args.num_robots >1 and self.robot1_near_robot2 and not self.turn_both:
            #     # print(self.applied_actions[0])
            #     self.applied_actions[0]=-5
                # self.applied_actions=[0]*2
            # else:

            # self.ep_action_dict["Prior_Action/Linear"] += abs(self.exp_actions[0])
            # self.ep_action_dict["Prior_Action/Angular"] += abs(self.exp_actions[1])
            if self.args.behaviour_cloning:
                self.applied_actions = self.w *np.array(self.exp_actions)
            else:
                self.applied_actions = (self.Kp/self.initial_Kp) *np.array(self.exp_actions)
            
            if not self.args.just_expert:
                # print("actionssssss",actions,type(actions))
                if self.args.Pretrained_cur:
                    self.applied_actions += self.action_multiplier*actions*(1-self.Kp/self.initial_Kp)
                elif self.args.behaviour_cloning:
                    self.applied_actions += self.action_multiplier*actions*(1-self.w)
                else:
                    self.applied_actions += self.action_multiplier*actions
        else:
            # print(self.goal_moved,"goal_moved")
            # if (self.args.reward_fn == 25 or self.args.reward_fn == 26 or self.args.reward_fn == 27 or self.args.reward_fn == 28 ) and (np.array(self.contacts) == True).any() and (self.applied_actions[0]>-1):
            # #if self.intersection_r1_r:
            # # if self.args.num_robots >1 and self.robot1_near_robot2 and not self.turn_both:
            #     self.applied_actions=[0]*2
            
            # else:   
            self.applied_actions = self.action_multiplier*actions
        # print("self.applied_actions",self.applied_actions,self)    
                # self.applied_actions = (self.Kp/self.initial_Kp) * np.array(self.exp_actions)
                # if not self.args.just_expert:
                #     self.applied_actions += self.action_multiplier*actions
        # print("self.exp_actions_after",self.exp_actions)

        # print("applied_action",self.applied_actions)
        
        # Network now outputs a twist message
        # print("actions",self,actions)

        # if self.applied_actions[0]*0.3>1 or  self.applied_actions[0]*0.3<-0.5:
        #     print("tham");exit()
        
        if self.tipped:
            self.applied_actions=[0]*2
        # print("applied_action",self.applied_actions)

        # clipped_linear_vel_command=np.clip(self.applied_actions[0], -0.5, 1)
        # clipped_angular_vel_command=np.clip(self.applied_actions[1], -1.5, 1.5)

        clipped_linear_vel_command=np.clip(self.applied_actions[0], -0.5, 0.75)
        clipped_angular_vel_command=np.clip(self.applied_actions[1], -0.75, 0.75)

        self.clipped_applied_actions=[clipped_linear_vel_command,clipped_angular_vel_command]

        # # print("clipped_applied_actions",self.clipped_applied_actions,self)
        # self.ep_action_dict["Action/Linear"] += abs(self.clipped_applied_actions[0]/0.75)
        # self.ep_action_dict["Action/Angular"] += abs(self.clipped_applied_actions[1]/0.75)
        # print(self.clipped_applied_actions[0],self.ep_action_dict["Action/Linear"])

        if self.args.unclipped_vel:
            track_actions = self.twist_to_tracks(self.applied_actions)    
        else:
            track_actions = self.twist_to_tracks(self.clipped_applied_actions)

        # print("track_actions",track_actions)
        # action_saving=[]
        for (a, tracks) in zip(track_actions,[self.left_track, self.right_track]):
            for track in tracks:
                p.setJointMotorControl2(self.Id, track, p.VELOCITY_CONTROL, targetVelocity=a, force=100)
            # print([a],track_actions,type([a]))
        # action_saving.append(a)
        # accc=pd.DataFrame(action_saving)
        # print(accc,type(accc))
        # accc.to_csv("action_pattern.csv")
        # print(track_actions)
        # action_saving.extend([track_actions[0]])
        # # for i in [track_actions[0]]:
        # #     action_saving.append(i)
        # print(action_saving)


        # df1 = pd.DataFrame({'Column1': column1})
        # df2 = pd.DataFrame({'Column2': column2})

        self.prev_actions = actions

        # p.stepSimulation()

    def return_step(self,action):
        # action=[0.0,1.5]
        self.actions_policy=action
        if self.args.render:
            time.sleep(self.args.sleep)
        self.get_observation()
        self.save_sim_state()
        #reward, done = self.get_reward()
        reward, done, termination = getattr(self, self.reward_fn_name)()
        # print("reward_before",reward)
        # print("action",action[1],"pre",self.pre_action[1])
        #-------------------------------------------------------------------------------------------------------
        # reward=reward-0.001*(((self.pre_action[0]-action[0])**2)+((self.pre_action[1]-action[1])**2))

        # # print("reward_after",reward)

        # self.pre_action=action

        # dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        # # print("time",current_time,"self.prev_actions",self.prev_actions,"current_action",action)
        
        # # print("Just_vx",self.vx, "self.yaw_vel",self.yaw_vel,"TIME",current_time)
        # # print(action[0])
        # # print(action[0][0])
        # scaling_f_linear=self.vx/action[0]
        # scaling_f_angular=self.yaw_vel/action[1]

        # self.time_saving.append(current_time)
        # self.velocity_saving1.append(self.vx)
        # self.velocity_saving2.append(self.yaw_vel)

        # self.action_saving1.append([action[0]])
        # self.action_saving2.append([action[1]])

        # self.scale_f_linear.append(scaling_f_linear)
        # self.scale_f_angular.append(scaling_f_angular)


        
        

        # # datafrm=pd.concat([column0,column1,column2],axis=1)
        # # # print("datafrm",datafrm)
        # # datafrm.to_csv("/home/kom018/behaviour_rl/action_time.csv")
        # # print("before actions",action)


        # time_s=pd.DataFrame(self.time_saving)
        # linear_vx=pd.DataFrame(self.velocity_saving1)
        # anglular_yvel=pd.DataFrame(self.velocity_saving2)
        # action1=pd.DataFrame(self.action_saving1)
        # action2=pd.DataFrame(self.action_saving2)
        # sf_linear=pd.DataFrame(self.scale_f_linear)
        # sf_angular=pd.DataFrame(self.scale_f_angular)

        # # print("action_after",action)


        # datafrm=pd.concat([time_s,action1,linear_vx,sf_linear,action2,anglular_yvel,sf_angular],axis=1)
        # # print("datafrm",datafrm)
        # datafrm.to_csv("/home/kom018/behaviour_rl/action_velocity_time_constant51.ods")
        #----------------------------------------------------------------------------------
        # Move the waypoint and static robot if close the waypoint
        # print(self.ep_goal_success, self.time_to_target, self.steps, self.dist_to_wp)
        #print("time_step",self.steps)
        #print("self.dist_to_wp",self.dist_to_wp)
        #self.Goal_pos,Goal_orn = p.getBasePositionAndOrientation(self.Goal)
        #print("self.Goal_pos",self.Goal_pos)
        #print("before",self.gap_point1,self.gap_point2,self.dist_gapwp1,self.dist_gapwp2)
        
        #print("counter",self.counter,"WP_Before",self.gap_point1,"wp2",self.gap_point2,"reach",self.gapwp1_reach,self.gapwp2_reach )
        #print("reach",self.gapwp1_reach,self.gapwp2_reach)
        
        if self.dist_to_wp < 1.0:
            
            self.number_Goal_Reached=self.number_Goal_Reached+1
            # print("Success",self.number_Goal_Reached)
            self.goal_reaching=True
            self.goal_moved=True
            #print("self.Goal_pos",self.Goal_pos)
            self.opposite_angle =0#175
            # self.opposite_angle *= -1
            self.wp1_reach=0
            self.wp2_reach=0
            self.wp3_reach=0
            self.wp4_reach=0

            self.gapwp1_reach=False
            self.gapwp2_reach=False
            
            #for robottogoal_angle in self.robottogoal_angles: 
                #print(robottogoal_angle)   
                # self.move_goal_and_static_robot(self.pos[0], self.pos[1], self.yaw,robottogoal_angle=robottogoal_angle)
            self.exp_actions = [0.0]*2
            # self.robottogoal_angle=None

            # for robot, angles in self.robottogoal_angles:
            #     if robot == self:
            #         # Assuming there's only one value in the angles list for simplicity
            #         self.robottogoal_angle = angles
            #         break
            #     else:
            #         # If the robot_name is not found, handle it accordingly
            #         print(f"Robot {self} not found in robottogoal_angles.")
                
            if self.args.gap_avoidance:
                
                # print("opposite_angle",self.opposite_angle,self.robottogoal_angle)
                # print("observation self.robottogoal_angle",self.robottogoal_angle)

                self.move_goal_and_static_robot(initial_x=self.pos[0], initial_y=self.pos[1], yaw=self.initial_yaw,robottogoal_angle=self.opposite_angle-self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)

                self.counter +=1
                #print("counter",self.counter)
                if self.counter % 2 == 0:
                    self.gap_point1=self.gap[2]
                    self.gap_point2=self.gap[3]
                    self.dist_gapwp1 = self.distance(self.pos, self.gap[2])
                    self.dist_gapwp2 = self.distance(self.pos, self.gap[3])
                else:
                    self.gap_point1=self.gap[3]
                    self.gap_point2=self.gap[2]
                    self.dist_gapwp1 = self.distance(self.pos, self.gap[3])
                    self.dist_gapwp2 = self.distance(self.pos, self.gap[2])
                    
                #print("WP_After",self.gap_point1,"wp2",self.gap_point2 )


                
            else:
                self.move_goal_and_static_robot(initial_x=self.pos[0], initial_y=self.pos[1], yaw=self.initial_yaw,robottogoal_angle=self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)
            #     # if self.args.gap_avoidance:
            #     #     self.gap=self.gap_generator(width=self.gap_width, depth=self.tunnel_depth,height=0.015,pos=self.pos2,wall_length = 20,goal_pos=self.mid_point_of_goals,lineId=self.lineIdWall,lineIdgap=self.lineIdgap,lineIdA=self.lineIdA,lineIdB=self.lineIdB)

            #     #     self.gap_orn=self.gap[4]

            #     #     self.wall1_pos=self.gap[5]
            #     #     self.wall2_pos=self.gap[6]

            #     #     self.Boolian=False
            #     #     self.Boolian2=False
            #     #     self.dist_gapwp1 = self.distance(self.pos, self.gap[2])
            #     #     self.dist_gapwp2 = self.distance(self.pos, self.gap[3])

            #     #     self.gap_point_moving = self.gap[2]
            #     #     self.dist_gapwp_mv = self.distance(self.pos, self.gap[2])


            self.goal_success.append(True)
            # print("Reached__________________________",self)
            self.time_to_goal=self.steps
            # print(self.steps,self)
            # print(self.time_to_goal,self.steps,self.timeStep_10Hz,self.timeStep_10Hz*self.steps,self)
            # print("Event")
            # THIS ONE
            # print("Time_to_goal",self.timeStep_10Hz*self.steps,self)
            # print("self.goal_success",self.goal_success,self)



 
        elif self.time_to_target < self.steps:

            if self.args.gap_avoidance:

                self.move_goal_and_static_robot(initial_x=self.pos[0], initial_y=self.pos[1], yaw=self.initial_yaw,robottogoal_angle=self.opposite_angle-self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)
            else:
                self.move_goal_and_static_robot(initial_x=self.pos[0], initial_y=self.pos[1], yaw=self.initial_yaw,robottogoal_angle=self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)
            
            self.goal_success.append(False)
            # print("Wrong_GOAL_SUCCESS",self.goal_success,self)
        # print("another",self.time_to_gapwp1)
        # print("time_wp2",self.time_to_gapwp2)
        # print("Time_to_gapWp1",self.time_to_gapwp1)
        # print("Time_to_gapWp2",self.time_to_gapwp2)
        # print("gapWp1_to_gapWp2",self.time_to_gapwp2-self.time_to_gapwp1)
        # print("Time_to_goal",self.time_to_goal)
        # print("Time_to_goal",self.timeStep_10Hz*self.steps,self)
        # print("gapWp2_to_goal",self.time_to_goal-self.time_to_gapwp2)
        # print("failure", self.trial-self.number_Goal_Reached)

        if  self.args.gap_avoidance:
            if not self.Boolian and self.dist_gapwp1 < 1:
                self.time_to_gapwp1=self.steps       
                self.Boolian =True

            if not self.Boolian2 and self.dist_gapwp2 < 1:
                self.time_to_gapwp2=self.steps       
                self.Boolian2 =True
                

            # print(self.gap_point_moving, self.gap_point1, self.gap_point2)

        # if self.args.gap_avoidance:
        #     if self.dist_gapwp1<1:
        #     self.move_goal_and_static_robot(self.pos[0], self.pos[1], self.yaw)

        #print("self.steps",self.steps)
        
        

        self.steps += 1

        self.endt = time.time()  # Record the end time after the simulation step
        self.timest = self.endt - self.st  # Calculate the time elapsed during the simulation step
        # print("Timestep:", self.timest/self.steps, "seconds",self.timeStep_10Hz)
        
        
        self.total_steps += 1
        self.total_reward += reward
        self.distance_to_goal =self.goal_reaching
        # print("ob_dic",self.ob_dict)
        return self.return_state(),reward,done,termination,self.ob_dict
        #print("total_reward",self.total_reward)
        #return np.array(self.robot1_bbox[0] +self.robot1_bbox[1] +self.robot1_bbox[2] +self.robot1_bbox[3] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3] + self.contacts + self.contacts2 + list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped]), reward, done, self.ob_dict
        # return np.array(list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped]), reward, done, self.ob_dict
        
        
        # motor_action(actions)
        # observation,reward,done=return_step(self)
        # return observation, reward, done, self.ob_dict

    def return_state(self):
        #zeros_array = list(np.zeros((4,)))
        self.Other_Robots_pos_list=[]
        self.Other_Robots_orn_list=[]
        self.Other_Robots_vx_list=[]
        self.Other_Robots_angular_vx_list=[]
        self.heading_error_other_robot=0
        

        for robot_pos_with_IDx in self.robots_pos_with_IDx:
            if str(robot_pos_with_IDx[0])!=str(self):
                self.heading_error_other_robot,_=self.calc_angle_error(robot_pos_with_IDx[1], self.pos, self.yaw)

                other_robot_egocentric_pos = self.world_to_robot(self.yaw, self.pos, robot_pos_with_IDx[1])

                self.Other_Robots_pos_list.append(other_robot_egocentric_pos)


        for robot_orn_with_IDx in self.robots_orn_with_IDx:
            if str(robot_orn_with_IDx[0])!=str(self):

                self.Other_Robots_orn_list.append(robot_orn_with_IDx[1])

        for robot_vx_with_IDx in self.robots_vx_with_IDx:
            if str(robot_vx_with_IDx[0])!=str(self):

                self.Other_Robots_vx_list.append(robot_vx_with_IDx[1])


        for robot_angular_vx_with_IDx in self.robots_angular_vx_with_IDx:
            if str(robot_angular_vx_with_IDx[0])!=str(self):

                self.Other_Robots_angular_vx_list.append(robot_angular_vx_with_IDx[1])
        # print("eject",self.Robots_pos_list,"whole",self.pos)
        # print("ENTIRE",self.robots_pos_with_IDx)
        #print(len(self.Other_Robots_pos_list),"robot_num",self.args.num_robots)
        # print(self,self.Other_Robots_pos_list,len(self.Other_Robots_pos_list),len([0]*1*(self.args.num_robots-1)))
        # print("a",self,self.Other_Robots_orn_list,len(self.Other_Robots_pos_list),len([0]*1*(self.args.num_robots-1)))
        # # print("b",self,self.Other_Robots_vx_list,len(self.Other_Robots_pos_list),len([0]*1*(self.args.num_robots-1)))
        # # print("c",self,self.Other_Robots_angular_vx_list,len(self.Other_Robots_pos_list),len([0]*1*(self.args.num_robots-1)))
        # print("self.heading_error_other_robot",self.heading_error_other_robot)

        #this part is needed to make equivalence. when 1st robot is called, he still has mismatched state. to fix that, we add empty list of equal number of state needed for multi-robot state number
        if self.args.num_robots==1:
            self.other_robots_positions=[]
            self.other_robots_orientation=[]
            self.other_robots_vx=[]
            self.other_robots_angular_vx=[]
        elif self.args.num_robots>1 and self.Other_Robots_pos_list==[]:
            self.other_robots_positions=[0]*2*(self.args.num_robots-1)
            self.other_robots_orientation=[0]*(self.args.num_robots-1)
            self.other_robots_vx=[0]*(self.args.num_robots-1)
            self.other_robots_angular_vx=[0]*(self.args.num_robots-1)
        elif self.args.num_robots>1:
            self.other_robots_positions=self.Other_Robots_pos_list[0]
            self.other_robots_orientation=self.Other_Robots_orn_list[0]
            self.other_robots_vx=self.Other_Robots_vx_list[0]
            self.other_robots_angular_vx=self.Other_Robots_angular_vx_list[0]

        if self.args.static_robots > 1:
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3])
        
        #Obstacle Avoidance Observations for Multi Robot
        elif self.args.obstacle_avoidance:    
            return np.array(self.wp_pos_robot + self.other_robots_positions +[self.roll, self.pitch, self.vx, self.yaw_vel]+ self.obs_pos_robot+[self.obs_corner1[0],self.obs_corner1[1]]+ [self.obs_corner2[0],self.obs_corner2[1]]+ [self.obs_corner3[0],self.obs_corner3[1]]+ [self.obs_corner4[0],self.obs_corner4[1]])
        #Obstacle Avoidance Observations for Single Robot
        # elif (self.args.obstacle_avoidance and len(self.Other_Robots_pos_list)!= len([0]*1*(self.args.num_robots-1))) or (self.args.obstacle_avoidance and self.args.num_robots==1):
        #     return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel] + [0]*2*(self.args.num_robots-1) + self.obs_pos_robot+[self.obs_corner1[0],self.obs_corner1[1]]+ [self.obs_corner2[0],self.obs_corner2[1]]+ [self.obs_corner3[0],self.obs_corner3[1]]+ [self.obs_corner4[0],self.obs_corner4[1]])    
        
        elif self.args.gap_avoidance and self.args.occupancy_map and self.args.use_perception and self.args.experiment_0:
            
            return np.array(self.wp_pos_robot +[self.vx, self.yaw_vel])
        
        elif self.args.gap_avoidance and self.args.occupancy_map and self.args.use_perception and self.args.experiment_1:
            
            return np.array(self.wp_pos_robot +[self.roll, self.pitch, self.vx, self.yaw_vel])
        
        elif self.args.gap_avoidance and self.args.occupancy_map and self.args.use_perception and self.args.experiment_2:
            
            return np.array(self.wp_pos_robot + self.other_robots_positions +[self.roll, self.pitch, self.vx, self.yaw_vel])
        
        elif self.args.gap_avoidance and self.args.occupancy_map and self.args.use_perception and self.args.experiment_3:
            # print(np.array(self.wp_pos_robot + [self.yaw] + self.other_robots_positions + self.other_robots_orientation+self.other_robots_vx+self.other_robots_angular_vx+[self.roll, self.pitch, self.vx, self.yaw_vel]))
            return np.array(self.wp_pos_robot + [self.yaw] + self.other_robots_positions + self.other_robots_orientation+self.other_robots_vx+self.other_robots_angular_vx+[self.roll, self.pitch, self.vx, self.yaw_vel])
        
        elif self.args.gap_avoidance and self.args.experiment_3:
            
            return np.array(self.wp_pos_robot + [self.yaw] + self.other_robots_positions + self.other_robots_orientation+self.other_robots_vx+self.other_robots_angular_vx+[self.roll, self.pitch, self.vx, self.yaw_vel]+  self.wall1_pos_robot + self.wall2_pos_robot+[self.wall1_corner1[0],self.wall1_corner1[1]]+ [self.wall1_corner2[0],self.wall1_corner2[1]]+ [self.wall1_corner3[0],self.wall1_corner3[1]]+ [self.wall1_corner4[0],self.wall1_corner4[1]]+[self.wall2_corner1[0],self.wall2_corner1[1]]+ [self.wall2_corner2[0],self.wall2_corner2[1]]+ [self.wall2_corner3[0],self.wall2_corner3[1]]+ [self.wall2_corner4[0],self.wall2_corner4[1]])

        elif self.args.gap_avoidance:
            
            return np.array(self.wp_pos_robot + self.other_robots_positions +[self.roll, self.pitch, self.vx, self.yaw_vel]+  self.wall1_pos_robot + self.wall2_pos_robot+[self.wall1_corner1[0],self.wall1_corner1[1]]+ [self.wall1_corner2[0],self.wall1_corner2[1]]+ [self.wall1_corner3[0],self.wall1_corner3[1]]+ [self.wall1_corner4[0],self.wall1_corner4[1]]+[self.wall2_corner1[0],self.wall2_corner1[1]]+ [self.wall2_corner2[0],self.wall2_corner2[1]]+ [self.wall2_corner3[0],self.wall2_corner3[1]]+ [self.wall2_corner4[0],self.wall2_corner4[1]])
        # elif self.args.gap_avoidance and len(self.Other_Robots_pos_list)== len([0]*1*(self.args.num_robots-1)) and not len(self.Other_Robots_pos_list)==0:
            
        #     return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+ self.Other_Robots_pos_list[0] + self.wall1_pos_robot + self.wall2_pos_robot+[self.wall1_corner1[0],self.wall1_corner1[1]]+ [self.wall1_corner2[0],self.wall1_corner2[1]]+ [self.wall1_corner3[0],self.wall1_corner3[1]]+ [self.wall1_corner4[0],self.wall1_corner4[1]]+[self.wall2_corner1[0],self.wall2_corner1[1]]+ [self.wall2_corner2[0],self.wall2_corner2[1]]+ [self.wall2_corner3[0],self.wall2_corner3[1]]+ [self.wall2_corner4[0],self.wall2_corner4[1]])

        # elif (self.args.gap_avoidance and len(self.Other_Robots_pos_list)!= len([0]*1*(self.args.num_robots-1))) or (self.args.gap_avoidance and self.args.num_robots==1):
            
        #     return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+[0]*2*(self.args.num_robots-1) + self.wall1_pos_robot + self.wall2_pos_robot+[self.wall1_corner1[0],self.wall1_corner1[1]]+ [self.wall1_corner2[0],self.wall1_corner2[1]]+ [self.wall1_corner3[0],self.wall1_corner3[1]]+ [self.wall1_corner4[0],self.wall1_corner4[1]]+[self.wall2_corner1[0],self.wall2_corner1[1]]+ [self.wall2_corner2[0],self.wall2_corner2[1]]+ [self.wall2_corner3[0],self.wall2_corner3[1]]+ [self.wall2_corner4[0],self.wall2_corner4[1]])
        # elif self.args.gap_avoidance and len(self.Other_Robots_pos_list)!= len([0]*2*(self.args.num_robots-1)):
            
        #     return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+[0]*2*(self.args.num_robots-1) + self.wall1_pos_robot + self.wall2_pos_robot+[self.wall1_corner1[0],self.wall1_corner1[1]]+ [self.wall1_corner2[0],self.wall1_corner2[1]]+ [self.wall1_corner3[0],self.wall1_corner3[1]]+ [self.wall1_corner4[0],self.wall1_corner4[1]]+[self.wall2_corner1[0],self.wall2_corner1[1]]+ [self.wall2_corner2[0],self.wall2_corner2[1]]+ [self.wall2_corner3[0],self.wall2_corner3[1]]+ [self.wall2_corner4[0],self.wall2_corner4[1]])
        elif len(self.Other_Robots_pos_list)== len([0]*1*(self.args.num_robots-1)) and not len(self.Other_Robots_pos_list)==0:
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+self.Other_Robots_pos_list) #+ zeros_array
        # elif self.args.gap_avoidance and self.args.insert_wall:

        elif len(self.Other_Robots_pos_list)!= len([0]*1*(self.args.num_robots-1)) or self.args.num_robots==1:
            #print(self.wp_pos_robot)
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+[0]*2*(self.args.num_robots-1)) #+ zeros_array

    # def get_reward_1(self):
    #     """
    #     Reward Function 1
    #     """
    #     #reward = 1.5*np.ex termination=Falsep(-2.5*max(0, self.target_speed - self.vx)**2)
    #     #done = False
    #     done=False
        
    #     dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
    #     #print(dist_to_goal)

    #     # if self.dist_to_robot2 < 2.0:                  #robot1 close to robot 2  distance < x
    #     # 	goal = np.exp(-0.5*self.dist_to_wp)
    #     # elif abs(self.heading_error) < 0.5:
    #     # 	goal = np.exp(-0.5*self.dist_to_wp)
    #     # else:	
    #     goal = 0
    #     if abs(self.heading_error) < 0.5:
    #         goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
    #     heading = 0.25*np.exp(-0.5*self.heading_error**2)
    #     #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
    #     neg = 0
    #     if self.vx < 0:
    #         neg = 0.25*self.vx 
    #     # if self.vx > 0 and self.heading_vx > 0:
    #         # goal = 0.5*np.clip(self.heading_vx, 0, 3)

    #     # goal = 1.5*np.exp(-10*(0.5 - self.heading_vx)**2)
    #     # goal = 1.5*np.exp(-10*(3.0 - self.heading_vx)**2)
    #     # neg = 0.25*self.vx if self.vx < 0 else 0
    #     # heading_obs = np.exp(-0.5*self.heading_error_obs**2)exper
    #     #print("goal", goal, "h", heading, "hO", heading_obs, "ng", neg)
    #     # reward = 1.0 * goal + 0.2 * heading #- 0.2 * heading_obs
    #     reward = goal + neg + heading
    #     # reward = goal + heading 
    #     #print("reward", reward)
        

    #     self.ep_reward_dict["Reward/goal"] += goal
    #     self.ep_reward_dict["Reward/neg"] += neg
    #     self.ep_reward_dict["Reward/heading"] += heading
    #     #self.ep_reward_dict["Reward/heading_obs"] += heading_obs
        
    #     #print(state_object[0])
    #     #print("prev",self.prev_dist_to_goal)
    #     #print(self.prev_dist_to_goal)
    #     #print((self.steps * self.timeStep_10Hz)+1)
    #     # TT= self.steps * self.timeStep_10Hz + 1
    #     # print(TT) # time travel per episode ( It is not travel time to goal. I want to stop the robot at the goal. So, I add time of whole episode)
        
        
        
        
    #     #print(dist_to_goal)
    #     #fixed_dist_goal=math.sqrt(((3 - self.state_goal[0]) ** 2 + (3 - self.state_goal[1]) ** 2))
    #     #print("dist_to_goal", dist_to_goal)
    #     #T= (fixed_dist_goal)*0.75 #Time to reach the goal where 0.75 is the velocity
        
    #     # reward = 0
    #     # if dist_to_goal < 0.5:
    #     #     reward = 100/TT

    #     #write me a reward function that define shortest possible distance in time

    #     #print(reward)
    #     #reward = self.prev_dist_to_goal - dist_to_goal
        
        
    #     distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
    #     #self.ep_reward_dict["Distance to Goal Improved"] += distance_improve
    #     #print(distance_improve)
    #     # print(reward)
    #     # if dist_to_goal < .2:
    #     #     reward = 1000/TT
    #     #print(reward)
    #     #print((self.steps * self.timeStep_10Hz)+1,"dist_to_goal", dist_to_goal,"time_to_goal",T, "reward", reward)
    #     #print("time",T)
    #     #reward = (max(self.prev_dist_to_goal - dist_to_goal, 0))/TT
    #     #print(reward)
    #     #print("difference_in_distance",self.prev_dist_to_goal - dist_to_goal)
        
    #     self.prev_dist_to_goal = dist_to_goal
    #     #print(dist_to_goal,self.prev_dist_to_goal)
    #     #print(self.pos)
        
    #     #if (self.pos[0] >= 4 or self.pos[0] <= -4 or self.pos[1] >= 4 or self.pos[1] <= -4):
    #         #done = True
    #     # Done by reaching goal
    #     #print("dist",dist_to_goal)
    #     #print("reward",reward)
        
    #     #print(self.contacts)


    #     #######################
    #     #uncomment this part if inlation radius is used

    #     if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
    #         done=True
    #         #print("MA Collision----------------")
    #     if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
    #         done=True
    #         print("Robot_hit_static_Robot",done)
    #     if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
    #         done=True
    #         #print("Hit_Obstacle-------Hit_Hit",done)
    #     if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
    #         done=True
    #         print("Hit_Gap_wall",done)
    #     ######################
        
    #     if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
    #         done=True
    #         #print("Hit_Wall/Contact",done)
    #     if self.tipped == True:
    #         done = True
    #         #print("Tipped",done)

        
    #     return reward, done, termination

    
    
    # #stop turning before moving
    # def get_reward_3(self):
    #     """
    #     Reward Function 3
    #     """
        termination=False
    #     done=False
        
    #     dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        
    #     goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
    #     heading = 0.25*np.exp(-0.5*self.heading_error**2)
    #     neg = 0
    #     if self.vx < 0:
    #         neg = 0.25*self.vx 
        
    #     reward = goal + neg + heading
        
        

    #     self.ep_reward_dict["Reward/goal"] += goal
    #     self.ep_reward_dict["Reward/neg"] += neg
    #     self.ep_reward_dict["Reward/heading"] += heading
        
        
    #     distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
    #     self.prev_dist_to_goal = dist_to_goal
        

    #     if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
    #         done=True
    #     if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
    #         done=True
    #         print("Robot_hit_static_Robot",done)
    #     if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
    #         done=True
    #     if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
    #         done=True
    #         print("Hit_Gap_wall",done)
        
            
    #     return reward, done, termination


    def get_reward_1(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        
        if abs(self.heading_error) < 0.5:
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
        

        collision=0
        MA_colision=0 

        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # print("Hit_GAP_WALL-------Hit_Hit",done)
            # done=True    
        

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
       
    def get_reward_2(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        
        if abs(self.heading_error) < 0.5:
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
        

        collision=0
        MA_colision=0 

        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            # collision= -10000
            # print("Hit_GAP_WALL-------Hit_Hit",done)
            done=True    
        

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    

    def get_reward_3(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        
        if abs(self.heading_error) < 0.5:
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
        

        collision=0
        MA_colision=0     
        

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_4(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))+(-5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_5(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-3*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))+(-3*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_6(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        
        if abs(self.heading_error) < 0.5:
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            # collision= -10000
            done=True
            # print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_7(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(1.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            # collision= -10000
            done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0 
        # print(self.actions)    
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_8(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -7*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -7*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))+(-1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            # collision= -10000
            done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True
        current_time = time.time() - self.start_time
        distance = 10 - dist_to_goal
        # print("TIME",current_time)
        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    #Real_reward--with reach 1000 and 1st collision
    def get_reward_9(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(1.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0 
        # print(self.actions)    
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    
    
    def get_reward_10(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        # print("observation_vx",self.vx,"observation_yvel",self.yaw_vel)
        # print("Spot_vx",self.vx,"Spot_yevl",self.yaw_vel)
        # if self.vx>1.2:
        #     print("titan_tham");exit()
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        
        if abs(self.heading_error) < 0.5:
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     # collision= -10000
        #     done=True
            # print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    

    def get_reward_11(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -7*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -7*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))+(-1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True
        current_time = time.time() - self.start_time
        distance = 10 - dist_to_goal
        # print("TIME",current_time)
        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    

    def get_reward_12(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))+(-1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # # print("TIME",current_time)
        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -5000
        #     done=True
        #     #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    

    def get_reward_13(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        # print("actions",self.actions_policy)
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -0.75*np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0

        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -0.75*np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        # print(self.steps/20 )
        # print(self.timeStep_10Hz )
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        # print("distance",distance)
        # print("dist_to_goal",dist_to_goal)
        # print("velocity",distance/current_time)
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     #collision= -10000
        #     print("Hit_-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     #done=True
        #     print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    

    def get_reward_14(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        # print("actions",self.actions_policy)
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -0.75*np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -0.75*np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0.25*np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0.25*np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     #done=True
        #     print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination

    def get_reward_15(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -0.75*np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -0.75*np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        # print(self.steps/20 )
        # print(self.timeStep_10Hz )
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        # print("distance",distance)
        # print("dist_to_goal",dist_to_goal)
        # print("velocity",distance/current_time)
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     #collision= -10000
        #     print("Hit_-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     #done=True
        #     print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_16(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal =0# -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal =0# -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0.25*np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0.25*np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        # print(self.steps/20 )
        # print(self.timeStep_10Hz )
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        # print("distance",distance)
        # print("dist_to_goal",dist_to_goal)
        # print("velocity",distance/current_time)
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     #collision= -10000
        #     print("Hit_-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     #done=True
        #     print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    



    def get_reward_17(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0.25*np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0.25*np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        # print(self.steps/20 )
        # print(self.timeStep_10Hz )
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        # print("distance",distance)
        # print("dist_to_goal",dist_to_goal)
        # print("velocity",distance/current_time)
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     #collision= -10000
        #     print("Hit_-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     #done=True
        #     print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_18(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0  

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and not self.turn_both:
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and self.turn_both:
        #     goal = np.exp(-0.5*(0.3 - self.heading_vx)**2) if self.vx < 0 else 0.0

            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                goal = np.exp(-0.5*(0.8 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     done=True
            #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    



    def get_reward_19(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0  

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -2*np.exp(-0.5*(0.3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -2*np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and self.turn_both:
        #     goal = np.exp(-0.5*(0.3 - self.heading_vx)**2) if self.vx < 0 else 0.0

            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                goal = np.exp(-0.5*(0.8 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        
        
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10000
            #print("Hit_GAP_WALL-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     done=True
            #print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_20(self):
        """
        Reward Function 2
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            reach =1000

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -7*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -7*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("goal",goal)
        # print(self.steps/20 )
        # print(self.timeStep_10Hz )
        # current_time = time.time() - self.start_time
        # distance = 10 - dist_to_goal
        # print("TIME",current_time)
        # print("distance",distance)
        # print("dist_to_goal",dist_to_goal)
        # print("velocity",distance/current_time)
        # if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
        #     collision= -10000
        #     done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     collision= -10000
            #done=True
            #print("Hit_GAP_WALL-------Hit_Hit",done)
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     #collision= -10000
        #     print("Hit_-------Hit_Hit",done)
            #done=True

        collision=0
        MA_colision=0     
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -5000
        #     #print("HIT_WALL")
        #     done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     #MA_colision= -5000
        #     #done=True
        #     print("MA Collision----------------")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True
            
        return reward, done, termination
    
    def get_reward_21(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1    

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -5*step_counter
            done=True


        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     collision= -10*step_counter
        #     #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    
    # def get_reward_sudocode(self):
       
    #     termination=False
        
        
    #     goal_proximity_reward=0
        
    #     heading_reward = 0.25*np.exp(-0.5*self.heading_error**2)
        
    #     forward_motion_incentive = 0
    #     if self.velocity < 0 and not virtual rays hit the other robot:
    #         forward_motion_incentive = 0.25*self.velocity
    #     elif virtual rays hit the other robot and self.velocity < 0:
    #         forward_motion_incentive=0
    #     elif both robot virtual rays hit robots each other and self.velocity < 0:    
    #         forward_motion_incentive = 0

    #     goal_completion_reward =0
    #     if self.dist_to_wp<1:
    #         goal_completion_reward =1000
        
        
    #     if any virtual rays hit the other robot:
    #         goal_proximity_reward = -np.exp(-0.5*(3 - self.heading_velocity)**2) if self.velocity > 0 else 0.0
    #     elif any virtual rays hit the other robot and the obstacles too:
    #         goal_proximity_reward = -np.exp(-0.5*(3 - self.heading_velocity)**2) if self.velocity > 0 else 0.0

    #     elif any virtual rays hit the wall1 but and not the other robot: 
    #         goal_proximity_reward = 0
    #         heading_reward = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
    #     elif any virtual rays hit the wall2 but and not the other robot:
    #         goal_proximity_reward = 0
    #         heading_reward = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        
    #     else:
    #         if abs(self.heading_error) < 0.5 and not any virtual rays hit the other robot:
    #             goal_proximity_reward = np.exp(-0.5*(1 - self.heading_velocity)**2) if self.vx > 0 else 0.0

        
    #     reward = goal_proximity_reward + heading_reward + forward_motion_incentive  + goal_completion_reward

            
    #     if robot tipped aboved a threshold angle == True:
    #         termination = True
            
    #     return reward, termination
    

    def get_reward_22(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        print("vx",self.vx,"yawvel",self.yaw_vel)
        # if self.vx>1.3:
        #     print("tham");exit()
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            # collision= -10*step_counter
            #print("HIT_WALL")
            done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_28(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     # MA_colision= -2*step_counter
        #     # print("NOT_DONE?")
        #     done=True


        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     # collision= -10*step_counter
        #     #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += step_counter
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_29(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            # print("NOT_DONE?")
            done=True


        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     # collision= -10*step_counter
        #     #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += step_counter
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination


    
    def get_reward_23(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -50
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_24(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -75
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_25(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -150
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_26(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            # collision= -150
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_27(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -1
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_2300(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        fluctuate=0
        if self.vx>1 or self.vx<-0.5 or self.yaw_vel <-1.5 or self.yaw_vel>1.5:
            fluctuate =-10
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -10
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision+fluctuate
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_2400(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        fluctuate=0
        if self.vx>1 or self.vx<-0.5 or self.yaw_vel <-1.5 or self.yaw_vel>1.5:
            fluctuate =-10

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -7
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision+fluctuate
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_2500(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000


        fluctuate=0
        if self.vx>1 or self.vx<-0.5 or self.yaw_vel <-1.5 or self.yaw_vel>1.5:
            fluctuate =-10

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -3
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision+fluctuate
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    
    def get_reward_255(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        # if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-0.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        
        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # collision= -5
            # print("HIT",self.vx)
            # print("COntacted")
            collision= -3
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination

    def get_reward_250(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("titan.vx",self.vx, "titan.yaw_vel",self.yaw_vel)
        # if self.vx>1.2:
        #     print("tham");exit()
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.k>0:
        #     # termination = True
        #     termination=True
        # print(self.k,self,done)

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        
        # print("Titan_vx",self.vx,"Titan_yevl",self.yaw_vel)
        # if self.vx>1:
        #     print("THAM");exit()
        speed_reward=1
        step_reward_for_speed=0.5
        if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
            #print("False")
            goal = np.exp(-step_reward_for_speed*(speed_reward - self.heading_vx)**2) if self.vx > 0 else 0.0

        # elif abs(self.heading_error) < 0.5 and (any(self.int_check_lines_vs_rbbox) or (np.array(self.contacts) == True).any()):
        #     goal = -np.exp(-5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # print("COntacted")
            # collision= -25*np.exp(-8*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            collision= -5
            done=True
        
        if self.tipped == True:
            collision= -10
            done = True
            # print("Tipping")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        

        if self.dist_to_wp<1:
            self.k=self.k+1
            

        if self.k>0:
            # termination = True
            termination=True
            
        return reward, done, termination
    

    def get_reward_260(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("titan.vx",self.vx, "titan.yaw_vel",self.yaw_vel)
        # if self.vx>1.2:
        #     print("tham");exit()
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.k>0:
        #     # termination = True
        #     termination=True
        # print(self.k,self,done)

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        
        # print("Titan_vx",self.vx,"Titan_yevl",self.yaw_vel)
        # if self.vx>1:
        #     print("THAM");exit()
        speed_reward=1
        step_reward_for_speed=0.5
        if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
            #print("False")
            goal = np.exp(-step_reward_for_speed*(speed_reward - self.heading_vx)**2) if self.vx > 0 else 0.0

        # elif abs(self.heading_error) < 0.5 and (any(self.int_check_lines_vs_rbbox) or (np.array(self.contacts) == True).any()):
        #     goal = -np.exp(-5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-5  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # print("COntacted")
            # collision= -25*np.exp(-8*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            collision= -10
            done=True
        
        if self.tipped == True:
            collision= -1
            done = True
            # print("Tipping")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_270(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("titan.vx",self.vx, "titan.yaw_vel",self.yaw_vel)
        # if self.vx>1.2:
        #     print("tham");exit()
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.k>0:
        #     # termination = True
        #     termination=True
        # print(self.k,self,done)

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        
        # print("Titan_vx",self.vx,"Titan_yevl",self.yaw_vel)
        # if self.vx>1:
        #     print("THAM");exit()
        speed_reward=1
        step_reward_for_speed=2.5
        if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
            #print("False")
            goal = np.exp(-step_reward_for_speed*(speed_reward - self.heading_vx)**2) if self.vx > 0 else 0.0

        # elif abs(self.heading_error) < 0.5 and (any(self.int_check_lines_vs_rbbox) or (np.array(self.contacts) == True).any()):
        #     goal = -np.exp(-5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # print("COntacted")
            # collision= -25*np.exp(-8*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            collision= -5
            done=True
        
        if self.tipped == True:
            collision= -5
            done = True
            # print("Tipping")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_280(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("titan.vx",self.vx, "titan.yaw_vel",self.yaw_vel)
        # if self.vx>1.2:
        #     print("tham");exit()
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.k>0:
        #     # termination = True
        #     termination=True
        # print(self.k,self,done)

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        
        # print("Titan_vx",self.vx,"Titan_yevl",self.yaw_vel)
        # if self.vx>1:
        #     print("THAM");exit()
        speed_reward=1
        step_reward_for_speed=2.5
        if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
            #print("False")
            goal = np.exp(-step_reward_for_speed*(speed_reward - self.heading_vx)**2) if self.vx > 0 else 0.0

        # elif abs(self.heading_error) < 0.5 and (any(self.int_check_lines_vs_rbbox) or (np.array(self.contacts) == True).any()):
        #     goal = -np.exp(-5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # print("COntacted")
            # collision= -25*np.exp(-8*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            collision= -7
            done=True
        
        if self.tipped == True:
            collision= -7
            done = True
            # print("Tipping")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    
    def get_reward_290(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("titan.vx",self.vx, "titan.yaw_vel",self.yaw_vel)
        # if self.vx>1.2:
        #     print("tham");exit()
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =3000

        # if self.k>0:
        #     # termination = True
        #     termination=True
        # print(self.k,self,done)

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        
        # print("Titan_vx",self.vx,"Titan_yevl",self.yaw_vel)
        # if self.vx>1:
        #     print("THAM");exit()
        speed_reward=1
        step_reward_for_speed=2.5
        if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
            #print("False")
            goal = np.exp(-step_reward_for_speed*(speed_reward - self.heading_vx)**2) if self.vx > 0 else 0.0

        # elif abs(self.heading_error) < 0.5 and (any(self.int_check_lines_vs_rbbox) or (np.array(self.contacts) == True).any()):
        #     goal = -np.exp(-5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # print("COntacted")
            # collision= -25*np.exp(-8*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            collision= -0.5
            done=True
        
        if self.tipped == True:
            collision= -0.5
            done = True
            # print("Tipping")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_300(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("titan.vx",self.vx, "titan.yaw_vel",self.yaw_vel)
        # if self.vx>1.2:
        #     print("tham");exit()
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        # if self.dist_to_wp<1:
        #     # self.k=self.k+1
        #     reach =3000

        # if self.k>0:
        #     # termination = True
        #     termination=True
        # print(self.k,self,done)

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        
        # print("Titan_vx",self.vx,"Titan_yevl",self.yaw_vel)
        # if self.vx>1:
        #     print("THAM");exit()
        speed_reward=1
        step_reward_for_speed=2.5
        if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
            #print("False")
            goal = np.exp(-step_reward_for_speed*(speed_reward - self.heading_vx)**2) if self.vx > 0 else 0.0

        # elif abs(self.heading_error) < 0.5 and (any(self.int_check_lines_vs_rbbox) or (np.array(self.contacts) == True).any()):
        #     goal = -np.exp(-5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # print("COntacted")
            # collision= -25*np.exp(-8*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            collision= -0.5
            done=True
        
        if self.tipped == True:
            collision= -0.5
            done = True
            # print("Tipping")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        

        # if self.dist_to_wp<1:
        #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    


    
    
    def get_reward_2888888(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("titan.vx",self.vx, "titan.yaw_vel",self.yaw_vel)
        # if self.vx>1.2:
        #     print("tham");exit()
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =20

        # if self.k>0:
        #     # termination = True
        #     termination=True
        # print(self.k,self,done)

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        
        # print("Titan_vx",self.vx,"Titan_yevl",self.yaw_vel)
        # if self.vx>1:
        #     print("THAM");exit()
        speed_reward=1
        step_reward_for_speed=-5
        if abs(self.heading_error) < 0.5 and not (np.array(self.contacts) == True).any():
            #print("False")
            goal = np.exp(-step_reward_for_speed*(speed_reward - self.heading_vx)**2) if self.vx > 0 else 0.0

        # elif abs(self.heading_error) < 0.5 and (any(self.int_check_lines_vs_rbbox) or (np.array(self.contacts) == True).any()):
        #     goal = -np.exp(-5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0  

        if self.intersection_r1_r:   #Multi RObot Collision
            # print("MA_hit")
            MA_colision=-10  
            done=True

        if ((np.array(self.contacts) == True).any()):  #Collision with Walls/anything
            # print("COntacted")
            # collision= -25*np.exp(-8*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
            collision= -0.4
            done=True
        
        if self.tipped == True:
            collision= -0.4
            done = True
            # print("Tipping")

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        
        
        ######################
        
        
            
        

        if self.dist_to_wp<1:
            self.k=self.k+1
            

        if self.k>0:
            # termination = True
            termination=True
            
        return reward, done, termination
    

    def get_reward_20007(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 70 and Reset wall collision with penalty 70 following reward 21
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox):
            neg = 0.25*self.vx
        elif any(self.int_check_lines_vs_rbbox) and self.vx < 0:
            neg=0
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.k>0:
        #     # termination = True
        #     termination=True

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
        # if self.k>0:
        #     done = True

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox): 
            goal = 0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-2.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0

        if self.intersection_r1_r:   #Multi RObot Collision
            MA_colision=-10    
            done=True

        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -1
            # #print("HIT_WALL")
            done=True

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     MA_colision= -150
        #     done=True

        # if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
        #     # collision= 100
        #     done=True
            # print("Hit_GAP_WALL-------Hit_Hit",done)
        #     print("MA Collision----------------")

        

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True


        if self.dist_to_wp<1:
            self.k=self.k+1
            

        if self.k>0:
            # termination = True
            termination=True
            
        return reward, done, termination

    def get_reward_28(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 150 and Reset wall collision with penaly 150 following reward 21
        """
        termination=False
        done=False
        # print("self.vx",self.vx, "self.yaw_vel",self.yaw_vel)
        

        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.k>0:
        #     # termination = True
        #     termination=True

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
            # print("self.yaw_vel",self.yaw_vel)
            # print("Falseeeeeeeeeeee")
        # if self.k>0:
        #     done = True
        # print(self.k,self,done)


        if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
            #print("False")
            goal = np.exp(-2.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0     
        # if ((np.array(self.contacts) == True).any() and self.vx>-0.3):  #Collision with Walls/anything
        #     collision= -20
        #     # print("HIT",self.vx)
        #     done=True

        # if self.intersection_r1_r:   #Multi RObot Collision
        #     MA_colision=-75 
        #     print("TRUE")   
        #     done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        # print("reward",reward)
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        
            # print("Robot_hit_other_Robot",done,self)
        # print("reward_after",reward)
        
        ######################
        
        
            
        if self.tipped == True:
            done = True


        if self.dist_to_wp<1:
            self.k=self.k+1
            

        if self.k>0:
            # termination = True
            termination=True
            
        return reward, done, termination
    

    def get_reward_20009(self):
        """
        Reward Function: Reset at Multi_robot Collision with Penalty 70 and Reset wall collision with penalty 70 following reward 21
        """
        termination=False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0 and not any(self.int_check_lines_vs_rbbox) and not (np.array(self.contacts) == True).any():
            neg = 0.25*self.vx
        elif (any(self.int_check_lines_vs_rbbox) and self.vx < 0) or ((np.array(self.contacts) == True).any() or self.vx < 0):
            neg=-0.1*self.vx
        elif self.turn_both and self.vx < 0:
            #print("TURN_BBBBBBBBBBBBTJH")
            neg = 0

        reach =0
        if self.dist_to_wp<1:
            # self.k=self.k+1
            reach =1000

        # if self.k>0:
        #     # termination = True
        #     termination=True

        # if self.vx>1 or self.vx<-0.5:
        #     reach =-50
        #     # print("self.vx",self.vx)
        #     # print("TRUEEEEEEEEEEEEEE")
        # if self.yaw_vel>1.5 or self.yaw_vel<-1.5:
        #     reach =-50
        # if self.k>0:
        #     done = True

        
           
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
        elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) ) :
            goal = -np.exp(-0.5*(3 - self.heading_vx)**2) if self.vx > 0 else 0.0
            #print("true")
            

            #heading = -3*0.25*np.exp(-0.5*self.heading_error_other_robot**2)

        # elif self.args.gap_avoidance and any(self.int_check_lines_vs_rbbox) and ((self.wall2_head or self.wall2_side1 or self.wall2_side2) or (self.wall1_head or self.wall1_side1 or self.wall1_side2) or ((self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2))):
        #     goal = 0
        #     heading = 0.25*np.exp(-0.5*self.heading_error_other_robot**2)
            #print("heading_MA",heading)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not any(self.int_check_lines_vs_rbbox): 
            goal = 0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2) and not (self.wall1_head or self.wall1_side1 or self.wall1_side2) and not any(self.int_check_lines_vs_rbbox):
            goal = 0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        # elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2) and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
        #     goal = np.exp(-0.5*(0.5 - self.heading_vx)**2) if self.vx > 0 else 0.0
            # heading = (-1*0.25*np.exp(-0.5*self.heading_error_to_wall1**2))-(1*0.25*np.exp(-0.5*self.heading_error_to_wall2**2))
        else:
            if abs(self.heading_error) < 0.5 and not any(self.int_check_lines_vs_rbbox):
                #print("False")
                goal = np.exp(-2.5*(1 - self.heading_vx)**2) if self.vx > 0 else 0.0
         

        collision=0
        MA_colision=0     
        if self.intersection_r1_r:   #Multi RObot Collision
            # MA_colision=-25    
            done=True

        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -1
            # #print("HIT_WALL")
            done=True

        reward = goal + neg + heading +reach+collision+MA_colision
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        if self.tipped == True:
            done = True

        if self.dist_to_wp<1:
            self.k=self.k+1
            

        if self.k>0:
            # termination = True
            termination=True
            
        return reward, done, termination

    
    def get_reward_30(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.1*step_counter
            #print("HIT_WALL")
            # done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += step_counter
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    
    def get_reward_31(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        # if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
        #     # MA_colision= -2*step_counter
        #     # print("Multi-Robot Collision")
        #     done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.2*step_counter
            # print("HIT Contact")
            # done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += step_counter
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    
    def get_reward_32(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.3*step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += step_counter
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        # print("GOALREWW",self.ep_reward_dict)
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_33(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            # collision= -0.8*step_counter
            collision= -10
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination


    def get_reward_34(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.5*step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    
    def get_reward_35(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.6*step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    
    def get_reward_36(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.7*step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination

    def get_reward_37(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.8*step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_38(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.9*step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_39(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += step_counter
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        # if self.k>0:
        #     # termination = True
        #     termination=True
            
        return reward, done, termination
    

    def get_reward_40(self):
        """
        Step Reward
        """
        termination=False
        done=False
        # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
        # print(self.heading_error_other_robot,nege)
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        goal=0
        neg=0
        heading=0


        
        # if self.k>0:
        #     termination = True
        # print(self.k)
        
           
        
        step_counter=0

        
        collision=0
        MA_colision=0  

        reach =0

        
        if self.dist_to_wp<1:
            self.k=self.k+1
            reach =1000   

        if self.steps>0 and not self.k>0:
            step_counter=step_counter+1
        elif self.k>0:
            step_counter=step_counter-1

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            # MA_colision= -2*step_counter
            done=True


        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            collision= -0.1*step_counter
            #print("HIT_WALL")
        #     done=True

        
            # print("MA Collision----------------")
        # print("self.steps",self.steps,step_counter)
        reward = reach+collision+MA_colision-step_counter
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        self.ep_reward_dict["Reward/MA_colision"] += MA_colision
        self.ep_reward_dict["Reward/collision"] += collision
        self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        
        # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
        #     done=True
        #     print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        
            
        # if self.tipped == True:
        #     done = True
        
        # # if self.dist_to_wp<1:
        # #     self.k=self.k+1
            

        if self.k>0:
            # termination = True
            termination=True
            
        return reward, done, termination
    

    # def get_reward_35(self):
    #     """
    #     Step Reward
    #     """
    #     termination=False
    #     done=False
    #     # nege = -5*0.25*np.exp(-0.5*self.heading_error_other_robot**2)
    #     # print(self.heading_error_other_robot,nege)
        
    #     dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
    #     goal=0
    #     neg=0
    #     heading=0


        
    #     # if self.k>0:
    #     #     termination = True
    #     # print(self.k)
        
           
        
    #     step_counter=0

        
    #     collision=0
    #     MA_colision=0  

    #     reach =0

        
    #     if self.dist_to_wp<1:
    #         self.k=self.k+1
    #         reach =1000   

    #     if self.steps>0 and not self.k>0:
    #         step_counter=step_counter+1
    #     elif self.k>0:
    #         step_counter=step_counter-1

    #     if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
    #         # MA_colision= -2*step_counter
    #         done=True


    #     if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
    #         collision= -0.8*step_counter
    #         #print("HIT_WALL")
    #     #     done=True

        
    #         # print("MA Collision----------------")
    #     # print("self.steps",self.steps,step_counter)
    #     reward = reach+collision+MA_colision-step_counter
        
        

    #     self.ep_reward_dict["Reward/goal"] += goal
    #     self.ep_reward_dict["Reward/neg"] += neg
    #     self.ep_reward_dict["Reward/heading"] += heading
    #     self.ep_reward_dict["Reward/MA_colision"] += MA_colision
    #     self.ep_reward_dict["Reward/collision"] += collision
    #     self.ep_reward_dict["Reward/reach"] += reach
        
        
        
        
    #     distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
    #     self.prev_dist_to_goal = dist_to_goal
        

        
    #     # if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
    #     #     done=True
    #     #     print("Robot_hit_static_Robot",done)
        
        
    #     ######################
        
        
            
    #     # if self.tipped == True:
    #     #     done = True
        
    #     # # if self.dist_to_wp<1:
    #     # #     self.k=self.k+1
            

    #     # if self.k>0:
    #     #     # termination = True
    #     #     termination=True
            
    #     return reward, done, termination


    def get_observation(self):
        # print("BOOT",self.exp_actions)
        #self.opposite_angle += 180
        #print(self.Goals_pos)
        self.body_xyz, orn = p.getBasePositionAndOrientation(self.Id)
        self.pos = self.body_xyz
        self.Goal_pos,Goal_orn = p.getBasePositionAndOrientation(self.Goal)
        #print(self.Goal_pos)
        

        if self.args.static_robots > 1 and self.args.insert_robot2:
            self.body_xyz2, orn2 = p.getBasePositionAndOrientation(self.Id2)
            self.pos2 = self.body_xyz2
            self.orn2 = list(orn2)
            self.qx2, self.qy2, self.qz2, self.qw2 = self.orn2
            self.roll2, self.pitch2, self.yaw2 = p.getEulerFromQuaternion(self.orn2)
            self.body_vxyz2, self.base_rot_vel2 = p.getBaseVelocity(self.Id2)

            self.roll_vel2 = self.base_rot_vel2[0]
            self.pitch_vel2 = self.base_rot_vel2[1]
            self.yaw_vel2 = self.base_rot_vel2[2]

        #print("pos_euler",self.pos)
        #print("self.body_xyz",self.body_xyz)
        #print("posx", self.pos[0],"posy", self.pos[1],"posz", self.pos[2])
        self.orn = list(orn)
        self.qx, self.qy, self.qz, self.qw = self.orn
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
        #print("orn",self.orn,"yaw",self.yaw)
        # print("self.yaw",self.yaw)
        self.body_vxyz, self.base_rot_vel = p.getBaseVelocity(self.Id)
        #print(type(self.body_xyz))
        #print(self.body_xyz[2])
        #print(self.pos)
        # k=[self.body_xyz[0]+0.7,1.5*self.body_xyz[1],self.body_xyz[2]]
        # l=[self.body_xyz[0]-0.7,1.5*self.body_xyz[1],self.body_xyz[2]]
        # m=[0,0,0]
        # n=30
        # p.addUserDebugLine(k,l,m,n,.2)
        self.roll_vel = self.base_rot_vel[0]
        self.pitch_vel = self.base_rot_vel[1]
        self.yaw_vel = self.base_rot_vel[2]
        # print("self.body_vxyz",self.body_vxyz,"self.base_rot_vel", self.base_rot_vel)



        #dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        #print(dist_to_goal)
        rot_speed = np.array(
        [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
            [np.sin(-self.yaw), np.cos(-self.yaw), 0],
            [		0,			 0, 1]]
        )

        self.contacts = []
        self.contacts2 = []
        for contact in self.contact_dict:
            self.contacts.append(len(p.getContactPoints(self.Id, -1, self.contact_dict[contact], -1))>0)
            if self.args.static_robots > 1 and self.args.insert_robot2:
                self.contacts2.append(len(p.getContactPoints(self.Id2, -1, self.contact_dict[contact], -1))>0)
            #self.contacts.append(len(p.getContactPoints(self.Id, self.Id2, self.contact_dict[contact], -1))>0)
            #self.contacts.append(len(p.getContactPoints(self.Id2, -1, self.contact_dict[contact], -1))>0)
        #print(self.contacts, self.contacts2)
        self.vx, self.vy, self.vz = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        
        

        if self.args.static_robots > 1 and self.args.insert_robot2:
            rot_speed2 = np.array(
            [[np.cos(-self.yaw2), -np.sin(-self.yaw2), 0],
                [np.sin(-self.yaw2), np.cos(-self.yaw2), 0],
                [		0,			 0, 1]]
            )
            self.vx2, self.vy2, self.vz2 = np.dot(rot_speed2, (self.body_vxyz2[0],self.body_vxyz2[1],self.body_vxyz2[2]))
        
        if abs(self.orn[0]) > 0.2 or abs(self.orn[1]) > 0.2:
            self.tipped = True
        else:
            self.tipped = False

        #print(self.body_vxyz[0]+self.body_vxyz[1])
        
        
        

        #Between Goal and Robot 1
        self.wp_pos_robot = self.world_to_robot(self.yaw, self.pos, self.state_goal)
        # print(self.wp_pos_robot)
        #print("waypoint_pos", self.wp_pos_robot)
        self.heading_error, self.target_angle = self.calc_angle_error(self.state_goal, self.pos, self.yaw)
        #print("heading_error", self.heading_error)
        self.dist_to_wp = math.sqrt(self.wp_pos_robot[0]**2 + self.wp_pos_robot[1]**2)
        # print("distanc-to_wp", self.dist_to_wp)

        rot_speed = np.array(
        [[np.cos(-self.target_angle), -np.sin(-self.target_angle), 0],
            [np.sin(-self.target_angle), np.cos(-self.target_angle), 0],
            [		0,			 0, 1]]
        )
        self.heading_vx, _, _ = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        #print("self.heading_vx",self.heading_vx)

        
        ########################
        #Do not use this part if you already used it in reset
        #Uncomment this part if you want to use dynamic inflation radius

        # m= 0.075
        # # m= 0.075+((abs(self.body_vxyz[0])+abs(self.body_vxyz[1]))*0.05)#0.075 #value of inflation radius
        
        # ########################
        #self.intersection = False
        # 	# #This part is for generating bounding box around any object except robots
        #self.square_bbox=self.bbox_generator(self.square, radius=2, height=0.5, lineId=[-1]*4)
        # if str(self)==str(self):
        #     print("True")
        # print(str(self));exit()
        # print(len(self.robots_pos_with_IDx))
        # print("g",len(self.robots_bbox))
        textureId = -1
        
        self.robot1_bbox=self.bbox_generator_titan1(0.075,self.pos,self.orn,self.lineId1) #0.075
        self.robot1_bbox.append(self.robot1_bbox[0])
        #self.intersection_r1_r1,_= self.intersection_check(self.robot1_bbox,self.robot1_bbox)
        # To set robot collision with obstacle
        for robot_bbox in self.robots_bbox:
            #print("k",robot_bbox,"whole",self.robots_bbox)
            if str(robot_bbox[0])==str(self):
                #print(str(robot_bbox[0]),str(self))
                self.intersection_r1_r=False
            elif str(robot_bbox[0]) != str(self):
                self.intersection_r1_r,_= self.intersection_check(self.robot1_bbox,robot_bbox[1])
                #print(num,robot_bbox[0]);exit()

                self.intersection_hline_rbbox,_= self.intersection_check(self.head_line_MA,robot_bbox[1])
                self.intersection_s1line_rbbox,_= self.intersection_check(self.side_line1g_MA,robot_bbox[1])
                self.intersection_s2line_rbbox,_= self.intersection_check(self.side_line2g_MA,robot_bbox[1])
                self.int_check_lines_vs_rbbox=[self.intersection_hline_rbbox,self.intersection_s1line_rbbox,self.intersection_s2line_rbbox]
                if self.intersection_r1_r:
                    break
            # else:
            #     self.intersection_r1_r=True
                

        #check intersection between robot1 rays to robot 2 bbox
        # if str(robot_bbox[0]) != str(self):
                #self.robot1_near_robot2=False
                
        
            


        
        if self.args.obstacle_avoidance or self.args.gap_avoidance:
            
            #print(self.robot1_bbox[0][1],self.robot1_bbox[0][2])

            # self.robot100_bbox=self.bbox_generator_titan2(0.075,self.pos,self.orn,self.lineId1bonus)
            # #self.robot100_bbox.append(self.robot100_bbox)
            # print(self.robot100_bbox)
            
            # Creating green safe bounding box around robot 1
            self.robot1_safe_box=self.bbox_generator_titan(0.8,self.pos,self.orn,self.lineId12, [.29,.45,.27])
            self.robot1_safe_box.append(self.robot1_safe_box[0])
   
            #drawing imaginary line from the heading corners of safe bbox to the goal
            self.corner1_points=(self.robot1_safe_box[0][0], self.robot1_safe_box[0][1], 0), (self.state_goal[0], self.state_goal[1], 0)
            self.corner2_points=(self.robot1_safe_box[1][0], self.robot1_safe_box[1][1], 0), (self.state_goal[0], self.state_goal[1], 0)
    
            
        
        if self.args.gap_avoidance:
            #generating gap
            
            # print(self.line_orn)
            # print(self.orn)

            if not self.args.insert_wall:

                self.gap=self.gap_generator(width=self.max_gap_among_all_robots_individual_gap_width, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = 20,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)

            #self.gap=self.gap_generator(width=self.max_gap_among_all_robots_individual_gap_width, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = 20,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)
            
            #self.gap=self.gap_generator(width=self.gap_width, depth=self.tunnel_depth,height=0.015,pos=self.pos2,wall_length = 20,goal_pos=self.state_goal,lineId=self.lineIdWall,lineIdgap=self.lineIdgap,lineIdA=self.lineIdA,lineIdB=self.lineIdB)
            #print(self.pos2,"LL",self.mid_point_of_goals,"MM",self.Goals_pos);exit()
            # self.gap=self.gap_generator(width=self.gap_width, depth=self.tunnel_depth,height=0.015,pos=self.pos2,wall_length = 20,goal_pos=self.mid_point_of_goals,lineId=self.lineIdWall,lineIdgap=self.lineIdgap,lineIdA=self.lineIdA,lineIdB=self.lineIdB)
            #self.gap_point1,self.gap_point2=self.gap[2],self.gap[3]
            
            # lineIdgap_F=p.addUserDebugLine(self.gap_point1, self.gap_point2, lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=self.lineId_wp1_wp2)
            
            

            #Measuring Heading error to different way points
            self.heading_error_gapwp1, _ = self.calc_angle_error(self.gap_point1, self.pos, self.yaw)
            self.heading_error_gapwp2, _ = self.calc_angle_error(self.gap_point2, self.pos, self.yaw)
            
            #Distance to waypoints:
            self.dist_gapwp1=self.distance(self.pos,self.gap_point1)
            self.dist_gapwp2=self.distance(self.pos,self.gap_point2)

            
            #self.gap_point_moving = self.gap[2]
            self.dist_gapwp_mv=self.distance(self.pos,self.gap_point1)
            # TT1= self.steps * self.timeStep_10Hz + 1
            # T=False
            # time=None
            # if self.dist_gapwp1<1:
            #     time=TT1
            #     T=time==TT1
                #T = True
            

            
            




            if self.args.num_robots>1 and self.args.MA_bootstrap:
                if self.dist_gapwp1<2:
                    # self.time_to_wp1=self.steps
                    self.gapwp1_reach=True#self.gapwp1_reach + 1
                # self.time_to_wp2=0
                if self.dist_gapwp2<2:
                        # self.time_to_wp2=self.steps
                        self.gapwp2_reach=True#self.gapwp2_reach + 1

            if self.args.num_robots>1 and self.args.MA_bootstrap_extreme:
                if self.dist_gapwp1<0.8:
                    # self.time_to_wp1=self.steps
                    self.gapwp1_reach=True#self.gapwp1_reach + 1
                # self.time_to_wp2=0
                if self.dist_gapwp2<0.8:
                        # self.time_to_wp2=self.steps
                        self.gapwp2_reach=True#self.gapwp2_reach + 1

            elif self.args.num_robots>1 and self.args.regular_bootstrap:
                if self.dist_gapwp1<3:
                    # self.time_to_wp1=self.steps
                    self.gapwp1_reach=True#self.gapwp1_reach + 1
                # self.time_to_wp2=0
                if self.dist_gapwp2<5:
                        # self.time_to_wp2=self.steps
                        self.gapwp2_reach=True#self.gapwp2_reach + 1

            
            else:
                if self.dist_gapwp1<0.5:
                        # self.time_to_wp1=self.steps
                        self.gapwp1_reach=True#self.gapwp1_reach + 1
                # self.time_to_wp2=0
                if self.dist_gapwp2<0.5:
                        # self.time_to_wp2=self.steps
                        self.gapwp2_reach=True#self.gapwp2_reach + 1

            # print("self.time_to_wp1",self.time_to_wp1,"self.time_to_wp2",self.time_to_wp2)
            # To set robot collision with gap walls
            self.intersection_r1_gapwall1,_= self.intersection_check(self.robot1_bbox,self.gap[0])
            self.intersection_r1_gapwall2,_= self.intersection_check(self.robot1_bbox,self.gap[1])

            

            # check the intersection with middle line and gap walls
            self.line1_points=(self.pos[0], self.pos[1], 0), (self.state_goal[0], self.state_goal[1], 0)
            self.intersection_line_gap_wall1,_= self.intersection_check(self.line1_points,self.gap[0])
            self.intersection_line_gap_wall2,_= self.intersection_check(self.line1_points,self.gap[1])
   
               # check the intersection with heading corner lines and gap walls
            
            
            self.intersection_headingcorner1_gap_wall1,_= self.intersection_check(self.corner1_points,self.gap[0])
            self.intersection_headingcorner1_gap_wall2,_= self.intersection_check(self.corner1_points,self.gap[1])
            
            self.intersection_headingcorner2_gap_wall1,_= self.intersection_check(self.corner2_points,self.gap[0])
            self.intersection_headingcorner2_gap_wall2,_= self.intersection_check(self.corner2_points,self.gap[1])
            #----------------------------
            
            


            #Rays for MA Collision Avoidance

            self.heading_line_end_MA=self.find_position_B(self.pos,distance_d=self.args.detect_distance,angle_degrees=math.degrees(self.yaw))
            self.head_line_MA=(self.pos[0], self.pos[1], 0.34), (self.heading_line_end_MA[0], self.heading_line_end_MA[1], 0.34)

            self.side_line1_endg_MA=self.find_position_B(self.robot1_safe_box[0],distance_d=0,angle_degrees=math.degrees(self.yaw))
            self.side_line2_endg_MA=self.find_position_B(self.robot1_safe_box[1],distance_d=0,angle_degrees=math.degrees(self.yaw))

            self.side_line1g_MA=self.robot1_bbox[3], (self.side_line2_endg_MA[0], self.side_line2_endg_MA[1], 0.34)

            self.side_line2g_MA=self.robot1_bbox[2], (self.side_line1_endg_MA[0], self.side_line1_endg_MA[1], 0.34)
            

            if self.args.ray_wall_type==0:
                #same rays to Wall and to MA rays
                #Generating Head line and Side Lines
                self.heading_line_end=self.find_position_B(self.pos,distance_d=self.args.detect_distance,angle_degrees=math.degrees(self.yaw))
                self.head_line=(self.pos[0], self.pos[1], 0.34), (self.heading_line_end[0], self.heading_line_end[1], 0.34) 
                self.side_line1_endg=self.find_position_B(self.robot1_safe_box[0],distance_d=0,angle_degrees=math.degrees(self.yaw))
                self.side_line2_endg=self.find_position_B(self.robot1_safe_box[1],distance_d=0,angle_degrees=math.degrees(self.yaw))

                self.side_line1g=self.robot1_bbox[3], (self.side_line2_endg[0], self.side_line2_endg[1], 0.34)

                self.side_line2g=self.robot1_bbox[2], (self.side_line1_endg[0], self.side_line1_endg[1], 0.34)

            elif self.args.ray_wall_type==1: 
                #Different rays to Wall and to MA rays
                #Generating Head line and Side Lines
                self.heading_line_end=self.find_position_B(self.pos,distance_d=self.args.detect_distance,angle_degrees=math.degrees(self.yaw))
                self.head_line=(self.pos[0], self.pos[1], 0.34), (self.heading_line_end[0], self.heading_line_end[1], 0.34)
                self.side_line1_endg=self.find_position_B(self.robot1_bbox[0],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))
                self.side_line2_endg=self.find_position_B(self.robot1_bbox[1],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))

                self.side_line1g=self.robot1_bbox[0], (self.side_line2_endg[0], self.side_line2_endg[1], 0.34)

                self.side_line2g=self.robot1_bbox[1], (self.side_line1_endg[0], self.side_line1_endg[1], 0.34)
            
            
            
            if self.args.debug:
                # self.intersection_s2line_rbbox
                #self.side_line1g_MA
                self.lineId=p.addUserDebugLine((self.pos[0], self.pos[1], 0.34), (self.heading_line_end[0], self.heading_line_end[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=1, replaceItemUniqueId=self.lineId_heading)

                # self.lineId_s1=p.addUserDebugLine((self.robot1_bbox[3][0], self.robot1_bbox[3][1], 0.34), (self.side_line1_endg[0], self.side_line1_endg[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=1, replaceItemUniqueId=self.lineId_side2)

                self.lineId_s2=p.addUserDebugLine((self.robot1_bbox[2][0], self.robot1_bbox[2][1], 0.34), (self.side_line2_endg[0], self.side_line2_endg[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=1, replaceItemUniqueId=self.lineId_side1)

                self.lineId_MA=p.addUserDebugLine((self.pos[0], self.pos[1], 0.34), (self.heading_line_end_MA[0], self.heading_line_end_MA[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=1, replaceItemUniqueId=self.lineId_heading_MA)

                # self.lineId_s1_MA=p.addUserDebugLine((self.robot1_bbox[3][0], self.robot1_bbox[3][1], 0.34), (self.side_line1_endg_MA[0], self.side_line1_endg_MA[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=1, replaceItemUniqueId=self.lineId_side2_MA)

                self.lineId_s2_MA=p.addUserDebugLine((self.robot1_bbox[2][0], self.robot1_bbox[2][1], 0.34), (self.side_line2_endg_MA[0], self.side_line2_endg_MA[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=1, replaceItemUniqueId=self.lineId_side1_MA)

            
                
            
            #Check head line ray with WALLs
            self.wall1_head,_=self.intersection_check(self.head_line, self.gap[0])
            self.wall2_head,_=self.intersection_check(self.head_line, self.gap[1])
            #print(self.obs_check)

            #check the intersection between 2 heading corner lines with obstacle

            self.wall1_side1,_=self.intersection_check(self.side_line1g,self.gap[0])
            self.wall2_side1,_=self.intersection_check(self.side_line1g,self.gap[1])
            
            self.wall1_side2,_=self.intersection_check(self.side_line2g,self.gap[0])
            self.wall2_side2,_=self.intersection_check(self.side_line2g,self.gap[1])
            
            

            

        if self.args.obstacle_avoidance:
            
            #generating obstacle
            self.square_bbox=self.bbox_generator_box(0.35,0.011,self.pos2,self.orn2,self.lineId_box1)
            self.square_bbox.append(self.square_bbox[0])
            # d1=self.distance(self.square_bbox[0],self.square_bbox[1])
            # d2=self.distance(self.square_bbox[1],self.square_bbox[2])
            # print(d1,d2)

            #Generating Heading Mid line
            self.heading_line_end=self.find_position_B(self.pos,distance_d=self.args.detect_distance,angle_degrees=math.degrees(self.yaw))
            self.head_line=(self.pos[0], self.pos[1], 0.34), (self.heading_line_end[0], self.heading_line_end[1], 0.34)

            self.side_line1_end=self.find_position_B(self.robot1_safe_box[0],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))
            self.side_line2_end=self.find_position_B(self.robot1_safe_box[1],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))

            self.side_line1=self.robot1_safe_box[0], (self.side_line2_end[0], self.side_line2_end[1], 0.34)

            self.side_line2=self.robot1_safe_box[1], (self.side_line1_end[0], self.side_line1_end[1], 0.34)
        

            #detect distance lines
            #pDrawing Heading Mid Line
            #if self.args.debug:
            # self.lineId=p.addUserDebugLine((self.pos[0], self.pos[1], 0.34), (self.heading_line_end[0], self.heading_line_end[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.06, replaceItemUniqueId=self.lineId_heading)
            # self.lineId=p.addUserDebugLine((self.robot1_safe_box[0][0], self.robot1_safe_box[0][1], 0.34), (self.side_line2_end[0], self.side_line2_end[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.06, replaceItemUniqueId=self.lineId_side1)
            # self.lineId=p.addUserDebugLine((self.robot1_safe_box[1][0], self.robot1_safe_box[1][1], 0.34), (self.side_line1_end[0], self.side_line1_end[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.06, replaceItemUniqueId=self.lineId_side2)
    

            
            

            # To set robot collision with obstacle
            for obstacle in self.obstacles:
                self.intersection_r1_box,_= self.intersection_check(self.robot1_bbox,obstacle)
                if self.intersection_r1_box:
                    break
   
   
            # check the intersection with heading corner lines of self bbox and the obstacle
            
            self.intersection_corner1_square,_= self.intersection_check(self.corner1_points,self.square_bbox)
            self.intersection_corner2_square,_= self.intersection_check(self.corner2_points,self.square_bbox)
            
            # check the intersection with middle line and obstacle
            self.line1_points=(self.pos[0], self.pos[1], 0), (self.state_goal[0], self.state_goal[1], 0)
            self.intersection_line_square,_= self.intersection_check(self.line1_points,self.square_bbox)
            
            #check the intersection with Head Line and obstacle 

            self.obs_check,_=self.intersection_check(self.head_line, self.square_bbox)
            #print(self.obs_check)

            #check the intersection between 2 heading corner lines with obstacle

            self.obs_check_2,_=self.intersection_check(self.side_line1,self.square_bbox)
            self.obs_check_3,_=self.intersection_check(self.side_line2,self.square_bbox)

            self.goal_dist=self.distance(self.pos,self.state_goal)
            #This is to make sure that keep taking decision after obs_check = True, not only just while obs_check = True
            if self.obs_check or self.obs_check_2 or self.obs_check_3:
                self.h =self.h+1
            elif self.goal_dist<1:
                self.h=0
            #print(self.h)

            
            
            # This part is hard part that ensure to freeze the moving robot position to get the position on exact moment of heading ray hitting the obstacle. Not changing the position after robot move
            if self.h == 1:  #this is the moment when heading rays hit obstacle
                hit_pos, hit_orn= p.getBasePositionAndOrientation(self.Id)
                self.poshit_x,self.poshit_y,self.poshit_z, self.ornhit_a,self.ornhit_b,self.ornhit_c,self.ornhit_d=hit_pos[0],hit_pos[1],hit_pos[2],hit_orn[0],hit_orn[1],hit_orn[2],hit_orn[3]

            if self.poshit_x is None:
                self.poshit_x= 0
            if self.poshit_y is None:
                self.poshit_y=0
            if self.poshit_z is None:
                self.poshit_z=0


            if self.ornhit_a is None:
                self.ornhit_a= 0
            if self.ornhit_b is None:
                self.ornhit_b=0
            if self.ornhit_c is None:
                self.ornhit_c=0
            if self.ornhit_d is None:
                self.ornhit_d=0

            

            self.intersection_wp2G_obs=None
            self.intersection_wp3G_obs=None
            self.dist_R12G = None
            self.dist_R13G = None
            self.dist_R124G = None
            self.dist_R134G = None


            if self.goal_dist <1:
                self.wp1_reach=0
                self.wp2_reach=0
                self.wp3_reach=0
                self.wp4_reach=0
                #self.goal_success.append(True)
            



            #Counting from when the heading rays hit the obstacle
            if self.h>0:
                #print("MOVE MOVE MOVE",self.poshit_x,self.poshit_y,self.poshit_z,"h_value",self.h,"ORN_HITS",self.ornhit_a,self.ornhit_b ,self.ornhit_c ,self.ornhit_d )
                self.poshit=(self.poshit_x,self.poshit_y,self.poshit_z)
                self.ornhit=(self.ornhit_a,self.ornhit_b ,self.ornhit_c ,self.ornhit_d)
                #generating safety bounding box aroung obstacle box
                self.safety_square_bbox=self.bbox_generator_box(2,0.011,self.pos2,self.orn2,self.lineId_box1_safety)
                self.safety_square_bbox.append(self.safety_square_bbox[0])
                #print(self.safety_square_bbox)

                #generating static bounding box around robot when hit
                self.robot1_static_box=self.bbox_generator_titan(0.8,self.poshit,self.ornhit,self.lineId12_static, [.1,.25,.9])
                self.robot1_static_box.append(self.robot1_static_box[0])

                #Generating waypoints based on closest point finding among the corners of the obstacle safety box from the robot static bbox heading points
                #self.corner_robot1 = [(tuple(self.robot1_static_box[0])),(tuple(self.robot1_static_box[1])),(tuple(self.robot1_static_box[2])),(tuple(self.robot1_static_box[3]))]
                self.corner_square_bigbox= [(tuple(self.safety_square_bbox[0])),(tuple(self.safety_square_bbox[1])),(tuple(self.safety_square_bbox[2])),(tuple(self.safety_square_bbox[3]))]
                closest_coordinates= self.find_closest_coordinates(self.poshit , self.corner_square_bigbox)

                self.cp=[]
                self.cd=[]
                for i, (min_dist, closest_point) in enumerate(closest_coordinates, start=1):
                    self.cp.append(closest_point)
                    self.cd.append(min_dist)
                self.way_point1,self.way_point2,self.way_point3,self.way_point4=self.cp
                D1,D2,D3,D4=self.cd
                # print(D1,D2,D3,D4)
                # print("CHILLLLLAAAAAAAAAAA",self.way_point1,self.way_point2,self.way_point3,self.way_point4)

                wall_dir= "Wall_URDF/"

                # self.Goal1 = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=self.way_point1)
                # self.Goal2 = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=self.way_point2)
                # self.Goal3 = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=self.way_point3)
                # self.Goal4 = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=self.way_point4)

                
                #Distance to waypoints:

                self.dist_wp1=self.distance(self.pos,self.way_point1)
                self.dist_wp2=self.distance(self.pos,self.way_point2)
                self.dist_wp3=self.distance(self.pos,self.way_point3)
                self.dist_wp4=self.distance(self.pos,self.way_point4)
                self.dist_goal=self.distance(self.pos,self.state_goal)
                


                #Measuring distance for different paths created by waypoint
                self.dist_R12G=self.distance(self.poshit,self.way_point1) + self.distance(self.way_point1,self.way_point2) +self.distance(self.way_point2,self.state_goal)
                self.dist_R124G=self.distance(self.poshit,self.way_point1) + self.distance(self.way_point1,self.way_point2) + self.distance(self.way_point2,self.way_point4) +self.distance(self.way_point4,self.state_goal)
                
                
                self.dist_R13G=self.distance(self.poshit,self.way_point1) + self.distance(self.way_point1,self.way_point3) +self.distance(self.way_point3,self.state_goal)
                self.dist_R134G=self.distance(self.poshit,self.way_point1) + self.distance(self.way_point1,self.way_point3) + self.distance(self.way_point3,self.way_point4) + self.distance(self.way_point4,self.state_goal)
                

                #checking intersection between the obstacle and the line from last waypoint to goal
                self.intersection_wp2G_obs,_= self.intersection_check((self.way_point2,self.state_goal),self.square_bbox)
                self.intersection_wp3G_obs,_= self.intersection_check((self.way_point3,self.state_goal),self.square_bbox)


                #Measuring Heading error to different way points
                self.heading_error_wp1, _ = self.calc_angle_error(self.way_point1, self.pos, self.yaw)
                self.heading_error_wp2, _ = self.calc_angle_error(self.way_point2, self.pos, self.yaw)
                self.heading_error_wp3, _ = self.calc_angle_error(self.way_point3, self.pos, self.yaw)
                self.heading_error_wp4, _ = self.calc_angle_error(self.way_point4, self.pos, self.yaw)

                if self.dist_wp1<2:
                    self.wp1_reach=self.wp1_reach + 1
                


                if self.dist_wp2<2:
                    self.wp2_reach=self.wp2_reach + 1
                

                if self.dist_wp3<2:
                    self.wp3_reach=self.wp3_reach + 1
                


                if self.dist_wp4<2:
                    self.wp4_reach=self.wp4_reach + 1

                # if self.dist_goal <1:
                
                #     self.goal_success.append(True)
                    #print(self.goal_success)
                

                #print(self.wp1_reach,self.wp2_reach,self.wp3_reach,self.wp4_reach)

            # pm=None
            # if self.h==1:
            #     pm,om=p.getBasePositionAndOrientation(self.Id)
            # print(pm+pm)


            
            
            
            
            

                

                
                
                #print(way_point1)
               # print(self.int_point_square[0])
            # self.waypoint = (self.int_point_square[0][0],self.int_point_square[0][1],0.05)
            # print("way",self.waypoint)

  
        
        if self.args.static_robots > 1:

        # 	# #This part is for setting inflation radious bounding box around robots
        
            self.robot1_bbox=self.bbox_generator_titan(0.075,self.pos,self.orn,self.lineId1)
            self.robot1_bbox.append(self.robot1_bbox[0])
            
            
            self.robot2_bbox=self.bbox_generator_titan(0.075,self.pos2,self.orn2,self.lineId2)
            self.robot2_bbox.append(self.robot2_bbox[0])

            #self.robot2_bbox=self.bbox_generator_titan2(0.0,self.pos2,self.orn2,self.lineId2)
            
   
            
        
        # 	# #This part is for generating big bounding box around robot2 to create way point
            self.robot2_bigbox=self.bbox_generator_titan(1,self.pos2,self.orn2,self.lineId_r2_big)
            self.robot2_bigbox.append(self.robot2_bigbox[0])


            
            self.intersection_r1_r2,_= self.intersection_check(self.robot1_bbox,self.robot2_bbox)

   
            #check intersection between mid line trajectory versus robot 2 master bounding box
            self.line1_points=(self.pos[0], self.pos[1], 0), (self.state_goal[0], self.state_goal[1], 0)
            self.intersection_line_r2,_= self.intersection_check(self.line1_points,self.robot2_bbox)
            
            # check for intersection between the two lines
            #print(self.intersection_line_r2)
            

        #Uncomment above section if you want to use inflation radius
               
        #print(tuple(self.robot1_bbox[0]))
        if self.args.static_robots > 1:
            #self.c_robot1 = [(tuple(self.robot1_bbox[0])),(tuple(self.robot1_bbox[1])),(tuple(self.robot1_bbox[2])),(tuple(self.robot1_bbox[3]))]
            self.c_robot1 = [(tuple(self.robot1_bbox[0])),(tuple(self.robot1_bbox[1]))]
            self.c_robot2 = [(tuple(self.robot2_bbox[0])),(tuple(self.robot2_bbox[1])),(tuple(self.robot2_bbox[2])),(tuple(self.robot2_bbox[3]))]
            # self.c_robot2_bigbox= [(tuple(self.robot2_bigbox[0])),(tuple(self.robot2_bigbox[1])),(tuple(self.robot2_bigbox[2])),(tuple(self.robot2_bigbox[3]))]
            # self.c_goal = [(tuple(self.state_goal))]
            # #self.dist_r1_r2,_ = self.min_distance_corners(self.c_robot1, self.c_robot2)
            # _,_,_,self.way_point2= self.min_distance_corners(self.c_goal , self.c_robot2_bigbox)
            # _,_,self.way_point1,_ = self.min_distance_corners(self.c_robot1, self.c_robot2_bigbox)
            #print("Waypoint1", self.way_point1, "Waypoint2", self.way_point2)
            #print("Minimum Distance between the corner points of robot1 and robot2:", self.dist_r1_r2)
            #print(tuple(self.state_goal))
            
   
  
  
  
        
        

        # print "Collision detected!" if the lines are intersecting
        # if self.intersection:
        # 	print("Collision detected!")


        

        if self.args.static_robots > 1:
            #Between Robot 1 and Robot 2
            self.robot2_pos_robot1 = self.world_to_robot(self.yaw, self.pos, self.state_robot2)
            #print("self.robot2_pos_robot1",self.robot2_pos_robot1)
            self.dist_to_robot2 = math.sqrt(self.robot2_pos_robot1[0]**2 + self.robot2_pos_robot1[1]**2)
            #print("self.dist_to_robot2 ",self.dist_to_robot2 )
            self.heading_error_obs, self.target_angle_obs = self.calc_angle_error(self.state_robot2, self.pos, self.yaw)
            #print("heading_error_obs", self.heading_error_obs)
            #print("target_angle_obs", self.target_angle_obs)
            self.robot2_avoid_angle = np.arctan2(0.7, self.dist_to_robot2)
            #print("robot2_avoid_angle",self.robot2_avoid_angle*(180/np.pi),self.robot2_avoid_angle)
        
        # robot2_avoid_angle = np.arctan2(0.7*self.yaw2, self.dist_to_robot2)
        # print("robot2_avoid_angleyaw",robot2_avoid_angle*(180/np.pi))
        # robot2_avoid_angle = np.arctan2(math.sqrt(0.7**2 + self.yaw2**2), self.dist_to_robot2)
        # print("robot2_avoid_anglesqrt",robot2_avoid_angle*(180/np.pi))
        # print(self.yaw2)
        # if self.args.num_robots > 1:
        #     rayLen = 3
        #     mat = p.getMatrixFromQuaternion(self.orn)
        # #print(self.orn)
        #     dir = [mat[0], mat[3], mat[6]]
        #     lines_from = []
        #     lines_to = []
        #     for n, line_from in enumerate(self.robot1_bbox[:2]):
        #         line_to = [line_from[0] + dir[0] * rayLen, line_from[1] + dir[1] * rayLen, line_from[2] + dir[2] * rayLen]
        #         line_from = [line_from[0] + dir[0] * 0.5, line_from[1] + dir[1] * 0.5, line_from[2] + dir[2] * 0.5]
        #         #line_from = [self.body_xyz[0] + dir[0] * 0.5, self.body_xyz[1] + dir[1] * 0.5, self.body_xyz[2] + dir[2] * 0.5]
        #         lines_from.append(line_from)
        #         lines_to.append(line_to)
        #     if self.args.debug:
        #         for n, (line_to, line_from) in enumerate(zip(lines_from, lines_to)):
        #             self.ray_line[n] = p.addUserDebugLine(line_from, line_to, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=self.ray_line[n])
        #     hits = p.rayTestBatch(lines_from, lines_to)
        # #print(hits[0])
        #     self.hit = [hits[0][0] > 0, hits[1][0] > 0]
            #print(self.hit)
        
        #Converting Obstacle Obstacle BBOX Corners position to egocentric position based on Robot 1
        if self.args.obstacle_avoidance:
            #print(self.square_bbox);exit()
            self.obs_corner1 = self.world_to_robot(self.yaw, self.pos, self.square_bbox[0])
            self.obs_corner2 = self.world_to_robot(self.yaw, self.pos, self.square_bbox[1])
            self.obs_corner3 = self.world_to_robot(self.yaw, self.pos, self.square_bbox[2])
            self.obs_corner4 = self.world_to_robot(self.yaw, self.pos, self.square_bbox[3])


        #Converting Obstacle Position to egocentric position based on Robot 1
        self.obs_pos_robot = self.world_to_robot(self.yaw, self.pos, self.pos2)
        self.heading_error_to_obs, self.target_angle_to_obs = self.calc_angle_error(self.pos2, self.pos, self.yaw)
        self.dist_to_obs = math.sqrt(self.obs_pos_robot[0]**2 + self.obs_pos_robot[1]**2)

        # print(self.pos2)
        # print(self.obs_pos_robot)
        #print(self.Other_Robots_pos_list)
        #Converting Obstacle Obstacle BBOX Corners position to egocentric position based on Robot 1
        # if self.args.insert_wall:
        #     #print()
        #     self.gap[0]=self.wall1_corners
        #     self.gap[1]=self.wall2_corners
        if self.args.gap_avoidance:
            #wall1 corners in egocentric view
            self.wall1_corner1 = self.world_to_robot(self.yaw, self.pos, self.gap[0][0])
            self.wall1_corner2 = self.world_to_robot(self.yaw, self.pos, self.gap[0][1])
            self.wall1_corner3 = self.world_to_robot(self.yaw, self.pos, self.gap[0][2])
            self.wall1_corner4 = self.world_to_robot(self.yaw, self.pos, self.gap[0][3])


            #wall2 corners in egocentric view
            self.wall2_corner1 = self.world_to_robot(self.yaw, self.pos, self.gap[1][0])
            self.wall2_corner2 = self.world_to_robot(self.yaw, self.pos, self.gap[1][1])
            self.wall2_corner3 = self.world_to_robot(self.yaw, self.pos, self.gap[1][2])
            self.wall2_corner4 = self.world_to_robot(self.yaw, self.pos, self.gap[1][3])
            


            #Converting Wall1 Position to egocentric position based on Robot 1
            self.wall1_pos_allocentric= self.calculate_rectangle_center(self.gap[0][0],self.gap[0][1],self.gap[0][2],self.gap[0][3])

            self.wall1_pos_robot = self.world_to_robot(self.yaw, self.pos, self.wall1_pos_allocentric)
            self.heading_error_to_wall1, self.target_angle_to_wall1 = self.calc_angle_error(self.wall1_pos_allocentric, self.pos, self.yaw)
            self.dist_to_wall1 = math.sqrt(self.wall1_pos_robot[0]**2 + self.wall1_pos_robot[1]**2)

            #Converting Wall2 Position to egocentric position based on Robot 1
            self.wall2_pos_allocentric= self.calculate_rectangle_center(self.gap[1][0],self.gap[1][1],self.gap[1][2],self.gap[1][3])
            self.wall2_pos_robot = self.world_to_robot(self.yaw, self.pos, self.wall2_pos_allocentric)
            self.heading_error_to_wall2, self.target_angle_to_wall2 = self.calc_angle_error(self.wall2_pos_allocentric, self.pos, self.yaw)
            self.dist_to_wall2 = math.sqrt(self.wall2_pos_robot[0]**2 + self.wall2_pos_robot[1]**2)
            #print(self.robots_angular_velocity_with_IDx,self.robots_vx_with_IDx,self.robots_orn_with_IDx)
            # print(self.pos2)
            # print(self.obs_pos_robot)

        # if self.args.num_robots>1 and self.args.gap_avoidance:

        #     #converting robot2 position from robot 1 egocentric and measure heading error to robot 2
        #     self.other_robots_positions_allocentric= (self.other_robots_positions[0],self.other_robots_positions[1])
        #     self.robot2_pos_in_robot1 = self.world_to_robot(self.yaw, self.pos, self.other_robots_positions_allocentric)
        #     self.heading_error_to_robot2, self.target_angle_to_robot2 = self.calc_angle_error(self.other_robots_positions_allocentric, self.pos, self.yaw)
        #     self.dist_to_robot2 = math.sqrt(self.robot2_pos_in_robot1[0]**2 + self.robot2_pos_in_robot1[1]**2)
        #     print(self.heading_error_to_robot2)


    def set_obstacles(self, list_of_obs_bbox):
        self.obstacles=list_of_obs_bbox
    
    def set_robot_bbox(self, list_of_robot_bbox):
        self.robots_bbox=list_of_robot_bbox

    def set_allrobot_positions(self, list_of_allrobot_positions):
        self.robots_pos_with_IDx=list_of_allrobot_positions

    def set_robottogoal_angle(self, list_of_robottogoal_angles):
        self.robottogoal_angles=list_of_robottogoal_angles
    
    def set_external_robots_pos(self, list_of_external_robots_pos):
        self.external_robots_pos=list_of_external_robots_pos

    def set_all_goal_poses(self, list_of_goals_pos):
        self.Goals_pos=list_of_goals_pos

    def set_external_goals_state(self, list_of_external_goals_state):
        self.external_goals_states_with_IDx=list_of_external_goals_state

    def set_wall1_corners(self, list_of_wall1_corners):
        self.wall1_corners=list_of_wall1_corners

    def set_wall2_corners(self, list_of_wall2_corners):
        self.wall2_corners=list_of_wall2_corners

    def set_Robots_ID(self, list_of_Robots_ID):
        self.All_Robot_ID=list_of_Robots_ID

    def set_turn_both(self, list_of_turn_both):
        self.turn_both=list_of_turn_both

    def set_max_robotcode_gap_width(self, max_gap_among_all_robots_individual_gap_width):
        self.max_gap_among_all_robots_individual_gap_width=max_gap_among_all_robots_individual_gap_width

    def set_allrobot_orientation(self, list_of_allrobot_orientation):
        self.robots_orn_with_IDx=list_of_allrobot_orientation

    def set_allrobot_vx(self, list_of_allrobot_vx):
        self.robots_vx_with_IDx=list_of_allrobot_vx

    def set_allrobot_angular_velocity(self, list_of_allrobot_angular_velocity):
        self.robots_angular_vx_with_IDx=list_of_allrobot_angular_velocity
        
    def set_random_robotinit(self, random_robot_init):
        self.random_robot_init=random_robot_init
        
        
        

    
        
        



    def world_to_robot(self, robot_yaw, robot, world):
        x,y = world[0] - robot[0], world[1] - robot[1]                       #longitudinal distance
        rot_mat = np.array([[np.cos(robot_yaw), np.sin(robot_yaw)],          #rotational distance
                             [-np.sin(robot_yaw), np.cos(robot_yaw)]])
        return list(np.dot(rot_mat, np.array([x, y])))
    

    def wrap_to_pi(self,angle):
        """
        Wrap an angle in radians to the range [-pi, pi].
        """
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def calc_angle_error(self, world, robot, angle):
        target_angle = np.arctan2(world[1] - robot[1], world[0] - robot[0])

        angle_error = self.wrap_to_pi(target_angle - angle)

        return angle_error, target_angle

    # def calc_angle_error(self, world, robot, angle):
    #     target_angle = np.arctan2(world[1] - robot[1], world[0] - robot[0])
    #     #print("target",target_angle)
    #     if ( target_angle < 0 and angle > 0 ):
    #         angle_error = ( 2*np.pi + target_angle ) - angle
    #     elif ( target_angle > 0 and angle < 0 ):
    #         angle_error = target_angle - ( 2*np.pi + angle )
    #     else:
    #         angle_error = target_angle - angle
    #     #print("before_angle_error",angle_error)

    #     if angle_error >= np.pi:
    #         angle_error = np.pi - angle_error
    #     elif angle_error <= -np.pi:
    #         angle_error = angle_error - np.pi
    #     #print("after_angle_error",angle_error)
    #     return angle_error, target_angle

    # def min_distance_corners(self, corners_robot1, corners_robot2):
    

    #     min_distance = float('inf')
    #     second_min_distance = float('inf')
    #     min_point = None
    #     second_min_point = None

    #     for corner1 in corners_robot1:
    #         for corner2 in corners_robot2:
    #             distance = math.sqrt((corner2[0] - corner1[0]) ** 2 + (corner2[1] - corner1[1]) ** 2)
    #             #print(dist)
    #             #min_distance = min(min_distance, dist)
    #             if distance < min_distance:
    #                 second_min_distance = min_distance
    #                 second_min_point = min_point
    #                 min_distance = distance
    #                 min_point = corner2
    #             elif distance < second_min_distance:
    #                 second_min_distance = distance
    #                 second_min_point = corner2

    #     return min_distance, second_min_distance, min_point, second_min_point

    def bbox_generator_titan(self,radius,pos,orn,lineId,lineColorRGB=[1, 0, 0]):
     
        x=(1.4/2)+radius
        y=(0.78/2)+radius
        z=0.235
        # get the self.corners of the bounding box
        corners = [(x, y, z),
                  (x,-y,z),
                  (-x,-y,z),
                  (-x,y,z),
                  (x,y,z)]
     
        robot_bbox=[]

        for i in range(len(corners)-1):
                
            start1 = p.multiplyTransforms(pos, orn, corners[i], [0, 0, 0, 1])[0]

            robot_bbox.append(list(start1))

            end1 = p.multiplyTransforms(pos, orn, corners[i+1], [0, 0, 0, 1])[0]
            # if self.args.debug:
            #         lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB, lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
        return robot_bbox
    
    def bbox_generator_titan1(self,radius,pos,orn,lineId,lineColorRGB=[1, 0, 0]):
     
        x=(1.4/2)+radius
        y=(0.78/2)+radius
        z=0.235
        # get the self.corners of the bounding box
        corners = [(x, y, z),
                  (x,-y,z),
                  (-x,-y,z),
                  (-x,y,z),
                  (x,y,z)]
     
        robot_bbox=[]

        for i in range(len(corners)-1):
                
            start1 = p.multiplyTransforms(pos, orn, corners[i], [0, 0, 0, 1])[0]

            robot_bbox.append(list(start1))

            end1 = p.multiplyTransforms(pos, orn, corners[i+1], [0, 0, 0, 1])[0]
            if self.args.debug:
                lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB, lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
        return robot_bbox
    
    def bbox_generator_titan2(self,radius,pos,orn,lineId,lineColorRGB=[1, 0, 0]):
     
        x=(1.4/2)+radius
        y=(0.78/2)+radius
        z=0.235
        # get the self.corners of the bounding box
        corners = [(x, y, z),
                  (x,-y,z),
                  (-x,-y,z),
                  (-x,y,z),
                  (x,y,z)]
     
        robot_bbox=[]
        start1 = p.multiplyTransforms(pos, orn, len(corners)-1, [0, 0, 0, 1])[0]

        robot_bbox.append(list(start1))

        #for i in range(len(corners)-1):
                
            

        #end1 = p.multiplyTransforms(pos, orn, corners[i+1], [0, 0, 0, 1])[0]
            # if self.args.debug:
            #         lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB, lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
        return robot_bbox

    def bbox_generator_box(self,radius,pos,orn,lineId,lineColorRGB=[1, 0, 0]):
     
        x=(0.5/2)+radius
        y=(0.5/2)+radius
        z=0.235 #box/robot height
        # get the self.corners of the bounding box
        corners = [(x, y, z),
                  (x,-y,z),
                  (-x,-y,z),
                  (-x,y,z),
                  (x,y,z)]
     
        robot_bbox=[]

        for i in range(len(corners)-1):
                
            start1 = p.multiplyTransforms(pos, orn, corners[i], [0, 0, 0, 1])[0]

            robot_bbox.append(list(start1))

            end1 = p.multiplyTransforms(pos, orn, corners[i+1], [0, 0, 0, 1])[0]
            #if self.args.debug:
            if self.args.debug:
                    lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB, lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
            #lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
        return robot_bbox

    def bbox_generator(self,object_id,radius,height,lineId):
     
        aabbMin, aabbMax = p.getAABB(object_id)
        pos, orn = p.getBasePositionAndOrientation(object_id)
        # get the self.corners of the bounding box
        r = radius #inflation radius
        h= height #height of the box with the plane
        # get the corners of the bounding box
        corners = [(aabbMin[0]*r, aabbMin[1]*r, aabbMin[2]*h),
                (aabbMin[0]*r, aabbMax[1]*r, aabbMin[2]*h),
                (aabbMax[0]*r, aabbMax[1]*r, aabbMin[2]*h),
                (aabbMax[0]*r, aabbMin[1]*r, aabbMin[2]*h),
                (aabbMin[0]*r, aabbMin[1]*r, aabbMin[2]*h)]
     
        object_bbox=[]

        for i in range(len(corners)-1):
                
            start1 = p.multiplyTransforms(pos, orn, corners[i], [0, 0, 0, 1])[0]

            object_bbox.append(list(start1))
            #print(object_bbox)

            end1 = p.multiplyTransforms(pos, orn, corners[i+1], [0, 0, 0, 1])[0]
            if self.args.debug:
                    lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
        return object_bbox

    def intersection_check(self, line1,line2):
        intersection = False
        intersection_p=[]
        for i in range(len(line1)-1):
                for j in range(len(line2)-1):

                    #print(self.intersection)
                    x1,y1,z1=line1[i]     #Rotating start coordinates for Robot 1
                    x2,y2,z2=line1[i+1]   #Rotating end coordinates for Robot 1
                    x3,y3,z3=line2[j]     #Rotating start coordinates for Robot 2
                    x4,y4,z4=line2[j+1]   #Rotating end coordinates for Robot 2


                    if (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1) == 0:
                        
                        intersection = True
                        #print("Denominator_Zero")
                    else:
                        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
                        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
                        #print("uA",uA)
                        #print("uB",uB)
      


                    # uA = ((x2-x1)*(y4-y3) - (y2-y1)*(x4-x3)) / ((x2-x1)*(y4-y3) - (y2-y1)*(x4-x3))
                    # uB = ((x3-x4)*(y1-y2) - (y3-y4)*(x1-x2)) / ((x2-x1)*(y4-y3) - (y2-y1)*(x4-x3))
                    #uA = ((end2[0]-start2[0])*(start1[1]-start2[1]) - (end2[1]-start2[1])*(start1[0]-start2[0])) / ((end2[1]-start2[1])*(end1[0]-start1[0]) - (end2[0]-start2[0])*(end1[1]-start1[1]))
                    #uB = ((end1[0]-start1[0])*(start1[1]-start2[1]) - (end1[1]-start1[1])*(start1[0]-start2[0])) / ((end2[1]-start2[1])*(end1[0]-start1[0]) - (end2[0]-start2[0])*(end1[1]-start1[1]))
                    #print("line1",uA,"line2", uB)
                        if 0 <= uA <= 1 and 0 <= uB <= 1:
                            intersection = True
                            intersection_point = (x1 + uA * (x2 - x1), y1 + uB * (y2 - y1))
                            intersection_p.append(intersection_point)
        return intersection, intersection_p

    def gap_generator(self,width, depth,height,pos,wall_length,goal_pos,lineId,lineIdgap,lineIdA,lineIdB):
        # print("gap_pos",pos)
        # print("gap_goal_pos",goal_pos)
        # print("gap_width",width)
        line_direction = [goal_pos[0] - pos[0], goal_pos[1] - pos[1], 0]
        perpendicular_direction = [line_direction[1], -line_direction[0], 0]
        orn = p.getQuaternionFromEuler([0, 0, math.atan2(perpendicular_direction[1], perpendicular_direction[0])])
        #------------------------------------
        x=width/2+wall_length
        y=depth
        z=height
        # get the self.corners of the bounding box
        corners = [(x, y, z),
                  (x,-y,z),
                  (-x,-y,z),
                  (-x,y,z),
                  (x,y,z)]
     
        robot_bbox=[] #bbox of big obstacles including gap

        for i in range(len(corners)-1):
                
            start1 = p.multiplyTransforms(pos, orn, corners[i], [0, 0, 0, 1])[0]

            robot_bbox.append(list(start1))

            end1 = p.multiplyTransforms(pos, orn, corners[i+1], [0, 0, 0, 1])[0]
            # if self.args.debug:
            # 	lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[0, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
        
        x=width/2
        cornersgap = [(x, y, z),
                  (x,-y,z),
                  (-x,-y,z),
                  (-x,y,z),
                  (x,y,z)]
     
        robot1_bbox=[] #bbox of middle gap box

        # if self.args.debug:
        #         lineIdgap[i]=p.addUserDebugLine((cornersgap[0][0]/2,cornersgap[0][1],.2),(-cornersgap[0][0]/2,-cornersgap[0][1],.2), lineColorRGB=[0, 0, 0], lineWidth=100, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])

        for i in range(len(cornersgap)-1):
                
            start1 = p.multiplyTransforms(pos, orn, cornersgap[i], [0, 0, 0, 1])[0]

            robot1_bbox.append(list(start1))

            end1 = p.multiplyTransforms(pos, orn, cornersgap[i+1], [0, 0, 0, 1])[0]
            #if self.args.debug:
                #lineIdgap[i]=p.addUserDebugLine(robot1_bbox[0], robot1_bbox[1], lineColorRGB=[0.2, 0.5, 1], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])
                #lineIdgap[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[0.2, 0.5, 1], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])
        
        # lineIdgap_A=p.addUserDebugLine(robot1_bbox[1], robot1_bbox[2], lineColorRGB=[0.2, 0.5, 1], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])
        # lineIdgap_B=p.addUserDebugLine(robot1_bbox[3], robot1_bbox[0], lineColorRGB=[0, 1, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])
        #print(robot1_bbox[1])

        #Gap_point Related Calculations
        PP1=self.calculate_midpoint(robot1_bbox[1], robot1_bbox[2])
        PP2=self.calculate_midpoint(robot1_bbox[3], robot1_bbox[0])
        #lineIdgap_C=p.addUserDebugLine(P1, P2, lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])
        P1=self.calculate_opposite_point(PP1,PP2,distance=2)
        P2=self.calculate_opposite_point(PP2,PP1,distance=2)
        #lineIdgap_D=p.addUserDebugLine(P1, P2, lineColorRGB=[0, 1, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])

        dist_p1_goal=self.distance(P1,goal_pos)
        dist_p2_goal=self.distance(P2,goal_pos)
        #print(dist_Wp1_goal,dist_Wp2_goal)
        if dist_p1_goal>dist_p2_goal:
            WP1=P1
            WP2=P2
        elif dist_p2_goal>dist_p1_goal:
            WP1=P2
            WP2=P1
        # #print(tuple(pos),WP1)
        # lineIdgap_D=p.addUserDebugLine(WP1, goal_pos, lineColorRGB=[0, 1, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])
        # lineIdgap_E=p.addUserDebugLine(WP2, goal_pos, lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])
        lineIdgap_F=p.addUserDebugLine(WP1, WP2, lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdgap[i])


        cornersA = [robot1_bbox[1],
                  robot1_bbox[0],
                  robot_bbox[0],
                  robot_bbox[1],
                  robot1_bbox[1]]
        
        robot2_bbox=[] #bbox of one side obstacle

        for i in range(len(cornersA)-1):
                
            start1 = cornersA[i]

            robot2_bbox.append(list(start1))

            end1 = cornersA[i+1]
            if self.args.debug:
               lineIdA[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdA[i])
     
        cornersB = [robot1_bbox[2],
                  robot1_bbox[3],
                  robot_bbox[3],
                  robot_bbox[2],
                  robot1_bbox[2]]
        
        robot3_bbox=[]  #bbox of other side obstacle

        for i in range(len(cornersB)-1):
                
            start1 = cornersB[i]

            robot3_bbox.append(list(start1))

            end1 = cornersB[i+1]
            if self.args.debug:
               lineIdB[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineIdB[i])
        
        Wall1_rectangle=robot2_bbox
        Wall2_rectangle=robot3_bbox
        

        Wall1_centre=[(Wall1_rectangle[0][i] + Wall1_rectangle[2][i]) / 2 for i in range(3)]
        Wall2_centre=[(Wall2_rectangle[0][i] + Wall2_rectangle[2][i]) / 2 for i in range(3)]
        # print("r1",robot1_bbox)
        # print("r2",robot2_bbox)
        #corners=robot2_bbox
        
        # p.createMultiBody(
        #     baseMass=1,
        #     baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_BOX, halfExtents=[length/2, width/2, height/2]),
        #     basePosition=[position_x, position_y, height / 2],
        #     baseOrientation=p.getQuaternionFromEuler([0, 0, yaw]),
        # )

        return Wall1_rectangle,Wall2_rectangle,WP1,WP2,orn,Wall1_centre,Wall2_centre
    
    def create_rectangle(self,corners,wall_length,wall_width,wall_height,orientation):

        # Calculate the center and half extents of the rectangle
        #half_extents = [(corners[2][i] - corners[0][i])/2 for i in range(3)]
        
        center = [(corners[0][i] + corners[2][i]) / 2 for i in range(3)]
        half_extents=[((wall_length/2)), wall_width, wall_height/2]
        #print("center",center)
        
        # Create a collision shape for the rectangle
        box_collision_shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)

        # Create the rectangle using createMultiBody and attach the collision shape
        box_id = p.createMultiBody(baseMass=0,
                                baseCollisionShapeIndex=box_collision_shape_id,
                                basePosition=center,baseOrientation=orientation)

        return box_id

    def find_position_B(self,position_a, distance_d, angle_degrees):
        # Convert the angle from degrees to radians
        angle_radians = math.radians(angle_degrees)
        

        # Calculate the coordinates (x, y) of position B
        x_b = position_a[0] + distance_d * math.cos(angle_radians)
        y_b = position_a[1] + distance_d * math.sin(angle_radians)
        z_b=0

        return x_b, y_b,z_b
    
    def perpendicular_angle(self,start_point, end_point):
        # Calculate the differences in x and y coordinates
        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]

        # Calculate the angle in radians using atan2
        angle_radians = math.atan2(delta_y, delta_x)

        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)

        # Ensure the angle is within the range [0, 360)
        angle_degrees = angle_degrees % 360

        #Perpendicular Angle
        perpendicular_angle = math.pi/2 - angle_radians

        return perpendicular_angle
    
    def distance(self,point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    

    def find_closest_coordinates(self,center_box1, box2_corners):
        distances = [(self.distance(center_box1, corner), corner) for corner in box2_corners]
        sorted_distances = sorted(distances, key=lambda x: x[0])
    
        return sorted_distances
    
    def komol(self,l,id):
                if l==1:
                    pm,om=p.getBasePositionAndOrientation(id)
                    
                
                    return pm[0],pm[1],pm[2]
                
    def calculate_midpoint(self,point1, point2):
        x1, y1, z1 = point1
        x2, y2, z1 = point2

        # Calculate the midpoint
        midpoint_x = (x1 + x2) / 2
        midpoint_y = (y1 + y2) / 2

        midpoint = (midpoint_x, midpoint_y,z1)
        return midpoint
    
    def calculate_opposite_point(self,pointA, pointB, distance):
        x1, y1,z1 = pointA
        x2, y2,z1 = pointB

        # Calculate the direction vector from A to B
        direction_vector = (x2 - x1, y2 - y1)

        # Normalize the direction vector (make it a unit vector)
        length = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5
        normalized_vector = (direction_vector[0] / length, direction_vector[1] / length)

        # Calculate the coordinates of pointC
        pointC_x = x1 + normalized_vector[0] * distance
        pointC_y = y1 + normalized_vector[1] * distance

        pointC = (pointC_x, pointC_y,z1)
        return pointC
    
    def calculate_rectangle_center(self,point1,point2,point3,point4):
        # Calculate the center point
        x1, y1, z1=point1
        x2, y2, z1=point2
        x3, y3, z1=point3
        x4, y4, z1=point4
        center_x = (x1 + x2 + x3 + x4) / 4
        center_y = (y1 + y2 + y3 + y4) / 4

        point =(center_x, center_y,z1)
        return point
    

    



    
