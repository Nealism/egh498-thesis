from cmath import e
from copy import deepcopy
import numpy as np
import pandas as pd
import cv2
import torch

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

class Env(EnvBasePB):
    
    def __init__(self, PATH=None, args=None, writer=None,posi=None):

        #Initiations like CPU parallelisation rank, arguments, render, path, writer for tensorboard plot, 
        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True
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
            self.ac_size = 3
            self.ob_size = 7
        else:
            self.ac_size = 3
            if self.args.static_robots > 1:
                self.ob_size = 18
            elif self.args.obstacle_avoidance:
            
                self.ob_size = 16+2*(self.args.num_robots-1)

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


        #Spot model lower level action size

        self.ac_size_walk_model=12

        #Initialising KP for bootstrap curr, time to goal, 
        # opposite angle to set goal position opposide side of wall if needed (not needed).
        #Start Timer
        self.Kp = 400
        self.initial_Kp = self.Kp
        self.time_to_goal=0
        self.time_to_gapwp1=0
        self.time_to_gapwp2=0
        
        self.opposite_angle=0

        self.start_time = time.time() 


        #Taking from Spot Pb -- this best return was used in reset
        self.best_return = 0


        #Limiting the Command Velocity in a threshold and setting the threshold here (Taken from Spot_pb)
        self.max_vx = 1.0
        self.max_vy = 0.5
        self.max_yaw_vel = 1.5

        self.min_vx = -0.5
        self.min_vy = -0.5
        self.min_yaw_vel = -1.5

        self.target_max_yaw_vel = 1.5


        #This was used to compute torque (Taken from Spot)
        self.action_scale = 0.5
        self.torque_kp = 20.0
        self.torque_kd = 0.5
        self.default_joints = np.array([0.0, 1.2, -2.0]*4)

        #Loading Lower level spot walking model
        SPOT_MODEL_PATH = "./resources/spot/2024_05_13_11_11_30/model.pt" 
        self.spot_pol = torch.load(SPOT_MODEL_PATH)

        
        #initialising single robot collision likelihood curr (Not Needed)
        if self.args.obstacle_avoidance and self.args.static_robots > 1 and self.args.single_collision_curr or self.args.cur:
            self.a=5.0
            self.b=0.5
        else:

            self.a=0.0
            self.b=0.0

        #initialising collision likelihood curr (Not Needed) but else command is needed
        if self.args.gap_avoidance and self.args.num_robots>1 and self.args.collision_likelihood_curr:
            self.increase_collision_rate=-2
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
                
                
                
            elif self.args.gap_avoidance:
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
                self.decrease_gap_width=0
                self.final_gap_width=self.args.final_gap_width
                #parameters for tunnel curr
                self.max_tunnel_depth = 0.2
                self.increase_tunnel_depth = 0.1
                self.max_gap_among_all_robots_individual_gap_width=self.max_gap_width
                
                
            elif self.args.gap_avoidance:
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
        
        


        #defining action space and observation space
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        
        #initialising step from -1
        self.steps = -1
   
        #Defining name of Reward types for tensorboard plots
        self.reward_names = ["Reward/goal", "Reward/heading", "Reward/heading_obs", "Reward/neg", "Reward/MA_colision", "Reward/collision","Reward/reach"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names}

        
    
        self.env_exp = None

        #Defining Initial joints and success criteria like goal success, cur success
        self.initial_joints = [0.0] * 15 + [ 0.5, -0.5, -1.5707] + [-0.5, 0.5, -1.5707]
        self.cur_success = deque([0.0], maxlen=5)
        self.success = deque([0.0], maxlen=1)
        self.ep_goal_success = 0.0
        self.ep_success = False

        #initialising terrain difficulty (Not Needed)
        if self.args.add_terrain:
            self.terrain_difficulty = self.args.initial_terrain_difficulty
        else:
            self.terrain_difficulty = 0
            self.terrain = None

        #initialising episode, total step, ob_dictionary, state to restore to check the joints
        self.episodes = -1
        self.total_steps = 0
        self.ob_dict = {}
        
        self.states_to_restore = ["pos", "orn", "joints", "base_vel", "joint_vel", "args", "episodes", "steps", "total_steps"]

        
        self.load_robot()

        

    def load_specific_robot(self):
        
        robot1=self.load_urdf_robot("./assets/urdfs/spot/urdf/spot.urdf")
        self.contact_list = [['base_link','front_rail','real_front_rail', 'real_rear_rail','rear_rail','front_left_hip','front_left_upper_leg', 'front_right_hip', 'front_right_upper_leg','rear_left_hip', 'rear_left_upper_leg','rear_right_hip', 'rear_right_upper_leg']]

        self.jdict = {}
        self.feet_dict = {}
        self.leg_dict = {}
        self.body_dict = {}
        self.feet = ["rear_left_lower_leg", "rear_right_lower_leg", "front_left_lower_leg", "front_right_lower_leg"]
        self.legs = ["rear_left_upper_leg", "rear_right_upper_leg", "front_left_upper_leg", "front_right_upper_leg"]
        self.feet_contact = {f:True for f in self.feet}
        self.ordered_joints = []
        self.ordered_joint_indices = []
        self.contact_dict = {}
        self.shin_dict = {}
        self.arm_dict = {}
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            # print()
            link_name = info[12].decode("ascii")
            if link_name in self.feet: self.feet_dict[link_name] = j
            if link_name in self.legs: self.leg_dict[link_name] = j
            if link_name=="pelvis": self.body_dict["body_link"] = j
            if link_name in self.contact_list: self.contact_dict[link_name] = j
            self.ordered_joint_indices.append(j)
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            

            lower, upper = (info[8], info[9])
            self.ordered_joints.append( (j, lower, upper) )
            self.jdict[jname] = j
        
        

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

        state_object=[np.random.uniform(-2, 2),np.random.uniform(-3, -3.5),0.00]
        wall_dir= "Wall_URDF/"
        self.Goal = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=state_object)
        # self.actions =
        #  {key:0.0 for key in self.motor_names}

        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(self.motor_names))

        for key in self.feet_dict:
            p.changeDynamics(self.Id, self.feet_dict[key],lateralFriction=0.9, spinningFriction=0.9)


    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        # print("What the ", self.ep_goal_success); exit()
        if self.args.obstacle_avoidance and self.args.gap_avoidance:
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "RC_Initial Distance to Goal": self.initial_goal_dist, "GC: Gap Width":self.max_gap_among_all_robots_individual_gap_width, "TC: Tunnel Width":self.increase_tunnel_depth,"CLC: distance between obstacle and path": self.a-self.b, "EC: Kp": self.Kp }
        elif self.args.gap_avoidance:
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "EC: Kp": self.Kp, "GC: Gap Width":self.max_gap_among_all_robots_individual_gap_width, "TC: Tunnel Width":self.increase_tunnel_depth,"Time_to_Goal":self.time_to_goal,"Time_to_gapwp1":self.time_to_gapwp1,"Time_gapwp1_gapwp2":self.time_to_gapwp2-self.time_to_gapwp1,"Time_gapwp2_goal":self.time_to_goal-self.time_to_gapwp2, "Collision_likelihood": self.increase_collision_rate}
        else:
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "RC_Initial Distance to Goal": self.initial_goal_dist, "EC: Kp": self.Kp }

        return_dict.update(self.reward_dict)
        return return_dict

    

    def get_success(self):
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        
        if self.args.cur_succ==0:
            #print("self.distance_to_goal",dist_to_goal,self.distance_to_goal)
            return self.distance_to_goal == True
        

    def check_for_success(self):
        return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()
    
    def check_both_for_success(self):
        return len(self.All_Robot_ID[0].cur_success) == 3 and len(self.All_Robot_ID[1].cur_success) == 3 and (np.array(self.All_Robot_ID[0].cur_success) == True).all() and (np.array(self.All_Robot_ID[1].cur_success) == True).all()
    

    def reset(self, terrain=None, test=False, restore_state=None):

        #Related to Bounding box
        self.intersection_r1_box= False
        self.intersection_r1_r= False
        self.robot1_near_robot2=False

        self.paused = False

        #Moving Goal after Reaching 
        self.goal_moved=False
        Initial_distance_to_goal=0
        
        self.prev_dist_to_goal= Initial_distance_to_goal

        self.ob_dict = {}
        for foot in self.feet_dict:
            self.ob_dict[foot] = False
            self.ob_dict["prev_" + foot] = False

        self.z_offset = 0

        #Update Reward Dictionary
        if self.steps > 0:
            for key in self.reward_dict:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 



        #Updating Success
        if self.episodes > -1:

            self.success.append(self.get_success())
            self.ep_success = self.get_success()		
            self.cur_success.append(self.ep_success)
            self.ep_goal_success = np.mean(self.goal_success) if self.goal_success else 0.0

        self.goal_success = []
        
        #Removing bodies like goal dots after reaching and also rays with time
        p.removeAllUserDebugItems()		

        p.removeBody(self.Goal)
        

        #Defining the position of Goal
        state_object=[np.random.uniform(-4, 4), np.random.uniform(-4, 4), 0.00]
        wall_dir= "Wall_URDF/"
        self.Goal = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=state_object)
        p.setCollisionFilterGroupMask(self.Goal, -1, collisionFilterGroup=0, collisionFilterMask=0) #Make sure goal has no collision
        
        
        #Save Sim State related to CPU Parallelisation
        if self.rank == 0 and self.args.record_sim and self.episodes > 0:
            self.record_sim_state(best=self.check_for_success(), test=test)
        
       


        self.steps = 0
        self.st=time.time()
        
        
        #Setting Position and Orientation of Robot
        initial_x, initial_y = np.random.uniform(0,4), np.random.uniform(0, 4) 
        self.initial_yaw = 0.0#np.random.uniform(-np.pi, np.pi) 
        self.initial_orn = p.getQuaternionFromEuler([0,0,self.initial_yaw])
        self.z_offset = 0



    
        ######___________ALL CURRICULUM STAGES ARE HERE__________________##################################################
        
        #########____EXPERT/GUIDED_CURRICULUM__########   
        
        

        if (self.args.cur or self.args.expert_curr) and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
            self.cur_success = deque([0.0], maxlen=5) 
        
           

        
        #########____Collision_Likelihood_CURRICULUM__########   

        if self.args.gap_avoidance and self.increase_collision_rate <3 and (self.args.cur or self.args.collision_likelihood_curr) and self.args.num_robots>1 and self.check_for_success():    
            self.increase_collision_rate += 1
            self.cur_success = deque([0.0], maxlen=5)
        
        elif self.args.gap_avoidance and self.increase_collision_rate >= 3 and self.args.collision_likelihood_curr:
            self.increase_collision_rate=3

        elif self.args.gap_avoidance and not self.args.collision_likelihood_curr:
            self.increase_collision_rate=-1
        
        
        # Robot move to goal
        for robot, angles in self.robottogoal_angles:
            if robot == self:
                # Assuming there's only one value in the angles list for simplicity
                self.robottogoal_angle = angles#[0]
                
                break
            # else:
            #     # If the robot_name is not found, handle it accordingly
            #     print(f"Robot {self} not found in robottogoal_angles.")
        
       
        
        self.robottogoal_angle *=  -self.increase_collision_rate
        

        
        #REGION_CUrriculum: Increasing Distance to Goal Gradually
        if (self.args.cur or self.args.region_curr) and self.check_for_success() and self.initial_goal_dist <= self.max_goal_dist:
            self.initial_goal_dist +=1 # = 0
            self.cur_success = deque([0.0], maxlen=5)
                		
        
        
        #GAP_CUrriculum: Reducing Gap Width Gradually
        if self.args.gap_avoidance and (self.args.cur or self.args.gap_curr):
            
            if self.args.num_robots>1 and self.check_for_success():
                
                if self.max_gap_width-self.decrease_gap_width > self.final_gap_width :         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                    self.decrease_gap_width += self.args.gap_decrease			
                    

                    self.cur_success = deque([0.0], maxlen=5)
                    
                    

            elif self.args.num_robots==1 and self.check_for_success():
                
                if self.max_gap_width-self.decrease_gap_width > self.final_gap_width:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                    self.decrease_gap_width += self.args.gap_decrease			
                    self.cur_success = deque([0.0], maxlen=5)
                    
                
                
        
               
        #Tunnel_CUrriculum: Increasing the Tunnel/Gap length Gradually
        if self.args.gap_avoidance and (self.args.cur or self.args.tunnel_curr) and self.check_for_success():
            if self.max_tunnel_depth-self.increase_tunnel_depth == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                self.increase_tunnel_depth = self.max_tunnel_depth
                		
            else:
                self.increase_tunnel_depth += 0.2			
                
                self.cur_success = deque([0.0], maxlen=5)

        
        #########____OBSTACLE_AVOIDANCE_CURRICULUM/Collision_likelihood_Curriculum__########
        # self.a is the fixed value of unit ( how far from the line) and self.b is the step size ( Here, step size is 0.5 unit)
        

        if (self.args.static_robots > 1 or self.args.obstacle_avoidance) and (self.args.cur or self.args.collision_likelihood_curr) and self.check_for_success():
            if self.a-self.b == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                self.b = self.a
                self.cur_success = deque([0.0], maxlen=5)
                		
            else:
                self.b +=0.1			
                
                self.cur_success = deque([0.0], maxlen=5)

        

    
        #Now--Setting Position of Robot using Set_position Function

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1])
            
        else:
            pos, orn, self.joints, self.base_vel, self.joint_vel = [initial_x, initial_y, self.z_offset+0.31],self.initial_orn, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
            self.robot_own_pos=None
            for robot, own_pos in self.external_robots_pos:
                if robot == self:
                    # Assuming there's only one value in the angles list for simplicity
                    self.robot_own_pos = own_pos
                    break
                # else:
                #     # If the robot_name is not found, handle it accordingly
                #     print(f"Robot {self} not found in pos.")
            
            
            pos=self.robot_own_pos
            
            # self.set_position(pos, orn, robot_id=self.Id)
            rand_scale = self.max_disturbance / self.final_disturbance
            # pos = [0,0,0.5 + np.random.uniform(-0.05, 0.05)]
            self.roll, self.pitch, self.yaw = [np.random.uniform(-0.05, 0.05), np.random.uniform(-0.05, 0.05), np.random.uniform(-0.05, 0.05)] 
            orn = p.getQuaternionFromEuler([self.roll, self.pitch, self.yaw])
            base_vel = [0,0,0]
            joints = []
            for j in self.ordered_joints:
                joints.append(np.clip(np.random.random() * rand_scale * 0.25 , j[1], j[2]))
            joints = self.default_joints + (np.random.random(self.ac_size_walk_model)*0.2 - 0.1)
            joint_vel = [0]*len(self.motors)
            self.set_position(pos, orn, joints, base_vel, joint_vel)

        
        self.actions_walk_model = np.zeros(self.ac_size_walk_model)
        self.prev_actions_walk_model = self.actions_walk_model
        
        # self.commands = np.zeros(3)

        self.commands = np.random.uniform([self.min_vx, self.min_vy, self.min_yaw_vel],[self.max_vx, self.max_vy, self.max_yaw_vel])
        
        # Set low lin velocities to zeros
        if np.random.random() < 0.8:
            self.commands[2] = np.random.choice([-1,1]) * np.random.uniform(1.0, self.target_max_yaw_vel)
        else:
            self.commands[2] = np.random.choice([-1,1]) * np.random.uniform(0, 1.0)
        
        self.commands[0] *= abs(self.commands[0])>0.1
        self.commands[1] *= abs(self.commands[1])>0.1
        self.commands[2] *= abs(self.commands[2])>0.1
        self.target_yaw = self.yaw       


        self.target_yaw = self.yaw
        self.sign = 1
            

        # self.robottogoal_angle=None
        self.external_goals_states=[]
        self.external_robots_states=[]
        
        for robot,goal in self.external_goals_states_with_IDx:
            self.external_goals_states.append(goal)
        
        for robot,r_position in self.external_robots_pos:
            self.external_robots_states.append(r_position)

        self.mid_point_of_goals=self.calculate_midpoint(self.external_goals_states[0],self.external_goals_states[-1])
        # self.mid_point_of_goals=(self.mid_point_of_goals[0],self.mid_point_of_goals[1],self.mid_point_of_goals[2])
        # self.mid_point_of_goals= (self.mid_point_of_goals[0],self.mid_point_of_goals[1])

        self.mid_point_of_robots=self.calculate_midpoint(self.external_robots_states[0],self.external_robots_states[-1])
        # self.mid_point_of_robots_offsetting=(self.mid_point_of_robots[0],self.mid_point_of_robots[1]+np.random.uniform(-1.2,1.2))
        # self.mid_point_of_robots=(self.mid_point_of_robots[0],self.mid_point_of_robots[1]-1.2)
        # self.mid_point_of_robots=(self.mid_point_of_robots[0],self.mid_point_of_robots[1]+np.random.uniform(-3,3))

        # Function to move the goal and the static robot
        if self.args.gap_avoidance:
            
            self.move_goal_and_static_robot(initial_x=pos[0], initial_y=pos[1], yaw=self.initial_yaw,robottogoal_angle=self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)
        else:
            self.move_goal_and_static_robot(initial_x=pos[0], initial_y=pos[1], yaw=self.initial_yaw,robottogoal_angle=self.robottogoal_angle,mid_point_goals=self.mid_point_of_goals,mid_point_robots=self.mid_point_of_robots)
        
        
        
        self.reset_time=self.timeStep_10Hz*self.steps
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


        self.goal_reaching=False

        self.time_saving=[]
        self.velocity_saving1=[]
        self.velocity_saving2=[]
        self.action_saving1=[]
        self.action_saving2=[]
        self.scale_f_linear=[]
        self.scale_f_angular=[]

        self.wall_length=1.7

        self.k=0

        

        

        

        


        
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
            
            #Set the Tunnel/Gap Depth from the Tunnel Curriculum in reset
            self.tunnel_depth= self.increase_tunnel_depth

            side_wall_moving_rate=-21
            
            # self.gap=self.gap_generator(width=self.max_gap_among_all_robots_individual_gap_width, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = self.wall_length,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)
            self.gap=self.gap_generator(width=self.max_gap_among_all_robots_individual_gap_width, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = self.wall_length,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)
            self.sidewalls=self.gap_generator(width=side_wall_moving_rate, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = 25,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)
            # self.sidewall_left=self.gap_generator(width=0.1, depth=self.All_Robot_ID[0].tunnel_depth,height=0.015,pos=self.All_Robot_ID[0].pos2,wall_length = 15,goal_pos=self.All_Robot_ID[0].mid_point_of_goals,lineId=self.All_Robot_ID[0].lineIdWall,lineIdgap=self.All_Robot_ID[0].lineIdgap,lineIdA=self.All_Robot_ID[0].lineIdA,lineIdB=self.All_Robot_ID[0].lineIdB)

            

            self.gap_point1,self.gap_point2=self.gap[2],self.gap[3]

            self.gap_orn=self.gap[4]
            

            wall_1_length = max(np.linalg.norm(np.array(self.gap[0][0]) - np.array(self.gap[0][2])), np.linalg.norm(np.array(self.gap[0][1]) - np.array(self.gap[0][3])))
            

            self.dist_gapwp1 = self.distance(pos, self.gap[2])
            self.dist_gapwp2 = self.distance(pos, self.gap[3])

            self.rectangle1_centre = [(self.gap[0][0][i] + self.gap[0][2][i]) / 2 for i in range(3)]
            self.rectangle2_centre = [(self.gap[1][0][i] + self.gap[1][2][i]) / 2 for i in range(3)]
            self.rectangle3_centre = [(self.sidewalls[0][0][i] + self.sidewalls[0][2][i]) / 2 for i in range(3)]
            self.rectangle4_centre = [(self.sidewalls[1][0][i] + self.sidewalls[1][2][i]) / 2 for i in range(3)]
            
            
            self.Boolian=False
            self.Boolian2=False


        self.get_observation()

        
        self.episodes += 1

        self.cur_time = 0
        self.total_reward = 0
        self.distance_to_goal=0
        

        # Time to take single step
        postuple= tuple(self.pos)
        allowance = 0.05 # allowance for flexibility in avoiding robot2
        if self.args.static_robots > 1:
            self.Initial_robot2_avoid_angle=self.robot2_avoid_angle + allowance #Set Robot 2 avoid angle in reset
        
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
            

        
    def compute_torques(self, actions):
        # print(actions.shape, self.default_joints.shape, sel)
        return self.torque_kp*(self.action_scale*actions + self.default_joints - np.array(self.joints_walking)) - self.torque_kd*(np.array(self.joint_vel_walking))



    def step2(self):

            self.actions_walk_model = self.Lower_action

            # for _ in range(int(self.timeStep_10Hz/self.simStep)):
            jointStates_walking = p.getJointStates(self.Id,self.ordered_joint_indices)
            self.joints_walking = list(np.array([jointStates_walking[j[0]][0] for j in self.ordered_joints[:int(self.ac_size_walk_model)]]))
            
            # Scale vels 
            self.joint_vel_walking = list(np.array([jointStates_walking[j[0]][1] for j in self.ordered_joints[:int(self.ac_size_walk_model)]]) / 10) 
            forces = self.compute_torques(self.Lower_action)

            
            forces = forces.reshape(-1)
            p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.TORQUE_CONTROL, forces=forces)


            self.get_observation2()

            return self.obs_buf
    

    def motor_action(self,actions):
        # print("spot action",actions,type(actions))
        # actions=np.array([1.0,0.0])
        self.exp_actions = [0.0]*3
        # print("SP_AC",actions)
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

        ##THIS MA BOOTSTRAP IS THE BEST AND SAVED############################
        if self.args.gap_avoidance and self.args.MA_bootstrap:
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

        elif self.args.gap_avoidance and (self.args.num_robots == 1):

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

        
    
        elif self.args.obstacle_avoidance :
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

    
        else:
            if abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
                self.exp_actions[0] = 0.25
            else:	
                self.exp_actions[0] = 0.0
            self.exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        

        



        self.exp_actions=[self.exp_actions[0],self.exp_actions[2],self.exp_actions[1]]

        if self.args.just_expert or (self.args.cur or self.args.expert_curr):
            #Make sure to uncomment it when freezing robot when hitting wall lines to work with multi robot
            if (self.args.reward_fn == 25 or self.args.reward_fn == 26 or self.args.reward_fn == 27) and (np.array(self.contacts) == True).any():#(self.intersection_r1_box or self.intersection_r1_r or self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):
            
                self.applied_actions=[0]*3
            else:
            
                self.applied_actions = (self.Kp/self.initial_Kp) *np.array(self.exp_actions)
                if not self.args.just_expert:
                    self.applied_actions += self.action_multiplier*actions
            
        else:
            self.applied_actions = self.action_multiplier*actions
        self.prev_actions = actions



    def motor_action_LL(self):
        

        
        lin_vel = 1.0
        ang_vel = 1.0
        commands_scale = np.array([1.0, 1.0, 1.0])
        dof_pos = 1.0
        dof_vel = 0.05


        clipped_linear_vel_command=np.clip(self.applied_actions[0], -0.75, 0.75)
        clipped_lateral_vel_command=np.clip(self.applied_actions[1], -0.5, 0.5)
        clipped_angular_vel_command=np.clip(self.applied_actions[2], -0.75, 0.75)
        self.commands=np.array([clipped_linear_vel_command,clipped_lateral_vel_command,clipped_angular_vel_command])
        
        self.Higher_input = np.concatenate((  (self.base_lin_vel * lin_vel).reshape([1,3]),
                                (self.base_ang_vel  * ang_vel).reshape([1,3]),
                                np.array([[self.roll, self.pitch]]),
                                (self.commands[:3] * commands_scale).reshape([1,3]),
                                ((self.dof_pos - self.default_joints) * dof_pos).reshape([1,self.ac_size_walk_model]),
                                (self.dof_vel * dof_vel).reshape([1,self.ac_size_walk_model]),
                                (np.array(self.contacts_floor)).reshape([1,8]),
                                self.actions_walk_model.reshape([1,self.ac_size_walk_model])
                                ),axis=-1)
     
        if self.args.jit_model:
            concatenate_part_r1=torch.as_tensor(np.array([self.Higher_input]), dtype=torch.float32).unsqueeze(dim=0)[0]
            self.Lower_action = self.spot_pol(concatenate_part_r1).detach().numpy()
        else:
            self.Lower_action = self.spot_pol.step(torch.tensor(np.array(self.Higher_input).astype(np.float32)), stochastic=False)[0]
            










