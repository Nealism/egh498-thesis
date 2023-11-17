from cmath import e
from copy import deepcopy
import numpy as np

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



#Currently, we are commenting our work on inlation radius. We will consider our inflation radius work before testing phase.
#Inflation radious code are specified some in reset, some in reward function and mostly in observation.

class Env(EnvBasePB):
    terrain_size = im_size = [1,100,100]
    
    def __init__(self, PATH=None, args=None, writer=None):

        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True
        Initial_distance_to_goal=0
        
        self.prev_dist_to_goal= Initial_distance_to_goal

        
        

        super().__init__(PATH)

        self.reward_fn_name = f'get_reward_{self.args.reward_fn}'
        #self.obs_fn_name = f'get_hlp_obs_{self.args.obs_fn}'
        self.reset_fn_name = f'reset_{self.args.reset_fn}'
        self.step_fn_name = f'step_{self.args.step_fn}'

        self.simStep = 1/240
        self.timeStep = 1/120
        if "pumpkin" in self.args.env:
            self.ac_size = 22
            self.ob_size = 7
        else:
            self.ac_size = 2
            if self.args.static_robots > 1:
                self.ob_size = 18
            elif self.args.obstacle_avoidance:
            
                self.ob_size = 16+3*(self.args.num_robots-1)
                
            elif self.args.gap_avoidance:
                
                self.ob_size = 26+3*(self.args.num_robots-1)
            
            else:
                self.ob_size = 6+3*(self.args.num_robots-1)
        self.Kp = 400
        self.initial_Kp = self.Kp
        
        

        if self.args.obstacle_avoidance and self.args.collision_likelihood_curr or self.args.cur:
            self.a=5.0
            self.b=0.5
        else:

            self.a=0.0
            self.b=0.0
            
        if self.args.gap_avoidance  and self.args.gap_curr or self.args.cur:
            #parameters for gap curr
            self.max_gap_width=2.5
            self.decrease_gap_width=self.args.gap_decrease
            self.final_gap_width=1
            #parameters for tunnel curr
            self.max_tunnel_depth = 5
            self.increase_tunnel_depth = 0.2
            
            
        elif self.args.gap_avoidance:
            self.max_gap_width=0.6
            self.decrease_gap_width=0
            self.max_tunnel_depth = 0.1
            self.increase_tunnel_depth = 0.1
            

        # if self.args.gap_avoidance and self.args.cur and self.args.tunnel_curr:
            
        # elif self.args.gap_avoidance:
        #     self.max_tunnel_depth=20
        #     self.increase_tunnel_depth=0


   
        

        if self.args.cur or self.args.region_curr:
            self.initial_goal_dist=3	
            self.max_goal_dist=10
        else:
            self.initial_goal_dist=15
            self.max_goal_dist=15
        
        self.action_multiplier = 0.1 

        # Needed if importing as Gym environment--  spaces.Discrete(self.ac_size) 
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        
        self.steps = -1
        
        self.reward_names = ["Reward/goal", "Reward/heading", "Reward/heading_obs", "Reward/neg"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 
    
        self.env_exp = None
        self.target_speed = 1.0
        self.target_yaw = 0.0
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
        #self.done = False

        # States that we want to restore, for resuming training after running a test
        self.states_to_restore = ["pos", "orn", "joints", "base_vel", "joint_vel", "args", "episodes", "steps", "total_steps"]

        # Things we want to log each training step (print and add to tensorboard)
        #self.log_things = {"Kp": self.Kp, "Success": self.cur_success, "Dist": self.max_disturbance, "Diffficulty": self.terrain_difficulty}

        self.load_robot()

        


    # def load_terrains(self):
    #     """
    #     Generates all Terrain objects for this environment and adds them to the terrains array.

    #     NOTE: By default, always load the ground truth
    #     NOTE: can optionally create other terrains 
    #     """
    #     # generate and load ground truth image
    #     gt_arr = self.terrain_generator.gen_rand_ground_truth(0, 255, self.cfg.terrain.gt_img_dim)
    #     gt_path = self.get_parent_dir(self.model_path)
    #     gt_name = f"ground_truth_{str(self.rank)}"
    #     gt_position = self.terr_cfg.hf_centre_pos
    #     gt_size = (*self.terr_cfg.gt_mj_dim, self.terr_cfg.hf_elev, self.terr_cfg.hf_depth)

    #     self.ground_truth = Hfield(gt_arr, gt_path, gt_name, gt_position, gt_size) 
    #     self.terrains.append(self.ground_truth)

    def load_specific_robot(self):

        if "pumpkin" in self.args.env:
            self.load_urdf_robot("./assets/urdfs/pumpkin.urdf")
            self.contact_list = ['pumpkin_chassis', 'pumpkin_lower_chassis']
        else:
            #state_object= [random.uniform(-4,4),random.uniform(4,1),0.00]
            robot1=self.load_urdf_robot("./assets/urdfs/dynamic_titan.urdf")
            self.contact_list = ['titan_chassis', 'left_11_wheel', 'right_11_wheel','left_1_wheel', 'right_1_wheel']
            if self.args.static_robots > 1 and self.args.insert_robot2:
                robot2=self.load_urdf_robot2("./assets/urdfs/dynamic_titan.urdf")
            if self.args.insert_box:
                wall_dir= "Wall_URDF/"
                self.square = p.loadURDF(wall_dir + "square.urdf", [0,2,0.5], useFixedBase=True)
            #robot2=self.load_urdf_robot("./assets/urdfs/dynamic_titan.urdf")
            self.contact_list2 = ['titan_chassis', 'left_11_wheel', 'right_11_wheel','left_1_wheel', 'right_1_wheel']
            wall_dir= "Wall_URDF/"
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
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "RC_Initial Distance to Goal": self.initial_goal_dist, "GC: Gap Width":self.max_gap_width-self.decrease_gap_width, "TC: Tunnel Width":self.increase_tunnel_depth,"CLC: distance between obstacle and path": self.a-self.b, "EC: Kp": self.Kp }
        elif self.args.gap_avoidance:
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "EC: Kp": self.Kp, "GC: Gap Width":self.max_gap_width-self.decrease_gap_width, "TC: Tunnel Width":self.increase_tunnel_depth}
        else:
            return_dict = {"Curriculum Success": self.cur_success, "Goal Success": self.ep_goal_success, "RC_Initial Distance to Goal": self.initial_goal_dist, "EC: Kp": self.Kp }

        return_dict.update(self.reward_dict)
        return return_dict

    

    def get_success(self):
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        #print("success_dist",dist_to_goal)
        # print(self.dist_to_wp)
        # print("d",dist_to_goal)
        if self.args.cur_succ==1:
            return self.total_reward > 700
        elif self.args.cur_succ==2:
            return dist_to_goal < 1.0
        elif self.args.cur_succ==3:
            return self.total_reward > 500
        elif self.args.cur_succ==4:
            return self.total_reward > 200
        elif self.args.cur_succ==5:
            return self.total_reward > 700
        elif self.args.cur_succ==6:
            return self.total_reward > 1000
        elif self.args.cur_succ==7:
            return self.total_reward > 1200
        elif self.args.cur_succ==8:
            return self.total_reward > 1350
        elif self.args.cur_succ==9:
            return self.total_reward > 2000
    

    def check_for_success(self):
        return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()

    def reset(self, terrain=None, test=False, restore_state=None):
        
        #self.load_simulator()
        #p.resetDebugVisualizerCamera(cameraDistance=10, cameraYaw=0, cameraPitch=-40, cameraTargetPosition=[0.55,-0.35,0.2])
        self.intersection_r1_box= False
        self.intersection_r1_r= False
        Initial_distance_to_goal=0
        
        self.prev_dist_to_goal= Initial_distance_to_goal

        if self.steps > 0:
            for key in self.reward_dict:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        if self.episodes > -1:

            self.success.append(self.get_success())
            #print("SUCCESS________________________________________",self.success)
            self.ep_success = self.get_success()
            #print("Episdoe_Succ", self.ep_success)			
            self.cur_success.append(self.ep_success)
            self.ep_goal_success = np.mean(self.goal_success) if self.goal_success else 0.0

        self.goal_success = []
        #print("GOAL", self.ep_goal_success)
        #print("cur",self.cur_success)
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

        #Robot1
        # initial_x, initial_y = np.random.uniform(-3, 3), np.random.uniform(3, 3.5) 
        initial_x, initial_y = np.random.uniform(0,4), np.random.uniform(0, 4) 
        #initial_x, initial_y = -2, -2 
        self.initial_yaw = np.random.uniform(-np.pi, np.pi) 
        self.initial_orn = p.getQuaternionFromEuler([0,0,self.initial_yaw])
        self.z_offset = 0

    
        ######___________ALL CURRICULUM STAGES ARE HERE__________________##################################################
        
        #########____EXPERT/GUIDED_CURRICULUM__########    

        if (self.args.cur or self.args.expert_curr) and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
            self.cur_success = deque([0.0], maxlen=5)
        
        #REGION_CUrriculum: Increasing Distance to Goal Gradually
        if (self.args.cur or self.args.region_curr) and self.check_for_success() and self.initial_goal_dist <= self.max_goal_dist:
            #self.initial_goal_dist=self.initial_goal_dist+self.increase_goal_dist
            #print(self.initial_goal_dist,self.max_goal_dist)
            # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
            self.initial_goal_dist +=1 # = 0
            self.cur_success = deque([0.0], maxlen=5)
                #print("cur_success", self.cur_success)			
            
        

        #GAP_CUrriculum: Reducing Gap Width Gradually
        if self.args.gap_avoidance and (self.args.cur or self.args.gap_curr) and self.check_for_success():
            #if self.max_gap_width-self.decrease_gap_width - self.final_gap_width == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                #self.decrease_gap_width = self.max_gap_width
            if self.max_gap_width-self.decrease_gap_width == self.final_gap_width:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                self.decrease_gap_width = self.max_gap_width-self.final_gap_width
                self.cur_success = deque([0.0], maxlen=5)
                #print("cur_success", self.cur_success)			
            else:
                self.decrease_gap_width += self.args.gap_decrease			
                
                self.cur_success = deque([0.0], maxlen=5)
                
        #Tunnel_CUrriculum: Increasing the Tunnel/Gap length Gradually
        if self.args.gap_avoidance and (self.args.cur or self.args.tunnel_curr) and self.check_for_success():
            if self.max_tunnel_depth-self.increase_tunnel_depth == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
                self.increase_tunnel_depth = self.max_tunnel_depth
                self.cur_success = deque([0.0], maxlen=5)
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
            # pos2, orn2, self.joints, self.base_vel, self.joint_vel = [initial_x2, initial_y2, self.z_offset+0.31],self.initial_orn2, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
            self.set_position(pos, orn, robot_id=self.Id)
            #self.h=0

        # Function to move the goal and the static robot
        self.move_goal_and_static_robot(initial_x=pos[0], initial_y=pos[1], yaw=self.initial_yaw)
        
        # print("robot_positions", pos2)
        # print("robot_state")
        # print(self.state_robot2)
        self.lineId_heading = -1
        self.lineId_side1 = -1
        self.lineId_side2 = -1
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
        self.lineIdgap=[-1]*4
        self.lineIdA=[-1]*4
        self.lineIdB=[-1]*4
        self.lineIdWall=[-1]*4
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

        self.gapwp1_reach=0
        self.gapwp2_reach=0

        

        
        if self.args.gap_avoidance:
            #THIS PART IS NEEDED FOR SETTING ORIENTATION OF GAP WITH THE MID LINE
            self.line1_start=(pos[0], pos[1])
            self.line1_end=(self.state_goal[0], self.state_goal[1])
            self.line1_angle=self.perpendicular_angle(self.line1_start,self.line1_end)
            #print("angle",self.line1_angle)
            self.line_orn=(0.0,0.0, self.line1_angle,0.1)
            
            #Set the Gap width taken from the gap curriculum in reset
            self.gap_width=self.max_gap_width-self.decrease_gap_width
            #print("Gap_Width",self.gap_width,"Decrease_gap",self.decrease_gap_width)
            
            #Set the Tunnel/Gap Depth from the Tunnel Curriculum in reset
            self.tunnel_depth= self.increase_tunnel_depth

        
            

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


    def move_goal_and_static_robot(self, initial_x, initial_y, yaw):

        # Get a new goal position, make sure it is far enough away from the robot. 
        #state_object=[np.random.uniform(-7, 7), np.random.uniform(-8, -6), 0.00]
        robot1_pos=(initial_x, initial_y)
        state_object=self.find_position_B(robot1_pos, self.initial_goal_dist, random.randint(0, 360))
        dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)
        #print(dist)
        # print(self.initial_goal_dist)
        while dist < 3:
            state_object=self.find_position_B(robot1_pos, 8, random.randint(0, 360))
            dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)

        # Estimate time to target, velocity in steps + time to turn + current steps + buffer for going around a robot / acceleration
        # Keep an eye on this, need to make sure there's enough time to get to the goal
        self.heading_error, _ = self.calc_angle_error(state_object, [initial_x, initial_y], yaw)
        self.time_to_target = dist / self.timeStep + abs(self.heading_error) / self.timeStep + self.steps + 500000
        #print(self.time_to_target)
        
        #Equation of the line trajectory from moving robot to goal
        if (initial_x-state_object[0])==0:
            initial_x=state_object[0]+0.01
            print("DENOM_ZERO")

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


    def twist_to_tracks(self, actions):
        radius = 0.14
        width = 0.78/2
        #print(actions)
        lin_vel = actions[0]
        ang_vel = actions[1]
        w_r = (lin_vel + ang_vel*width)/radius
        w_l = (lin_vel - ang_vel*width)/radius
        return [w_l, w_r]
    
    #def step(self, actions):
        #print("AAA",actions)
        #print(self)
        # actions=[2.5,5]

        # actions = 0.5*actions
        # ===========================
        # This is an expert functionexper
        # ===========================
    def motor_action(self,actions):
        #print("motor action",actions)
        exp_actions = [0.0]*2
        # ##########################__RAY_LINE___###################
        #if self.args.num_robots > 1:
        # 	if self.hit[0] == True:
        # 		exp_actions[0] = 0.0
        # 		exp_actions[1] = -0.5
        # 	elif self.hit[1] == True:
        # 		exp_actions[0] = 0.0
        # 		exp_actions[1] = 0.5
        # 	elif abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
        # 		exp_actions[0] = 0.25
        # 		exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        # 	else:	
        # 		exp_actions[0] = 0.0
        # 		exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        # if self.args.gap_avoidance:
        # ####################_______WAY_POINT_ATTEMPT_FAILED______######################
        #     if (self.intersection_line_gap_wall1== True or self.intersection_line_gap_wall2==True) and abs(self.heading_error) < 1.6: 
                
        #         exp_actions[0] = 0.1
        #         exp_actions[1] = 0.5#*np.clip(self.heading_error_wp1, -1, 1)
                
        #     elif (self.intersection_headingcorner1_gap_wall1 == True or self.intersection_headingcorner1_gap_wall2 == True) and abs(self.heading_error) < 1.6:
        #         exp_actions[0] = 0.05
        #         exp_actions[1] = -0.5	
        #     elif (self.intersection_headingcorner2_gap_wall1 == True or self.intersection_headingcorner2_gap_wall2 == True) and abs(self.heading_error) < 1.6:
        #         exp_actions[0] = 0.05
        #         exp_actions[1] = 0.5
        #     elif abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
        #         exp_actions[0] = 0.25
        #         exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        #     else:	
        #         exp_actions[0] = 0.0
        #         exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)

        if self.args.gap_avoidance:
        # ####################_______WAY_POINT_SYSTEM______#####
            if self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2 or self.intersection_r1_r:
                exp_actions[0] = 0
                exp_actions[1] = 0
            else:
                exp_actions[0] = 0.08
                exp_actions[1] = 0.5*np.clip(self.heading_error_gapwp1, -1, 1)
                if self.gapwp1_reach>0.5:
                    exp_actions[0] = 0.08
                    exp_actions[1] = 0.5*np.clip(self.heading_error_gapwp2, -1, 1)
                    if self.gapwp2_reach>1:
                        exp_actions[0] = 0.08
                        exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)


    
        elif self.args.obstacle_avoidance :
        # ####################_______WayPoint System Inspired by Bug 2 algorithm______######################
            if self.intersection_r1_box or self.intersection_r1_r:
                exp_actions[0] = 0
                exp_actions[1] = 0
                #print("MAMMMMAAAAAAAAAAAAAAAAAAAAAAA",exp_actions[0],exp_actions[1])

            elif self.intersection_wp2G_obs == None or self.intersection_wp3G_obs == None or self.dist_R12G == None or self.dist_R13G == None or self.dist_R124G==None or self.dist_R134G==None:
                if abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
                    exp_actions[0] = 0.15
                else:	
                    exp_actions[0] = 0.0
                exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)

            elif (self.intersection_wp2G_obs == True and self.intersection_wp3G_obs == False) or (self.intersection_wp2G_obs == False and self.intersection_wp3G_obs == False and self.dist_R13G<self.dist_R12G):
                exp_actions[0] = 0.1
                exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    exp_actions[0] = 0.1
                    exp_actions[1] = 0.5*np.clip(self.heading_error_wp3, -1, 1)
                    if self.wp3_reach>0:
                        exp_actions[0] = 0.1
                        exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                
                    


            elif (self.intersection_wp3G_obs == True and self.intersection_wp2G_obs == False) or (self.intersection_wp2G_obs == False and self.intersection_wp3G_obs == False and self.dist_R12G<self.dist_R13G):
                exp_actions[0] = 0.1
                exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    exp_actions[0] = 0.1
                    exp_actions[1] = 0.5*np.clip(self.heading_error_wp2, -1, 1)
                    if self.wp2_reach>0:
                        exp_actions[0] = 0.1
                        exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                
                    

            elif self.intersection_wp2G_obs == True and self.intersection_wp3G_obs == True and self.dist_R124G<self.dist_R134G:
                exp_actions[0] = 0.1
                exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    exp_actions[0] = 0.1
                    exp_actions[1] = 0.5*np.clip(self.heading_error_wp2, -1, 1)
                    if self.wp2_reach>0:
                        exp_actions[0] = 0.1
                        exp_actions[1] = 0.5*np.clip(self.heading_error_wp4, -1, 1)
                        if self.wp4_reach>0:
                            exp_actions[0] = 0.1
                            exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
                
                    


            elif self.intersection_wp2G_obs == True and self.intersection_wp3G_obs == True and self.dist_R134G<self.dist_R124G:
                exp_actions[0] = 0.1
                exp_actions[1] = 0.5*np.clip(self.heading_error_wp1, -1, 1)
                if self.wp1_reach>0:
                    exp_actions[0] = 0.1
                    exp_actions[1] = 0.5*np.clip(self.heading_error_wp3, -1, 1)
                    if self.wp3_reach>0:
                        exp_actions[0] = 0.1
                        exp_actions[1] = 0.5*np.clip(self.heading_error_wp4, -1, 1)
                        if self.wp4_reach>0:
                            exp_actions[0] = 0.1
                            exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)

            
                
                    


        # ####################_______BUG_1_intersection_only______######################
            # if self.intersection_line_square== True and abs(self.heading_error) < 1.6: 
            #     # self.square_bigbox=self.bbox_generator_box(3,0.035,self.pos2,self.orn2,self.lineId_box1big)
            #     # self.square_bigbox.append(self.square_bigbox[0])
            #     # self.corner_robot1 = [(tuple(self.robot1_bbox[0])),(tuple(self.robot1_bbox[1]))]
            #     # self.corner_square_bigbox= [(tuple(self.square_bigbox[0])),(tuple(self.square_bigbox[1])),(tuple(self.square_bigbox[2])),(tuple(self.square_bigbox[3]))]
            #     # _,_,self.way_point1,self.way_point2= self.min_distance_corners(self.corner_robot1 , self.corner_square_bigbox)
            #     # self.heading_error_wp1, _ = self.calc_angle_error(self.way_point1, self.pos, self.yaw)
            #     # self.heading_error_wp2, _ = self.calc_angle_error(self.way_point2, self.pos, self.yaw)
            #     exp_actions[0] = 0.1
            #     exp_actions[1] = 0.5#*np.clip(self.heading_error_wp1, -1, 1)
            #     # if self.args.obstacle_avoidance:
            #     # 	exp_actions[0] = 0.2
            #     # 	exp_actions[1] = 0.5*np.clip(self.heading_error_wp2, -1, 1)
            # elif self.intersection_corner1_square == True and abs(self.heading_error) < 1.6:
            #     exp_actions[0] = 0.05
            #     exp_actions[1] = -0.5	
            # elif self.intersection_corner2_square ==True and abs(self.heading_error) < 1.6:
            #     exp_actions[0] = 0.05
            #     exp_actions[1] = 0.5
            # elif abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
            #     exp_actions[0] = 0.25
            #     exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
            # else:	
            #     exp_actions[0] = 0.0
            #     exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)

        ######################____OLD_IS_GOLD___#################################

        # 	if abs(self.heading_error) < 0.5 and self.dist_r1_r2 >1.5 and self.dist_to_wp > 1.0:
        # 		exp_actions[0] = 0.25
        # 		exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
            
        # 	elif abs(self.heading_error) < 1.5 and self.dist_r1_r2 <1.5 and self.dist_to_wp > 1.0:
        # 		exp_actions[0] = 0.04
        # 		exp_actions[1] = -0.5*np.clip(self.heading_error_obs, -1, 1)
        # 	else:	
        # 		exp_actions[0] = 0.0
        # 		exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
    
        else:
            if abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
                exp_actions[0] = 0.25
            else:	
                exp_actions[0] = 0.0
            exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
        
        if self.args.just_expert or (self.args.cur or self.args.expert_curr):
            if self.intersection_r1_box or self.intersection_r1_r:
                applied_actions=[0]*2
            else:
                applied_actions = (self.Kp/self.initial_Kp) * np.array(exp_actions)
                if not self.args.just_expert:
                    applied_actions += self.action_multiplier*actions
            
        else:
            if self.intersection_r1_box or self.intersection_r1_r:
                applied_actions=[0]*2
                #print("sss")
            else:
                
                applied_actions = self.action_multiplier*actions
                
                # applied_actions = (self.Kp/self.initial_Kp) * np.array(exp_actions)
                # if not self.args.just_expert:
                #     applied_actions += self.action_multiplier*actions

        #print("action",applied_actions)
        
        # Network now outputs a twist message
        track_actions = self.twist_to_tracks(applied_actions)

        for (a, tracks) in zip(track_actions,[self.left_track, self.right_track]):
            for track in tracks:
                p.setJointMotorControl2(self.Id, track, p.VELOCITY_CONTROL, targetVelocity=a*20, force=100)
        
        self.prev_actions = actions

        # p.stepSimulation()

    def return_step(self,actions):
        if self.args.render:
            time.sleep(self.args.sleep)
        self.get_observation()
        self.save_sim_state()
        #reward, done = self.get_reward()
        reward, done = getattr(self, self.reward_fn_name)()

        # Move the waypoint and static robot if close the waypoint
        # print(self.ep_goal_success, self.time_to_target, self.steps, self.dist_to_wp)
        if self.dist_to_wp < 1.0:
            self.move_goal_and_static_robot(self.pos[0], self.pos[1], self.yaw)
            self.goal_success.append(True)
            self.time_to_goal=self.steps
            #print("True_goal",self.goal_success)

        #elif self.time_to_target < self.steps or done:
        elif self.time_to_target < self.steps:
            self.move_goal_and_static_robot(self.pos[0], self.pos[1], self.yaw)
            self.goal_success.append(False)
            #print(self.goal_success)

        self.steps += 1
        self.total_steps += 1
        self.total_reward += reward
        return self.return_state(),reward,done,self.ob_dict
        #print("total_reward",self.total_reward)
        #return np.array(self.robot1_bbox[0] +self.robot1_bbox[1] +self.robot1_bbox[2] +self.robot1_bbox[3] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3] + self.contacts + self.contacts2 + list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped]), reward, done, self.ob_dict
        # return np.array(list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped]), reward, done, self.ob_dict
        
        
        # motor_action(actions)
        # observation,reward,done=return_step(self)
        # return observation, reward, done, self.ob_dict

    def return_state(self):
        #zeros_array = list(np.zeros((4,)))
        self.Other_Robots_pos_list=[]
        for robot_pos_with_IDx in self.robots_pos_with_IDx:
            if str(robot_pos_with_IDx[0])!=str(self):
                other_robot_egocentric_pos = self.world_to_robot(self.yaw, self.pos, robot_pos_with_IDx[1])

                self.Other_Robots_pos_list.append(other_robot_egocentric_pos)
        # print("eject",self.Robots_pos_list,"whole",self.pos)
        # print("ENTIRE",self.robots_pos_with_IDx)
        #print(len(self.Other_Robots_pos_list),"robot_num",self.args.num_robots)
        #print(self,self.Other_Robots_pos_list)

        if self.args.static_robots > 1:
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3])
        
        #Obstacle Avoidance Observations for Multi Robot
        elif self.args.obstacle_avoidance and len(self.Other_Robots_pos_list)==len([0]*3*(self.args.num_robots-1)):    
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel] + self.Other_Robots_pos_list + self.obs_pos_robot+[self.obs_corner1[0],self.obs_corner1[1]]+ [self.obs_corner2[0],self.obs_corner2[1]]+ [self.obs_corner3[0],self.obs_corner3[1]]+ [self.obs_corner4[0],self.obs_corner4[1]])
        #Obstacle Avoidance Observations for Single Robot
        elif self.args.obstacle_avoidance:
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel] + [0]*3*(self.args.num_robots-1) + self.obs_pos_robot+[self.obs_corner1[0],self.obs_corner1[1]]+ [self.obs_corner2[0],self.obs_corner2[1]]+ [self.obs_corner3[0],self.obs_corner3[1]]+ [self.obs_corner4[0],self.obs_corner4[1]])    
        

        elif self.args.gap_avoidance and len(self.Other_Robots_pos_list)==len([0]*3*(self.args.num_robots-1)):
            
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+ self.Other_Robots_pos_list + self.wall1_pos_robot + self.wall2_pos_robot+[self.wall1_corner1[0],self.wall1_corner1[1]]+ [self.wall1_corner2[0],self.wall1_corner2[1]]+ [self.wall1_corner3[0],self.wall1_corner3[1]]+ [self.wall1_corner4[0],self.wall1_corner4[1]]+[self.wall2_corner1[0],self.wall2_corner1[1]]+ [self.wall2_corner2[0],self.wall2_corner2[1]]+ [self.wall2_corner3[0],self.wall2_corner3[1]]+ [self.wall2_corner4[0],self.wall2_corner4[1]])
        elif self.args.gap_avoidance:
            
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+[0]*3*(self.args.num_robots-1) + self.wall1_pos_robot + self.wall2_pos_robot+[self.wall1_corner1[0],self.wall1_corner1[1]]+ [self.wall1_corner2[0],self.wall1_corner2[1]]+ [self.wall1_corner3[0],self.wall1_corner3[1]]+ [self.wall1_corner4[0],self.wall1_corner4[1]]+[self.wall2_corner1[0],self.wall2_corner1[1]]+ [self.wall2_corner2[0],self.wall2_corner2[1]]+ [self.wall2_corner3[0],self.wall2_corner3[1]]+ [self.wall2_corner4[0],self.wall2_corner4[1]])
        elif len(self.Other_Robots_pos_list)==len([0]*3*(self.args.num_robots-1)):
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+self.Other_Robots_pos_list) #+ zeros_array
        else:
            #print(self.wp_pos_robot)
            return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel]+[0]*3*(self.args.num_robots-1)) #+ zeros_array

    def get_reward_1(self):
        """
        Reward Function 1
        """
        #reward = 1.5*np.exp(-2.5*max(0, self.target_speed - self.vx)**2)
        #done = False
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        #print(dist_to_goal)

        # if self.dist_to_robot2 < 2.0:                  #robot1 close to robot 2  distance < x
        # 	goal = np.exp(-0.5*self.dist_to_wp)
        # elif abs(self.heading_error) < 0.5:
        # 	goal = np.exp(-0.5*self.dist_to_wp)
        # else:	
        goal = 0
        if abs(self.heading_error) < 0.5:
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        #heading_obs = np.exp(-0.5*self.heading_error_obs**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 
        # if self.vx > 0 and self.heading_vx > 0:
            # goal = 0.5*np.clip(self.heading_vx, 0, 3)

        # goal = 1.5*np.exp(-10*(0.5 - self.heading_vx)**2)
        # goal = 1.5*np.exp(-10*(3.0 - self.heading_vx)**2)
        # neg = 0.25*self.vx if self.vx < 0 else 0
        # heading_obs = np.exp(-0.5*self.heading_error_obs**2)exper
        #print("goal", goal, "h", heading, "hO", heading_obs, "ng", neg)
        # reward = 1.0 * goal + 0.2 * heading #- 0.2 * heading_obs
        reward = goal + neg + heading
        # reward = goal + heading 
        #print("reward", reward)
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        #self.ep_reward_dict["Reward/heading_obs"] += heading_obs
        
        #print(state_object[0])
        #print("prev",self.prev_dist_to_goal)
        #print(self.prev_dist_to_goal)
        #print((self.steps * self.timeStep)+1)
        # TT= self.steps * self.timeStep + 1
        # print(TT) # time travel per episode ( It is not travel time to goal. I want to stop the robot at the goal. So, I add time of whole episode)
        
        
        
        
        #print(dist_to_goal)
        #fixed_dist_goal=math.sqrt(((3 - self.state_goal[0]) ** 2 + (3 - self.state_goal[1]) ** 2))
        #print("dist_to_goal", dist_to_goal)
        #T= (fixed_dist_goal)*0.75 #Time to reach the goal where 0.75 is the velocity
        
        # reward = 0
        # if dist_to_goal < 0.5:
        #     reward = 100/TT

        #write me a reward function that define shortest possible distance in time

        #print(reward)
        #reward = self.prev_dist_to_goal - dist_to_goal
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        #self.ep_reward_dict["Distance to Goal Improved"] += distance_improve
        #print(distance_improve)
        # print(reward)
        # if dist_to_goal < .2:
        #     reward = 1000/TT
        #print(reward)
        #print((self.steps * self.timeStep)+1,"dist_to_goal", dist_to_goal,"time_to_goal",T, "reward", reward)
        #print("time",T)
        #reward = (max(self.prev_dist_to_goal - dist_to_goal, 0))/TT
        #print(reward)
        #print("difference_in_distance",self.prev_dist_to_goal - dist_to_goal)
        
        self.prev_dist_to_goal = dist_to_goal
        #print(dist_to_goal,self.prev_dist_to_goal)
        #print(self.pos)
        
        #if (self.pos[0] >= 4 or self.pos[0] <= -4 or self.pos[1] >= 4 or self.pos[1] <= -4):
            #done = True
        # Done by reaching goal
        #print("dist",dist_to_goal)
        #print("reward",reward)
        
        #print(self.contacts)


        #######################
        #uncomment this part if inlation radius is used

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            done=True
            print("Hit_Gap_wall",done)
        ######################
        
        if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
            done=True
            #print("Hit_Wall/Contact",done)
        if self.tipped == True:
            done = True
            #print("Tipped",done)

        
        return reward, done

    
    
    #stop turning before moving
    def get_reward_3(self):
        """
        Reward Function 3
        """
       
        done=False
        
        dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
        
        goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        heading = 0.25*np.exp(-0.5*self.heading_error**2)
        neg = 0
        if self.vx < 0:
            neg = 0.25*self.vx 
        
        reward = goal + neg + heading
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            done=True
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            done=True
            print("Hit_Gap_wall",done)
        
            
        return reward, done
    
    
    
    
    
    #Same to 26
    def get_reward_24(self):
        """
        Reward Function 22
        """
       
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
            heading = -0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            done=True
            print("Hit_Gap_wall",done)
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    #Same to reward 30
    def get_reward_25(self):
        """
        Reward Function 22
        """
       
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
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            done=True
            print("Hit_Gap_wall",done)
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    #Real_reward--with reach 1000 and 1st collision
    def get_reward_26(self):
        """
        Reward Function 22
        """
       
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
            heading = -0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Gap_wall",done)

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    
    
    def get_reward_27(self):
        """
        Reward Function 26
        """
       
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
            heading = -2*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -2*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -2*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    def get_reward_28(self):
        """
        Reward Function 26
        """
       
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
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            #done=True
            print("Hit_GAP_WALL-------Hit_Hit",done)

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    

    def get_reward_29(self):
        """
        Reward Function 26
        """
       
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
            heading = -4*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -4*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -4*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    #Real_reward--with reach 1000 and 3rd collision
    def get_reward_30(self):
        """
        Reward Function 22
        """
       
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
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    

    #Real_reward--with reach 1000 and 1st collision
    def get_reward_31(self):
        """
        Reward Function 22
        """
       
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
            reach =2000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    
    
    def get_reward_32(self):
        """
        Reward Function 26
        """
       
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
            reach =2000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -2*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -2*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -2*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    def get_reward_33(self):
        """
        Reward Function 26
        """
       
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
            reach =3000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -3*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    

    def get_reward_34(self):
        """
        Reward Function 26
        """
       
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
            reach =2000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -4*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -4*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -4*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done
    
    #Real_reward--with reach 1000 and 3rd collision
    def get_reward_35(self):
        """
        Reward Function 22
        """
       
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
            reach =2000

        
            
        if self.args.obstacle_avoidance and (self.obs_check or self.obs_check_2 or self.obs_check_3):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_obs**2)
        elif self.args.gap_avoidance and (self.wall1_head or self.wall1_side1 or self.wall1_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall1**2)
        elif self.args.gap_avoidance and (self.wall2_head or self.wall2_side1 or self.wall2_side2):
            goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
            heading = -5*0.25*np.exp(-0.5*self.heading_error_to_wall2**2)
        else:
            if abs(self.heading_error) < 0.5:
                goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
        
        collision=0
        if self.args.obstacle_avoidance and self.intersection_r1_box:   #Multi RObot Collision
            collision= -10000
            done=True
            #print("Hit_Obstacle-------Hit_Hit",done)
        if self.args.gap_avoidance and (self.intersection_r1_gapwall1 or self.intersection_r1_gapwall2):   #Multi RObot Collision
            collision= -10000
            done=True

        reward = goal + neg + heading + collision +reach
        
        

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/neg"] += neg
        self.ep_reward_dict["Reward/heading"] += heading
        
        
        
        
        distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
        
        self.prev_dist_to_goal = dist_to_goal
        

        if self.intersection_r1_r==True: # intersection between robot bbox with other robot bbox
            done=True
            #print("MA Collision----------------")
        if self.args.static_robots > 1 and self.intersection_r1_r2:   #Multi RObot Collision
            done=True
            print("Robot_hit_static_Robot",done)
        
        
        ######################
        
        # if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
        #     done=True
            
        # if self.tipped == True:
        #     done = True
            
        return reward, done


    def get_observation(self):
        
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
        
        if abs(self.orn[0]) > 0.35 or abs(self.orn[1]) > 0.35:
            self.tipped = True
        else:
            self.tipped = False

        #print(self.body_vxyz[0]+self.body_vxyz[1])
        
        
        

        #Between Goal and Robot 1
        self.wp_pos_robot = self.world_to_robot(self.yaw, self.pos, self.state_goal)
        #print(self.wp_pos_robot)
        #print("waypoint_pos", self.wp_pos_robot)
        self.heading_error, self.target_angle = self.calc_angle_error(self.state_goal, self.pos, self.yaw)
        #print("heading_error", self.heading_error)
        self.dist_to_wp = math.sqrt(self.wp_pos_robot[0]**2 + self.wp_pos_robot[1]**2)
        #print("distanc-to_wp", self.dist_to_wp)

        rot_speed = np.array(
        [[np.cos(-self.target_angle), -np.sin(-self.target_angle), 0],
            [np.sin(-self.target_angle), np.cos(-self.target_angle), 0],
            [		0,			 0, 1]]
        )
        self.heading_vx, _, _ = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))

        
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
                if self.intersection_r1_r:
                    break
            # else:
            #     self.intersection_r1_r=True
        
            


        
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
            
            self.gap=self.gap_generator(width=self.gap_width, depth=self.tunnel_depth,height=0.015,pos=self.pos2,wall_length = 20,goal_pos=self.state_goal,lineId=self.lineIdWall,lineIdgap=self.lineIdgap,lineIdA=self.lineIdA,lineIdB=self.lineIdB)
            
            self.gap_point1,self.gap_point2=self.gap[2],self.gap[3]

            

            #Measuring Heading error to different way points
            self.heading_error_gapwp1, _ = self.calc_angle_error(self.gap_point1, self.pos, self.yaw)
            self.heading_error_gapwp2, _ = self.calc_angle_error(self.gap_point2, self.pos, self.yaw)
            
            #Distance to waypoints:
            self.dist_gapwp1=self.distance(self.pos,self.gap_point1)
            self.dist_gapwp2=self.distance(self.pos,self.gap_point2)
            TT1= self.steps * self.timeStep + 1
            T=False
            time=None
            if self.dist_gapwp1<1:
                time=TT1
                T=time==TT1
                #T = True

            
            # print("time",time)
            # print("T",T)
            self.time_to_wp1=0
            if self.dist_gapwp1<2:
                    self.time_to_wp1=self.steps
                    self.gapwp1_reach=self.gapwp1_reach + 1
            self.time_to_wp2=0
            if self.dist_gapwp2<2:
                    self.time_to_wp2=self.steps
                    self.gapwp2_reach=self.gapwp2_reach + 1

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
            
            #Generating Head line and Side Lines
            self.heading_line_end=self.find_position_B(self.pos,distance_d=self.args.detect_distance,angle_degrees=math.degrees(self.yaw))
            self.head_line=(self.pos[0], self.pos[1], 0.34), (self.heading_line_end[0], self.heading_line_end[1], 0.34)

            # self.side_line1_end=self.find_position_B(self.robot1_safe_box[0],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))
            # self.side_line2_end=self.find_position_B(self.robot1_safe_box[1],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))

            # self.side_line1=self.robot1_safe_box[0], (self.side_line2_end[0], self.side_line2_end[1], 0.34)

            # self.side_line2=self.robot1_safe_box[1], (self.side_line1_end[0], self.side_line1_end[1], 0.34)

            self.side_line1_endg=self.find_position_B(self.robot1_bbox[0],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))
            self.side_line2_endg=self.find_position_B(self.robot1_bbox[1],distance_d=self.args.detect_distance/2,angle_degrees=math.degrees(self.yaw))

            self.side_line1g=self.robot1_bbox[0], (self.side_line2_endg[0], self.side_line2_endg[1], 0.34)

            self.side_line2g=self.robot1_bbox[1], (self.side_line1_endg[0], self.side_line1_endg[1], 0.34)
            
            #if self.args.debug:
            # self.lineId=p.addUserDebugLine((self.pos[0], self.pos[1], 0.34), (self.heading_line_end[0], self.heading_line_end[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.06, replaceItemUniqueId=self.lineId_heading)
            # self.lineId=p.addUserDebugLine((self.robot1_bbox[0][0], self.robot1_bbox[0][1], 0.34), (self.side_line2_endg[0], self.side_line2_endg[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.06, replaceItemUniqueId=self.lineId_side1)
            # self.lineId=p.addUserDebugLine((self.robot1_bbox[1][0], self.robot1_bbox[1][1], 0.34), (self.side_line1_endg[0], self.side_line1_endg[1], 0.34), lineColorRGB=[0, 0, 1], lineWidth=50, lifeTime=0.06, replaceItemUniqueId=self.lineId_side2)
            
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

            # print(self.pos2)
            # print(self.obs_pos_robot)

    def set_obstacles(self, list_of_obs_bbox):
        self.obstacles=list_of_obs_bbox
    
    def set_robot_bbox(self, list_of_robot_bbox):
        self.robots_bbox=list_of_robot_bbox

    def set_allrobot_positions(self, list_of_allrobot_positions):
        self.robots_pos_with_IDx=list_of_allrobot_positions
        



    def world_to_robot(self, robot_yaw, robot, world):
        x,y = world[0] - robot[0], world[1] - robot[1]                       #longitudinal distance
        rot_mat = np.array([[np.cos(robot_yaw), np.sin(robot_yaw)],          #rotational distance
                             [-np.sin(robot_yaw), np.cos(robot_yaw)]])
        return list(np.dot(rot_mat, np.array([x, y])))

    def calc_angle_error(self, world, robot, angle):
        target_angle = np.arctan2(world[1] - robot[1], world[0] - robot[0])
        #print("target",target_angle)
        if ( target_angle < 0 and angle > 0 ):
            angle_error = ( 2*np.pi + target_angle ) - angle
        elif ( target_angle > 0 and angle < 0 ):
            angle_error = target_angle - ( 2*np.pi + angle )
        else:
            angle_error = target_angle - angle

        if angle_error > np.pi:
            angle_error = np.pi - angle_error
        elif angle_error < -np.pi:
            angle_error = angle_error - np.pi

        return angle_error, target_angle

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
            if self.args.debug:
                    lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB, lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
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

    def bbox_generator_box(self,radius,height,pos,orn,lineId):
     
        x=(0.5/2)+radius
        y=(0.5/2)+radius
        z=height
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
            lineId[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=lineId[i])
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
            print(object_bbox)

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
                        print("Denominator_Zero")
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

        line_direction = [goal_pos[0] - pos[0], goal_pos[1] - pos[1], 0]
        perpendicular_direction = [line_direction[1], -line_direction[0], 0]
        orn = p.getQuaternionFromEuler([0, 0, math.atan2(perpendicular_direction[1], perpendicular_direction[0])])
        #------------------------------------
        x=width+wall_length
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
        
        x=width
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
        P1=self.calculate_opposite_point(PP1,PP2,distance=2.5)
        P2=self.calculate_opposite_point(PP2,PP1,distance=2.5)
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
        # print("r1",robot1_bbox)
        # print("r2",robot2_bbox)
        corners=robot2_bbox
        
        rectangle_id1=self.create_rectangle(robot2_bbox,wall_length,depth,0.34/2,orn)
        rectangle_id2=self.create_rectangle(robot3_bbox,wall_length,depth,0.34/2,orn)
        # p.createMultiBody(
        #     baseMass=1,
        #     baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_BOX, halfExtents=[length/2, width/2, height/2]),
        #     basePosition=[position_x, position_y, height / 2],
        #     baseOrientation=p.getQuaternionFromEuler([0, 0, yaw]),
        # )

        return robot2_bbox,robot3_bbox,WP1,WP2
    
    def create_rectangle(self,corners,wall_length,wall_width,wall_height,orientation):

        # Calculate the center and half extents of the rectangle
        #half_extents = [(corners[2][i] - corners[0][i])/2 for i in range(3)]
        
        center = [(corners[0][i] + corners[2][i]) / 2 for i in range(3)]
        half_extents=[((wall_length/2)), wall_width, wall_height/2]
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
                
    
