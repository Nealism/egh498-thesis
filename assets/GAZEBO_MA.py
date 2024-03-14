import rospy
from geometry_msgs.msg import TwistStamped, PoseStamped
from nav_msgs.msg import Odometry, OccupancyGrid
import numpy as np
import scipy
import time



import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.distributions.normal import Normal
from torch.distributions.categorical import Categorical
from models.core import MLPActorCriticPerception
import pybullet as p




# im = env.get_image()

class RLRobot():
    def __init__(self, cmd_topic, topic1_robotpos, topic2_other_robotpos, topic3_robotvel, topic4_other_robotvel,topic5_goalpos, occupancy_topic, model):
        self.action_pub = rospy.Publisher(cmd_topic, TwistStamped)
        # self.state_topic = state_topic1,state_topic2
        self.robot_topic=topic1_robotpos
        self.other_robot_topic=topic2_other_robotpos
        self.goal_pos=topic5_goalpos
        self.model=model
        self.im_topic=occupancy_topic

        self.robot_pose=None
        self.other_robot_pose=None
        self.robot_vel=None
        self.other_robot_vel=None

        self.im=None
        
        rospy.Subscriber(topic1_robotpos, PoseStamped, self.odom_callback1)
        rospy.Subscriber(topic2_other_robotpos, PoseStamped, self.odom_callback2)
        rospy.Subscriber(topic3_robotvel, TwistStamped, self.odom_callback3)
        rospy.Subscriber(topic4_other_robotvel, TwistStamped, self.odom_callback4)
        # rospy.Subscriber(topic5_goalpos, PoseStamped, self.odom_callback5)
        # rospy.Subscriber(topic6_goal2pos, PoseStamped, self.odom_callback6)
        rospy.Subscriber(occupancy_topic, OccupancyGrid, self.occupancy_callback6)
        self.map_publisher = rospy.Publisher("/modified_occupancy_map", OccupancyGrid, queue_size=10)


        

    def odom_callback1(self, msg1:PoseStamped):
        self.robot_pose = msg1.pose

    def odom_callback2(self, msg2:PoseStamped):
        self.other_robot_pose = msg2.pose

    def odom_callback3(self, msg3:TwistStamped):
        self.robot_vel = msg3.twist

    def odom_callback4(self, msg4:TwistStamped):
        self.other_robot_vel = msg4.twist

    # def goal_callback5(self, goal_msg):
    #     self.goal_pose = goal_msg.pose
        
    def occupancy_callback6(self, msg6:OccupancyGrid):
        # Convert the occupancy map data to a numpy array
        # print(msg6)
        map_data = np.array(msg6.data).reshape((msg6.info.height, msg6.info.width))
        # print(msg6.info.height)
        # Calculate the indices for the central 8x8 region
        start_row = (msg6.info.height - 80) // 2
        end_row = start_row + 80
        start_col = (msg6.info.width - 80) // 2
        end_col = start_col + 80

        # Extract the central 8x8 region
        central_region = map_data[start_row:end_row, start_col:end_col]

        # Scale the values to 0 or 100
        scaled_map = np.where(central_region > 0, 1, 0)

        # Update the message with the modified map data
        modified_msg = msg6
        modified_msg.data = scaled_map.flatten().tolist()
        modified_msg.info.width = 80
        modified_msg.info.height = 80
        # print(modified_msg)
        self.im=modified_msg.data 

        # Publish the modified occupancy map
        self.map_publisher.publish(modified_msg)

    # def publish_action(self):
    #     if self.robot1_pose is not None and self.robot2_pose is not None and self.goal_pose is not None:
    #         observation = self.get_observation()
    #         action = self.model.step(torch.tensor(observation))
    #         self.execute_action(action)

    def get_observation(self):

        # self.goal_pos=self.goal_pose
        #seting robot own position x and y
        self.robot_own_posX=self.robot_pose.position.x
        self.robot_own_posY=self.robot_pose.position.y

        self.robot_own_position=(self.robot_own_posX,self.robot_own_posY)
        
        #seting robot own orientation in euler -- roll pitch yaw
        self.orn=self.robot_pose.orientation.x, self.robot_pose.orientation.y, self.robot_pose.orientation.z, self.robot_pose.orientation.w 
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
        

        #seting other robot position x and y and converting egocentric to own robot
        self.other_robot_posX=self.other_robot_pose.position.x
        self.other_robot_posY=self.other_robot_pose.position.y
        self.other_robot_position=(self.other_robot_posX,self.other_robot_posY)
        
        self.other_robot_egocentric_position=self.world_to_robot(self.yaw, self.robot_own_position, self.other_robot_position)

        
        #seting other robot orientation in euler -- roll pitch yaw
        self.other_robot_orn=self.other_robot_pose.orientation.x, self.other_robot_pose.orientation.y, self.other_robot_pose.orientation.z, self.other_robot_pose.orientation.w 
        self.other_robot_roll, self.other_robot_pitch, self.other_robot_yaw = p.getEulerFromQuaternion(self.other_robot_orn)
        
        
        
        #seting robot own velocity angular and linear
        self.angular_velocity=self.robot_vel.angular.z
        self.linear_velocity=self.robot_vel.linear.x

        #seting other robot velocity angular and linear
        self.other_robot_angular_velocity=self.other_robot_vel.angular.z
        self.other_robot_linear_velocity=self.other_robot_vel.linear.x

        #setting goal position x and y and convering as egocentric to robot
        self.goal_position = self.goal_pos#np.array([self.goal_pose.position.x, self.goal_pose.position.y])
        
        self.goal_egocentric_position=self.world_to_robot(self.yaw, self.robot_own_position, self.goal_position)
        # print(self.goal_egocentric_position[0],self.goal_egocentric_position[1],self.yaw, self.other_robot_egocentric_position[0],self.other_robot_egocentric_position[1], self.other_robot_yaw,self.other_robot_linear_velocity, self.other_robot_angular_velocity,self.roll, self.pitch,self.linear_velocity,self.angular_velocity)

        return (self.goal_egocentric_position[0],self.goal_egocentric_position[1],self.yaw, self.other_robot_egocentric_position[0],self.other_robot_egocentric_position[1], self.other_robot_yaw,
                               self.other_robot_linear_velocity, self.other_robot_angular_velocity,
                               self.roll, self.pitch,self.linear_velocity,self.angular_velocity)

    def get_occupancy_image(self):
        
        if self.im is not None:
            self.occupancy_map_image=self.im

        return self.occupancy_map_image

    # def goal_callback5(self, goal_msg):
    #     self.goal_pose = goal_msg.pose
    
    # def odom_callback1(self, msg1:PoseStamped):
    #     # Update your state
    #     self.x = msg1.pose.position.x
    #     self.y = msg1.pose.position.y
        

    #     self.qx =  msg1.pose.orientation.x
    #     self.qy = msg1.pose.orientation.y
    #     self.qz = msg1.pose.orientation.z 
    #     self.qw = msg1.pose.orientation.w

    #     self.orn=self.qx, self.qy, self.qz, self.qw 
    #     self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
    #     rospy.loginfo(f"x {self.x} y {self.y} yaw {self.yaw} {self.state_topic}")
        

    def world_to_robot(self, robot_yaw, robot, world):
        x,y = world[0] - robot[0], world[1] - robot[1]                       #longitudinal distance
        rot_mat = np.array([[np.cos(robot_yaw), np.sin(robot_yaw)],          #rotational distance
                             [-np.sin(robot_yaw), np.cos(robot_yaw)]])
        return list(np.dot(rot_mat, np.array([x, y])))
    
    def step_R1(self):
        msg = TwistStamped() # create a message

        
        
        
        if self.robot_pose is not None and self.other_robot_pose is not None and self.robot_vel is not None and self.other_robot_vel is not None and self.goal_pos is not None and self.im is not None:
            observation = self.get_observation()
            im=self.get_occupancy_image()
            action = pol.step(torch.as_tensor(np.array(observation), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
            # print("action",action[0][0])
            msg.twist.linear.x = action[0][0]    
            msg.twist.angular.z = action[0][1]#np.pi /2
        # Action = self.model(state)
        # Assemble the msg using the acction
        # self.action_pub.publish(msg)

        # msg.twist.linear.x = 0.6    
        # msg.twist.angular.z = 0#np.pi /2
        # Take your state and foward your model, get an acction
        

        # Execute the acction 
        self.action_pub.publish(msg)

    def step_R3(self):
        msg = TwistStamped() # create a message

        if self.robot_pose is not None and self.other_robot_pose is not None and self.robot_vel is not None and self.other_robot_vel is not None and self.goal_pos is not None and self.im is not None:


            observation = self.get_observation()
            im=self.get_occupancy_image()
            action = pol.step(torch.as_tensor(np.array(observation), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        
            msg.twist.linear.x = action[0][0]    
            msg.twist.angular.z = action[0][1]#np.pi /2
        # Action = self.model(state)
        # Assemble the msg using the acction
        # self.action_pub.publish(msg)

        # msg.twist.linear.x = 0.3
        # msg.twist.angular.z = 0#np.pi /2
        # Take your state and foward your model, get an acction
        

        # Execute the acction 
        self.action_pub.publish(msg)

if __name__ == "__main__":
    rospy.init_node("robotclass_test")

    #model = RL(warever to load it)
    pol = torch.load("/data/r21TG1.5N/2024_03_03_04_28_37/model.pt")
    # print(pol)
    goal_R1=(28,-1)
    goal_R2=(28,1)

    R1 = RLRobot("/r1/cmd_vel_stamped","/r1/slam/odom/high/pose","/r3/slam/odom/high/pose","/r1/slam/odom/high/velocity","/r3/slam/odom/high/velocity",goal_R1, "/r1/costmap_global/occupancy_grid", pol)
    R3 = RLRobot("/r3/cmd_vel_stamped","/r3/slam/odom/high/pose","/r1/slam/odom/high/pose","/r3/slam/odom/high/velocity","/r1/slam/odom/high/velocity",goal_R2, "/r3/costmap_global/occupancy_grid", pol)
    
    # print(R1)

    control_rate = rospy.Rate(50) # 10 Hz
    t1=time.time()
    while not rospy.is_shutdown():

        
        # action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        R1.step_R1()
        R3.step_R3()
        control_rate.sleep()
        print(time.time()-t1)
        t1=time.time()

