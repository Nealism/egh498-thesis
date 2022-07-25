import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
import numpy as np
import time
from collections import deque
import rospy
from sensor_msgs.msg import JointState, Imu, PointField, PointCloud2, Image
import sensor_msgs.point_cloud2 as pc2
from gazebo_msgs.srv import SetModelState, SetModelConfiguration
from gazebo_msgs.msg import ModelState, ModelStates
from geometry_msgs.msg import Twist, TwistStamped, Vector3, Quaternion, Pose
from std_srvs.srv import SetBool, Empty, Trigger
from std_msgs.msg import Float64, Header, String
from sensor_msgs.msg import Image
from multiagent_msgs.msg import RobotStatus
from nav_msgs.msg import OccupancyGrid
from rasg_nav_msgs.msg import DensePointCloud2, TopometricWaypointActionGoal
import cv2
from scipy.spatial.transform import Rotation
import ros_numpy
from assets.obstacles_gz import Obstacles
# from height_map import HeightMap
from height_map import HeightMap
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
# import ros_numpy
from cv_bridge import CvBridge
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
np.set_printoptions(precision=3, suppress=True)

# from rospy.numpy_msg import numpy_msg
# from rospy_tutorials.msg import Floats
# import tf_conversions

class Env():
    # dt = 1/2
    dt = 1/10
    # Target is 10Hz, but running sim at double speed, so sim length is 1/20
    # dt = 1/20
    # dt = 1/200
    vx_target = 0.5
    # im_size = [120,120,1]  
    # num_stacked = 1
    # im_size = [60,60,1]  
    # im_size = [80,80,1]  
    aux_size = 6
    steps = 0
    total_steps = 0
    episodes = 0
    tipped = False
    max_action = np.array([0.5, 0.5])
    resolution = 0.1
    def __init__(self, PATH=None, args=None, rank=0, gap_detector=None):
        self.PATH = PATH
        self.args = args
        self.rank = rank
        self.gap_detector = gap_detector
        self.num_workers = comm.Get_size()
        self.difficulty = self.args.difficulty
        self.use_wp = False
        self.use_z = False
        # self.use_z = True
        # self.use_terrain = False
        self.use_terrain = True
        if self.args.label_bit:
            self.ac_size = 3
        else:
            self.ac_size = 2

        if self.use_wp:
            self.ob_size = 9
        else:
            if not self.args.vis:
                # self.single_ob_size = 11 
                # if self.gap_detector is not None:
                if self.args.use_gaps:
                    # self.single_ob_size = 7 + 64
                    if self.use_z:
                        self.single_ob_size = 9 + 32
                    else:
                        self.single_ob_size = 9 + self.args.aux_size
                else:
                    self.single_ob_size = 9 + self.args.aux_size
            else:
                # if args.subt_om:
                #     self.single_ob_size = 11
                # else:
                # self.single_ob_size = 11
                if self.args.train_detector:
                    self.detect_ob_size = 9
                self.single_ob_size = 7
            self.ob_size = self.single_ob_size * self.args.stacked

        if self.args.vis_type == "depth":
            self.im_size = self.single_im_size = [64,64,1]
        else:
            if args.subt_om:
                self.single_im_size = [120,120,1]
                self.im_size = [120*self.args.stacked, 120, 1]
            else:
                # self.single_im_size = [60,60,1]
                self.im_size = self.single_im_size = [80,80,1]
                # self.im_size = [self.single_im_size[0]*self.args.stacked, self.single_im_size[1], 1]

        self.robot_name = 'r' + str(self.rank + 1)
        rospy.init_node('titan_rl_node_' + self.robot_name, anonymous=False) 
        
        if self.rank == 0:
            self.pause_sim = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
            self.unpause_sim = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        
        # subcribe_list = ['/' + self.robot_name + '/cmd_vel_stamped']
        # publish_list = ['/' + self.robot_name + '/cmd_vel_stamped']
        self.initialise_subscribers()
        self.initialise_publishers()
        self.initialise_services()
        if self.args.env != 'subt' and self.use_terrain:
            self.obstacles = Obstacles(rank=self.rank, num_workers=self.num_workers, args=self.args)

        self.state = ['roll','pitch','roll_vel','pitch_vel','vx','vy','vz']
        self.ob_dict = {}
        self.ep_rewards = deque(maxlen=5)
        self.total_reward = 0
        self.t1 = time.time()

        self.initial_pos = self.pos_cb = None
        self.initial_orn = self.orn_cb = None
        # self.hm_cb = np.zeros(self.im_size)
        # # self.t1 = time.time()
        # while self.pos_cb is None:
        #     time.sleep(0.0001)
        self.waypoint_pos = self.waypoint_pos_cb = self.pos = self.initial_pos = self.pos_cb
        self.waypoint_orn = self.waypoint_orn_cb = self.orn = self.initial_orn = self.orn_cb
        # self.last_flat_pos = self.pos
        # rot = Rotation.from_quat([self.orn[0], self.orn[1], self.orn[2], self.orn[3]])
        # self.last_flat_yaw = self.yaw = rot.as_euler('xyz', degrees=False)[2]
        # =================================================================
        # DO NOT DELETE - Python quaternion code
        # =================================================================
        # rot = Rotation.from_quat([self.initial_orn[0], self.initial_orn[1], self.initial_orn[2], self.initial_orn[3]])
        # yaw = rot.as_euler('xyz', degrees=False)[2]
        # rot = Rotation.from_euler('xyz', [0, 0, yaw], degrees=False)        
        # self.orn = self.orn_cb = self.initial_orn = rot.as_quat()        
        # =================================================================
        # if self.robot_name == 'r1':
        #     self.pos = self.initial_pos = self.pos_cb = [0,1,0.4]
        # else:
        #     self.pos = self.initial_pos = self.pos_cb = [0,-1,0.4]
        # self.orn = self.orn_cb = self.initial_orn = [0,0,0,1]
        self.y_offset = 15*self.rank
        self.cur_buf = deque(maxlen=3)
        self.prev_min_difficulty = None
        self.min_difficulty = self.difficulty
        self.br = CvBridge()
        self.Kp = 1

        self.avg_vx = deque(maxlen=100)
        self.avg_vx_world = deque(maxlen=100)
        self.avg_yaw = deque(maxlen=100)
        self.next_positions = [i for i in range(self.num_workers*2)]
        self.reached_goal = False

        self.stacked_obs = deque(maxlen=self.args.stacked)
        # self.stacked_imgs = deque(maxlen=self.args.stacked)
        self.goal_num = self.first_goal = 0
        self.goal_reached = False
        self.label = False
        self.pred = False
        self.success = [0]
        self.pitch_coef = 5.0
        

    def reset_robot(self):
        # rosservice call /slam/map/clear_agent "data: 'r1'" 
        # reset_agent_slam_msg = String()
        # reset_agent_slam_msg.string = self.robot_name
        # rospy.wait_for_service(' /slam/map/clear_agent')
        # self.reset_agent_slam(reset_agent_slam_msg)
        # # /slam_atlas_map/clear_agent
        #  service: slam/map/clear

        # Reset agent_interface position
        # 9c
        # self.respawn_locations = {
        #                         1:{'pos':[12, -1, 0.4], 'orn':[0,0,0.2,0.9]},
        #                         2:{'pos':[7.8, -14.8, 0.4], 'orn':[0,0,0.67,0.74]},
        #                         3:{'pos':[13, -33, 0.4], 'orn':[0,0,0.89,0.44]}
        #                         }

        # # if self.args.rand_respawn:
        # # x, y = np.random.uniform(10,20), np.random.choice([np.random.uniform(0,1),np.random.uniform(1,2)])
        # # self.pos = self.initial_pos = [x, y, 0.4]
        # # z = np.random.random()
        # # w = np.sqrt(1 - z**2)
        # # self.orn = self.initial_orn = [0, 0, z, w]
        # if self.robot_name == 'r1':
        #     loc = 3
        # else:
        #     loc = 2
        # self.pos = self.initial_pos = self.respawn_locations[loc]['pos']
        # self.orn = self.initial_orn = self.respawn_locations[loc]['orn']


        
        # Service call to gazebo/
        # self.pos = self.pos_cb = self.initial_pos
        # self.orn = self.pos_orn = self.initial_orn
        sms = ModelState()
        sms.model_name = '_' + self.robot_name
        sms.pose.position.x = self.initial_x
        sms.pose.position.y = self.initial_y
        sms.pose.position.z = self.initial_z 
        sms.pose.orientation.x = self.initial_orn[0]
        sms.pose.orientation.y = self.initial_orn[1]
        sms.pose.orientation.z = self.initial_orn[2]
        sms.pose.orientation.w = self.initial_orn[3]
        # sms.pose.orientation.z = self.initial_orn[2]
        # sms.pose.orientation.w = self.initial_orn[3]
        rospy.wait_for_service('/gazebo/set_model_state')
        try:
            response_model = self.reset_agent_gazebo(sms)
        except: 
            print("Failed to reset pose")

    def reset(self):
        # if self.goal_num > 1:
        #     self.success = [1.0]
        # elif self.goal_num  > 3:
        #     self.success = [2.0]
        # if self.goal_num  > self.first_goal:
        self.switched, self.switched_back, self.detected = False, False, False
                
        if self.args.label_bit or self.args.train_detector:
            self.pred_buffer = []
            if self.pred:
                if self.args.train_detector:
                    # self.success = [self.reached_detect_goal]
                    self.success = [self.goal_reached]
                else:
                    self.success = [self.goal_reached]
        else:
            self.success = [self.goal_reached]
        self.goal_reached = False
        # else:
            # self.success = [0.0]
        
        
        self.publish_actions([0,0]) 

        
        if self.episodes > 0 and self.args.record_step:
            self.save_sim_data()
        else:
            self.sim_data = []

        # self.slow_reset()

        # if self.tipped:
        #     self.slow_reset()
            # self.reset_robot()
        # if self.tipped or self.steps > self.args.horizon*3:
        # self.reset_robot()
        # else:
        # if self.args.env != 'subt':
        #     self.obstacles.delete_model()
        #     self.obstacles.generate_model(difficulty=self.difficulty)
        #     self.t1 = time.time()
        #     self.box_info = self.obstacles.spawn_model()
        #     print("took this long to spawn obstacle", time.time() - self.t1)

        # Random initial position:
        # self.initial_x = np.random.uniform(0, 1)
        # self.initial_y = np.random.uniform( -1,  +1) + self.y_offset
        # self.initial_z = 0.15
        
        # self.initial_orn[0] = 0
        # self.initial_orn[1] = 0
        # self.initial_orn[2] = np.random.uniform(-0.5, 0.5)
        # self.initial_orn[3] = np.sqrt(1 - self.initial_orn[2]**2)

        # max_terrain_difficulty = 1 
        # max_terrain_difficulty = 5
        max_terrain_difficulty = 15
        if self.episodes > 0:
            if not self.args.oct:
                self.cur_buf.append(self.goal_dist < 2.0)
            else:
                self.cur_buf.append(self.reached_goal)

            # self.cur_buf.append(self.pos[0] > (self.x_offset + 10))
            # self.cur_buf.append(self.total_reward > 100)
            # if self.difficulty < 5 and len(self.cur_buf) == 3 and (np.array(self.cur_buf)>((self.difficulty-1)*20 + 10)).all():
            # if self.difficulty < 5 and len(self.cur_buf) == 3 and (sum(self.cur_buf)>(self.x_offset + 10)).all():
            if not self.args.cur and self.difficulty < max_terrain_difficulty and sum(self.cur_buf) == 3:
                self.cur_buf = deque(maxlen=3)
                # %%%%%%%%%%%%%%%%
                # THIS NEEDS TO BE UNCOMMENTED IF YOU WANT TO USE TERRAIN CURRICULUM
                # %%%%%%%%%%%%%%%%
                # self.difficulty += 1
            if self.args.cur:
                # if self.difficulty == max_terrain_difficulty and sum(self.cur_buf) == 3:
                if sum(self.cur_buf) == 3:
                    self.cur_buf = deque(maxlen=3)
                    self.Kp = 0.75*self.Kp
                    if self.Kp < 0.1:
                        self.Kp = 0
                        self.args.cur = False
                # reduce expert curriculum
        # self.ep_Kp = np.random.uniform(max(self.Kp - 0.2, 0), self.Kp)
        self.ep_Kp = self.Kp

        if self.min_difficulty != self.prev_min_difficulty and self.use_terrain:
        
        # if self.episodes % 64 == 0:
            self.cur_buf = deque(maxlen=3)
            self.difficulty = self.min_difficulty
            if self.args.individual:
                self.obstacles.delete_model()
                self.obstacles.generate_model(difficulty=self.min_difficulty, individual=self.args.individual, rank=self.rank)
                self.t1 = time.time()
                self.box_info, self.goals = self.obstacles.spawn_model()
                print(self.rank,  "took this long to spawn obstacle", time.time() -  self.t1) 
                self.goals = self.goals[self.rank]
            else:
                self.box_info = None
                self.goals = None
                self.aux_goals = None
                self.detect_goals = None
                self.small_goals = None
                if self.rank == 0:
                    print("trying to spawn")
                    self.obstacles.delete_model()
                    self.obstacles.generate_model(difficulty=self.min_difficulty)
                    self.t1 = time.time()
                    self.box_info, self.goals, self.aux_goals, self.detect_goals = self.obstacles.spawn_model()
                    print("took this long to spawn obstacle", time.time() - self.t1)        
                    # self.world_pub.publish(self.height_map.world.ravel())
                # Share world map and goals
                self.box_info = comm.bcast(self.box_info, root=0)
                self.goals = comm.bcast([self.goals], root=0)[0]
                self.aux_goals = comm.bcast([self.aux_goals], root=0)[0]
                self.detect_goals = comm.bcast([self.detect_goals], root=0)[0]
                if not self.args.oct:
                    self.goals = self.goals[self.rank]
            # comm.Barrier()
            
            # self.height_map = height_map(self.box_info, self.im_size, grid_size=self.resolution, initial_yaw=self.initial_yaw, robot_pos=[self.initial_x, self.initial_y])
            if self.use_terrain:
                self.height_map = HeightMap(self.box_info, self.single_im_size, grid_size=self.resolution, args=self.args, rank=self.rank)
                self.height_map.map_extents
                self.z_offset = self.height_map.z_offset
            else:
                self.z_offset = 0

        self.prev_min_difficulty = self.min_difficulty
        self.reached_goal = False
        
        # self.initial_x = ((self.difficulty-1)*20 + 12)
        # self.x_offset = (self.difficulty-1)*20
        # if self.use_terrain:
        if self.args.oct:
            # radius = 12
            # radius = 25 - 8
            # dist = 25
            # theta = np.pi * (22.5 * (j + k*(22.5))) / 180

            self.area = self.next_positions[self.rank]
            self.first_goal = np.random.choice([0,2])
            self.goal_num = self.first_goal
            self.goal_x = self.goals[self.area][self.goal_num]['x']
            self.goal_y = self.goals[self.area][self.goal_num]['y']
            theta = np.arctan2(self.goal_y, self.goal_x)
            if self.area < 16:
                k = 0
            else:
                k = 1
            radius = 45*(k*0.75+1)
            self.initial_angle = theta
            # Square
            # Random point inside a square 3.5x3.5 (so we can still see the door)
            # rand_x = np.random.uniform(-3.5, 3.5)
            # rand_y = np.random.uniform(-3.5, 3.5)

            # # Rotate and translate into world frame, centred at 3m back from the goalx and goaly
            # radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 3
            # centre_x = 


            if self.args.train_detector:

                # goal2 = [self.goals[self.area][self.goal_num]['x'], self.goals[self.area][self.goal_num]['y']]
                # goal3 = [self.goals[self.area][self.goal_num + 1]['x'], self.goals[self.area][self.goal_num + 1]['y']]
                
                # rad1 = np.sqrt( goal2[0] * goal2[0] + goal2[1] * goal2[1] ) - 4.0
                # goal1 = [(rad1) * np.cos(theta) + np.sqrt(np.random.uniform(0, 0.5)) * np.cos(np.random.uniform(0.0, 2.0*np.pi)), \
                #         (rad1) * np.sin(theta) + np.sqrt(np.random.uniform(0, 0.5)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))]          

                # rad2 = np.sqrt( goal3[0] * goal3[0] + goal3[1] * goal3[1] ) + 4.0
                # goal4 = [(rad2) * np.cos(theta) + np.sqrt(np.random.uniform(0, 0.5)) * np.cos(np.random.uniform(0.0, 2.0*np.pi)), \
                #         (rad2) * np.sin(theta) + np.sqrt(np.random.uniform(0, 0.5)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))]

                # self.goal_list = [goal1, goal2, goal3, goal4]
                

                if (self.first_goal == 0):
                    self.pred = self.aux_goals[self.area][0]['label']
                    self.door_size = self.aux_goals[self.area][0]['door_size']
                else:
                    self.pred = self.aux_goals[self.area][1]['label']
                    self.door_size = self.aux_goals[self.area][1]['door_size']

                # x_offset = (radius) * np.cos(theta)
                # y_offset = (radius) * np.sin(theta)
                # # ground_size = [15, np.random.uniform(4,6), 1]
                # ground_size = [7.5, np.random.uniform(4,6), 1]

                # if self.first_goal == 0:
                #     x = -ground_size[0]/3 + ground_size[0]*2/3 
                # else:
                #     x = -ground_size[0]/3 + 2*ground_size[0]*2/3  

                # detect_dist = 3.0

                # x1 = x_offset + (x-detect_dist)*np.cos(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.cos(np.random.uniform(0.0, 2.0*np.pi)) 
                # y1 = y_offset + (x-detect_dist)*np.sin(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                # if np.random.random() <= 0.8:
                #     # Second goal on the other side of the door, self.pred should comes from the gz env (if too small == false)
                #     x2 = x_offset + (x+detect_dist)*np.cos(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.cos(np.random.uniform(0.0, 2.0*np.pi)) 
                #     y2 = y_offset + (x+detect_dist)*np.sin(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                # else:
                #     x2 = x_offset + (x-detect_dist)*np.cos(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                #     y2 = y_offset + (x-detect_dist)*np.sin(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                #     self.pred = False
                
                x1, y1 = self.goals[self.area][self.goal_num]['x'], self.goals[self.area][self.goal_num]['y']
                # goal1_radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 4
                goal1_radius = np.sqrt( x1*x1 + y1*y1) - 1.5
                goal1_x = (goal1_radius) * np.cos(theta) + np.sqrt(np.random.uniform(0, 1.5)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                goal1_y = (goal1_radius) * np.sin(theta) + np.sqrt(np.random.uniform(0, 1.5)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))               

                # # if np.random.random() <= 0.75:
                x2, y2 = self.goals[self.area][self.goal_num+1]['x'], self.goals[self.area][self.goal_num+1]['y']
                goal2_radius = np.sqrt( x2*x2 + y2*y2) + 4
                goal2_x = (goal2_radius) * np.cos(theta) + np.sqrt(np.random.uniform(0, 2.5)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                goal2_y = (goal2_radius) * np.sin(theta) + np.sqrt(np.random.uniform(0, 2.5)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))    


            

                # # else:
                # #     goal2_radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 4
                # #     goal2_x = (goal2_radius) * np.cos(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                # #     goal2_y = (goal2_radius) * np.sin(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))    
                # #     self.pred = False

                # print("TRYING RAND GOAL")
                goal1 = [goal1_x, goal1_y]
                goal2 = [goal2_x, goal2_y]

                # goal1 = [self.detect_goals[self.area][self.goal_num]['x'],self.detect_goals[self.area][self.goal_num]['y']]
                # goal2 = [self.detect_goals[self.area][self.goal_num+1]['x'],self.detect_goals[self.area][self.goal_num+1]['y']]

                if self.args.single_wp:
                    self.goal_list = [goal2]
                else:
                    self.goal_list = [goal1, goal2]

                self.goal_list_num = 0

                if self.args.single_wp:
                    radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 1.5
                    self.x_offset = (radius) * np.cos(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.5)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                    self.y_offset = (radius) * np.sin(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.5)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                else:
                    radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 4.5
                    self.x_offset = (radius) * np.cos(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.5)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                    self.y_offset = (radius) * np.sin(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.5)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))    

                theta = np.random.uniform(theta-np.pi, theta+np.pi)

            else:

                # radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 1.5
                # self.x_offset = (radius) * np.cos(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.5)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                # self.y_offset = (radius) * np.sin(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.5)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                # theta = np.random.uniform(theta-1.5, theta+1.5)
            
                radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 1.5
                self.x_offset = (radius) * np.cos(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.0)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                self.y_offset = (radius) * np.sin(self.initial_angle) + np.sqrt(np.random.uniform(0, 1.0)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                theta = np.random.uniform(theta-1.25, theta+1.25)


            # if (self.first_goal == 0):
            #     self.pred = self.aux_goals[self.area][0]['label']
            # else:
            #     self.pred = self.aux_goals[self.area][1]['label']

            # if self.args.label_bit:
            #     # Options are: 50% true (0.8-0.85), goal through door
            #     # 50% false: small goal 25% (0-0.8) and goal through door, or 25% (0-0.85) and goal on this side 
            #     self.pred = True
            #     if (self.first_goal == 0 and self.aux_goals[self.area][0]['size'] >= 0.8) or (self.first_goal == 2 and self.aux_goals[self.area][1]['size'] >= 0.8):
            #         if np.random.random() <= 0.25:
            #             # Same side
            #             self.pred = False
            #         else:
            #             # Goal on other side
            #             self.pred = True
            #     else:
            #         # Too small
            #         self.pred = False

            # if self.area < 16:
            #     # radius = 22
            #     # radius = 45-8
                
            #     radius = 45-10
            #     theta = np.pi * (22.5 * self.area) / 180
            # else:
            #     # radius = 37
            #     # radius = 79-8
            #     radius = 79-10
            #     theta = np.pi * (22.5* (self.area + 22.5)) / 180

            # if theta >= np.pi:
            #     theta = theta - 2*np.pi
            
            # self.goals[self.area][self.goal_num]['x']
            # self.goals[self.area][self.goal_num]['y']
            
            # Rand dist, angle in front, and theta (robot orientation) from goal
            # radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - np.random.uniform(0.0,2.0)
            # radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - np.random.uniform(0.0,3.5)
            # 1.5m from goal
            # radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 3.0
            # radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y ) - 2.0

            
            # radius = np.sqrt( self.goal_x * self.goal_x + self.goal_y * self.goal_y )
            # if 
            # angle = np.random.uniform(theta, theta)
            

            # self.goal_x = 0
            # self.goal_y = 0
            
            # self.goal_num = 0
            # self.goal_num = 1

            self.initial_x = self.x_offset
            self.initial_y = self.y_offset
            self.initial_z = 0.3
            # self.initial_yaw = theta + np.random.uniform(-1.25, 1.25)
            # self.initial_yaw = np.random.uniform(theta-1.5, theta+1.5)
            self.initial_yaw = theta
        
        else:
            self.area = np.random.randint(0,4)
            # else:
            # self.area = 0
            
            self.x_offset = self.area*20
            self.goal_num = 0
            
            
            if self.use_terrain and self.args.cur:
                self.goal_x = self.goals[self.area][self.goal_num]['x']
                self.goal_y = self.goals[self.area][self.goal_num]['y']
            else:
                self.goal_x = 0
                self.goal_y = 0
            
        
        # Random start point
            self.initial_x = 0.2 + np.random.uniform(0.0, 1.0) + self.x_offset
            self.initial_y = np.random.uniform( -1,  1) + self.y_offset
            self.initial_z = 0.3
            # self.initial_yaw = np.random.uniform(-3.0, 3.0)
            self.initial_yaw = np.random.uniform(-1.0, 1.0)
            
        # Straight start point
        # self.initial_x = 0.2 + self.x_offset
        # self.initial_y = self.y_offset
        # self.initial_z = 0.2
        # self.initial_yaw = 0        

        rot = Rotation.from_euler('xyz', [0, 0, self.initial_yaw], degrees=False)        
        self.initial_orn = rot.as_quat()    

        # self.initial_z = self.initial_z + self.z_offset 
        self.initial_z = 0.2
        self.initial_robot_pos = [self.initial_x, self.initial_y, self.initial_z]
        self.reset_robot()

        self.steps = 0
        self.total_reward = 0
        self.episodes += 1
        self.step_sim()
        self.prev_actions = [0]*2
        # self.pos_cb = self.pos
        # self.orn_cb = self.orn
        # self.twist_lin = [0,0,0]
        # self.twist_ang = [0,0,0]
        self.angle_error, self.target_angle = 0, self.initial_yaw
        self.prev_pos = self.pos = self.pos_cb
        rot = Rotation.from_quat([self.orn_cb[0], self.orn_cb[1], self.orn_cb[2], self.orn_cb[3]])
        self.prev_rot = rot.as_euler('xyz', degrees=False)
        self.reached_detect_goal = False
        self.get_observation()
        self.im = self.get_im()
        if self.args.use_gaps or self.args.run_gaps:
            self.z, self.gap = self.gap_detector.step(self.im)
            # self.z, self.gap = [0]*64, [0]*self.aux_size

            # self.im = self.gap
            # self.im = self.z
        self.prev_detected = 0
        self.stacked_obs = deque(maxlen=self.args.stacked)
        # self.stacked_imgs = deque(maxlen=self.args.stacked)

        for _ in range(self.args.stacked):
            
            

            if self.args.use_gaps:
                if self.use_z:
                    self.stacked_obs.append(self.body + list(self.z))
                else:
                    self.stacked_obs.append(self.body + list(self.gap))
            else:
                self.stacked_obs.append(self.body)
            
        
        self.t_test = time.time()
        if self.rank == 0:
            # world_message = np.array(self.im_size + list(self.height_map.world_offset) + list(self.height_map.world.shape) + list(self.height_map.world.reshape([np.prod(self.height_map.world.shape), 1])), dtype=np.float32)
            
            world_message = np.array(self.single_im_size + list(self.height_map.world_offset) + list(self.height_map.world.shape) + list(self.height_map.world.reshape([np.prod(self.height_map.world.shape), 1])), dtype=np.float32)
            self.world_pub.publish(world_message)

        # print(self.rank, np.ravel(np.array(self.goal_list, dtype=np.float32)))
        if self.args.train_detector:
            self.goal_pub.publish(np.ravel(np.array(self.goal_list, dtype=np.float32)))

        # local_goal_list = []
        # for goal in self.goal_list:
            # goal_xyz = self.world_to_robot(self.yaw, self.pos, goal)
            # local_goal_list.append([goal_xyz[0], goal_xyz[1]])
            # goal_message = np.array((self.goal_list), dtype=np.float32)       
        
        # return np.concatenate(self.stacked_obs)

        # if self.use_wp:
        #     return  np.array(self.orn + self.waypoint_orn + [self.dist_to_waypoint])
        # else:
        #     return np.array(self.body)
        # return np.array(self.body), im
        return np.concatenate(self.stacked_obs), self.im

    def step(self, actions, est_aux=None, run_pol=None):
        # actions = [actions[0]/4, actions[1]/4]
        # if self.args.label_bit:
        #     actions = [actions[1], actions[2]]
        #     self.pred = actions[0]
        # else:
            # actions = [actions[0], actions[1]]
        
        if run_pol is not None:
            # if run_pol[0] >= 0.5 and not self.switched and not self.switched_back:
            #     self.switched = True
            #     self.detected = True
            # # self.detected = run_pol[0] > 0.5
            # if self.switched and not self.switched_back and run_pol[0] < 0.5:
            #     self.detected = False
            #     self.switched_back = True
            # self.detected = run_pol[0] > 0.0
            self.detected = self.run_pol = run_pol[0]
            # self.detected = self.run_pol > 3.0
            # self.detected = self.run_pol > 0.
            # if self.args.supervised:
            # self.detected = self.run_pol > 0.5
            # else:
                # self.detected = self.run_pol > 1.0
            
            # if self.pred == True and not self.goal_reached and self.goal_list_num == (len(self.goal_list) - 1):
            #     self.detected = 1
            # else:
            #     self.detected = 0

            # self.detected = False
            if self.detected > 1.0:    
                self.actions = actions
            else:
                self.expert_actions = self.get_expert()
                self.actions = self.expert_actions
            # print(self.actions)
        else:
            self.actions = actions

        # self.actions = [0, 0]
        # self.expert_actions = self.get_expert()
        if self.args.cur:
            if self.pos[0] < (12 + self.x_offset):
                self.actions = [self.actions[0] + self.expert_actions[0], self.actions[1] + self.expert_actions[1]]
                # actions = [np.clip(expert_actions[0], -1.0, 1.0), np.clip(expert_actions[1], -1.0, 1.0)]
            
        self.publish_actions(self.actions) 
        self.step_sim()
        self.im = self.get_im()
        self.get_observation()
        if self.args.use_gaps or self.args.run_gaps:
            self.z, self.gap = self.gap_detector.step(self.im)
            # self.z, self.gap = [0]*64, [0]*self.aux_size
            # self.im = self.gap
        elif self.args.aux or self.args.just_aux:
            self.gap = est_aux
        else:
            self.gap = [0]*self.aux_size
            # self.im = self.z
        reward, done = self.get_reward(actions)
        self.total_reward += reward
        if self.args.record_step: 
            self.record_sim_data()
        self.prev_actions = actions
        self.steps += 1
        self.total_steps += 1
        
        # if self.gap is not None:
        #     est_aux = self.gap
        # if self.steps % 1 == 0:
        if self.steps % 10 == 0:
            
            
            
            # if self.args.subt_om:
            #     # hm_message = np.array([self.pos[0]/self.height_map.grid_size, self.pos[1]/self.height_map.grid_size, self.initial_yaw] + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
            #     # hm_message = np.array([self.pos[0]/self.height_map.grid_size, self.pos[1]/self.height_map.grid_size, 0]  + self.aux + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
            #     # if est_aux is None:
            #         # hm_message = np.array([self.pos[0], self.pos[1], 0]  + self.aux + [0]*self.aux_size + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
            #     # else:
            #     hm_message = np.array([self.pos[0], self.pos[1], 0]  + self.aux + list(self.gap) + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
            # else:
                # hm_message = np.array([self.pos[0]/self.height_map.grid_size, self.pos[1]/self.height_map.grid_size, self.yaw] + self.aux + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
                # if est_aux is None:
                #     hm_message = np.array([self.pos[0], self.pos[1], self.yaw] + self.aux + [0]*self.aux_size + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
                # else:
            hm_message = np.array([self.pos[0], self.pos[1], self.yaw] + self.aux + list(self.gap) + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
            

            self.hm_pub.publish(hm_message)
            # if self.args.train_detector:
            #     if self.args.single_wp:
            #         gl = [self.goal_list[0][0], self.goal_list[0][1], self.goal_list[0][0], self.goal_list[0][1]]
            #     else:
            #         gl = [self.goal_list[0][0], self.goal_list[0][1], self.goal_list[1][0], self.goal_list[1][1]]
            #     goal_message = np.array(gl, dtype=np.float32)
            #     self.goal_pub.publish(goal_message)

        if self.steps % 10 == 0:
            if self.hm_flat():
                self.last_flat_pos = self.pos
                self.last_flat_yaw = self.yaw

        if not self.reached_goal and self.goal_num == 4 and self.goal_dist < 2.0:
        # if not self.reached_goal and self.goal_num >= 2:
            self.reached_goal = True

        if self.args.use_gaps:
            
            if self.use_z:
                self.stacked_obs.append(self.body + list(self.z))
            else:
                self.stacked_obs.append(self.body + list(self.gap))
        else:
            self.stacked_obs.append(self.body)

        
        # return np.concatenate(self.stacked_obs), reward, done, self.ob_dict

        # if self.use_wp:
        #     return np.array(self.orn + self.waypoint_orn + [self.dist_to_waypoint]), reward, done, self.ob_dict
        # else:
        #     # return np.array(self.orn), reward, done, self.ob_dict
        # return np.array(self.body), im, reward, done, self.ob_dict
        
        return np.concatenate(self.stacked_obs), self.im, reward, done, self.ob_dict

    def get_reward(self, actions):
        done = False
        
        # reward = np.exp(-2.5*abs(max(0, 0.5 - self.vx)))
        # multi = self.pos[0] > (6 + self.x_offset)

        # reward = np.exp(-2.5*abs(max(0, 1.0 - self.vx)))
        # # reward = np.exp(-2.5*abs(0.5 - self.vx))
        # # reward = np.exp(-2.5*abs(1.0 - self.vx))
        # if self.vx < 0:
        #     reward -= 0.1*abs(self.vx)
        # # reward += 0.1*(self.pos[0] - self.x_offset)
        # # if self.use_wp:
        # #     # reward = np.exp(-2.5*abs(max(0, 0.5 - actions[0])))
        # #     # reward -= 0.05*actions[1]**2
        # #     reward += 0.1*np.exp(-2.5*np.sum(abs(np.array(self.orn) - np.array(self.waypoint_orn))))
        # #     reward += 0.1*np.exp(-2.5*self.dist_to_waypoint)
        # reward -= 0.001*np.sum((np.array(actions) - np.array(self.prev_actions))**2)
        # reward -= 1.0*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
        # if abs(self.yaw) > 1.5 and self.pos[0] < (12 + self.x_offset):
        #     # reward -= 0.5*self.yaw**2
        
        #     reward -= 0.1*self.yaw**2
        # if self.dist_error > 3:
        #     reward = 2*np.exp(-1.0*(1.0-self.vx)**2)
        # elif self.dist_error == 0:
        #     reward = 0
        # else:
        #     if self.pos[0] < (12 + self.x_offset):
        #         # reward = 2*np.exp(-1.0*self.goal_dist) * self.vx
        #         reward = 2*np.exp(-1.0*self.dist_error) * self.vx
        #         # reward = 2*np.exp(-1.0*self.goal_dist)
        #     else:
        #         # reward = 2*np.exp(-1.0*self.goal_dist) 
        #         reward = 2*np.exp(-1.0*self.dist_error) 
        # if self.pos[0] > (13 + self.x_offset):
        #     reward = 2*np.exp(-2.5*abs(self.vx))
        # else:

        # 250, 12/250
        # target_pos = 15 * (self.args.horizon - self.steps) / self.args.horizon
        # reward = np.exp(-1.0 * (self.goal_dist - target_pos)**2)
        # 
        # reward -= 0.1*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)

        # reward = 2 * np.exp(-2.5*(self.vx)**2)

        # if self.goal_dist < 2.0:
        #     reward = np.exp(-2.5*(self.vx)**2)
        # else:
        #     reward = np.exp(-2.5*(1.0 - self.vx)**2) 
        # reward += np.exp(-1.0*np.sum((np.array(self.initial_orn) - np.array(self.orn))**2))
        

        # reward = np.exp(-2.5*(1.0 - self.target_vx)**2) 
        # # reward += np.exp(-2.5*np.sum((np.array(self.actions) - self.expert_actions)**2)) 
        # # reward = np.exp(-2.5*abs(max(0, 1.0 - self.target_vx)))
        # # if abs(self.angle_error) > 1.6 and self.goal_num != 4:
        
        # 
        # reward -= 0.1*abs(self.angle_error)
        # # reward -= 0.5*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
        # reward -= 0.1*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
        # if self.target_vx < 0:
        #     reward += self.target_vx 
        
        # if self.steps > 50 and (self.target_vx > 0 and self.target_vx < 0.3):
        #     reward -= 0.5*(1.0 - self.target_vx)**2
        
        # Was working? before I fixed the time bug
        # if self.goal_num == (self.first_goal + 1):
        #     reward = 1.75 - (0 - self.vx)**2
        # else:
        #     # if abs(self.door_angle_error) < 1.5707 and self.door_dist < 3.5:            
        #     reward = 1.75 - ((self.vx_target - self.target_vx)/self.vx_target)**2
        #     reward -= 0.2*self.angle_error**2
        #     # else:
        #         # reward = 0.25 - 0.125*(1.0 - self.target_vx)**2
        # if self.vx < 0:
        #     reward += self.vx 
        # reward -= 0.05*self.actions[1]**2



        # x_diff = self.goals[self.area][self.first_goal + 1]['x'] - self.pos[0]
        # y_diff = self.goals[self.area][self.first_goal + 1]['y'] - self.pos[1]
        # goal_dist = np.sqrt(x_diff * x_diff + y_diff * y_diff)
        # reward += np.exp(-0.25*goal_dist**2)
        # reward = 2 - 1.5*(1.0 - self.target_vx)**2
            # reward -= 0.2*abs(self.angle_error)
        
        # reward = 1.0*self.goal_reached
        if self.args.train_detector:
            '''
            Summary of train_detector: 80% of terrains have a big enough gap, 80% of the time the goals go through the gap. Other times either the gap is too small, or the goal is on the same side as where the robot starts. If the robot reaches the final goal, reward is vx = 0, else reward is the target_vx (velocity in the direction of the goal). Also provide a penalty on the self.detected (if the door policy should be used) or not, i.e. pred = false if door is too small or goal is on the same side as the robot, else pred = true if the robot is in the channel (between the two markers). TODO: add rviz markers!!
            '''
            reward = 0
            run_pol = np.clip(self.run_pol, -1, 1)
            if self.args.single_wp:
                if self.pred == True:
                    reward += 1.0 - 1.0*(self.detected - 1.0)**2
                else:
                    reward += 1.0 - 1.0*(self.detected - 0.0)**2
            else:
                if self.pred == True and not self.goal_reached and self.goal_list_num == (len(self.goal_list) - 1):
                    # print("door policy")
                    if self.args.add_reward:
                        reward += 1.5*np.exp(-10*(0.5 - self.target_vx)**2)
                        reward -= 0.1*self.angle_error**2
                    # reward += 1.0 - 1.0*(self.detected - 1.0)**2
                    if self.args.supervised:
                        reward = 2.0
                    else:
                        reward += 1.0 - 1.0*(run_pol - 1.0)**2

                    # reward -= 1.0*(self.detected - 1.0)**2

                # if self.pred == True:
                    # If in the channel
                    # if not self.goal_reached and self.goal_list_num == (len(self.goal_list) - 1):
                    #     if not self.goal_reached:
                            
                        # else:
                        #     reward += 1.5*np.exp(-10*(0.5 - self.vx)**2)
                        #     reward -= 0.1*(self.yaw - self.initial_angle)**2

                    # if not self.goal_reached and self.goal_list_num == (len(self.goal_list) - 1):
                    #     reward -= 0.2*(self.detected - 1.0)**2
                    # else:
                    #     reward -= 0.2*(self.detected - 1.0)**2
                    # reward -= 0.1*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
                else:
                    # print("other controller")

                    # self.detected should be 0
                    # reward -= 1.0*(self.detected - 0.0)**2
                    # angle = np.arctan2(self.goal_list_goal[1], self.goal_list_goal[0])
                    if self.args.add_reward:
                        if self.reached_detect_goal:
                            reward = 1.5*np.exp(-10*(0.0 - self.vx)**2)
                        else:
                            target_rot = np.array(
                                [[np.cos(-self.angle_list_error), -np.sin(-self.angle_list_error), 0],
                                    [np.sin(-self.angle_list_error), np.cos(-self.angle_list_error), 0],
                                    [		0,			 0, 1]]
                                )
                            target_vx, _, _ = np.dot(target_rot, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
                            reward = 1.5*np.exp(-10*(0.5 - target_vx)**2)
                            reward -= 0.1*self.angle_list_error**2
                    if self.args.supervised:
                        reward = -2.0
                    else:
                        reward += 1.0 - 1.0*(run_pol - -1.0)**2
                    
                    # reward -= 0.2*(self.run_pol - 0.0)**2
                    # reward -= 0.2*(self.detected - 0.0)**2


            # reward -= 0.05*self.actions[1]**2
            # reward -= 0.5*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            # reward -= 0.75*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            
            # reward -= 0.75*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            # reward -= 0.001*np.sum((np.array(self.actions) - np.array(self.prev_actions))**2)
            # if self.vx < 0:
            #     # reward += 0.5*self.vx 
            #     reward += 0.25*self.vx 
                
            # if self.prev_detected != self.detected:
            #     reward -= 5
            # self.prev_detected = self.detected




            # dist = np.sqrt(self.goal_list_goal[1]**2 + self.goal_list_goal[0]**2)
            # # reward = 0.5*np.exp(-0.25*dist**2)


            # if self.reached_detect_goal:
            #     reward = 1.5*np.exp(-10*(0.0 - self.vx)**2)
            #     # angle = self.initial_yaw
            #     # reward += 0.5
            # else:
            #     angle = np.arctan2(self.goal_list_goal[1], self.goal_list_goal[0])
            #     target_rot = np.array(
            #         [[np.cos(-angle), -np.sin(-angle), 0],
            #             [np.sin(-angle), np.cos(-angle), 0],
            #             [		0,			 0, 1]]
            #         )
            #     target_vx, _, _ = np.dot(target_rot, (self.vx,0,0))
            #     reward = 1.5*np.exp(-10*(0.5 - target_vx)**2)

            #     # reward += 0.5*np.exp(-2*angle**2)
            
            # if self.pred == True:
            #     if not self.goal_reached and self.goal_list_num == (len(self.goal_list) - 1):
            #         reward -= 0.2*(self.detected - 1.0)**2
            #     else:
            #         reward -= 0.2*(self.detected - 1.0)**2
            #     # reward -= 0.1*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            # else:
            #     # self.detected should be 0
            #     # reward -= 1.0*(self.detected - 0.0)**2
            #     reward -= 0.2*(self.detected - 0.0)**2

            # reward -= 0.5*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)

            # if self.prev_detected != self.detected:
            #     reward -= 5
            # self.prev_detected = self.detected


            # else:
            #         
            #         # self.detected should be 1 if the robot is in the door channel
            #         # reward -= 0.5*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            #         # if self.goal_num == (self.first_goal + 1) and not self.goal_reached:
            #             reward -= 1.0*(self.detected - 1.0)**2
            #             
            #         else:
            #             reward -= 1.0*(self.detected - 0.0)**2
            
            # reward -= 0.2*(self.prev_detected - float(self.detected))**2
            # self.prev_detected = self.detected


            # reward += 0.1*np.exp(-10*(0.5 - self.vx)**2)
            
            # reward += 0.5*self.detected
        else:
            reward = 0
            if not self.goal_reached:
                reward += 1.5*np.exp(-10*(0.5 - self.target_vx)**2)
                reward -= 0.1*self.angle_error**2
            else:
                reward += 1.5*np.exp(-10*(0.5 - self.vx)**2)
                reward -= 0.1*(self.yaw - self.initial_angle)**2

                # THIS IS DIFFERENT FROM WHEN IT WAS WORKING, set to zero if at goal
                # reward += 1.5*np.exp(-10*(0.0 - self.vx)**2)
            
            # reward += np.exp(-0.1*(self.goal_dist)**2)
            # reward += np.exp(-5*(self.angle_error)**2)

            reward -= 0.05*self.actions[1]**2
            # reward -= 0.5*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            # reward -= 0.75*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            # print("this is increased from the last one")
            # reward -= 1.0*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            # reward -= 2.0*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            # reward -= 5.0*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            if self.args.obstacle_type == "gaps":
                reward -= self.pitch_coef*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
            reward -= 0.001*np.sum((np.array(self.actions) - np.array(self.prev_actions))**2)
            if self.vx < 0:
                # old:
                reward += 0.25*self.vx 
                # reward += 0.5*self.vx 
                
    
            if self.args.label_bit:
                # reward -= 0.1*(self.label - self.pred)**2
                self.pred_buffer.append((self.label - self.pred)**2)


        # if abs(self.angle_error) > 1.0:
        #     reward -= 0.1*abs(self.angle_error) 

        # # if self.extra_reward:
        # if self.goal_num > 3:
        #     reward += 1.0
        # elif self.goal_num > 1:
        #     reward += 0.5


        # if self.goal_num == 4:
        #     reward = 2 - 1.5*(1.0 - self.vx)**2
        # else:
        #     reward = 2 - 1.5*(1.0 - self.target_vx)**2
        #     reward -= 0.2*abs(self.angle_error)
        # reward -= 0.2*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
        # reward -= 0.001*np.sum((np.array(self.actions) - np.array(self.prev_actions))**2)


            # if self.target_vx < 0:


            #     reward += self.target_vx 
        
        
        # if time.time() - self.t_test > 0.06:
        #     print(self.rank, self.steps, time.time() - self.t_test)
        # self.t_test = time.time()1

        

        # if abs(self.angle_error) > 1.6 and self.goal_num != 4:
        #     target_vx )
        #     print("greater", self.rank, self.yaw, self.target_angle)
        # else:
        #     
        #     print(self.rank, self.yaw, self.target_angle)

            

        # if self.rank == 4:
            
        
        # if angle_error > 0.2:
        #     reward = angle_error
            # reward -= 0.1*self.angle_error**2
        # reward -= 0.001*np.sum((np.array(actions) - np.array(self.prev_actions))**2)
        
        # reward -= 0.1*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
        
        # self.angle_error = np.arctan2(self.goal_y - self.pos[1], self.goal_x - self.pos[0]) - self.yaw
        # if abs(self.angle_error) < 0.5:
        #     self.dist_error = self.goal_dist
        # else:
        #     self.dist_error = 0
        # reward += np.exp(-1.0*self.goal_dist) 
        
        


        # reward += np.exp(-2.5*abs(max(0, np.array([]) 1.0 - self.vx)))
        
        # if self.steps > self.args.horizon or self.tipped or abs(self.yaw) > 1.5707:
        # if self.steps > self.args.horizon or self.tipped:
        # # if self.steps > self.args.horizon or self.tipped or (self.steps > 500 and np.mean(self.avg_vx) < 0.3):
        #     done = True

            # if self.tipped:
            #     reward = -25
        return reward, done
    
    def get_observation(self):

        # Velocity from temporal differences (need to see if we can get this from somewhere else)
        # self.vx, self.vy, self.vz = [(self.pos_cb[0] - self.pos[0])/self.dt, (self.pos_cb[1] - self.pos[1])/self.dt, (self.pos_cb[2] - self.pos[2])/self.dt] 
        
        self.pos = self.pos_cb
        self.orn = self.orn_cb
        
        self.waypoint_pos = self.waypoint_pos_cb
        self.waypoint_orn = self.waypoint_orn_cb
        # if abs(self.orn[0]) > 0.35 or abs(self.orn[1]) > 0.35:
        


        rot = Rotation.from_quat([self.orn[0], self.orn[1], self.orn[2], self.orn[3]])
        self.roll, self.pitch, self.yaw = rot.as_euler('xyz', degrees=False)
        
        if self.use_wp:
            self.dist_to_waypoint = np.sqrt(np.sum((self.pos[0] - self.waypoint_pos[0])**2 + (self.pos[1] - self.waypoint_pos[1])**2 + (self.pos[2] - self.waypoint_pos[2])**2))
        
        # self.base_rot_vel = self.gz_twist_ang_cb
        # self.body_vxyz = self.gz_twist_lin_cb

        # Finite differences for velocity (unsure if we have access to this through the imu?) Clipped to 2m/s
        self.body_vxyz = np.clip((np.array(self.pos) - np.array(self.prev_pos))/self.dt, -1.5, 1.5)
        self.base_rot_vel = np.clip((np.array([self.roll, self.pitch, self.yaw]) - np.array(self.prev_rot))/self.dt, -np.pi, np.pi)
        self.prev_pos = self.pos
        self.prev_rot = [self.roll, self.pitch, self.yaw]

        self.roll_vel = self.base_rot_vel[0]
        self.pitch_vel = self.base_rot_vel[1]
        self.yaw_vel = self.base_rot_vel[2]

        # rot = np.array(
        # [[np.cos(self.yaw), -np.sin(self.yaw), 0],
        #     [np.sin(self.yaw), np.cos(self.yaw), 0],
        #     [		0,			 0, 1]]
        # )

        # Unsure why this is correct, but seems to be..
        rot = np.array(
        [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
            [np.sin(-self.yaw), np.cos(-self.yaw), 0],
            [		0,			 0, 1]]
        )

        self.vx, self.vy, self.vz = np.dot(rot, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        
        # target_q = Rotation.from_quat([self.initial_orn[0], self.initial_orn[1], self.initial_orn[2], self.initial_orn[3]])
        # self.
        # _, _, self.target_yaw = target_q.as_euler('xyz', degrees=False)

        # target_goal_num = self.goal_num + 1 if self.goal_num < 4 else 4
        # self.target_goal_x = self.goals[self.area][4]['x']
        # self.target_goal_y = self.goals[self.area][4]['y']

        # self.final_angle_error = np.arctan2(self.target_goal_y - self.pos[1], self.target_goal_x - self.pos[0]) - self.yaw
        # self.final_angle_error, self.final_target_angle = self.calc_angle_error(self.goals[self.area][4]['x'], self.goals[self.area][4]['y'], self.pos[0], self.pos[1], self.yaw)


        self.avg_vx.append(self.vx) 
        self.avg_vx_world.append(self.body_vxyz[0]) 
        self.avg_yaw.append(self.yaw) 

        # From pb?
        # rot_speed = np.array([[np.cos(-yaw), -np.sin(-yaw), 0], [np.sin(-yaw), np.cos(-yaw), 0], [0, 0, 1]])
        # vx, vy, vz = np.dot(rot_speed,
        #                 self.robot_body.speed())  # rotate speed back to body point of view

        if abs(self.pitch) > 1.0 or abs(self.roll) > 1.0:
            self.tipped = True
        else:
            self.tipped = False

        if self.args.obstacle_type == "gaps":
            self.goal_x = self.goals[self.area][self.goal_num]['x']
            self.goal_y = self.goals[self.area][self.goal_num]['y']
            x_diff = self.goal_x - self.pos[0]
            y_diff = self.goal_y - self.pos[1]
            self.goal_dist = np.sqrt(x_diff * x_diff + y_diff * y_diff)
            # if self.use_terrain and self.goal_dist < 0.5 and self.goal_num < 4:        
            if self.use_terrain and self.goal_dist < 0.5 and self.goal_num < ( self.first_goal + 1 ):
                
                self.goal_num += 1
                # self.goal_num += 2
                # if self.goal_num > 4:
            #         self.goal_num = 4
                self.goal_x = self.goals[self.area][self.goal_num]['x']
                self.goal_y = self.goals[self.area][self.goal_num]['y']
                x_diff = self.goal_x - self.pos[0]
                y_diff = self.goal_y - self.pos[1]
                self.goal_dist = np.sqrt(x_diff * x_diff + y_diff * y_diff)

            if not self.goal_reached and self.goal_dist < 0.5 and self.goal_num == ( self.first_goal + 1 ):
            # if not self.goal_reached and self.goal_dist < 0.5:
                if self.args.label_bit:
                    if self.label:                        
                        self.goal_reached = True
                else:
                    self.goal_reached = True

            # self.aux = self.get_aux()

            self.goal_x1 = self.goals[self.area][self.first_goal]['x']
            self.goal_y1 = self.goals[self.area][self.first_goal]['y']
            x_diff = self.goal_x1 - self.pos[0]
            y_diff = self.goal_y1 - self.pos[1]
            self.goal_dist1 = np.sqrt(x_diff * x_diff + y_diff * y_diff)
            self.angle_error1, _ = self.calc_angle_error(self.goal_x1, self.goal_y1, self.pos[0], self.pos[1], self.yaw)

            self.goal_x2 = self.goals[self.area][self.first_goal+1]['x']
            self.goal_y2 = self.goals[self.area][self.first_goal+1]['y']
            x_diff = self.goal_x2 - self.pos[0]
            y_diff = self.goal_y2 - self.pos[1]
            self.goal_dist2 = np.sqrt(x_diff * x_diff + y_diff * y_diff)
            self.angle_error2, _ = self.calc_angle_error(self.goal_x2, self.goal_y2, self.pos[0], self.pos[1], self.yaw)

            self.goal_angle1, self.goal_dist1 = self.angle_error1, self.goal_dist1
            self.goal_angle2, self.goal_dist2 = self.angle_error2, self.goal_dist2
            # self.goal_points = [self.goal_angle, self.goal1_dist, self.goal2_angle, self.goal2_dist]

            if self.goal_num >= 2:
                door_num = 1
            else:
                door_num = 0
            door_x, door_y = self.aux_goals[self.area][door_num]['x'], self.aux_goals[self.area][door_num]['y']
            door_angle, door_size = self.aux_goals[self.area][door_num]['yaw'], self.aux_goals[self.area][door_num]['door_size']
            x_diff = door_x - self.pos[0]
            y_diff = door_y - self.pos[1]
            self.door_dist = np.sqrt(x_diff * x_diff + y_diff * y_diff)
            self.door_angle_error, self.door_target_angle = self.calc_angle_error(door_x, door_y, self.pos[0], self.pos[1], self.yaw)

            # if 
            # self.aux = [1.0, self.door_angle_error, self.door_dist, door_angle, size]
            if self.goal_angle2 < 1.0 and self.goal_angle2 > -1.0 and (self.goal_dist2 < 3.5 or self.goal_dist1 < 3.5):

                # pt_before_angle = np.arctan2(pt_before[1],pt_before[0])
                # pt_before_dist = np.sqrt( pt_before[1]*pt_before[1] + pt_before[0]*pt_before[0] )
                # pt_after_angle = np.arctan2(pt_after[1],pt_after[0])
                # pt_after_dist = np.sqrt( pt_after[1]*pt_after[1] + pt_after[0]*pt_after[0] )
                # labels.append([1, door_size, pt_before_angle, pt_before_dist, pt_after_angle, pt_after_dist])
                self.aux = [1.0, door_size, self.goal_angle1, self.goal_dist1, self.goal_angle2, self.goal_dist2]
            else:
                self.aux = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            self.aux = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        goal_x, goal_y = self.goals[self.area][self.goal_num]['x'], self.goals[self.area][self.goal_num]['y']
        self.angle_error, self.target_angle = self.calc_angle_error(goal_x, goal_y, self.pos[0], self.pos[1], self.yaw)

        target_rot = np.array(
        [[np.cos(-self.target_angle), -np.sin(-self.target_angle), 0],
            [np.sin(-self.target_angle), np.cos(-self.target_angle), 0],
            [		0,			 0, 1]]
        )
        self.target_vx, _, _ = np.dot(target_rot, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))


        if self.args.train_detector:

            self.goal_list_goal = self.world_to_robot(self.yaw, self.pos, self.goal_list[self.goal_list_num])
            # self.goal_list_dist = np.sqrt(self.goal_list_goal[0] * self.goal_list_goal[0] + self.goal_list_goal[1] * self.goal_list_goal[1])
            # self.angle_list_error = np.arctan2(self.goal_list_goal[1], self.goal_list_goal[0])
            
            x_diff = self.goal_list[self.goal_list_num][0] - self.pos[0]
            y_diff = self.goal_list[self.goal_list_num][1] - self.pos[1]
            self.goal_list_dist = np.sqrt(x_diff * x_diff + y_diff * y_diff)
            self.angle_list_error, _ = self.calc_angle_error(self.goal_list[self.goal_list_num][0], self.goal_list[self.goal_list_num][1], self.pos[0], self.pos[1], self.yaw)

            if self.goal_list_dist < 0.5 and self.goal_list_num < (len(self.goal_list) - 1):
                self.goal_list_num += 1
                self.goal_list_goal = self.world_to_robot(self.yaw, self.pos, self.goal_list[self.goal_list_num])
                # self.goal_list_dist = np.sqrt(self.goal_list_goal[0] * self.goal_list_goal[0] + self.goal_list_goal[1] * self.goal_list_goal[1])
                # self.angle_list_error = np.arctan2(self.goal_list_goal[1], self.goal_list_goal[0])
                x_diff = self.goal_list[self.goal_list_num][0] - self.pos[0]
                y_diff = self.goal_list[self.goal_list_num][1] - self.pos[1]
                self.goal_list_dist = np.sqrt(x_diff * x_diff + y_diff * y_diff)
                self.angle_list_error, _ = self.calc_angle_error(self.goal_list[self.goal_list_num][0], self.goal_list[self.goal_list_num][1], self.pos[0], self.pos[1], self.yaw)
            elif not self.reached_detect_goal and self.goal_list_dist < 0.5 and self.goal_list_num == (len(self.goal_list) - 1):
                # Reached the final goal
                self.reached_detect_goal = True

            # On side1, and can see goal1
            if self.goal_dist1 < self.goal_dist2 and self.goal_dist1 < 3.5 and abs(self.angle_error1) < np.pi/2:
                self.gaps = np.array([self.door_size, self.angle_error1, self.goal_dist1, self.angle_error2, self.goal_dist2])
            # On side1, and can see goal2
            elif self.goal_dist1 < self.goal_dist2 and self.goal_dist2 < 3.5 and abs(self.angle_error2) < np.pi/2:
                self.gaps = np.array([self.door_size, self.angle_error1, self.goal_dist1, self.angle_error2, self.goal_dist2])
            # On side2, and can see goal2
            elif self.goal_dist1 > self.goal_dist2 and self.goal_dist2 < 3.5 and abs(self.angle_error2) < np.pi/2:
                self.gaps = np.array([self.door_size, self.angle_error2, self.goal_dist2, self.angle_error1, self.goal_dist1])
            # On side2, and can see goal1
            elif self.goal_dist1 > self.goal_dist2 and self.goal_dist1 < 3.5 and abs(self.angle_error1) < np.pi/2:
                self.gaps = np.array([self.door_size, self.angle_error2, self.goal_dist2, self.angle_error1, self.goal_dist1])
            # Gap out of field of view
            else:
                self.gaps = np.array([-1.0,-1.0,-1.0,-1.0,-1.0])
            # self.detect_ob = np.array([self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel, self.goal_list_goal[0], self.goal_list_goal[1]])
            self.detect_ob = np.array([self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel, self.goal_list_dist, self.angle_list_error])

        
        self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel]

        # self.body = [self.vx, self.vy, self.vz, self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel, self.body_xyz[2] - self.z_offset]
        # if not self.args.vis:
        #     if self.args.use_gaps:
        #         # self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel] + self.im
        #         self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel, goal[0], goal[1]] 
        #         # self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel] + list(self.z)
        #     else:
        #         self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel, goal[0], goal[1]] + self.aux
        #     # self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel] + self.goal_points 
        # else:
        #     if self.args.subt_om:
        #         # self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel] + self.goal_points + self.orn
        #         self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel, goal[0], goal[1]] + self.orn
        #     else:
        #         self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel, goal[0], goal[1]] 
        #         # self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel] + self.goal_points 
        # self.body = [self.vx, self.vy, self.vz, self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel, self.yaw]


        # self.hm = self.hm_cb
        # self.vx, self.vy, self.vz = [0,0,0]

        # rot_speed = np.array(
        #   [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
        #     [np.sin(-self.yaw), np.cos(-self.yaw), 0],
        #     [		0,			 0, 1]]
        # )

        # self.contacts = []
        # for contact in self.contact_dict:
        #   self.contacts.append(len(p.getContactPoints(self.Id, -1, self.contact_dict[contact], -1))>0)

        # self.vx, self.vy, self.vz = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        
        # # Policy shouldn't know yaw
        # self.body = [self.vx, self.vy, self.vz, self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel, self.pos[2] - self.z_offset]

    def get_aux(self):
        return self.aux

    def calc_angle_error(self, goal_x, goal_y, pos_x, pos_y, angle):
        target_angle = np.arctan2(goal_y - pos_y, goal_x - pos_x)
        if ( target_angle <= 0 and angle <= 0 ) or ( target_angle >= 0 and angle >= 0 ):
            angle_error = target_angle - angle
        elif ( target_angle <= 0 and target_angle > -np.pi/2 and angle >= 0 ): 
            angle_error = target_angle - angle
        elif ( target_angle >= 0 and angle <= 0 and angle > -np.pi/2 ): 
            angle_error = target_angle - angle
        elif ( target_angle <= 0 and angle >= 0 ):
            angle_error = ( 2*np.pi + target_angle ) - angle
        elif ( target_angle >= 0 and angle <= 0 ):
            angle_error = target_angle - ( 2*np.pi + angle )
        return angle_error, target_angle

    # def calc_angle_error(self, goal_x, goal_y, pos_x, pos_y, angle):
    #     target_angle = np.arctan2(goal_y - pos_y, goal_x - pos_x)
    #     if ( target_angle < 0 and angle < 0 ) or ( target_angle > 0 and angle > 0 ):
    #         angle_error = target_angle - angle
    #     elif ( target_angle < 0 and target_angle > -np.pi/2 and angle > 0 ): 
    #         angle_error = target_angle - angle
    #     elif ( target_angle > 0 and angle < 0 and angle > -np.pi/2 ): 
    #         angle_error = target_angle - angle
    #     elif ( target_angle < 0 and angle > 0 ):
    #         angle_error = ( 2*np.pi + target_angle ) - angle
    #     elif ( target_angle > 0 and angle < 0 ):
    #         angle_error = target_angle - ( 2*np.pi + angle )
    #     return angle_error, target_angle

    def get_expert(self):
        # angle_error = np.arctan2(self.goal_x - self.pos[0], self.goal_y - self.pos[1]) - self.yaw
        # self.target_angle = np.arctan2(self.goal_y - self.pos[1], self.goal_x - self.pos[0])
        # angle = self.yaw 
        # self.angle_error = self.calc_angle_error(self.target_angle, angle)


        # if abs(self.angle_error) < 1.5707 and self.goal_dist < 3.0 and self.goal_dist > 0.25:            
        # if abs(self.angle_error) < 1.5707 and self.goal_dist < 2.5:            
        # Detect door, 1 radian and 5 meters away
        # if abs(self.door_angle_error) < 1.5707 and self.door_dist < 3.5:            
            # self.angle_error, self.target_angle = self.calc_angle_error(self, goal_x, goal_y, pos_x, pos_y, angle):
            # gx, gy = self.goals[self.area][self.goal_num]['x'], self.goals[self.area][self.goal_num]['y']
            # gx1, gy1 = self.goals[self.area][self.goal_num+1]['x'], self.goals[self.area][self.goal_num+1]['y']
            # self.goal_angle = np.arctan2(gy1 - gy, gx1 - gx) 
            # self.aux = [1.0, self.angle_error, self.goal_dist, self.goal_angle, size]
            # self.aux = [1.0, self.door_angle_error, self.door_dist, door_angle, size]
            
            # self.aux = [1.0, door_x, door_y, door_angle, size]
            
            # self.aux = [1.0, self.door_angle_error, self.door_dist, door_angle, size]
            



            # self.est_aux = [1.0, self.door_x - self.pos[0], self.door_y - self.pos[1], door_angle, size]

            # self.aux = [1.0, self.door_angle_error, self.door_dist, door_angle, size]
            
            # if abs(self.angle_error) < 0.25:
            #     self.dist_error = self.goal_dist
            # else:
            #     self.dist_error = 0
        # else:
            # if self.rank == 0:
            #     if abs(self.angle_error) < 1.5707:
            #         print(self.rank, "can't see, further than 2.5", self.goal_dist, self.goal_num)
            #     else:
            #         print(self.rank, "can't see, greater than 1.570", self.angle_error)

            # self.dist_error = 1.0
            # self.angle_error = 0.0
            # self.aux = [0,0,0,0,0]
            # self.target_vx = None
            # self.angle_error, self.target_angle = 0, self.initial_yaw

        # return self.Kp * np.clip( self.dist_error, 0, 1.0), self.Kp * np.clip( self.angle_error, -2, 2)

        # if self.goal_num >= 2:
        #     goal_num = 1
        # else:
        #     goal_num = 0
        # goal_x, goal_y, size = self.aux_goals[self.area][goal_num]['x'],  self.aux_goals[self.area][goal_num]['y'], self.aux_goals[self.area][goal_num]['size']
        # goal_x, goal_y, size = self.aux_goals[self.area][self.goal_num]['x'],  self.aux_goals[self.area][self.goal_num]['y'], self.aux_goals[self.area][goal_num]['size']
        # angle_error, _ = self.calc_angle_error(self.goals[self.area][4]['x'], self.goals[self.area][4]['y'], self.pos[0], self.pos[1], self.yaw)
        # goal_x, goal_y = self.goal_x, self.goal_y
        # angle_error, _ = self.calc_angle_error(goal_x, goal_y, self.pos[0], self.pos[1], self.yaw)
        # x_diff = goal_x - self.pos[0]
        # y_diff = goal_y - self.pos[1]
        # dist_error = np.sqrt(x_diff * x_diff + y_diff * y_diff)
        # if abs(angle_error) < 1.0 and dist_error < 2.5 and dist_error > 0.25:            
        #     self.aux = [1.0, angle_error, dist_error, size]
        # else:
        #     self.aux = [0,0,0,0]

        # if abs(self.pitch) > 0.25:
        #     
        #     return 2*self.pitch, 2*self.roll

        if abs(self.angle_list_error) < 0.25:
            self.dist_error = self.goal_list_dist
        else:
            self.dist_error = 0
        # return self.ep_Kp * np.clip( self.dist_error, 0, 1.0), self.ep_Kp * np.clip( self.angle_error, -2, 2)
        return self.ep_Kp * np.clip( self.dist_error, 0, 0.5), self.ep_Kp * np.clip( self.angle_list_error, -2, 2)

    def slow_reset(self):
        max_vel = 0.01
        max_orn_vel = 0.01
        sms = ModelState()
        sms.model_name = '_' + self.robot_name
        steps = int(max(max((np.array(self.pos) - np.array(self.last_flat_pos))/max_vel), (self.yaw - self.last_flat_yaw)/max_orn_vel))
        print(steps)
        for _ in range(steps):
            new_pos = np.array(self.pos) + np.clip((np.array(self.last_flat_pos) - np.array(self.pos)), -max_vel, max_vel)
            new_yaw = self.yaw + np.clip((self.last_flat_yaw - self.yaw), -max_orn_vel, max_orn_vel)
            print(new_pos, self.pos, self.last_flat_pos, self.yaw, self.last_flat_yaw)
            rot = Rotation.from_euler('xyz', [0, 0, new_yaw], degrees=False)        
            new_orn = rot.as_quat()       
            sms.pose.position.x = new_pos[0]
            sms.pose.position.y = new_pos[1]
            sms.pose.position.z = new_pos[2] + 0.15
            sms.pose.orientation.x = new_orn[0]
            sms.pose.orientation.y = new_orn[1]
            sms.pose.orientation.z = new_orn[2]
            sms.pose.orientation.w = new_orn[3]
            rospy.wait_for_service('/gazebo/set_model_state')
            try:
                response_model = self.reset_agent_gazebo(sms)
            except: 
                print("Failed to reset pose")
            self.step_sim()
            self.get_observation()

    def hm_flat(self):
        # Return true if the costmap around the robot is less than a threshold (ground is flat)
        return (self.hm[50:70,50:70,0] < 0.5).all()

    def get_im(self, total_steps=0):
        # if not self.args.vis:
        #     # self.hm = np.zeros(self.im_size)
        #     self.hm = np.zeros(self.single_im_size)
        # else:
        if not self.use_terrain:
        # if :
            self.hm = np.zeros(self.single_im_size)
        else:
            if self.args.env == 'subt' or self.args.vis_type == "depth":
                # self.hm = np.array(self.hm_cb).reshape(self.im_size).astype(np.float32) 
                self.hm = self.hm_cb
            else:
                if self.args.subt_om:
                    # self.hm = self.height_map.get_hm(self.pos, robot_yaw=self.initial_yaw)
                    self.hm = self.height_map.get_hm(self.pos, robot_yaw=0)
                else:
                    self.hm = self.height_map.get_hm(self.pos, robot_yaw=self.yaw)
                # self.hm = self.height_map.get_hm(self.pos, robot_yaw=self.yaw, display=True)

            # if self.args.display_im and total_steps % 100 == 0:
                # self.height_map.display_om(self.hm, self.pos, self.yaw, self.initial_robot_pos, self.initial_yaw, world=self.height_map.world, rank=self.rank)

                # self.hm = self.height_map.get_hm(display=self.args.display_im)
            # if self.args.display_im:
            #     cv2.imshow('frame', self.hm)
            #     cv2.waitKey(1)
        
        return self.hm
        # if len(self.stacked_imgs) != self.args.stacked:
        #     for i in range(self.args.stacked):
        #         
        #         
        #         self.stacked_imgs.append(self.hm)
                
        # self.hm = np.concatenate(self.stacked_imgs)
        # return np.concatenate(self.stacked_imgs)
        # return 
        # return self.hm

    def save_sim_data(self, PATH=None, last_steps=False):
        if self.rank == 0 or last_steps:
            if PATH is not None:
                path = PATH
            else:
                path = self.PATH
            try:
                if last_steps:
                    np.save(path + 'sim_data.npy', np.array(self.sim_data, dtype=object)[-300:,:])     
                else:
                    np.save(path + 'sim_data.npy', np.array(self.sim_data, dtype=object))     
                np.save(path + 'box_info.npy', np.array(self.box_info, dtype=object))
                self.sim_data = []
            except Exception as e:
                print("Save sim data error:")
                print(e)

    def record_sim_data(self):
        if len(self.sim_data) > 100000: return
        # pos, orn = p.getBasePositionAndOrientation(self.Id)
        pos = self.pos
        orn = self.orn
        data = [pos, orn]
        self.sim_data.append(data)


    def step_sim(self):
        # self.pause_unpause(pause=False)
        # t1 = time.time()
        while time.time() - self.t1 < self.dt:
            time.sleep(0.00001)
        
        # self.pause_unpause(pause=True)
        self.t1 = time.time()

    def pause_unpause(self, pause=True):
        if pause:
            # rospy.wait_for_service('/gazebo/pause_physics')
            self.pause_sim()
        elif not pause:
            # rospy.wait_for_service('/gazebo/unpause_physics')
            self.unpause_sim()

    # =================================================
    # == ROS STUFF ====================================
    # =================================================
    def initialise_publishers(self):
        self.cmd_vel_publisher = rospy.Publisher('/' + self.robot_name + '/cmd_vel_stamped', TwistStamped, queue_size=1)
        # self.agent_interface_pub = rospy.Publisher('/' + self.robot_name + '/agent_interface_status', RobotStatus, queue_size=1)
        if self.rank == 0:
            self.world_pub = rospy.Publisher('/world', numpy_msg(Floats), queue_size=1, latch=True)
        # self.hm_pub = rospy.Publisher('/' + self.robot_name + '/om', numpy_msg(Floats), queue_size=1)
        # self.hm_pub = rospy.Publisher('/' + self.robot_name + '/om', numpy_msg(Floats), queue_size=1)
        self.hm_pub = rospy.Publisher('/' + self.robot_name + '/om', numpy_msg(Floats), queue_size=1, latch=True)
        self.goal_pub = rospy.Publisher('/' + self.robot_name + '/goal', numpy_msg(Floats), queue_size=1, latch=True)
        # self.pos_pub = rospy.Publisher('/' + self.robot_name + '/pos', numpy_msg(Floats), queue_size=1)
        # self.hm_pub = rospy.Publisher('/' + self.robot_name + '/om', Image, queue_size=1)
        # numpy_msg(Floats)
        # self.bounding_box_pub = rospy.Publisher('/' + self.robot_name + '/om_bounding_box', numpy_msg(Floats), queue_size=1)
        # msg = CvBridge().cv_to_imgmsg(cv2.fromarray(a))
        # a = numpy.fromarray(CvBridge().imgmsg_to_cv(msg))

    def initialise_subscribers(self):
        print("initialising subscribers for ", self.robot_name)
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.modelStatesCallback)
        if self.args.vis_type == "depth":
            rospy.Subscriber('/_' + self.robot_name + '/depth/image_raw', Image, self.depthImageCallback)
        else:
            if self.args.env == 'subt':
                rospy.Subscriber('/' + self.robot_name + '/agent_interface_status', RobotStatus, self.statusCallback)
                if self.args.costmap:
                    rospy.Subscriber('/' + self.robot_name + '/height_map_to_costmap/costmap', DensePointCloud2, self.hmCallback)
                else:
                    rospy.Subscriber('/' + self.robot_name + '/height_map_to_costmap/occupancy_grid', OccupancyGrid, self.hmCallback)
                # elif self.args.vis == 'cm':
                rospy.Subscriber('/' + self.robot_name + '/topometric_waypoint/goal', TopometricWaypointActionGoal, self.waypointCallback)
            # rospy.Subscriber('/' + self.robot_name + '/joint_states', JointState, self.jointStateCallback)


    def initialise_services(self):
        # self.reset_agent_slam = rospy.ServiceProxy('/slam/map/clear_agent', String())
        self.reset_agent_gazebo = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState())

    # =================================================
    # == Pub Actions ==================================
    # =================================================
    def publish_actions(self, actions):
        linear = Vector3()
        angular = Vector3()
        cmd_vel_stamped = TwistStamped()
        cmd_vel_stamped.twist.linear.x = actions[0]
        cmd_vel_stamped.twist.angular.z = actions[1]
        cmd_vel_stamped.header = Header()
        cmd_vel_stamped.header.stamp = rospy.Time.now()
        self.cmd_vel_publisher.publish(cmd_vel_stamped)

    # =================================================
    # == Callbacks ====================================
    # =================================================
    def statusCallback(self, msg):
        self.pos_cb = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
        self.orn_cb = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]
    
    def costmapCallback(self, msg):
        # self.hm_cb = np.nan_to_num(np.array([p[1] for p in pc2.read_points(msg.data)]).reshape(self.im_size)) + 1
        if self.args.costmap:
            self.hm_cb = np.nan_to_num(np.array([p[1] for p in pc2.read_points(msg.data)]).astype(np.float32).reshape(self.im_size)) + 0.5
        else:
            self.hm_cb = (np.nan_to_num(np.array(msg.data).astype(np.float32).reshape(self.im_size)) + 1) / 101
            
    
    def depthImageCallback(self, msg):
        image_data = msg
        self.hm_cb = np.frombuffer(image_data.data, dtype=np.uint8).reshape(image_data.height, image_data.width, -1)
        
    def waypointCallback(self, data):
        msg = data.goal
        self.waypoint_pos_cb = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
        self.waypoint_orn_cb = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]
    
    # def jointStateCallback(self, msg):
    #     self.joints = msg.position
    #     self.joint_vel = msg.velocity
        # if self.steps > 0:
        #   for i in range(self.ac_size):  
        #     if not (msg.effort[i] < 0.00001 and msg.effort[i] > -0.00001):
        #       self.joint_effort[i] = msg.effort[i]        

    def modelStatesCallback(self, msg):
        # pass
        num = [i for i, name in enumerate(msg.name) if name == '_' + self.robot_name]
        if len(num) > 0:
            num = num[0]
            if self.args.env != 'subt':
                self.pos_cb = [msg.pose[num].position.x, msg.pose[num].position.y, msg.pose[num].position.z]
                self.orn_cb = [msg.pose[num].orientation.x, msg.pose[num].orientation.y, msg.pose[num].orientation.z, msg.pose[num].orientation.w]
            self.gz_twist_lin_cb = [msg.twist[num].linear.x, msg.twist[num].linear.y, msg.twist[num].linear.z]
            self.gz_twist_ang_cb = [msg.twist[num].angular.x, msg.twist[num].angular.y, msg.twist[num].angular.z]
            # if self.rank == 0:
                
    
    def get_hm(self):
        om = np.ones(self.im_size).astype(np.float32)
        # [boxIds, positions, sizes, frictions, colours]
        grid_size = self.resolution
        x_offset = int(self.pos[0] / grid_size)
        y_offset = int(self.pos[1] / grid_size)
        x_min = x_offset - self.im_size[0]/2
        x_max = x_offset + self.im_size[0]/2
        y_min = y_offset - self.im_size[1]/2
        y_max = y_offset + self.im_size[1]/2
        if self.box_info is not None:
            positions = self.box_info[1]
            sizes = self.box_info[2]
            for pos, size in zip(positions, sizes):
                x, y, z = int(pos[0]/grid_size),int(pos[1]/grid_size), int(pos[2]/grid_size) 
                x_size, y_size, z_size = int(size[0]/grid_size), int(size[1]/grid_size), int(size[2]/grid_size)
                yaw = pos[5]
                points  = np.array([[dx, dy] for dx in range(x-x_size, x+x_size) for dy in range(y-y_size, y+y_size)]).T
                
                # om_pts =  np.array([[y_offset, x_offset]]).T + self.transform_rot(yaw, pos[:2], points) 
                om_pts = np.array([[x_offset, y_offset]]).T - self.transform_rot(yaw + np.pi/2, [pos[0], pos[1]], points)
                
                om_pts[0,:] = np.clip(om_pts[0,:], x_min, x_max)
                om_pts[1,:] = np.clip(om_pts[1,:], y_min, y_max)
                
                
                # om[om_pts[0,:],om_pts[1,:]] = (z + z_size/grid_size) > 0
                om[om_pts[0,:],om_pts[1,:]] = (z + z_size/grid_size) < 0.2
                # om[om_pts[0,:],om_pts[1,:]] = (z + z_size/grid_size) > 0.2

        return np.flip(np.swapaxes(om, 0, 1), axis=0)
    
    def world_to_robot(self, robot_yaw, robot, world):
        # For some reason I always have trouble remember this
        x,y = world[0] - robot[0], world[1] - robot[1]
        rot_mat = np.array([[np.cos(robot_yaw), -np.sin(robot_yaw), 0],
                             [np.sin(robot_yaw), np.cos(robot_yaw), 0], 
                            [0, 0, 1]])
        return np.dot(rot_mat, np.array([x, y, 0]))

    def transform_rot(self, yaw, pos, points):
        rot_mat = np.array(
                [[np.cos(yaw), -np.sin(yaw)],
                [np.sin(yaw), np.cos(yaw)]])
        # return np.add(np.dot(rot_mat,points.T).T, pos).astype(np.int32)
        return np.add(np.dot(rot_mat,points).T, pos).astype(np.int32).T

    def log_stuff(self, logger, writer, iters_so_far):
        self.iters_so_far = iters_so_far
        difficulty = MPI.COMM_WORLD.allgather(self.difficulty)
        self.min_difficulty = np.min(difficulty)
        # self.min_difficulty = np.mean(difficulty)
        cur_buf = MPI.COMM_WORLD.allgather(sum(self.cur_buf))
        Kp = MPI.COMM_WORLD.allgather(self.Kp)
        avg_vx = MPI.COMM_WORLD.allgather(np.mean(self.avg_vx))
        success = MPI.COMM_WORLD.allgather(np.mean(self.success))

        if self.args.label_bit:
            pred_buffer = MPI.COMM_WORLD.allgather(np.mean(self.pred_buffer))           

        if self.rank == 0:
            # self.next_positions = [i for i in range(32)]
            self.next_positions = [i for i in range(48)]
            np.random.shuffle(self.next_positions)
        else:
            self.next_positions = None
        self.next_positions = comm.bcast(self.next_positions, root=0)
        if self.rank == 0:
            print("next: ", self.next_positions)
        # *self.iters_so_far%2
        # worlds = [i for i in range(self.num_workers)]
        # worlds = [i for i in range(self.num_workers, self.num_workers*2)]
        # random.shuffle(worlds)

        # difficulty = MPI.COMM_WORLD.allgather([i for i in range(self.num_workers*2)])
        # difficulty = MPI.COMM_WORLD.allgather(sum(self.ep_rewards))
        if self.iters_so_far > 200:
            self.pitch_coef = min(5.0 + (self.iters_so_far-200)/10, 100)
        if self.rank == 0:
            logger.record_tabular("success", np.mean(success))
            writer.add_scalar("success", np.mean(success), self.iters_so_far)   
            logger.record_tabular("difficulty", np.min(difficulty))
            writer.add_scalar("difficulty", np.min(difficulty), self.iters_so_far)   
            logger.record_tabular("Kp", np.max(Kp))
            writer.add_scalar("Kp", np.max(Kp), self.iters_so_far)   
            logger.record_tabular("vx", np.mean(self.avg_vx))
            writer.add_scalar("vx", np.mean(self.avg_vx), self.iters_so_far)   
            logger.record_tabular("vx_world", np.mean(self.avg_vx_world))
            writer.add_scalar("vx_world", np.mean(self.avg_vx_world), self.iters_so_far)   
            logger.record_tabular("yaw", np.mean(self.avg_yaw))
            writer.add_scalar("yaw", np.mean(self.avg_yaw), self.iters_so_far)   
            logger.record_tabular("pitch coef", self.pitch_coef)
            writer.add_scalar("pitch coef", self.pitch_coef, self.iters_so_far)   
            print("success", success)
            print("difficulty", difficulty, self.difficulty)
            print("cur_buf", cur_buf, sum(self.cur_buf))
            print("Kp", Kp, self.Kp)
            print("avg vx", np.around(avg_vx,decimals=2))
            if self.args.label_bit:
                logger.record_tabular("pred_buffer", np.mean(pred_buffer))
                writer.add_scalar("pred_buffer", np.mean(pred_buffer), self.iters_so_far)   
                print("pred_buffer", np.array(pred_buffer))


        # logger.record_tabular("max_disturbance", self.max_disturbance)
        # writer.add_scalar("cur", self.cur, self.iters_so_far)   
        # logger.record_tabular("cur", self.cur)
        # writer.add_scalar("Kp", self.Kp, self.iters_so_far)   
        # logger.record_tabular("Kp", self.Kp)0
