### This Code is Authored by "MD MOSTAFIZUR RAHMAN KOMOL" 
# The code is for testing RL model with Multi Robot System passing through Narrow Gap in Gazebo SIM
# In this code, Ros Topics for Robot Information and Occupancy map is called in Init. Init function also call the RL model as topic which is loaded using torch. 
# Occupancy Map local function align occupancy map to proper axis and convert to binary 2D cell grid with 0 and 1. 
# Occupancy map to image function convert values to image
# Get Occupancy Image Return Occupancy map input
# Get Observation Return the Robot Information like Robot Relative Goal Position, Robot Roll, Pitch, Heading Velocity, Angular Velocity
# World to Robot Function is to convert global goal coordinates to robot relative goal posiiton
# Step_R1 function is for Robot 1 action execution. Here, Robot Information and Occupancy Map is called from observation function and get occupancy image. Such individual robot input is then input into RL model and we get robot 1 actions (linear and angular velocity) which we send to robot through twist msg command. This function also draw the map of occupancy of robot 1.
# Step_R3 function is for robot 2 action execution. Here, Robot Information and Occupancy Map is called from observation function and get occupancy image. Such individual robot input is then input into RL model and we get robot 2 actions (linear and angular velocity) which we send to robot through twist msg command. This function also draw the map of occupancy of robot 2.
# Then we simply execute the code using rospy, we load the RL models using torch.load(directory), we define goal, we run the class, we run the step_R1 and Step_R3 functions in a control loop of 10 Hz.


import rospy
from geometry_msgs.msg import TwistStamped, PoseStamped
from nav_msgs.msg import Odometry, OccupancyGrid
import numpy as np
import time
import cv2
import torch
import pybullet as p
import time
from rosgraph_msgs.msg import Clock


class RLRobot():
    
    def __init__(self, cmd_topic, topic1_robotpos, topic3_robotvel, topic5_goalpos, occupancy_topic, model_mu,model_z):
        self.action_pub = rospy.Publisher(cmd_topic, TwistStamped)
        self.robot_topic=topic1_robotpos
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
        rospy.Subscriber(topic3_robotvel, TwistStamped, self.odom_callback3)
        rospy.Subscriber(occupancy_topic, OccupancyGrid, self.occupancy_callbacklocal)
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
        
        
    def occupancy_callbacklocal(self, msg6:OccupancyGrid):
        # Convert the occupancy map data to a numpy array
        width = msg6.info.width
        height = msg6.info.height
        map_data = np.array(msg6.data).reshape((height, width))

        #Flip the map horizontally
        map_data = np.fliplr(map_data)
        
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
        
        
    
        
        

    def occupancy_map_to_image(self,occupancy_map):
        # Convert the list of lists to a NumPy array
        occupancy_map_array = np.array(occupancy_map)
        
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

        
        self.robot_own_posX=self.robot_pose.position.x
        self.robot_own_posY=self.robot_pose.position.y

        self.poses_x.append(self.robot_own_posX)
        self.poses_y.append(self.robot_own_posY)

        self.robot_own_position=(self.robot_own_posX,self.robot_own_posY)
        
        self.orn=self.robot_pose.orientation.x, self.robot_pose.orientation.y, self.robot_pose.orientation.z, self.robot_pose.orientation.w 
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
        

        
        #seting robot own velocity angular and linear
        self.angular_velocity=self.robot_vel.angular.z
        self.linear_velocity=self.robot_vel.linear.x
        

        self.buffer_linear_obs.append(self.linear_velocity)
        self.buffer_angular_obs.append(self.angular_velocity)
        
        #setting goal position x and y and convering as egocentric to robot
        self.goal_position = self.goal_pos
        
        self.goal_egocentric_position=self.world_to_robot(self.yaw, self.robot_own_position, self.goal_position)

        self.buffer_relative_goal_pos_x_obs.append(self.goal_egocentric_position[0])
        self.buffer_relative_goal_pos_y_obs.append(self.goal_egocentric_position[1])

        self.buffer_roll_obs.append(self.roll)
        self.buffer_pitch_obs.append(self.pitch)
        

        return (self.goal_egocentric_position[0],self.goal_egocentric_position[1], self.roll, self.pitch,self.linear_velocity,self.angular_velocity)

    

    def world_to_robot(self, robot_yaw, robot, world):
        x,y = world[0] - robot[0], world[1] - robot[1]                       #longitudinal distance
        rot_mat = np.array([[np.cos(robot_yaw), np.sin(robot_yaw)],          #rotational distance
                             [-np.sin(robot_yaw), np.cos(robot_yaw)]])
        return list(np.dot(rot_mat, np.array([x, y])))
    
    


    def step_R1(self):
        msg = TwistStamped() # create a message

        if self.robot_pose is not None and self.robot_vel is not None and self.goal_pos is not None and self.im is not None:
            
            t2=time.time()
            self.observations_r1 = self.get_observation()
            self.im_ocupancy=self.get_occupancy_image()
            
            a_r1=torch.as_tensor(np.array(self.observations_r1), dtype=torch.float32).unsqueeze(dim=0)
            b_r1=self.model_z(torch.as_tensor(self.im_ocupancy, dtype=torch.float32))
            
            concatenate_part_r1=torch.concat((a_r1,b_r1),-1)

            
            self.actions = self.model_mu(concatenate_part_r1)
            
            clipped_linear_vel_command=np.clip(self.actions[0][0].detach().numpy(), -0.5, 0.75)
            clipped_angular_vel_command=np.clip(self.actions[0][1].detach().numpy(), -1.5, 1.5)

            self.actions[0]=torch.tensor([clipped_linear_vel_command,clipped_angular_vel_command])
            
            msg.twist.linear.x = self.actions[0][0]
            msg.twist.angular.z = self.actions[0][1] 
            

        # Execute the acction 
            self.action_pub.publish(msg)

            self.buffer_linear_action.append(msg.twist.linear.x.detach().numpy())
            self.buffer_angular_action.append(msg.twist.angular.z.detach().numpy())
            
            self.image_r1 = self.occupancy_map_to_image(self.im_ocupancy)
            
            self.robot1_images.append(self.image_r1)
            

            # # Create a window with the specified name
            cv2.namedWindow("R1 Occupancy Map", cv2.WINDOW_NORMAL)

            # Resize the window to a desired size
            cv2.resizeWindow("R1 Occupancy Map", 800, 600)
            # Display the image
            cv2.imshow("R1 Occupancy Map", self.image_r1)
            cv2.waitKey(1)

    def step_R3(self):
        msg = TwistStamped() # create a message

        
        if self.robot_pose is not None and self.robot_vel is not None and self.goal_pos is not None and self.im is not None:

            
            self.observations = self.get_observation()
            self.im_ocupancy=self.get_occupancy_image()
            
            a=torch.as_tensor(np.array(self.observations), dtype=torch.float32).unsqueeze(dim=0)
            b=self.model_z(torch.as_tensor(self.im_ocupancy, dtype=torch.float32))
            
            
            concatenate_part=torch.concat((a,b),-1)

            
            self.actions_r3 = self.model_mu(concatenate_part)
            

            clipped_linear_vel_command_r3=np.clip(self.actions_r3[0][0].detach().numpy(), -0.5, 0.75)
            clipped_angular_vel_command_r3=np.clip(self.actions_r3[0][1].detach().numpy(), -1.5, 1.5)
            
            self.actions_r3[0]=torch.tensor([clipped_linear_vel_command_r3,clipped_angular_vel_command_r3])


            msg.twist.linear.x = self.actions_r3[0][0]   
            msg.twist.angular.z = self.actions_r3[0][1]
        

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
            cv2.imshow("R3 Occupancy Map", self.image_r3)
            cv2.waitKey(1)
            

if __name__ == "__main__":
    rospy.init_node("robotclass_test")

    #model = RL(warever to load it)
    
    mu_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan3/mu_net.jit")
    z_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan3/z_net.jit")
    
    # mu_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan85/mu_net_S.jit")
    # z_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan85/z_net_S.jit")
    
    goal_R1=(8,-0.5)
    goal_R2=(8,1.3)


    R1 = RLRobot("/r1/cmd_vel_stamped","/r1/slam/odom/high/pose","/r1/slam/odom/high/velocity",goal_R1, "/r1/costmap_local/occupancy_grid", mu_net,z_net)
    R3 = RLRobot("/r3/cmd_vel_stamped","/r3/slam/odom/high/pose","/r3/slam/odom/high/velocity",goal_R2, "/r3/costmap_local/occupancy_grid", mu_net,z_net)
    
    act=None
    control_rate = rospy.Rate(10) # 10 Hz
    t1=time.time()
    
    
    while not rospy.is_shutdown():
        if R1.robot_pose is not None and R1.robot_vel is not None and R1.goal_pos is not None and R1.im is not None and R3.robot_pose is not None and R3.robot_vel is not None and R3.goal_pos is not None and R3.im is not None:
            R1.step_R1()
            R3.step_R3()
        control_rate.sleep()

        R1.buffer_time.append(R1.current_sim_time.to_sec())
        R3.buffer_time.append(R3.current_sim_time.to_sec())
        
        t1=time.time()

        

