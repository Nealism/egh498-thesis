from assets.env_titan_pb_2 import Env as RobotEnv
import pybullet as p
from assets.env_base_pb import EnvBasePB
from mpi4py import MPI
comm = MPI.COMM_WORLD
from gym import spaces
import numpy as np
import cv2



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
                if self.args.return_fn==1:
                    self.ob_size = 14
                elif self.args.return_fn==2:
                    self.ob_size = 8
                elif self.args.return_fn==3:
                    self.ob_size = 16
                elif self.args.return_fn==4:
                    self.ob_size = 9
                elif self.args.return_fn==5:
                    self.ob_size = 17
            else:
                self.ob_size = 6
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
            # Global map initialization
            self.global_map_size_x = 100.0
            self.global_map_size_y = 100.0
            self.global_resolution = 0.1  # 0.1 meters per row and column
            self.global_num_rows = int(self.global_map_size_y / self.global_resolution)
            self.global_num_cols = int(self.global_map_size_x / self.global_resolution)
            self.global_map = np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32)

            # Local map initialization
            self.local_map_size_x = 8.0
            self.local_map_size_y = 8.0
            self.local_resolution = self.global_resolution
            self.local_num_rows = int(self.local_map_size_y / self.local_resolution)
            self.local_num_cols = int(self.local_map_size_x / self.local_resolution)
            self.local_map = np.zeros((self.local_num_rows, self.local_num_cols), dtype=np.float32)


    def reset(self):
        res = []
        self.obstacles=[]
        self.robots_bbox=[]
        self.steps = 0
        for Robot in self.robots:
            Robot.set_robot_bbox(self.robots_bbox)
            if self.args.obstacle_avoidance:
                Robot.set_obstacles(self.obstacles)
            res.append(Robot.reset())
        #print("GREAAATTTTTT", res)
        return res



    def step(self,actions):
        obs = []
        rews=[]
        dones=[]
        self.ob_dicts=[]

        self.obstacles=[]
        self.robots_bbox=[]
        self.robots_pos=[]
        self.local_heightmaps=[]
        self.local_heightmap_positions=[]
        self.Goals_pos=[]
        self.Obstacles_pos=[]
        for Robot in self.robots:
            #print(Robot,"s",self.robots)
            #self.ns.append(n)
            #self.ns.append(n)
            self.robots_bbox.append((Robot,Robot.robot1_bbox))
            self.robots_pos.append(Robot.pos[:2])
            self.Goals_pos.append(Robot.state_goal[:2])
            self.Obstacles_pos.append(Robot.pos2[:2])
        #print("self.Goals_pos",self.Goals_pos)
        if self.args.obstacle_avoidance:
            for Robot in self.robots:
                self.obstacles.append(Robot.square_bbox)

        for action,Robot in zip(actions,self.robots):
            
            Robot.motor_action(action)

        p.stepSimulation()

        for action,Robot in zip(actions,self.robots):
            
            Robot.set_robot_bbox(self.robots_bbox)
            if self.args.obstacle_avoidance:
                Robot.set_obstacles(self.obstacles)
            ob,rew,done, self.ob_dict=Robot.return_step(action)
            

            #Occupancy Map actions:
            
                
        

            # Robot.Id
            obs.append(ob)
            rews.append(rew)
            dones.append(done)

            self.ob_dicts.append(self.ob_dict)

        if self.args.occupancy_map: 
            #print(self.Obstacles_pos)   
            #A=self.insert_obstacle_with_object(self.Obstacles_pos[0][0], self.Obstacles_pos[0][1], 0, 1.0, 1.0, 0.2)  # Place the obstacle and a PyBullet object
            for obstacle_pos in self.Obstacles_pos:
                B=self.insert_obstacle_with_object(obstacle_pos[0], obstacle_pos[1], 0, 1.0, 1.0, 0.2)  # Place the obstacle and a PyBullet object
            # Get the local heightmap and its position within the local map

            #print(self.orn2)
            turtlebot_data=[]
            for robot_pos in self.robots_pos:
                local_heightmap, local_heightmap_position = self.get_heightmap(robot_pos)
                self.local_heightmaps.append(local_heightmap)
                self.local_heightmap_positions.append(local_heightmap_position)
                turtlebot_data.append((local_heightmap, local_heightmap_position, robot_pos))

            #print("local_heightmap1", self.local_heightmap_positions,len(self.local_heightmap_positions))
            # np.savetxt('occupancy_map1.txt', self.local_heightmaps[0])
            # np.savetxt('occupancy_map2.txt', self.local_heightmaps[1])
            #     M=self.visualize_maps(self.global_map, local_heightmap,local_heightmap_position,robot_pos)
            #     M_list.append(M)
            # # print("local_heightmap",local_heightmap,len(local_heightmap))
            # # print("all_local_heightmaps",self.local_heightmaps,len(self.local_heightmaps))
            # MM=M_list[0]
            # MM=M_list[1]
            # self.imshow_map(M)
            #print(self.robots_pos)
            #turtlebot_data=self.local_heightmaps,self.local_heightmap_positions,self.robots_pos
            #M=self.visualize_maps(self.global_map, turtlebot_data)
            # print(self.robots_pos[1])
            # print(self.Goals_pos[1])
            M=self.visualize_maps(self.global_map, self.local_heightmaps,self.local_heightmap_positions,self.robots_pos,self.Goals_pos)
            
            
        self.steps += 1
        #print("length",(self.robots_bbox))
        return obs, rews, dones, self.ob_dict
    
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

    def insert_obstacle_with_object(self,position_x, position_y, yaw, length, width, height):
        # Convert obstacle position and dimensions to grid indices
        grid_x_center = int((position_x + self.global_map_size_x / 2) / self.global_resolution)
        grid_y_center = int((position_y + self.global_map_size_y / 2) / self.global_resolution)
        
        # Calculate half-length and half-width in grid cells
        half_length_cells = int(length / (2 * self.global_resolution))
        half_width_cells = int(width / (2 * self.global_resolution))
        
        # Set the obstacle region in the global map to a higher value for visualization
        for i in range(grid_x_center - half_length_cells, grid_x_center + half_length_cells + 1):
            for j in range(grid_y_center - half_width_cells, grid_y_center + half_width_cells + 1):
                if 0 <= i < self.global_num_rows and 0 <= j < self.global_num_cols:
                    self.global_map[i, j] = 2.0  # Mark the obstacle as occupied with a value of 2

        # # Create a PyBullet box object to represent the obstacle
        # p.createMultiBody(
        #     baseMass=1,
        #     baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_BOX, halfExtents=[length/2, width/2, height/2]),
        #     basePosition=[position_x, position_y, height / 2],
        #     baseOrientation=p.getQuaternionFromEuler([0, 0, yaw]),
        # )

    # Function to get the local heightmap
    def get_heightmap(self,robot_position):
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

        # Extract the local heightmap from the global map
        local_heightmap = self.global_map[
            local_x_indices:local_x_indices + self.local_num_rows, local_y_indices:local_y_indices + self.local_num_cols
        ]

        # Calculate the position of the local heightmap within the local map
        local_heightmap_x_min = local_x_min
        local_heightmap_x_max = local_x_max
        local_heightmap_y_min = local_y_min
        local_heightmap_y_max = local_y_max

        #print("local_heightmap", local_heightmap,local_heightmap.shape)
         

        return local_heightmap, (local_heightmap_x_min, local_heightmap_x_max, local_heightmap_y_min, local_heightmap_y_max)

    # Function to visualize the maps using OpenCV

    def visualize_maps(self,global_map, local_heightmaps, local_heightmap_positions, robot_positions,goal_positions):
        #Scale the maps for visualization
        scaled_global_map = (global_map - np.min(global_map)) / (np.max(global_map) - np.min(global_map)) * 200
        # Convert to uint8 and create color images
        scaled_global_map = scaled_global_map.astype(np.uint8)
        global_map_image = cv2.cvtColor(scaled_global_map, cv2.COLOR_GRAY2BGR)
        # Set colors: Blue for global map, Green for local heightmap, Red for obstacles
        global_map_image[:, :, 0] = 255  # Blue channel to 255 for global map (blue color)

        
        #print("len",len(self.robots_pos))
        # Find obstacle cells and mark them as red
        obstacle_indices = np.where(global_map == 2.0)
        for i, j in zip(obstacle_indices[0], obstacle_indices[1]):
            global_map_image[i, j] = (0, 0, 255)  # Red color

        x_min,x_max,y_min,y_max=[],[],[],[]
        turtlebots_x_index,turtlebots_y_index=[],[]
        Goals_x_index,Goals_y_index=[],[]
        #prev_positions=[(0,0),(0,0)]
        heightmap_images=[]
        #print(robot_positions)
        for robot_position, goal_position,local_heightmap,local_heightmap_position in zip(robot_positions,goal_positions, local_heightmaps,local_heightmap_positions):
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
            #print("P",prev_positions)
            #print("C",robot_positions)
            
            

            # turtlebot_x_prev = int((prev_position[0] + self.global_map_size_x / 2) / self.global_resolution)
            # turtlebot_y_prev = int((prev_position[1] + self.global_map_size_y / 2) / self.global_resolution)
            # x_prev=turtlebot_x_prev
            # y_prev=turtlebot_y_prev
            
            # # Set the obstacle region in the global map to a higher value for visualization
            # for k in range(x_prev - half_length, x_prev + half_length + 1):
            #     for l in range(y_prev - half_width, y_prev + half_width + 1):
            #         if 0 <= k < self.global_num_rows and 0 <= l < self.global_num_cols:
            #             self.global_map[k, l] = 0.0  # Mark the obstacle as occupied with a value of 2
            
            # # Find obstacle cells and mark them as red
            # robot_indices = np.where(global_map == 1.0)
            # for m, n in zip(robot_indices[0], robot_indices[1]):
            #     global_map_image[m, n] = (255, 0, 0)  # Blue color

            # prev_positions=robot_positions
            # print("PC",prev_positions)
            x_min.append(local_map_x_min_index)
            x_max.append(local_map_x_max_index)
            y_min.append(local_map_y_min_index)
            y_max.append(local_map_y_max_index)
            turtlebots_x_index.append(turtlebot_x_index)
            turtlebots_y_index.append(turtlebot_y_index)

            Goals_x_index.append(Goal_x_index)
            Goals_y_index.append(Goal_y_index)

            heightmap_images.append(heightmap_image)
        #print("aa",heightmap_images)
        for i in range(len(self.robots_pos)):
            
            global_map_image[
            x_min[i]:x_max[i],
            y_min[i]:y_max[i],] = heightmap_images[i]

        for i in range(len(self.robots_pos)):
            global_map_image = cv2.circle(global_map_image, (turtlebots_y_index[i], turtlebots_x_index[i]), 5, (255, 0, 0), -1)
            global_map_image = cv2.circle(global_map_image, (Goals_y_index[i], Goals_x_index[i]), 5, (0, 255, 0), -1)
            

        for i in range(len(self.robots_pos)):
            # Calculate half-length and half-width in grid cells
            half_length = int(1.4 / (2 * self.global_resolution))
            half_width = int(0.7 / (2 * self.global_resolution))
            x_index=turtlebots_x_index[i]
            y_index=turtlebots_y_index[i]
            
            # Set the obstacle region in the global map to a higher value for visualization
            for k in range(x_index - half_length, x_index + half_length + 1):
                for l in range(y_index - half_width, y_index + half_width + 1):
                    if 0 <= k < self.global_num_rows and 0 <= l < self.global_num_cols:
                        self.global_map[k, l] = 1.0  # Mark the obstacle as occupied with a value of 2

            # Find obstacle cells and mark them as red
            robot_indices = np.where(global_map == 1.0)
            for m, n in zip(robot_indices[0], robot_indices[1]):
                global_map_image[m, n] = (255, 255, 255)  # Blue color


        cv2.imshow("Global Map with Local Heightmaps", global_map_image)
        cv2.waitKey(10)


    











