from assets.env_titan_pb_2 import Env as RobotEnv
import pybullet as p
from assets.env_base_pb import EnvBasePB
from mpi4py import MPI
comm = MPI.COMM_WORLD
from gym import spaces
import numpy as np
import cv2
import math
from copy import deepcopy



class Env(EnvBasePB):
    def __init__(self, PATH=None, args=None, writer=None):
    #def __init__(self, args.num_robots):
        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True
        
        super().__init__(PATH)

        self.all_log_things = [{} for _ in range(args.num_robots)]

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
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        self.steps = -1

        self.load_simulator()
        
        objects = p.loadMJCF("./assets/xmls/ground.xml")
        self.worldId = objects[0]
        self.robots=[RobotEnv(PATH=PATH, args=args, writer=writer) for n in range(args.num_robots)]
        # for Robot in self.robots:


        # #self.robots=[RobotEnv() for n in [args.num_robots]]
        #     print("GOOOD PRINTTT",Robot.reset())

        if self.args.occupancy_map:
            
            self.global_map_list=[]
            # Global map initialization
            #self.global_map=[]
            # for r in range(self.args.num_robots):
            #     print("r",r)
            self.global_map_size_x = 100.0
            self.global_map_size_y = 100.0
            self.global_resolution = 0.1  # 0.1 meters per row and column
            self.global_num_rows = int(self.global_map_size_y / self.global_resolution)
            self.global_num_cols = int(self.global_map_size_x / self.global_resolution)
            #self.global_map= np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32)
            # self.global_map[1]= np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32)
            self.global_map_list=[np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32) for _ in range(self.args.num_robots)]
            #print(self.global_map_list[1]);exit()
            #self.global_map2 = np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32)
            #print("len",len(self.global_map_list),"len1",len(self.global_map))
            # Local map initialization
            self.local_map_size_x = 8.0
            self.local_map_size_y = 8.0
            self.local_resolution = self.global_resolution
            self.local_num_rows = int(self.local_map_size_y / self.local_resolution)
            self.local_num_cols = int(self.local_map_size_x / self.local_resolution)
            self.local_map = np.zeros((self.local_num_rows, self.local_num_cols), dtype=np.float32)
            #if self.args.use_perception:
            self.im_size = [1,self.local_map.shape[0],self.local_map.shape[1]]
            #print("Im",self.im_size,"local",self.local_map.shape);exit()
    def reset(self):
        res = []
        self.obstacles=[]
        self.robots_bbox=[]
        self.robots_pos=[]
        self.robots_pos_with_IDx=[]
        self.steps = 0
        self.occupancy_maps=[]
        for Robot in self.robots:
            Robot.set_robot_bbox(self.robots_bbox)
            Robot.set_allrobot_positions(self.robots_pos_with_IDx)
            if self.args.obstacle_avoidance:
                Robot.set_obstacles(self.obstacles)
            res.append(Robot.reset())
        self.get_observation()
        #print("GREAAATTTTTT", res);exit()
        return res



    def step(self,actions):
        obs = []
        rews=[]
        dones=[]
        # self.ob_dicts=[]

        # self.obstacles=[]
        # self.robots_bbox=[]
        # self.robots_pos=[]
        # self.robots_orn=[]
        # self.local_heightmaps=[]
        # self.local_heightmap_positions=[]
        # self.Goals_pos=[]
        # self.Obstacles_pos=[]
        # self.robots_pos_with_IDx=[]
        # for Robot in self.robots:
        #     #print(Robot,"s",self.robots)
        #     #self.ns.append(n)
        #     #self.ns.append(n)
        #     self.robots_bbox.append((Robot,Robot.robot1_bbox))
        #     self.robots_pos_with_IDx.append((Robot,list(Robot.pos)))
        #     self.robots_pos.append(Robot.pos)
        #     self.robots_orn.append(Robot.yaw)
        #     self.Goals_pos.append(Robot.state_goal)
        #     self.Obstacles_pos.append(Robot.pos2)
        # #print("self.Goals_pos",self.Goals_pos)
        # if self.args.obstacle_avoidance:
        #     for Robot in self.robots:
        #         self.obstacles.append(Robot.square_bbox)

        for action,Robot in zip(actions,self.robots):
            
            Robot.motor_action(action)

        p.stepSimulation()
        #print("action_length",actions,"robot",self.robots)
        for action,Robot in zip(actions,self.robots):
            
            Robot.set_robot_bbox(self.robots_bbox)
            Robot.set_allrobot_positions(self.robots_pos_with_IDx)
            if self.args.obstacle_avoidance:
                Robot.set_obstacles(self.obstacles)
            ob,rew,done, self.ob_dict=Robot.return_step(action)
            #print("action_length",action,"robot",Robot)

            obs.append(ob)
            rews.append(rew)
            dones.append(done)
            #print("inside_rewards",rews)

            self.ob_dicts.append(self.ob_dict)

        
            #self.local_map = np.zeros((self.local_num_rows, self.local_num_cols), dtype=np.float32)
            
        self.steps += 1
        self.get_observation()
        return obs, rews, dones, self.ob_dict
    
    def get_image(self):

        if self.args.occupancy_map: 
            
            #self.occupancy_maps=[]
            turtlebot_data=[]
            self.local_heightmaps=[]
            self.local_heightmap_positions=[]
            for robot_pos,robot_orn in zip(self.robots_pos,self.robots_orn):

                local_heightmap, local_heightmap_position = self.get_heightmap(robot_pos,robot_orn)
                self.local_heightmaps.append(local_heightmap)
                self.local_heightmap_positions.append(local_heightmap_position)
                turtlebot_data.append((local_heightmap, local_heightmap_position, robot_pos))

            
            M=self.visualize_maps(self.global_map_list, self.local_heightmaps,self.local_heightmap_positions,self.robots_pos,self.Goals_pos,self.Obstacles_pos)
            #N=self.visualize_maps(self.global_map2, self.local_heightmaps,self.local_heightmap_positions,self.robots_pos,self.Goals_pos,self.Obstacles_pos)
            self.h1=np.savetxt('occupancy_map1.txt', self.local_heightmaps[0])
            #self.h2=np.savetxt('occupancy_map2.txt', self.local_heightmaps[1])
            self.occupancy_maps=deepcopy(self.local_heightmaps)
            #print(self.occupancy_maps)
            self.global_map_list=[np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32) for _ in range(self.args.num_robots)]

            # for r in range(self.args.num_robots):
            #     self.global_map = np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32)
            #     self.global_map_list.append(self.global_map)
        #print(self.occupancy_maps);exit()
        return np.array(self.occupancy_maps).reshape([self.args.num_robots]+self.im_size)
    
    def get_observation(self):

        obs = []
        rews=[]
        dones=[]
        self.ob_dicts=[]

        self.obstacles=[]
        self.robots_bbox=[]
        self.robots_pos=[]
        self.robots_orn=[]
        
        self.Goals_pos=[]
        self.Obstacles_pos=[]
        self.robots_pos_with_IDx=[]
        for Robot in self.robots:
            #print(Robot,"s",self.robots)
            #self.ns.append(n)
            #self.ns.append(n)
            self.robots_bbox.append((Robot,Robot.robot1_bbox))
            self.robots_pos_with_IDx.append((Robot,list(Robot.pos)))
            self.robots_pos.append(Robot.pos)
            self.robots_orn.append(Robot.yaw)
            self.Goals_pos.append(Robot.state_goal)
            self.Obstacles_pos.append(Robot.pos2)
        #print("self.Goals_pos",self.Goals_pos)
        if self.args.obstacle_avoidance:
            for Robot in self.robots:
                self.obstacles.append(Robot.square_bbox)

    
    def log_stuff(self, logger, num, writer, iters_so_far):
        log_things = self.robots[num].get_log_things()
        for thing in log_things:
            if isinstance(log_things[thing], int) or isinstance(log_things[thing], float):
                self.robots[num].all_log_things["all_" + thing + str(num)] = MPI.COMM_WORLD.allgather(log_things[thing])
            else:
                self.robots[num].all_log_things["all_" + thing + str(num)] = MPI.COMM_WORLD.allgather(np.mean(log_things[thing]))
            if self.rank == 0:
                print(thing, self.robots[num].all_log_things["all_" + thing + str(num)])
                writer.add_scalar(thing + "/" + str(num), np.mean(self.robots[num].all_log_things["all_" + thing + str(num)]), iters_so_far)
    
    
        # # Create a PyBullet box object to represent the obstacle
        # p.createMultiBody(
        #     baseMass=1,
        #     baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_BOX, halfExtents=[length/2, width/2, height/2]),
        #     basePosition=[position_x, position_y, height / 2],
        #     baseOrientation=p.getQuaternionFromEuler([0, 0, yaw]),
        # )

    # Function to get the local heightmap
    def get_heightmap(self,robot_position,robot_orientation):
        # Calculate the boundaries of the local map based on robot_position and local_map_size
        local_x_min = robot_position[0] - self.local_map_size_x / 2
        local_x_max = robot_position[0] + self.local_map_size_x / 2
        local_y_min = robot_position[1] - self.local_map_size_y / 2
        local_y_max = robot_position[1] + self.local_map_size_y / 2

        # Calculate grid indices for the local map within the global map
        local_x_indices = np.clip(
            np.array(((local_x_min + self.global_map_size_x / 2) / self.global_resolution), dtype=int), 0, self.global_num_rows - 1
        )
        local_y_indices = np.clip(
            np.array(((local_y_min + self.global_map_size_y / 2) / self.global_resolution), dtype=int), 0, self.global_num_cols - 1
        )

        for global_map in self.global_map_list:
            # Extract the local heightmap from the global map
            local_heightmap = global_map[
                local_x_indices:local_x_indices + self.local_num_rows, local_y_indices:local_y_indices + self.local_num_cols
            ]


        

            # Calculate the position of the local heightmap within the local map
            local_heightmap_x_min = local_x_min
            local_heightmap_x_max = local_x_max
            local_heightmap_y_min = local_y_min
            local_heightmap_y_max = local_y_max

            #print("local_heightmap", local_heightmap,local_heightmap.shape)
            # Rotate the local heightmap based on the robot's orientation
            local_heightmap = np.rot90(local_heightmap, k=int(math.degrees(robot_orientation) / 90))
         

        return local_heightmap, (local_heightmap_x_min, local_heightmap_x_max, local_heightmap_y_min, local_heightmap_y_max)

    # Function to visualize the maps using OpenCV

    def visualize_maps(self,global_map_list, local_heightmaps, local_heightmap_positions, robot_positions,goal_positions,obstalce_positions):
        

        
        #print("len",len(self.robots_pos))
        

        x_min,x_max,y_min,y_max=[],[],[],[]
        turtlebots_x_index,turtlebots_y_index=[],[]
        obstacles_x_index,obstacles_y_index=[],[]
        Goals_x_index,Goals_y_index=[],[]
        #prev_positions=[(0,0),(0,0)]
        globalmap_images=[]
        heightmap_images=[]
        #print(robot_positions)
        for robot_position, goal_position,local_heightmap,local_heightmap_position, obstalce_position,global_map in zip(robot_positions,goal_positions, local_heightmaps,local_heightmap_positions,obstalce_positions,global_map_list):
            #Scale the maps for visualization
            scaled_global_map = (global_map - np.min(global_map)) / (np.max(global_map) - np.min(global_map)) * 200
            # Convert to uint8 and create color images
            scaled_global_map = scaled_global_map.astype(np.uint8)
            global_map_image = cv2.cvtColor(scaled_global_map, cv2.COLOR_GRAY2BGR)
            # Set colors: Blue for global map, Green for local heightmap, Red for obstacles
            global_map_image[:, :, :] = 128  # Blue channel to 255 for global map (blue color)
            
            
            #print("WEW",local_heightmaps,len(local_heightmaps), local_heightmap_positions,len(local_heightmap_positions))
            scaled_heightmap = (local_heightmap - np.min(local_heightmap)) / (np.max(local_heightmap) - np.min(local_heightmap)) * 200
            scaled_heightmap = scaled_heightmap.astype(np.uint8)
            heightmap_image = cv2.cvtColor(scaled_heightmap, cv2.COLOR_GRAY2BGR)
            heightmap_image[:, :, 1] = 155  # Green channel to 255 for local heightmap (green color)
            #print("HP",heightmap_image)
            # Calculate the position of the local heightmap within the global map
            local_map_x_min = local_heightmap_position[0]
            local_map_x_max = local_heightmap_position[1]
            local_map_y_min = local_heightmap_position[2]
            local_map_y_max = local_heightmap_position[3]

            
            local_map_x_min_index = int((local_map_x_min + self.global_map_size_x / 2) / self.global_resolution)
            local_map_x_max_index = int((local_map_x_max + self.global_map_size_x / 2) / self.global_resolution)
            local_map_y_min_index = int((local_map_y_min + self.global_map_size_y / 2) / self.global_resolution)
            local_map_y_max_index = int((local_map_y_max + self.global_map_size_y / 2) / self.global_resolution)

            turtlebot_x_index = int((robot_position[0] + self.global_map_size_x / 2) / self.global_resolution)
            turtlebot_y_index = int((robot_position[1] + self.global_map_size_y / 2) / self.global_resolution)
            
            
            Goal_x_index = int((goal_position[0] + self.global_map_size_x / 2) / self.global_resolution)
            Goal_y_index = int((goal_position[1] + self.global_map_size_y / 2) / self.global_resolution)
            
            obstacle_x_index = int((obstalce_position[0] + self.global_map_size_x / 2) / self.global_resolution)
            obstacle_y_index = int((obstalce_position[1] + self.global_map_size_y / 2) / self.global_resolution)

            x_min.append(local_map_x_min_index)
            x_max.append(local_map_x_max_index)
            y_min.append(local_map_y_min_index)
            y_max.append(local_map_y_max_index)
            turtlebots_x_index.append(turtlebot_x_index)
            turtlebots_y_index.append(turtlebot_y_index)

            Goals_x_index.append(Goal_x_index)
            Goals_y_index.append(Goal_y_index)

            
            obstacles_x_index.append(obstacle_x_index)
            obstacles_y_index.append(obstacle_y_index)

            globalmap_images.append(global_map_image)
            heightmap_images.append(heightmap_image)
        #print("aa",heightmap_images)
        #print(len(globalmap_images));exit()
        for global_map_image in globalmap_images:
            for i in range(len(self.robots_pos)):
                global_map_image[
                x_min[i]:x_max[i],
                y_min[i]:y_max[i],] = heightmap_images[i]
        #print(i)
        # Find obstacle cells and mark them as red
        if self.args.obstacle_avoidance:
            for global_map in global_map_list:
                for i in range(len(self.Obstacles_pos)):

                    # Calculate half-length and half-width in grid cells
                    half_length_cells = int(1.2 / (2 * self.global_resolution))
                    half_width_cells = int(1.2 / (2 * self.global_resolution))
                    
                    grid_x_center=obstacles_x_index[i]
                    grid_y_center=obstacles_y_index[i]


                    # Set the obstacle region in the global map to a higher value for visualization
                    for p in range(grid_x_center - half_length_cells, grid_x_center + half_length_cells + 1):
                        for q in range(grid_y_center - half_width_cells, grid_y_center + half_width_cells + 1):
                            if 0 <= p < self.global_num_rows and 0 <= q < self.global_num_cols:
                                global_map[p, q] = 1.0
        for index,(global_map,global_map_image) in enumerate(zip(global_map_list,globalmap_images)):
            for i in range(len(self.robots_pos)):
                global_map_image = cv2.circle(global_map_image, (turtlebots_y_index[i], turtlebots_x_index[i]), 5, (255, 0, 0), -1)
                global_map_image = cv2.circle(global_map_image, (Goals_y_index[i], Goals_x_index[i]), 5, (0, 255, 0), -1)
            
                # print("index",index,"i",i)
                if index!=i:
                #     print("True")
                    # Calculate robot-length and robot-width in grid cells
                    robot_length = int(1.4 / (2 * self.global_resolution))
                    robot_width = int(0.7 / (2 * self.global_resolution))
                    x_index=turtlebots_x_index[i]
                    y_index=turtlebots_y_index[i]
                    
                    # Set the obstacle region in the global map to a higher value for visualization
                    for k in range(x_index - robot_length, x_index + robot_length + 1):
                        for l in range(y_index - robot_width, y_index + robot_width + 1):
                            if 0 <= k < self.global_num_rows and 0 <= l < self.global_num_cols:
                                global_map[k, l] = 1.0  # Mark the obstacle as occupied with a value of 1
                # elif index==i:
                #     print("True")
                #     # Calculate robot-length and robot-width in grid cells
                #     robot_length = int(1.4 / (2 * self.global_resolution))
                #     robot_width = int(0.7 / (2 * self.global_resolution))
                #     x_index=turtlebots_x_index[i]
                #     y_index=turtlebots_y_index[i]
                    
                #     # Set the obstacle region in the global map to a higher value for visualization
                #     for k in range(x_index - robot_length, x_index + robot_length + 1):
                #         for l in range(y_index - robot_width, y_index + robot_width + 1):
                #             if 0 <= k < self.global_num_rows and 0 <= l < self.global_num_cols:
                #                 global_map[k, l] = 0.0

        for (global_map_image,global_map) in zip(globalmap_images,global_map_list):
            obstacle_indices = np.where(global_map == 1.0)
            # obstacle_indices2 = np.wherdee(global_map == 2.0)
            for f, g in zip(obstacle_indices[0], obstacle_indices[1]):
                global_map_image[f, g] = (0, 0, 255)  # Red color
            # for f, g in zip(obstacle_indices2[0], obstacle_indices2[1]):
            #     global_map_image[f, g] = (0, 155, 255)  # Red color
            # # Find obstacle cells and mark them as red
            # robot_indices = np.where(global_map == 1.0)
            # for m, n in zip(robot_indices[0], robot_indices[1]):
            #     global_map_image[m, n] = (0, 0, 255)  # Blue color
            
            # Find obstacle cells and mark them as red
            # robot_indices = np.where(global_map == 2.0)
            # for m, n in zip(robot_indices[0], robot_indices[1]):
            #     global_map_image[m, n] = (150, 0, 150)  # Blue color

            
        if self.args.map_show:

            # # Create separate OpenCV windows for each global map
            # cv2.namedWindow("Global Map with Local Heightmaps1", cv2.WINDOW_NORMAL)
            # cv2.namedWindow("Global Map with Local Heightmaps2", cv2.WINDOW_NORMAL)
            for index,global_map_image in enumerate(globalmap_images):
                #cv2.imshow("Global Map with Local Heightmaps"+str(index), globalmap_images)
                window_name = "Global Map with Local Heightmaps" + str(index)
                cv2.imshow(window_name, global_map_image)

            # cv2.imshow("Global Map with Local Heightmaps1", globalmap_images[0])
            # cv2.imshow("Global Map with Local Heightmaps2", globalmap_images[1])
            # Wait for a short delay to ensure the first window is initialized
            #cv2.waitKey(100)    
            #cv2.imshow("Global Map with Local Heightmaps2", globalmap_images[1])
            cv2.waitKey(10)
                #cv2.destroyAllWindows()



    











