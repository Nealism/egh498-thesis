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

from rosgraph_msgs.msg import Clock




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

        self.buffer_linear_obs=[0]
        self.buffer_angular_obs=[0]

        self.poses_x=[0]
        self.poses_y=[0]

        self.buffer_time=[]
        # self.image_r1=None


        

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
        # Convert the occupancy map data to a numpy array
        width = msg6.info.width
        height = msg6.info.height
        map_data = np.array(msg6.data).reshape((height, width))

        #Flip the map horizontally
        # map_data = np.fliplr(map_data)
        #map_data = np.flipud(map_data)
        map_data = np.rot90(map_data, k=-1)


        # # # this part needed if use 70X70 map
        # # # Calculate the indices for the central 70x70 region
        # # start_row = (height - 70) // 2
        # # end_row = start_row + 70
        # # start_col = (width - 70) // 2
        # # end_col = start_col + 70

        # # # Extract the central 70x70 region
        # # central_region = map_data[start_row:end_row, start_col:end_col]

        # # # Create an empty 80x80 array
        # # resized_map = np.zeros((80, 80))

        # # # Calculate the indices for inserting the central region into the resized map
        # # resized_start_row = (80 - 70) // 2
        # # resized_end_row = resized_start_row + 70
        # # resized_start_col = (80 - 70) // 2
        # # resized_end_col = resized_start_col + 70

        # # Insert the central region into the resized map
        # resized_map[resized_start_row:resized_end_row, resized_start_col:resized_end_col] = central_region

        # # Convert values greater than 0 to 1
        # self.scaled_map = np.where(resized_map > 0, 1, 0)


        # Convert values greater than 0 to 1
        self.scaled_map = np.where(map_data > 0, 1, 0)

        # Create a new OccupancyGrid message for the modified map
        modified_msg = OccupancyGrid()
        modified_msg.header = msg6.header
        modified_msg.info = msg6.info
        modified_msg.info.width = 80
        modified_msg.info.height = 80
        modified_msg.data = self.scaled_map.flatten().tolist()
        self.im=modified_msg.data 
        # # Publish the modified occupancy map
        # self.map_publisher.publish(modified_msg)
        
    def occupancy_callbackglobal(self, msg6:OccupancyGrid):
        # Convert the occupancy map data to a numpy array
        # print(msg6)
        map_data = np.array(msg6.data).reshape((msg6.info.height, msg6.info.width))
        # print("map_original",map_data)
        #map_data = np.flipud(map_data)
        map_data = np.rot90(map_data, k=-1)
        # print(msg6.info.height)
        
        ## This part needed if occupancy is 70 x 70
        # # Calculate the indices for the central 8x8 region
        # start_row = (msg6.info.height - 80) // 2
        # end_row = start_row + 80
        # start_col = (msg6.info.width - 80) // 2
        # end_col = start_col + 80

        # # Extract the central 8x8 region
        # central_region = map_data[start_row:end_row, start_col:end_col]

        # # Scale the values to 0 or 100
        # self.scaled_map = np.where(central_region > 0, 1, 0)
        
        
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


        # Publish the modified occupancy map
        # self.map_publisher.publish(modified_msg)

    # def publish_action(self):
    #     if self.robot1_pose is not None and self.robot2_pose is not None and self.goal_pose is not None:
    #         observation = self.get_observation()
    #         action = self.model.step(torch.tensor(observation))
    #         self.execute_action(action)
        

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
        

        # #seting other robot position x and y and converting egocentric to own robot
        # self.other_robot_posX=self.other_robot_pose.position.x
        # self.other_robot_posY=self.other_robot_pose.position.y
        # self.other_robot_position=(self.other_robot_posX,self.other_robot_posY)
        
        # self.other_robot_egocentric_position=self.world_to_robot(self.yaw, self.robot_own_position, self.other_robot_position)

        
        # #seting other robot orientation in euler -- roll pitch yaw
        # self.other_robot_orn=self.other_robot_pose.orientation.x, self.other_robot_pose.orientation.y, self.other_robot_pose.orientation.z, self.other_robot_pose.orientation.w 
        # self.other_robot_roll, self.other_robot_pitch, self.other_robot_yaw = p.getEulerFromQuaternion(self.other_robot_orn)
        
        
        
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

        

        

        # #seting other robot velocity angular and linear
        # self.other_robot_angular_velocity=self.other_robot_vel.angular.z
        # self.other_robot_linear_velocity=self.other_robot_vel.linear.x

        #setting goal position x and y and convering as egocentric to robot
        self.goal_position = self.goal_pos#np.array([self.goal_pose.position.x, self.goal_pose.position.y])
        
        self.goal_egocentric_position=self.world_to_robot(self.yaw, self.robot_own_position, self.goal_position)
        # print(self.goal_egocentric_position[0],self.goal_egocentric_position[1],self.yaw, self.other_robot_egocentric_position[0],self.other_robot_egocentric_position[1], self.other_robot_yaw,self.other_robot_linear_velocity, self.other_robot_angular_velocity,self.roll, self.pitch,self.linear_velocity,self.angular_velocity)

        return (self.goal_egocentric_position[0],self.goal_egocentric_position[1], self.roll, self.pitch,self.linear_velocity,self.angular_velocity)

    

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

        
        
        
        # if self.robot_pose is not None and self.other_robot_pose is not None and self.robot_vel is not None and self.other_robot_vel is not None and self.goal_pos is not None and self.im is not None:
        if self.robot_pose is not None and self.robot_vel is not None and self.goal_pos is not None and self.im is not None:
            
            t2=time.time()
            self.observations_r1 = self.get_observation()
            self.im_ocupancy=self.get_occupancy_image()
            # print("R1 input",self.observations_r1)
            
            # self.actions = pol.step(torch.as_tensor(np.array(self.observations), dtype=torch.float32), torch.as_tensor(self.im_ocupancy, dtype=torch.float32), stochastic=False)[0]
            a_r1=torch.as_tensor(np.array(self.observations_r1), dtype=torch.float32).unsqueeze(dim=0)
            b_r1=self.model_z(torch.as_tensor(self.im_ocupancy, dtype=torch.float32))
            print(a_r1,"br1",b_r1)
            print(np.array(a_r1.detach().numpy()).shape,np.array(b_r1.detach().numpy()).shape);exit()
            # print(a.shape)
            # print(b.shape)
            concatenate_part_r1=torch.concat((a_r1,b_r1),-1)

            
            self.actions = self.model_mu(concatenate_part_r1)
            clipped_linear_vel_command=np.clip(self.actions[0][0].detach().numpy(), -0.5, 1)
            clipped_angular_vel_command=np.clip(self.actions[0][1].detach().numpy(), -1.5, 1.5)

            self.actions[0]=torch.tensor([clipped_linear_vel_command,clipped_angular_vel_command])
            # print("r1_action",self.actions[0])
            # print("r1_wholeac",self.actions,type(self.actions),len(self.actions))
            msg.twist.linear.x = self.actions[0][0] #*0.4    
            msg.twist.angular.z = self.actions[0][1] #*0.8#np.pi /2
            # msg.twist.linear.x = 0  
            # msg.twist.angular.z = 1.5
            # print("msg.twist.angular.z",msg.twist.angular.z)

            # print("linear_actions_r1",self.actions[0][0] )

        # Action = self.model(state)
        # Assemble the msg using the acction
        # self.action_pub.publish(msg)

        # msg.twist.linear.x = 0.6    
        # msg.twist.angular.z = 0#np.pi /2
        # Take your state and foward your model, get an acction
        

        # Execute the acction 
            self.action_pub.publish(msg)

            # output_dir ="/home/kom018/behaviour_rl/Results_plots/Action_plots"
            output_dir ="/refarm/src/multi_robot_rl/scripts"

            self.buffer_linear_action.append(msg.twist.linear.x.detach().numpy())
            self.buffer_angular_action.append(msg.twist.angular.z.detach().numpy())
            # print("self.buffer_linear_action",self.buffer_linear_action);exit()
            # ttg=round(self.steps*self.timeStep_10Hz,2)
            

            # self.image = self.occupancy_map_to_image(self.im_ocupancy)


            # # Create a window with the specified name
            # cv2.namedWindow("Occupancy Map", cv2.WINDOW_NORMAL)

            # # Resize the window to a desired size
            # cv2.resizeWindow("Occupancy Map", 800, 600)
            # # Display the image
            # cv2.imshow("Occupancy Map", self.image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            self.image_r1 = self.occupancy_map_to_image(self.im_ocupancy)
            # print("OC",self.image_r1,self.current_sim_time.to_sec())
            # print("break")

            df1 = pd.DataFrame(self.im_ocupancy)
            csv_path = os.path.join(output_dir, 'occ.csv')
            df1.to_csv(csv_path, index=False)

            # # Create a window with the specified name
            cv2.namedWindow("R1 Occupancy Map", cv2.WINDOW_NORMAL)

            # Resize the window to a desired size
            cv2.resizeWindow("R1 Occupancy Map", 800, 600)
            # Display the image
            cv2.imshow("R1 Occupancy Map", self.image_r1)
            cv2.waitKey(1)

    def step_R3(self):
        msg = TwistStamped() # create a message

        # if self.robot_pose is not None and self.other_robot_pose is not None and self.robot_vel is not None and self.other_robot_vel is not None and self.goal_pos is not None and self.im is not None:
        if self.robot_pose is not None and self.robot_vel is not None and self.goal_pos is not None and self.im is not None:

            
            self.observations = self.get_observation()
            self.im_ocupancy=self.get_occupancy_image()
            
            # print("R3 input",self.observations)
            #self.actions = pol.step(torch.as_tensor(np.array(self.observations), dtype=torch.float32), torch.as_tensor(self.im_ocupancy, dtype=torch.float32), stochastic=False)[0]
            # self.actions = self.model_mu(torch.concat(torch.as_tensor(np.array(self.observations), dtype=torch.float32), ))  , stochastic=False
            a=torch.as_tensor(np.array(self.observations), dtype=torch.float32).unsqueeze(dim=0)
            b=self.model_z(torch.as_tensor(self.im_ocupancy, dtype=torch.float32))
            
            # print(a.shape)
            # print(b.shape)
            concatenate_part=torch.concat((a,b),-1)

            
            self.actions_r3 = self.model_mu(concatenate_part)

            clipped_linear_vel_command_r3=np.clip(self.actions_r3[0][0].detach().numpy(), -0.5, 1)
            clipped_angular_vel_command_r3=np.clip(self.actions_r3[0][1].detach().numpy(), -1.5, 1.5)
            
            self.actions_r3[0]=torch.tensor([clipped_linear_vel_command_r3,clipped_angular_vel_command_r3])


            #self.mu = self.mu_net(torch.concat((obs, self.z_net(im)), -1))
            # self.actions = self.model_mu(torch.concat((torch.as_tensor(np.array(self.observations), dtype=torch.float32), self.model_z(torch.as_tensor(self.im_ocupancy, dtype=torch.float32))), -1))
            # print("actions_r3",self.actions_r3[0] )
            # print("action",self.action[0][0])
            msg.twist.linear.x = self.actions_r3[0][0] #*0.4   
            msg.twist.angular.z = self.actions_r3[0][1]#*0.8#np.pi /2
            # msg.twist.linear.x = 1 #*0.4   
            # msg.twist.angular.z = 0#*0.8#np.pi /2
            # print("msg.twist.angular.z",msg.twist.angular.z)
            
        # Action = self.model(state)
        # Assemble the msg using the acction
        # self.action_pub.publish(msg)

        # msg.twist.linear.x = 0.3
        # msg.twist.angular.z = 0#np.pi /2
        # Take your state and foward your model, get an acction
        

        # Execute the acction 
            self.action_pub.publish(msg)

            self.buffer_linear_action.append(msg.twist.linear.x.detach().numpy())
            self.buffer_angular_action.append(msg.twist.angular.z.detach().numpy())
            self.image_r3 = self.occupancy_map_to_image(self.im_ocupancy)



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
    mu_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/FC/mu_net.jit")
    z_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/FC/z_net.jit")

    
    # print(pol)
    goal_R1=(28,-0.5)
    goal_R2=(28,0.5)

    # R1 = RLRobot("/r1/cmd_vel_stamped","/r1/slam/odom/high/pose","/r3/slam/odom/high/pose","/r1/slam/odom/high/velocity","/r3/slam/odom/high/velocity",goal_R1, "/r1/costmap_local/occupancy_grid", mu_net,z_net)
    # R3 = RLRobot("/r3/cmd_vel_stamped","/r3/slam/odom/high/pose","/r1/slam/odom/high/pose","/r3/slam/odom/high/velocity","/r1/slam/odom/high/velocity",goal_R2, "/r3/costmap_local/occupancy_grid", mu_net,z_net)
    
    # R1 = RLRobot("/r1/cmd_vel_stamped","/r1/slam/odom/high/pose","/r3/slam/odom/high/pose","/r1/slam/odom/high/velocity","/r3/slam/odom/high/velocity",goal_R1, "/r1/costmap_local/occupancy_grid", mu_net,z_net)
    # R3 = RLRobot("/r3/cmd_vel_stamped","/r3/slam/odom/high/pose","/r1/slam/odom/high/pose","/r3/slam/odom/high/velocity","/r1/slam/odom/high/velocity",goal_R2, "/r3/costmap_local/occupancy_grid", mu_net,z_net)


    R1 = RLRobot("/r1/cmd_vel_stamped","/r1/slam/odom/high/pose","/r1/slam/odom/high/velocity",goal_R1, "/r1/costmap_local/occupancy_grid", mu_net,z_net)
    R3 = RLRobot("/r3/cmd_vel_stamped","/r3/slam/odom/high/pose","/r3/slam/odom/high/velocity",goal_R2, "/r3/costmap_local/occupancy_grid", mu_net,z_net)
    
    
    control_rate = rospy.Rate(10) # 10 Hz
    t1=time.time()
    # R3.buffer_time.append(time.time()-R3.t1)
    
    while not rospy.is_shutdown():

       
        # action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        R1.step_R1()
        R3.step_R3()
        control_rate.sleep()
        # print("R1.buffer_linear_action",R1.buffer_linear_action)
        R1.buffer_time.append(R1.current_sim_time.to_sec())
        R3.buffer_time.append(R3.current_sim_time.to_sec())
        
        
        # # self.current_sim_time
        # # print("TIME",time.time()-t1,R1.buffer_time,"ac")
        
        # # output_dir ="/home/kom018/behaviour_rl/Results_plots/Action_plots"
        if R3.current_sim_time.to_sec()>10:
            output_dir ="/refarm/src/multi_robot_rl/scripts/plots"

            plt.figure()
            plt.plot(R1.buffer_time, R1.buffer_linear_obs, label='Robot1\'s Linear Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Robot1\'s Linear Velocity')
            plt.title('Robot1\'s Linear Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R1\'s_Linear_Velocity_plot.png'))

            # Plot the angular velocity actions over time
            plt.figure()
            plt.plot(R1.buffer_time, R1.buffer_angular_obs, label='Robot1\'s Angular Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Robot1\'s Angular Velocity')
            plt.title('Robot1\'s Angular Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R1\'s_Angular_Velocity_plot.png'))

            plt.figure()
            plt.plot(R1.buffer_time, R1.buffer_linear_action, label='Command Linear Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Command Linear Velocity')
            plt.title('Robot1\'s Command Linear Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R1_Command_Linear_Velocity_plot.png'))

            # Plot the angular velocity actions over time
            plt.figure()
            plt.plot(R1.buffer_time, R1.buffer_angular_action, label='Command Angular Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Command Angular Velocity')
            plt.title('Robot1\'s Command Angular Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R1_Command_angular_velocity_plot.png'))



            # Plot the trajectory
            plt.figure(figsize=(10, 6))
            plt.plot(R1.poses_x, R1.poses_y, label='Trajectory', marker='o', markersize=5, linestyle='-')

            # Annotate with time points
            for i in range(0, len(R1.buffer_time), 10):  # Annotate every 10th current_time step
                plt.annotate(f't={R1.buffer_time[i]:.1f}', (R1.poses_x[i], R1.poses_y[i]), textcoords="offset points", xytext=(10,-10), ha='center')

            # Labels and title
            plt.xlabel('X position')
            plt.ylabel('Y position')
            plt.title('Robot1 Trajectory Over current_time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R1_trajectory.png'))


            # # Save plot to a file
            # output_directory = 'plots'
            # os.makedirs(output_directory, exist_ok=True)
            # file_path = os.path.join(output_directory, 'robot_trajectory.png')
            # plt.savefig(file_path)

            data = {
            "Time": R1.buffer_time,
            "Command Linear Velocity": R1.buffer_linear_action,
            "Command Angular Velocity": R1.buffer_angular_action,
            "Robot's Linear Velocity": R1.buffer_linear_obs,
            "Robot's Angular Velocity": R1.buffer_angular_obs
            }
            df = pd.DataFrame(data)
            csv_path = os.path.join(output_dir, 'r1_actions_data.csv')
            df.to_csv(csv_path, index=False)
            df = pd.DataFrame(R1.scaled_map)
            csv_path = os.path.join(output_dir, 'r1_occu.csv')
            df.to_csv(csv_path, index=False)

            #ROBOT2
            plt.figure()
            plt.plot(R3.buffer_time, R3.buffer_linear_obs, label='Robot2\'s Linear Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Robot2\'s Linear Velocity')
            plt.title('Robot2\'s Linear Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R2\'s_Linear_Velocity_plot.png'))

            # Plot the angular velocity actions over time
            plt.figure()
            plt.plot(R3.buffer_time, R3.buffer_angular_obs, label='Robot2\'s Angular Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Robot2\'s Angular Velocity')
            plt.title('Robot2\'s Angular Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R2\'s_Angular_Velocity_plot.png'))

            plt.figure()
            plt.plot(R3.buffer_time, R3.buffer_linear_action, label='Command Linear Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Command Linear Velocity')
            plt.title('Robot2\'s Command Linear Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R2_Command_Linear_Velocity_plot.png'))

            # Plot the angular velocity actions over time
            plt.figure()
            plt.plot(R3.buffer_time, R3.buffer_angular_action, label='Command Angular Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Command Angular Velocity')
            plt.title('Robot2\'s Command Angular Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R2_Command_angular_velocity_plot.png'))


            # Plot the trajectory
            plt.figure(figsize=(10, 6))
            plt.plot(R3.poses_x, R3.poses_y, label='Trajectory', marker='o', markersize=5, linestyle='-')

            # Annotate with time points
            for i in range(0, len(R3.buffer_time), 10):  # Annotate every 10th current_time step
                plt.annotate(f't={R3.buffer_time[i]:.1f}', (R3.poses_x[i], R3.poses_y[i]), textcoords="offset points", xytext=(10,-10), ha='center')

            # Labels and title
            plt.xlabel('X position')
            plt.ylabel('Y position')
            plt.title('Robot2 Trajectory Over current_time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'R2_trajectory.png'))


            #PLOT BOTH ROBOT TRAJECTORY IN ONE PLOT
            # Plot the first trajectory
            plt.plot(R1.poses_x, R1.poses_y, label='Robot 1 Trajectory', marker='o', markersize=5, linestyle='-', color='blue')
            # Annotate the first trajectory with time points
            for i in range(0, len(R3.buffer_time), 10):  # Annotate every 10th R3.buffer_time step
                plt.annotate(f't={R3.buffer_time[i]:.1f}', (R1.poses_x[i], R1.poses_y[i]), textcoords="offset points", xytext=(10, -10), ha='center', color='blue')

            # Plot the second trajectory
            plt.plot(R3.poses_x, R3.poses_y, label='Robot 2 Trajectory', marker='o', markersize=5, linestyle='-', color='red')
            # Annotate the second trajectory with R3.buffer_time points
            for i in range(0, len(R3.buffer_time), 10):  # Annotate every 10th R3.buffer_time step
                plt.annotate(f't={R3.buffer_time[i]:.1f}', (R3.poses_x[i], R3.poses_y[i]), textcoords="offset points", xytext=(10, -10), ha='center', color='red')

            # Labels and title
            plt.xlabel('X position')
            plt.ylabel('Y position')
            plt.title('Two Robot Trajectories Over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'Merged_trajectory.png'))


            data = {
            "Time": R3.buffer_time,
            "Command Linear Velocity": R3.buffer_linear_action,
            "Command Angular Velocity": R3.buffer_angular_action,
            "Robot's Linear Velocity": R3.buffer_linear_obs,
            "Robot's Angular Velocity": R3.buffer_angular_obs
            }
            df = pd.DataFrame(data)
            csv_path = os.path.join(output_dir, 'r2_actions_data.csv')
            df.to_csv(csv_path, index=False)
            df = pd.DataFrame(R3.scaled_map)
            csv_path = os.path.join(output_dir, 'r2_occu.csv')
            df.to_csv(csv_path, index=False)
            print("THAM");exit()



        # # if np.array(R1.buffer_time).shape != np.array(R1.buffer_linear_obs).shape:
        # #     R1.buffer_linear_obs = np.zeros_like(R1.buffer_time)
        # # print("T",R1.current_sim_time.to_sec())
        # # output_dir ="/refarm/src/multi_robot_rl/scripts"
        # # print("R1.buffer_linear_obs",R1.buffer_linear_obs,R1.buffer_time)
        # plt.figure()
        # plt.plot(R1.buffer_time, R1.buffer_linear_obs, label='Robot\'s Linear Velocity')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Robot\'s Linear Velocity')
        # plt.title('Robot\'s Linear Velocity over Time')
        # plt.legend()
        # plt.grid(True)
        # plt.savefig(os.path.join(output_dir, 'Robot\'s_Linear_Velocity_plot.png'))

        # # Plot the angular velocity actions over time
        # plt.figure()
        # plt.plot(R1.buffer_time, R1.buffer_angular_obs, label='Robot\'s Angular Velocity')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Robot\'s Angular Velocity')
        # plt.title('Robot\'s Angular Velocity over Time')
        # plt.legend()
        # plt.grid(True)
        # plt.savefig(os.path.join(output_dir, 'Robot\'s_Angular_Velocity_plot.png'))

        # plt.figure()
        # plt.plot(R1.buffer_time, R1.buffer_linear_action, label='Command Linear Velocity')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Command Linear Velocity')
        # plt.title('Command Linear Velocity over Time')
        # plt.legend()
        # plt.grid(True)
        # plt.savefig(os.path.join(output_dir, 'Command_Linear_Velocity_plot.png'))

        # # Plot the angular velocity actions over time
        # plt.figure()
        # plt.plot(R1.buffer_time, R1.buffer_angular_action, label='Command Angular Velocity')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Command Angular Velocity')
        # plt.title('Command Angular Velocity over Time')
        # plt.legend()
        # plt.grid(True)
        # plt.savefig(os.path.join(output_dir, 'Command_angular_velocity_plot.png'))

        # # data = {
        # # "Time": R1.buffer_time,
        # # "Command Linear Velocity": R1.buffer_linear_action,
        # # "Command Angular Velocity": R1.buffer_angular_action,
        # # "Robot's Linear Velocity": R1.buffer_linear_obs,
        # # "Robot's Angular Velocity": R1.buffer_angular_obs
        # # }


        # # df = pd.DataFrame(data)
        # # csv_path = os.path.join(output_dir, 'actions_data.csv')
        # # df.to_csv(csv_path, index=False)
        
        # print("overal",time.time()-R1.t1)
        print("Sim_time",R1.current_sim_time.to_sec())
        # # print("Sim_time",R1.time_list[-1])
        # # if R1.current_sim_time>10:
        # # if R1.current_sim_time.to_sec()>10:
        # print("THAM");exit()

        print("step_time",time.time()-t1)
        
        t1=time.time()

        

