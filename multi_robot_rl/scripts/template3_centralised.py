import rospy
from geometry_msgs.msg import TwistStamped, PoseStamped
from nav_msgs.msg import Odometry, OccupancyGrid
import numpy as np
import scipy
import time
import cv2



import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.distributions.normal import Normal
from torch.distributions.categorical import Categorical
from models.core import MLPActorCriticPerception
import pybullet as p


import time
import matplotlib.pyplot as plt
import os
import pandas as pd
import imageio

from rosgraph_msgs.msg import Clock
from scipy.ndimage import label, generate_binary_structure




# im = env.get_image()

class RLRobot():
    # def __init__(self, cmd_topic, topic1_robotpos, topic2_other_robotpos, topic3_robotvel, topic4_other_robotvel,topic5_goalpos, occupancy_topic, model_mu,model_z):
    def __init__(self, cmd_topic, topic1_robotpos, topic3_robotvel, topic5_goalpos, occupancy_topic, model_mu,model_z):
        self.action_pub = rospy.Publisher(cmd_topic, TwistStamped)
        # self.state_topic = state_topic1,state_topic2
        self.robot_topic=topic1_robotpos
        # self.other_robot_topic=topic2_other_robotpos
        self.goal_pos=topic5_goalpos
        self.model_mu=model_mu
        self.model_z=model_z
        self.im_topic=occupancy_topic

        self.robot_pose=None
        self.other_robot_pose=None
        self.robot_vel=None
        self.other_robot_vel=None

        self.start_time=None
        self.current_sim_time=None
        self.time_list=[]

        self.robot1_images=[]
        self.robot3_images=[]
        

        self.im=None
        
        rospy.Subscriber(topic1_robotpos, PoseStamped, self.odom_callback1)
        # rospy.Subscriber(topic2_other_robotpos, PoseStamped, self.odom_callback2)
        rospy.Subscriber(topic3_robotvel, TwistStamped, self.odom_callback3)
        # rospy.Subscriber(topic4_other_robotvel, TwistStamped, self.odom_callback4)
        # rospy.Subscriber(topic5_goalpos, PoseStamped, self.odom_callback5)
        # rospy.Subscriber(topic6_goal2pos, PoseStamped, self.odom_callback6)
        rospy.Subscriber(occupancy_topic, OccupancyGrid, self.occupancy_callbacklocal)
        # self.map_publisher = rospy.Publisher("/modified_occupancy_map", OccupancyGrid, queue_size=10)
        rospy.Subscriber("/clock", Clock, self.clock_callback)
        self.t1=time.time()



        self.buffer_linear_action=[0]
        self.buffer_angular_action=[0]

        self.buffer_relative_goal_pos_x_obs=[0]
        self.buffer_relative_goal_pos_y_obs=[0]

        self.buffer_roll_obs=[0]
        self.buffer_pitch_obs=[0]

        self.buffer_linear_obs=[0]
        self.buffer_angular_obs=[0]

        self.poses_x=[0]
        self.poses_y=[0]

        self.buffer_time=[]
        # self.image_r1=None

        self.map_storage=[]


        

    def odom_callback1(self, msg1:PoseStamped):
        self.robot_pose = msg1.pose

    def odom_callback2(self, msg2:PoseStamped):
        self.other_robot_pose = msg2.pose

    def odom_callback3(self, msg3:TwistStamped):
        self.robot_vel = msg3.twist

    def odom_callback4(self, msg4:TwistStamped):
        self.other_robot_vel = msg4.twist

    def clock_callback(self,data):
        if self.start_time is None:
            self.start_time = data.clock
        self.current_sim_time = data.clock - self.start_time
        # print("_____________________________",self.current_sim_time.to_sec())
        # rospy.loginfo("Current simulation time: %s seconds", self.current_sim_time.to_sec())
        # self.time_list.append(self.current_sim_time.to_sec())

    # def goal_callback5(self, goal_msg):
    #     self.goal_pose = goal_msg.pose
        
    def occupancy_callbacklocal(self, msg6:OccupancyGrid):
        
        width = msg6.info.width
        height = msg6.info.height
        map_data = np.array(msg6.data).reshape((height, width))

        #Flip the map horizontally
        map_data = np.fliplr(map_data)
        # map_data = np.flipud(map_data)
        map_data = np.rot90(map_data, k=1)


        
        self.ascaled_map = np.where(map_data == 100, 1, 0)
        self.map_storage.append(self.ascaled_map)
        self.scaled_map=self.ascaled_map

        

        # Create a new OccupancyGrid message for the modified map
        modified_msg = OccupancyGrid()
        modified_msg.header = msg6.header
        modified_msg.info = msg6.info
        modified_msg.info.width = 80
        modified_msg.info.height = 80
        modified_msg.data = self.scaled_map.flatten().tolist()
        self.im=modified_msg.data 
        
        
    def occupancy_callbackglobal(self, msg6:OccupancyGrid):
        
        map_data = np.array(msg6.data).reshape((msg6.info.height, msg6.info.width))
        

        #Flip the map horizontally
        map_data = np.fliplr(map_data)
        # map_data = np.flipud(map_data)
        map_data = np.rot90(map_data, k=1)
        
        
        
        
        self.scaled_map = np.where(map_data > 0, 1, 0)
        # print("map_scaled",self.scaled_map)

        # Update the message with the modified map data
        modified_msg = msg6
        modified_msg.data = self.scaled_map.flatten().tolist()
        modified_msg.info.width = 80
        modified_msg.info.height = 80
        # print(modified_msg)
        self.im=modified_msg.data 
        # print("ow",np.array(self.im).shape)
        # print("r1",time.time()-self.t1)
        self.t1=time.time()


        
        

    def occupancy_map_to_image(self,occupancy_map):
        # Convert the list of lists to a NumPy array
        occupancy_map_array = np.array(occupancy_map)
        # print("occupancy_map_array.shape",occupancy_map_array.shape)
        # Determine the dimensions of the occupancy map
        rows, cols = occupancy_map_array.shape
        
        # Create an empty image with the same dimensions as the occupancy map
        image = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        # Assign grey color where occupancy_map is 0
        image[occupancy_map_array == 0] = (128, 128, 128)  # Grey
        
        # Assign red color where occupancy_map is 1
        image[occupancy_map_array == 1] = (0, 0, 255)  # Red
        
        return image
    

    

    

    
    def get_occupancy_image(self):
        
        
        if self.im is not None:
            self.occupancy_map_image=self.scaled_map

        return self.occupancy_map_image

    def get_observation(self):

        # self.goal_pos=self.goal_pose
        #seting robot own position x and y
        self.robot_own_posX=self.robot_pose.position.x
        self.robot_own_posY=self.robot_pose.position.y

        self.poses_x.append(self.robot_own_posX)
        self.poses_y.append(self.robot_own_posY)

        self.robot_own_position=(self.robot_own_posX,self.robot_own_posY)
        # print("self.robot_own_position",self.robot_own_position)
        #seting robot own orientation in euler -- roll pitch yaw
        self.orn=self.robot_pose.orientation.x, self.robot_pose.orientation.y, self.robot_pose.orientation.z, self.robot_pose.orientation.w 
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
        

       
        
        
        #seting robot own velocity angular and linear
        self.angular_velocity=self.robot_vel.angular.z
        self.linear_velocity=self.robot_vel.linear.x
        # print("self.angular_velocity",self.angular_velocity)



        
        # print("obs_lin_vel",self.linear_velocity,"obs_ang_vel",self.angular_velocity,self)
        # self.buffer_time.append(time.time()-self.t1)
        # print("TIME",time.time()-t1,self.buffer_time,"ob")
        self.buffer_linear_obs.append(self.linear_velocity)
        self.buffer_angular_obs.append(self.angular_velocity)
        # output_dir ="/home/kom018/behaviour_rl/Results_plots/Action_plots"

        

        

        
        #setting goal position x and y and convering as egocentric to robot
        self.goal_position = self.goal_pos#np.array([self.goal_pose.position.x, self.goal_pose.position.y])
        
        self.goal_egocentric_position=self.world_to_robot(self.yaw, self.robot_own_position, self.goal_position)

        self.buffer_relative_goal_pos_x_obs.append(self.goal_egocentric_position[0])
        self.buffer_relative_goal_pos_y_obs.append(self.goal_egocentric_position[1])

        self.buffer_roll_obs.append(self.roll)
        self.buffer_pitch_obs.append(self.pitch)
        # print(self.goal_egocentric_position[0],self.goal_egocentric_position[1],self.yaw, self.other_robot_egocentric_position[0],self.other_robot_egocentric_position[1], self.other_robot_yaw,self.other_robot_linear_velocity, self.other_robot_angular_velocity,self.roll, self.pitch,self.linear_velocity,self.angular_velocity)

        return (self.goal_egocentric_position[0],self.goal_egocentric_position[1], self.roll, self.pitch,self.linear_velocity,self.angular_velocity)

    

   
        

    def world_to_robot(self, robot_yaw, robot, world):
        x,y = world[0] - robot[0], world[1] - robot[1]                       #longitudinal distance
        rot_mat = np.array([[np.cos(robot_yaw), np.sin(robot_yaw)],          #rotational distance
                             [-np.sin(robot_yaw), np.cos(robot_yaw)]])
        return list(np.dot(rot_mat, np.array([x, y])))
    
    


    def step_R1(self,action):
        msg = TwistStamped() # create a message

        
        
        
        # if self.robot_pose is not None and self.other_robot_pose is not None and self.robot_vel is not None and self.other_robot_vel is not None and self.goal_pos is not None and self.im is not None:
        if self.robot_pose is not None and self.robot_vel is not None and self.goal_pos is not None and self.im is not None:
            
            t2=time.time()
            # self.observations_r1 = self.get_observation()
            self.im_ocupancy=self.get_occupancy_image()
            # # print("R1 input",self.observations_r1)
            
            self.actions = action
            clipped_linear_vel_command=np.clip(self.actions[0].detach().numpy(), -0.5, 1)
            clipped_angular_vel_command=np.clip(self.actions[1].detach().numpy(), -1.5, 1.5)

            self.actions=torch.tensor([clipped_linear_vel_command,clipped_angular_vel_command])
            # print("r1_action",self.actions[0])
            # print("r1_wholeac",self.actions,type(self.actions),len(self.actions))
            msg.twist.linear.x = self.actions[0] #*0.4    
            msg.twist.angular.z = self.actions[1] #*0.8#np.pi /2
            
        

        # Execute the acction 
            self.action_pub.publish(msg)

            # output_dir ="/home/kom018/behaviour_rl/Results_plots/Action_plots"
            output_dir ="/refarm/src/multi_robot_rl/scripts"

            self.buffer_linear_action.append(msg.twist.linear.x.detach().numpy())
            self.buffer_angular_action.append(msg.twist.angular.z.detach().numpy())
            
            self.image_r1 = self.occupancy_map_to_image(self.im_ocupancy)
            # print("OC",self.image_r1,self.current_sim_time.to_sec())
            # print("break")
            self.robot1_images.append(self.image_r1)
            

            # # Create a window with the specified name
            cv2.namedWindow("R1 Occupancy Map", cv2.WINDOW_NORMAL)

            # Resize the window to a desired size
            cv2.resizeWindow("R1 Occupancy Map", 800, 600)
            # Display the image
            cv2.imshow("R1 Occupancy Map", self.image_r1)
            cv2.waitKey(1)

    def step_R3(self,action):
        msg = TwistStamped() # create a message

        # if self.robot_pose is not None and self.other_robot_pose is not None and self.robot_vel is not None and self.other_robot_vel is not None and self.goal_pos is not None and self.im is not None:
        if self.robot_pose is not None and self.robot_vel is not None and self.goal_pos is not None and self.im is not None:

            
            # self.observations = self.get_observation()
            self.im_ocupancy=self.get_occupancy_image()
            
            self.actions_r3=action

            clipped_linear_vel_command_r3=np.clip(self.actions_r3[0].detach().numpy(), -0.5, 1)
            clipped_angular_vel_command_r3=np.clip(self.actions_r3[1].detach().numpy(), -1.5, 1.5)
            
            self.actions_r3=torch.tensor([clipped_linear_vel_command_r3,clipped_angular_vel_command_r3])


            
            msg.twist.linear.x = self.actions_r3[0] #*0.4   
            msg.twist.angular.z = self.actions_r3[1]#*0.8#np.pi /2
            
        

        # Execute the acction 
            self.action_pub.publish(msg)

            self.buffer_linear_action.append(msg.twist.linear.x.detach().numpy())
            self.buffer_angular_action.append(msg.twist.angular.z.detach().numpy())
            self.image_r3 = self.occupancy_map_to_image(self.im_ocupancy)
            self.robot3_images.append(self.image_r3)


            # # Create a window with the specified name
            cv2.namedWindow("R3 Occupancy Map", cv2.WINDOW_NORMAL)

            # Resize the window to a desired size
            cv2.resizeWindow("R3 Occupancy Map", 800, 600)
            # Display the image
            cv2.imshow("R3 Occupancy Map", self.image_r3)
            cv2.waitKey(1)
            # cv2.destroyAllWindows()

if __name__ == "__main__":
    rospy.init_node("robotclass_test")

    #model = RL(warever to load it)
    # pol = torch.load("/data/r21TG1.3N_FINAL_MA_MODEL_ME67_2/2024_03_10_05_35_53/model.pt")
    mu_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan2/mu_net.jit")
    z_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan2/z_net.jit")

   

    goal_R1=(8,-0.5)
    goal_R2=(8,0.5)

    
    R1 = RLRobot("/r1/cmd_vel_stamped","/r1/slam/odom/high/pose","/r1/slam/odom/high/velocity",goal_R1, "/r1/costmap_local/occupancy_grid", mu_net,z_net)
    R3 = RLRobot("/r3/cmd_vel_stamped","/r3/slam/odom/high/pose","/r3/slam/odom/high/velocity",goal_R2, "/r3/costmap_local/occupancy_grid", mu_net,z_net)
    
    act=None
    control_rate = rospy.Rate(10) # 10 Hz
    t1=time.time()
    
    
    while not rospy.is_shutdown():
            # R3.buffer_time.append(time.time()-R3.t1)
        if R1.robot_pose is not None and R1.robot_vel is not None and R1.goal_pos is not None and R1.im is not None and R3.robot_pose is not None and R3.robot_vel is not None and R3.goal_pos is not None and R3.im is not None:
            joint_observation=[R1.get_observation(),R3.get_observation()]
            joint_map=[R1.get_occupancy_image(),R3.get_occupancy_image()]

            a=torch.as_tensor(np.array(joint_observation), dtype=torch.float32).unsqueeze(dim=0)
            b=z_net(torch.as_tensor(joint_map, dtype=torch.float32))
            # print(a[0],"br1",b)
            # print(np.array(a[0].detach().numpy()).shape,np.array(b.detach().numpy()).shape)
            # print(a.shape)
            # print(b.shape)
            concatenate_part=torch.concat((a[0],b),-1)

            
            act = mu_net(concatenate_part)
            # print(act[0],"act",act[1])
       
        # action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
            R1.step_R1(act[0])
            R3.step_R3(act[1])
        control_rate.sleep()
        # print("R1.buffer_linear_action",R1.buffer_linear_action)
        R1.buffer_time.append(R1.current_sim_time.to_sec())
        R3.buffer_time.append(R3.current_sim_time.to_sec())
        
        
        # # self.current_sim_time
        # # print("TIME",time.time()-t1,R1.buffer_time,"ac")
        
        # # output_dir ="/home/kom018/behaviour_rl/Results_plots/Action_plots"
        if R3.current_sim_time.to_sec()>20:
        
            print("THAM");exit()



        
        # print("Sim_time",R1.current_sim_time.to_sec())
        

        # print("step_time",time.time()-t1)
        
        t1=time.time()

        

