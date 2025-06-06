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
# import cv2
import torch
import pybullet as p
import time
# from rosgraph_msgs.msg import Clock


class RLRobot():
    
    def __init__(self, cmd_topic, topic1_robotpos, topic3_robotvel, topic5_goalpos, occupancy_topic, model_full_fc,cnn_to_vector, cnn):
        self.action_pub = rospy.Publisher(cmd_topic, TwistStamped)
        self.robot_topic=topic1_robotpos
        self.goal_pos=topic5_goalpos
        # self.model_output_layer=model_output_layer
        # self.model_feature_layers=model_feature_layers
        # self.model_z=model_z

        self.model_full_fc = model_full_fc
        self.cnn = cnn
        self.cnn_to_vector = cnn_to_vector
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
        # rospy.Subscriber("/clock", Clock, self.clock_callback)
        self.t1=time.time()




        

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
        #self.map_storage.append(self.ascaled_map)
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

        

        self.robot_own_position=(self.robot_own_posX,self.robot_own_posY)
        
        self.orn=self.robot_pose.orientation.x, self.robot_pose.orientation.y, self.robot_pose.orientation.z, self.robot_pose.orientation.w 
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
        

        
        #seting robot own velocity angular and linear
        self.angular_velocity=self.robot_vel.angular.z
        self.linear_velocity=self.robot_vel.linear.x
        

        
        
        #setting goal position x and y and convering as egocentric to robot
        self.goal_position = self.goal_pos
        
        self.goal_egocentric_position=self.world_to_robot(self.yaw, self.robot_own_position, self.goal_position)

        
        

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

            # 1. Prepare observation vector
            a_r1 = torch.as_tensor(np.array(self.observations_r1), dtype=torch.float32).unsqueeze(dim=0)  # [1, obs_dim]

            # 2. Image input
            image_tensor = torch.as_tensor(self.im_ocupancy, dtype=torch.float32).unsqueeze(0)  # [1, C, H, W]

            # 3. CNN feature extraction
            cnn_output = self.cnn(image_tensor)  # output: [1, 64]
            # print("CNN output:", cnn_output.shape)

            # 4. Combine observation and image features
            combined_input = torch.cat((a_r1, cnn_output), dim=-1)  # shape [1, 6 + 64] = [1, 70]
            # print("Combined input:", combined_input.shape)

            # 5. Pass through full FC layers (which you had named cnn_to_vector)
            feature_vector = self.cnn_to_vector(combined_input)

            # print("FEATUR",feature_vector)
            self.actions = self.model_full_fc(feature_vector) 
            # self.actions = self.cnn_to_vector(combined_input)


            # # Prepare observation tensor
            # a_r1 = torch.as_tensor(np.array(self.observations_r1), dtype=torch.float32).unsqueeze(dim=0)

            # # Step 1: CNN image feature extraction
            # image_tensor = torch.as_tensor(self.im_ocupancy, dtype=torch.float32).unsqueeze(0)  # [B,C,H,W] assumed
            # cnn_output = self.model_feature_layers(image_tensor)

            # # Step 2: Flatten + FC from image features
            # image_features = self.model_z(cnn_output)

            # # Step 3: Concatenate image + observation
            # combined_input = torch.concat((a_r1, image_features), dim=-1)

            # # #Step 4: Final output layer
            # self.actions = self.model_output_layer(combined_input)
            #_____________________OLD__________________
            # a_r1=torch.as_tensor(np.array(self.observations_r1), dtype=torch.float32).unsqueeze(dim=0)
            # b_r1=self.model_z(torch.as_tensor(self.im_ocupancy, dtype=torch.float32))
            
            # concatenate_part_r1=torch.concat((a_r1,b_r1),-1)
            # print("ACTIONS",self.actions)
            
            # self.actions = self.model_mu(concatenate_part_r1)
            
            clipped_linear_vel_command=np.clip(self.actions[0][0].detach().numpy(), -0.5, 0.8)
            # clipped_angular_vel_command=np.clip(self.actions[0][1].detach().numpy(), -1.5, 1.5)
            clipped_angular_vel_command=np.clip(self.actions[0][1].detach().numpy(), -0.75, 0.75)

            #change from tensor to float just , not np array
            self.actions[0]=torch.tensor([clipped_linear_vel_command,clipped_angular_vel_command])
            
            msg.twist.linear.x = self.actions[0][0]
            msg.twist.angular.z = self.actions[0][1] 
            

        # Execute the acction 
            self.action_pub.publish(msg)
            # print(msg)

            
            
            self.image_r1 = self.occupancy_map_to_image(self.im_ocupancy)
            
            self.robot1_images.append(self.image_r1)
            

            # # # Create a window with the specified name
            # cv2.namedWindow("R1 Occupancy Map", cv2.WINDOW_NORMAL)

            # # Resize the window to a desired size
            # cv2.resizeWindow("R1 Occupancy Map", 800, 600)
            # # Display the image
            # cv2.imshow("R1 Occupancy Map", self.image_r1)
            # cv2.waitKey(1)

    
            

if __name__ == "__main__":
    rospy.init_node("robotclass_test")

    #model = RL(warever to load it)
    
    # mu_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan3/mu_net.jit")
    # z_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan3/z_net.jit")

    titan_output_layer = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/Jit_model_Heterogeneous/titan_output_13.jit")
    # mu_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/Jit_model_Heterogeneous/mu_net.jit")
    z_net = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/Jit_model_Heterogeneous/z_net_13.jit")
    feature_layers = torch.load("/refarm/src/multi_robot_rl/scripts/JIT_models/Jit_model_Heterogeneous/feature_layers_13.jit")

    # mu_net = torch.load("/home/aslab/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan3/mu_net.jit")
    # z_net = torch.load("/home/aslab/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan3/z_net.jit")
    
    
    
    # goal_R1=(8,-0.5)
    # goal_R1=(8,0.5)
    # goal_R1=(12,1)
    # goal_R1=(8,-1.85) #1m
    goal_R1=(8,-1.8)
    


    # R1 = RLRobot("/r1/cmd_vel_stamped","/r1/slam/odom/high/pose","/r1/slam/odom/high/velocity",goal_R1, "/r1/costmap_local/occupancy_grid", mu_net,z_net)
    R1 = RLRobot("/bear/cmd_vel_stamped","/r3/slam/odom/high/pose","/r3/slam/odom/high/velocity",goal_R1, "/r3/costmap_local/occupancy_grid",titan_output_layer, feature_layers, z_net)
    # print()
    
    act=None
    control_rate = rospy.Rate(10) # 10 Hz
    t1=time.time()
    
    
    while not rospy.is_shutdown():
        if R1.robot_pose is not None and R1.robot_vel is not None and R1.goal_pos is not None and R1.im is not None:
            R1.step_R1()
            
        control_rate.sleep()

        
        
        
        t1=time.time()

        

