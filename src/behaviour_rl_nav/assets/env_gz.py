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
# from multiagent_msgs.msg import RobotStatus
from nav_msgs.msg import OccupancyGrid
# from rasg_nav_msgs.msg import DensePointCloud2, TopometricWaypointActionGoal
import cv2
from scipy.spatial.transform import Rotation
# import ros_numpy
from assets.obstacles_gz import Obstacles
# from height_map import HeightMap
# from height_map import HeightMap
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
# import ros_numpy
from cv_bridge import CvBridge
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
np.set_printoptions(precision=3, suppress=True)
from gym import spaces

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
    steps = 0
    total_steps = 0
    episodes = 0
    tipped = False
    max_action = np.array([0.5, 0.5])
    resolution = 0.1
    def __init__(self, PATH=None, args=None, writer=None):
        self.PATH = PATH
        self.args = args
        self.writer = writer
        self.rank = comm.Get_rank()
        self.num_workers = comm.Get_size()
        self.difficulty = self.args.difficulty

        self.ac_size = 2
        print("might be worth trying stacked obstervation")
        # self.ob_size = 9
        self.ob_size = 7

        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        self.im_size = self.single_im_size = [80,80,1]

        self.robot_name = 'r' + str(self.rank + 1)
        rospy.init_node('titan_rl_node_' + self.robot_name, anonymous=False) 
        
        if self.rank == 0:
            self.pause_sim = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
            self.unpause_sim = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        
        self.initialise_subscribers()
        self.initialise_publishers()
        self.initialise_services()
        # if self.args.env != 'subt' and self.use_terrain:
        #     self.obstacles = Obstacles(rank=self.rank, num_workers=self.num_workers, args=self.args)

        self.state = ['roll','pitch','roll_vel','pitch_vel','vx','vy','vz']
        self.ob_dict = {}
        self.ep_rewards = deque(maxlen=5)
        self.total_reward = 0
        self.t1 = time.time()

        self.initial_pos = self.pos_cb = None
        self.initial_orn = self.orn_cb = None
        self.waypoint_pos = self.waypoint_pos_cb = self.pos = self.initial_pos = self.pos_cb
        self.waypoint_orn = self.waypoint_orn_cb = self.orn = self.initial_orn = self.orn_cb
        
        # =================================================================
        # DO NOT DELETE - Python quaternion code
        # =================================================================
        # rot = Rotation.from_quat([self.initial_orn[0], self.initial_orn[1], self.initial_orn[2], self.initial_orn[3]])
        # yaw = rot.as_euler('xyz', degrees=False)[2]
        # rot = Rotation.from_euler('xyz', [0, 0, yaw], degrees=False)        
        # self.orn = self.orn_cb = self.initial_orn = rot.as_quat()        
        # =================================================================

        # self.orn = self.orn_cb = self.initial_orn = [0,0,0,1]
        self.y_offset = 15*self.rank
        # self.cur_buf = deque(maxlen=3)
        self.prev_min_difficulty = None
        self.min_difficulty = self.difficulty
        self.use_terrain = False
        # self.br = CvBridge()
        self.Kp = 1

        self.avg_vx = deque(maxlen=100)
        self.avg_vx_world = deque(maxlen=100)
        self.avg_yaw = deque(maxlen=100)
        # self.next_positions = [i for i in range(self.num_workers*2)]
        # self.reached_goal = False

        # self.stacked_obs = deque(maxlen=self.args.stacked)
        # # self.stacked_imgs = deque(maxlen=self.args.stacked)
        # self.goal_num = self.first_goal = 0
        self.goal_reached = False
        # self.label = False
        # self.pred = False
        # self.success = [0]
        self.pitch_coef = 5.0

        self.world_shape = [513, 513]
        # Made this so we can scale to 64 robots (move a max dist of 4 meters, with costmap of 4x4 = 8 meters all around)
        self.size = [64, 64, 3]
        self.pixel_scale = np.rint(self.world_shape[0] / self.size[0])

        self.start_locations = [[(4 + i*8),(4 + j*8)] for i in range(8) for j in range(8)]
        self.get_world_map()

    def robot_to_hm(self, x, y):
        hm_coords = [int(np.rint(x * self.pixel_scale)), int(np.rint(y * self.pixel_scale))]
        return hm_coords

    def get_world_map(self):
        self.world_map = cv2.imread("$HOME/Dropbox/csiro_ws/src/behaviour_rl_nav/gazebo/worlds/heightmap_test.png", cv2.IMREAD_GRAYSCALE)
        # print(self.world_map.shape); exit()

    def reset_robot(self):
        sms = ModelState()
        # sms.model_name = '_' + self.robot_name
        sms.model_name = self.robot_name
        sms.pose.position.x = self.initial_x
        sms.pose.position.y = self.initial_y
        sms.pose.position.z = self.initial_z 
        sms.pose.orientation.x = self.initial_orn[0]
        sms.pose.orientation.y = self.initial_orn[1]
        sms.pose.orientation.z = self.initial_orn[2]
        sms.pose.orientation.w = self.initial_orn[3]
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
                
        self.success = [self.goal_reached]
        self.goal_reached = False
        # else:
            # self.success = [0.0]
        
        
        self.publish_actions([0,0]) 

        
        if self.episodes > 0 and self.args.record_sim:
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

            # comm.Barrier()
            
            # self.height_map = height_map(self.box_info, self.im_size, grid_size=self.resolution, initial_yaw=self.initial_yaw, robot_pos=[self.initial_x, self.initial_y])
            # if self.use_terrain:
            #     self.height_map = HeightMap(self.box_info, self.single_im_size, grid_size=self.resolution, args=self.args, rank=self.rank)
            #     self.height_map.map_extents
            #     self.z_offset = self.height_map.z_offset
            # else:
            #     self.z_offset = 0

        self.prev_min_difficulty = self.min_difficulty
        self.reached_goal = False
        

        self.area = np.random.randint(0,4)
        # else:
        # self.area = 0
        
        self.x_offset = self.area*20
        self.goal_num = 0
        
        
        # if self.use_terrain and self.args.cur:
        #     self.goal_x = self.goals[self.area][self.goal_num]['x']
        #     self.goal_y = self.goals[self.area][self.goal_num]['y']
        # else:
        #     self.goal_x = 0
        #     self.goal_y = 0
        
        
        #     # Random start point
        #     self.initial_x = 0.2 + np.random.uniform(0.0, 1.0) + self.x_offset
        #     self.initial_y = np.random.uniform( -1,  1) + self.y_offset
        #     self.initial_z = 0.3
        #     # self.initial_yaw = np.random.uniform(-3.0, 3.0)
        #     self.initial_yaw = np.random.uniform(-1.0, 1.0)
            
        # Straight start point
        # self.initial_x = 0.2 + self.x_offset
        # self.initial_y = self.y_offset
        # self.initial_z = 0.2
        # self.initial_yaw = 0        
        self.initial_x = self.start_locations[self.rank][0]
        self.initial_y = self.start_locations[self.rank][1]
        self.initial_yaw = np.random.uniform(-np.pi, np.pi)

        rot = Rotation.from_euler('xyz', [0, 0, self.initial_yaw], degrees=False)        
        self.initial_orn = rot.as_quat()    

        # self.initial_z = self.initial_z + self.z_offset 
        self.initial_z = 0.2
        self.initial_robot_pos = [self.initial_x, self.initial_y, self.initial_z]
        print("Resetting robot ", self.robot_name, self.initial_x, self.initial_y, self.initial_yaw)
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
        
        # print("waiting for pos and orn")
        while self.orn_cb is None and self.pos_cb is None:
            time.sleep(0.01)
        # print("got pos and orn")

        rot = Rotation.from_quat([self.orn_cb[0], self.orn_cb[1], self.orn_cb[2], self.orn_cb[3]])
        self.prev_rot = rot.as_euler('xyz', degrees=False)
        self.reached_detect_goal = False

        self.get_observation()
        self.im = self.get_im()
        # if self.args.use_gaps or self.args.run_gaps:
        #     self.z, self.gap = self.gap_detector.step(self.im)
            # self.z, self.gap = [0]*64, [0]*self.aux_size

            # self.im = self.gap
            # self.im = self.z
        self.prev_detected = 0
        self.stacked_obs = deque(maxlen=self.args.stacked)
        # self.stacked_imgs = deque(maxlen=self.args.stacked)

        for _ in range(self.args.stacked):

            # if self.args.use_gaps:
            #     if self.use_z:
            #         self.stacked_obs.append(self.body + list(self.z))
            #     else:
            #         self.stacked_obs.append(self.body + list(self.gap))
            # else:
                # self.stacked_obs.append(self.body)
            self.stacked_obs.append(self.body)
            
        
        self.t_test = time.time()
        # if self.rank == 0:
            
        #     world_message = np.array(self.single_im_size + list(self.height_map.world_offset) + list(self.height_map.world.shape) + list(self.height_map.world.reshape([np.prod(self.height_map.world.shape), 1])), dtype=np.float32)
        #     self.world_pub.publish(world_message)

        # if self.use_wp:
        #     return  np.array(self.orn + self.waypoint_orn + [self.dist_to_waypoint])
        # else:
        #     return np.array(self.body)
        # return np.array(self.body), im
        # return np.concatenate(self.stacked_obs), self.im
        return np.concatenate(self.stacked_obs)

    def step(self, actions, est_aux=None, run_pol=None):

        if run_pol is not None:

            self.detected = self.run_pol = run_pol[0]

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
        # if self.args.use_gaps or self.args.run_gaps:
        #     self.z, self.gap = self.gap_detector.step(self.im)
        #     # self.z, self.gap = [0]*64, [0]*self.aux_size
        #     # self.im = self.gap
        # elif self.args.aux or self.args.just_aux:
        #     self.gap = est_aux
        # else:
        #     self.gap = [0]*self.aux_size
            # self.im = self.z
        reward, done = self.get_reward(actions)
        self.total_reward += reward
        if self.args.record_sim: 
            self.record_sim_data()
        self.prev_actions = actions
        self.steps += 1
        self.total_steps += 1
        
        # if self.gap is not None:
        #     est_aux = self.gap
        # if self.steps % 1 == 0:
        # if self.steps % 10 == 0:
            
        #     hm_message = np.array([self.pos[0], self.pos[1], self.yaw] + self.aux + list(self.gap) + list(self.hm.reshape([np.prod(self.single_im_size), 1])), dtype=np.float32)
            

            # self.hm_pub.publish(hm_message)

        if self.steps % 10 == 0:
            if self.hm_flat():
                self.last_flat_pos = self.pos
                self.last_flat_yaw = self.yaw

        if not self.reached_goal and self.goal_num == 4 and self.goal_dist < 2.0:
        # if not self.reached_goal and self.goal_num >= 2:
            self.reached_goal = True

        # if self.args.use_gaps:
            
        #     if self.use_z:
        #         self.stacked_obs.append(self.body + list(self.z))
        #     else:
        #         self.stacked_obs.append(self.body + list(self.gap))
        # else:
        self.stacked_obs.append(self.body)
        
        # return np.concatenate(self.stacked_obs), self.im, reward, done, self.ob_dict
        return np.concatenate(self.stacked_obs), reward, done, self.ob_dict

    def get_reward(self, actions):
        done = False

        reward = 0
        if not self.goal_reached:
            reward += 1.5*np.exp(-10*(0.5 - self.target_vx)**2)
            reward -= 0.1*self.angle_error**2
        else:
            reward += 1.5*np.exp(-10*(0.5 - self.vx)**2)
            reward -= 0.1*(self.yaw - self.initial_angle)**2

        reward -= 0.05*self.actions[1]**2
        # if self.args.obstacle_type == "gaps":
        reward -= self.pitch_coef*np.sum((np.array([self.roll, self.pitch]) - np.array([0,0]))**2)
        reward -= 0.001*np.sum((np.array(self.actions) - np.array(self.prev_actions))**2)
        if self.vx < 0:
            # old:
            reward += 0.25*self.vx 
            # reward += 0.5*self.vx 

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
        
        # if self.use_wp:
        #     self.dist_to_waypoint = np.sqrt(np.sum((self.pos[0] - self.waypoint_pos[0])**2 + (self.pos[1] - self.waypoint_pos[1])**2 + (self.pos[2] - self.waypoint_pos[2])**2))

        # Finite differences for velocity (unsure if we have access to this through the imu?) Clipped to 2m/s
        self.body_vxyz = np.clip((np.array(self.pos) - np.array(self.prev_pos))/self.dt, -1.5, 1.5)
        self.base_rot_vel = np.clip((np.array([self.roll, self.pitch, self.yaw]) - np.array(self.prev_rot))/self.dt, -np.pi, np.pi)
        self.prev_pos = self.pos
        self.prev_rot = [self.roll, self.pitch, self.yaw]

        self.roll_vel = self.base_rot_vel[0]
        self.pitch_vel = self.base_rot_vel[1]
        self.yaw_vel = self.base_rot_vel[2]

        # Unsure why this is correct, but seems to be..
        rot = np.array(
        [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
            [np.sin(-self.yaw), np.cos(-self.yaw), 0],
            [		0,			 0, 1]]
        )

        self.vx, self.vy, self.vz = np.dot(rot, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
    
        self.avg_vx.append(self.vx) 
        self.avg_vx_world.append(self.body_vxyz[0]) 
        self.avg_yaw.append(self.yaw) 

        if abs(self.pitch) > 1.0 or abs(self.roll) > 1.0:
            self.tipped = True
        else:
            self.tipped = False


        # goal_x, goal_y = self.goals[self.area][self.goal_num]['x'], self.goals[self.area][self.goal_num]['y']
        # self.angle_error, self.target_angle = self.calc_angle_error(goal_x, goal_y, self.pos[0], self.pos[1], self.yaw)

        target_rot = np.array(
        [[np.cos(-self.target_angle), -np.sin(-self.target_angle), 0],
            [np.sin(-self.target_angle), np.cos(-self.target_angle), 0],
            [		0,			 0, 1]]
        )
        self.target_vx, _, _ = np.dot(target_rot, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        
        self.body = [self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel]


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


    def get_expert(self):

        if abs(self.angle_list_error) < 0.25:
            self.dist_error = self.goal_list_dist
        else:
            self.dist_error = 0
        # return self.ep_Kp * np.clip( self.dist_error, 0, 1.0), self.ep_Kp * np.clip( self.angle_error, -2, 2)
        return self.ep_Kp * np.clip( self.dist_error, 0, 0.5), self.ep_Kp * np.clip( self.angle_list_error, -2, 2)


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
        # TODO: setup for refarm, decide how we visualise
        # if self.args.vis_type == "depth":
        #     rospy.Subscriber('/_' + self.robot_name + '/depth/image_raw', Image, self.depthImageCallback)
        # else:
        #     if self.args.env == 'subt':
        #         rospy.Subscriber('/' + self.robot_name + '/agent_interface_status', RobotStatus, self.statusCallback)
        #         if self.args.costmap:
        #             rospy.Subscriber('/' + self.robot_name + '/height_map_to_costmap/costmap', DensePointCloud2, self.hmCallback)
        #         else:
        #             rospy.Subscriber('/' + self.robot_name + '/height_map_to_costmap/occupancy_grid', OccupancyGrid, self.hmCallback)
        #         # elif self.args.vis == 'cm':
        #         rospy.Subscriber('/' + self.robot_name + '/topometric_waypoint/goal', TopometricWaypointActionGoal, self.waypointCallback)
        #     # rospy.Subscriber('/' + self.robot_name + '/joint_states', JointState, self.jointStateCallback)


    def initialise_services(self):
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
        print("in status callback")
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
        # print("in model states cb",)
        # print(msg)
        # pass
        # num = [i for i, name in enumerate(msg.name) if name == '_' + self.robot_name]
        num = [i for i, name in enumerate(msg.name) if name == self.robot_name]
        # print(num)
        if len(num) > 0:
            num = num[0]
            if self.args.env != 'subt':
                self.pos_cb = [msg.pose[num].position.x, msg.pose[num].position.y, msg.pose[num].position.z]
                self.orn_cb = [msg.pose[num].orientation.x, msg.pose[num].orientation.y, msg.pose[num].orientation.z, msg.pose[num].orientation.w]
            self.gz_twist_lin_cb = [msg.twist[num].linear.x, msg.twist[num].linear.y, msg.twist[num].linear.z]
            self.gz_twist_ang_cb = [msg.twist[num].angular.x, msg.twist[num].angular.y, msg.twist[num].angular.z]
            # if self.rank == 0:
                
    
    def get_hm(self, pos, robot_yaw=0):

        
        # Can maybe still use this? Need world_map
        om = np.ones(self.im_size).astype(np.float32)
        # [boxIds, positions, sizes, frictions, colours]
        grid_size = self.resolution
        x_offset = int(self.pos[0] / grid_size)
        y_offset = int(self.pos[1] / grid_size)
        x_min = x_offset - self.im_size[0]/2
        x_max = x_offset + self.im_size[0]/2
        y_min = y_offset - self.im_size[1]/2
        y_max = y_offset + self.im_size[1]/2
        # if self.box_info is not None:
            # positions = self.box_info[1]
            # sizes = self.box_info[2]
        # for pos, size in zip(pose):

        x, y, z = int(pos[0]/grid_size),int(pos[1]/grid_size), int(pos[2]/grid_size) 
        # x_size, y_size, z_size = int(size[0]/grid_size), int(size[1]/grid_size), int(size[2]/grid_size)
        yaw = robot_yaw
        # points  = np.array([[dx, dy] for dx in range(x-x_size, x+x_size) for dy in range(y-y_size, y+y_size)]).T
        points  = np.array([[dx, dy] for dx in range(x-self.im_size[0], x+self.im_size[0]) for dy in range(y-self.im_size[1], y+self.im_size[1])]).T
        
        # om_pts =  np.array([[y_offset, x_offset]]).T + self.transform_rot(yaw, pos[:2], points) 
        om_pts = np.array([[x_offset, y_offset]]).T - self.transform_rot(yaw + np.pi/2, [pos[0], pos[1]], points)
        
        om_pts[0,:] = np.clip(om_pts[0,:], x_min, x_max)
        om_pts[1,:] = np.clip(om_pts[1,:], y_min, y_max)
        
        
        # om[om_pts[0,:],om_pts[1,:]] = (z + z_size/grid_size) > 0
        # om[om_pts[0,:],om_pts[1,:]] = (z + z_size/grid_size) < 0.2
        om[om_pts[0,:],om_pts[1,:]] = self.world_map[om_pts[0,:],om_pts[1,:]]
        # om[om_pts[0,:],om_pts[1,:]] = (z + z_size/grid_size) > 0.2

        return np.flip(np.swapaxes(om, 0, 1), axis=0)
    
    def world_to_robot(self, robot_yaw, robot, world):
        # For some reason I always have trouble remembering this
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
            

        # logger.record_tabular("max_disturbance", self.max_disturbance)
        # writer.add_scalar("cur", self.cur, self.iters_so_far)   
        # logger.record_tabular("cur", self.cur)
        # writer.add_scalar("Kp", self.Kp, self.iters_so_far)   
        # logger.record_tabular("Kp", self.Kp)0
