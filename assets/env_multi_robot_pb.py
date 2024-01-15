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
import random



class Env(EnvBasePB):
    def __init__(self, PATH=None, args=None, writer=None):
    #def __init__(self, args.num_robots):
        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True
        #self.robottogoal_angles=[(200),(250)]
        self.rectangle_id1=0
        self.rectangle_id2=0
        
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
                self.ob_size = 16+2*(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_1 and self.args.occupancy_map and self.args.use_perception:
                #print("owch")    
                self.ob_size = 6#+2 *(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_2 and self.args.occupancy_map and self.args.use_perception:
                
                #print("owch")
                self.ob_size = 6+2 *(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_3 and self.args.occupancy_map and self.args.use_perception:
                
                #print("owch")
                self.ob_size = 6+5 *(self.args.num_robots-1)
                
            elif self.args.gap_avoidance:
                self.ob_size = 26+2*(self.args.num_robots-1)
            else:
                #print("nowch")
                self.ob_size = 6+2*(self.args.num_robots-1)
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
        self.Goals_pos=[]
        self.initial_goal_distances=[]
        self.gap_walls_thickness=[]
        #self.gap_walls_length=[]
        self.gap_walls1_centre=[]
        self.gap_walls2_centre=[]
        self.external_goals_states=[]
        self.external_goals_states_with_IDx=[]
        self.wall1_corners=[]
        self.wall2_corners=[]
        self.All_Robot_ID=[]

        self.robots_orn_with_IDx=[]
        self.robots_vx_with_IDx=[]
        self.robots_angular_vx_with_IDx=[]
        
        

        bodies_to_remove = [self.rectangle_id1, self.rectangle_id2]
        
        random_0_10=random.uniform(0,10),random.uniform(0,10),0.31

        for Robot in self.robots:
            self.initial_goal_distances.append(Robot.initial_goal_dist)
            self.All_Robot_ID.append(Robot)
            
            
            # 
            # self.gap_walls_length.append(Robot.each_wall_length)

        if self.args.gap_avoidance and self.args.insert_wall:
            
            p.removeBody(self.rectangle_id1)
            p.removeBody(self.rectangle_id2)
            
             
            

        if self.args.num_robots ==4:
            self.robottogoal_angles=[(self.robots[0],0),(self.robots[1],0),(self.robots[2],0),(self.robots[3],0)]
            self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+2,0.31]),(self.robots[2],[list(random_0_10)[0]+0,list(random_0_10)[1]-2,0.31]),(self.robots[3],[list(random_0_10)[0]+0,list(random_0_10)[1]-4,0.31])]
            # self.external_robots_pos=[(self.robots[0],[1,1,0.31]),(self.robots[1],[2.5,2.5,0.31]),(self.robots[2],[4,4,0.31])]
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                self.external_goals_states.append(self.external_goal_state)
                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))

        elif self.args.num_robots ==3:
            self.robottogoal_angles=[(self.robots[0],0),(self.robots[1],0),(self.robots[2],0)]
            self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+2,0.31]),(self.robots[2],[list(random_0_10)[0]+0,list(random_0_10)[1]-2,0.31])]
            # self.external_robots_pos=[(self.robots[0],[1,1,0.31]),(self.robots[1],[2.5,2.5,0.31]),(self.robots[2],[4,4,0.31])]
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                self.external_goals_states.append(self.external_goal_state)
                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        elif self.args.num_robots ==2:
            if self.args.collision_likelihood_curr:
                self.robottogoal_angles=[(self.robots[0],-5),(self.robots[1],5)]
            elif not self.args.collision_likelihood_curr:
                self.robottogoal_angles=[(self.robots[0],15),(self.robots[1],-15)]

            self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+2,0.31])]
            # self.external_robots_pos=[(self.robots[0],[0,0,0.31]),(self.robots[1],[-2,-1.5,0.31])]
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                self.external_goals_states.append(self.external_goal_state)

                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        else:
            self.robottogoal_angles=[(self.robots[0],0)]
            self.external_robots_pos=[(self.robots[0],list(random_0_10))]
            #self.external_robots_pos=[(self.robots[0],[0,1,0.31])]
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                self.external_goals_states.append(self.external_goal_state)
                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))

        # self.mid_point_of_goals=self.calculate_midpoint(self.external_goals_states[0],self.external_goals_states[-1])
        #print("self.mid_point_of_goals",self.mid_point_of_goals)

        
            
        

        self.steps = 0
        self.occupancy_maps=[]
        for Robot in self.robots:
            # self.Goals_pos.append(Robot.state_goal)
            Robot.set_Robots_ID(self.All_Robot_ID)
            Robot.set_robot_bbox(self.robots_bbox)
            Robot.set_allrobot_positions(self.robots_pos_with_IDx)
            Robot.set_allrobot_orientation(self.robots_orn_with_IDx)
            Robot.set_allrobot_vx(self.robots_vx_with_IDx)
            Robot.set_allrobot_angular_velocity(self.robots_angular_vx_with_IDx)

            Robot.set_external_goals_state(self.external_goals_states_with_IDx)
            Robot.set_all_goal_poses(self.Goals_pos)
            Robot.set_external_robots_pos(self.external_robots_pos)
            Robot.set_robottogoal_angle(self.robottogoal_angles)
            Robot.set_wall1_corners(self.wall1_corners)
            Robot.set_wall1_corners(self.wall2_corners)

            if self.args.obstacle_avoidance:
                Robot.set_obstacles(self.obstacles)
            
            res.append(Robot.reset())


            if self.args.gap_avoidance:
                self.gap_walls1_centre.append(Robot.rectangle1_centre)
                self.gap_walls2_centre.append(Robot.rectangle2_centre)
                self.gap_walls_thickness.append(Robot.tunnel_depth)

        if self.args.num_robots>1 and self.args.gap_avoidance:
            self.max_gap_among_all_robots_individual_gap_width=max(self.All_Robot_ID[0].gap_width,self.All_Robot_ID[1].gap_width)  
        elif self.args.num_robots==1 and self.args.gap_avoidance:
            self.max_gap_among_all_robots_individual_gap_width=self.All_Robot_ID[0].gap_width


        
        #print("GP_MA",self.max_gap_among_all_robots_individual_gap_width,self.All_Robot_ID[0].gap_width,self.All_Robot_ID[1].gap_width)

        if self.args.gap_avoidance and self.args.insert_wall:
            # self.rectangle_id1=self.square
            # self.rectangle_id2=self.square

            wall1_corners=Robot.gap[0]
            wall2_corners=Robot.gap[1]
            #print(wall1_corners,wall2_corners)

            
            self.rectangle_id1=self.create_rectangle(ID=1,corners=Robot.gap[0],wall_length=20,wall_width=Robot.tunnel_depth,wall_height=0.5,orientation=Robot.gap_orn)
            self.rectangle_id2=self.create_rectangle(ID=2,corners=Robot.gap[1],wall_length=20,wall_width=Robot.tunnel_depth,wall_height=0.5,orientation=Robot.gap_orn)

            

            
                # self.gap_walls_length.append(Robot.each_wall_length)
        self.get_observation()
        #print("GREAAATTTTTT", self.initial_goal_distances)
        return res



    def step(self,actions):
        obs = []
        rews=[]
        dones=[]
        self.Both_Robots_stuck=[]
        self.turn_both=False
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

            if self.args.gap_avoidance:
                self.Both_Robots_stuck.append(Robot.robot1_near_robot2)


            # print("self.Both_Robots_stuck",self.Both_Robots_stuck,len(self.Both_Robots_stuck))
            if all(self.Both_Robots_stuck) and len(self.Both_Robots_stuck)==2:
                
                self.turn_both=True
                # print("turn_both",self.turn_both)


        p.stepSimulation()
        #print("action_length",actions,"robot",self.robots)
        for action,Robot in zip(actions,self.robots):
            
            Robot.set_robot_bbox(self.robots_bbox)
            Robot.set_allrobot_positions(self.robots_pos_with_IDx)
            Robot.set_allrobot_orientation(self.robots_orn_with_IDx)
            Robot.set_allrobot_vx(self.robots_vx_with_IDx)
            Robot.set_allrobot_angular_velocity(self.robots_angular_vx_with_IDx)

            Robot.set_all_goal_poses(self.Goals_pos)
            Robot.set_robottogoal_angle(self.robottogoal_angles)
            Robot.set_external_robots_pos(self.external_robots_pos)
            if self.args.obstacle_avoidance:
                Robot.set_obstacles(self.obstacles)

            if self.args.gap_avoidance:
                Robot.set_turn_both(self.turn_both)
                Robot.set_max_robotcode_gap_width(self.max_gap_among_all_robots_individual_gap_width)
            
                
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

            
            M=self.visualize_maps(self.global_map_list, self.local_heightmaps,self.local_heightmap_positions,self.robots_pos,self.Goals_pos,self.Obstacles_pos,self.gap_walls1_centre,self.gap_walls2_centre)
            #N=self.visualize_maps(self.global_map2, self.local_heightmaps,self.local_heightmap_positions,self.robots_pos,self.Goals_pos,self.Obstacles_pos)
            #self.h1=np.savetxt('occupancy_map1.txt', self.local_heightmaps[0])
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
        #print("GREAAATTTTTT", self.initial_goal_distances)

        self.obstacles=[]
        self.robots_bbox=[]
        self.robots_pos=[]
        self.robots_orn=[]
        
        self.Goals_pos=[]
        self.Obstacles_pos=[]
        self.robots_pos_with_IDx=[]
        self.wall1_corners=[]
        self.wall2_corners=[]
        self.robots_orn_with_IDx=[]
        self.robots_vx_with_IDx=[]
        self.robots_angular_vx_with_IDx=[]
        

        # self.rectangle_id3=self.create_rectangle(corners=self.gap[0],wall_length=20,wall_width=self.tunnel_depth,wall_height=0.5,orientation=self.gap_orn)
        # for Robot in self.robots:
        #     self.initial_goal_distances.append(Robot.initial_goal_dist)

        # if self.args.num_robots ==3:
        #     self.robottogoal_angles=[(self.robots[0],10),(self.robots[1],30),(self.robots[2],50)]
        #     self.external_robots_pos=[(self.robots[0],[1,1,0.31]),(self.robots[1],[2.5,2.5,0.31]),(self.robots[2],[4,4,0.31])]
        #     for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
        #         self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
        #         self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        # elif self.args.num_robots ==2:
        #     self.robottogoal_angles=[(self.robots[0],0),(self.robots[1],0)]
        #     self.external_robots_pos=[(self.robots[0],[0,0,0.31]),(self.robots[1],[0,2.5,0.31])]
        #     for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
        #         self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
        #         self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        # else:
        #     self.robottogoal_angles=[(self.robots[0],0)]
        #     self.external_robots_pos=[(self.robots[0],[1,1,0.31])]
        #     for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
        #         self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
        #         self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))


        for Robot in self.robots:
            #print(Robot,"s",self.robots)
            #self.ns.append(n)
            #self.ns.append(n)

            self.robots_orn_with_IDx.append((Robot,[Robot.yaw]))
            self.robots_vx_with_IDx.append((Robot,[Robot.vx]))
            self.robots_angular_vx_with_IDx.append((Robot,[Robot.yaw_vel]))
            
            self.robots_bbox.append((Robot,Robot.robot1_bbox))
            self.robots_pos_with_IDx.append((Robot,list(Robot.pos)))
            self.robots_pos.append(Robot.pos)
            self.robots_orn.append(Robot.yaw)
            self.Goals_pos.append(Robot.state_goal)
            self.Obstacles_pos.append(Robot.pos2)
            # self.wall1_corners.append(Robot.gap[0])
            # self.wall2_corners.append(Robot.gap[1])
        #print(self.robots_pos_with_IDx)
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
    
    def visualize_maps(self,global_map_list, local_heightmaps, local_heightmap_positions, robot_positions,goal_positions,obstalce_positions,gap_walls1_centre,gap_walls2_centre):
        

        #
        #print("len",len(self.robots_pos))
        

        x_min,x_max,y_min,y_max=[],[],[],[]
        turtlebots_x_index,turtlebots_y_index=[],[]

        obstacles_x_index,obstacles_y_index=[],[]

        gap_wall1s_x_index,gap_wall1s_y_index,gap_wall2s_x_index,gap_wall2s_y_index=[],[],[],[]
        Goals_x_index,Goals_y_index=[],[]
        #prev_positions=[(0,0),(0,0)]
        globalmap_images=[]
        heightmap_images=[]
        #print(robot_positions)
        #print("a",obstalce_positions);exit()
        # ,gap_wall1_centre,gap_wall2_centre
        # ,gap_walls1_centre,gap_walls2_centre
        if self.args.gap_avoidance:
            for gap_wall1_centre,gap_wall2_centre in zip(gap_walls1_centre,gap_walls2_centre):
                
                gap_wall1_x_index = int((gap_wall1_centre[0] + self.global_map_size_x / 2) / self.global_resolution)
                gap_wall1_y_index = int((gap_wall1_centre[1] + self.global_map_size_y / 2) / self.global_resolution)

                gap_wall2_x_index = int((gap_wall2_centre[0] + self.global_map_size_x / 2) / self.global_resolution)
                gap_wall2_y_index = int((gap_wall2_centre[1] + self.global_map_size_y / 2) / self.global_resolution)

                gap_wall1s_x_index.append(gap_wall1_x_index)
                gap_wall1s_y_index.append(gap_wall1_y_index)

                gap_wall2s_x_index.append(gap_wall2_x_index)
                gap_wall2s_y_index.append(gap_wall2_y_index)

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
                    
                    #print("o",obstacles_x_index);exit()
                    grid_x_center=obstacles_x_index[i]
                    grid_y_center=obstacles_y_index[i]


                    # Set the obstacle region in the global map to a higher value for visualization
                    for p in range(grid_x_center - half_length_cells, grid_x_center + half_length_cells + 1):
                        for q in range(grid_y_center - half_width_cells, grid_y_center + half_width_cells + 1):
                            if 0 <= p < self.global_num_rows and 0 <= q < self.global_num_cols:
                                global_map[p, q] = 1.0
        
        if self.args.gap_avoidance:
            for global_map in global_map_list:
                for i in range(len(self.gap_walls1_centre)):

                    # Calculate half-length and half-width in grid cells
                    half_length_cells = int(self.gap_walls_thickness[0] / (2 * self.global_resolution))
                    half_width_cells = int(20 / (2 * self.global_resolution))
                    #half_width_cells = int(self.gap_walls_length[0] / (2 * self.global_resolution))
                    
                    #print("rr",self.gap_walls1_centre);exit
                    wall1_x_center=gap_wall1s_x_index[i]
                    wall1_y_center=gap_wall1s_y_index[i]

                    wall2_x_center=gap_wall2s_x_index[i]
                    wall2_y_center=gap_wall2s_y_index[i]


                    # Set the obstacle region in the global map to a higher value for visualization
                    for p in range(wall1_x_center - half_length_cells, wall1_x_center + half_length_cells + 1):
                        for q in range(wall1_y_center - half_width_cells, wall1_y_center + half_width_cells + 1):
                            if 0 <= p < self.global_num_rows and 0 <= q < self.global_num_cols:
                                global_map[p, q] = 1.0

                    # Set the obstacle region in the global map to a higher value for visualization
                    for p in range(wall2_x_center - half_length_cells, wall2_x_center + half_length_cells + 1):
                        for q in range(wall2_y_center - half_width_cells, wall2_y_center + half_width_cells + 1):
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


    def gap_generator(self,width, depth,height,pos,wall_length,goal_pos,lineId,lineIdgap,lineIdA,lineIdB):
        # print("gap_pos",pos)
        # print("gap_goal_pos",goal_pos)

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
        P1=self.calculate_opposite_point(PP1,PP2,distance=2)
        P2=self.calculate_opposite_point(PP2,PP1,distance=2)
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
        
        Wall1_rectangle=robot2_bbox
        Wall2_rectangle=robot3_bbox
        

        Wall1_centre=[(Wall1_rectangle[0][i] + Wall1_rectangle[2][i]) / 2 for i in range(3)]
        Wall2_centre=[(Wall2_rectangle[0][i] + Wall2_rectangle[2][i]) / 2 for i in range(3)]
        # print("r1",robot1_bbox)
        # print("r2",robot2_bbox)
        #corners=robot2_bbox
        
        # p.createMultiBody(
        #     baseMass=1,
        #     baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_BOX, halfExtents=[length/2, width/2, height/2]),
        #     basePosition=[position_x, position_y, height / 2],
        #     baseOrientation=p.getQuaternionFromEuler([0, 0, yaw]),
        # )

        return Wall1_rectangle,Wall2_rectangle,WP1,WP2,orn,Wall1_centre,Wall2_centre
    
    def create_rectangle(self,ID,corners,wall_length,wall_width,wall_height,orientation):

        # Calculate the center and half extents of the rectangle
        #half_extents = [(corners[2][i] - corners[0][i])/2 for i in range(3)]
        
        center = [(corners[0][i] + corners[2][i]) / 2 for i in range(3)]
        half_extents=[((wall_length/2)), wall_width, wall_height/2]

        
        # Create a collision shape for the rectangle
        box_collision_shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)

        # Create the rectangle using createMultiBody and attach the collision shape
        ID = p.createMultiBody(baseMass=0,
                                baseCollisionShapeIndex=box_collision_shape_id,
                                basePosition=center,baseOrientation=orientation)

        return ID
    
    def find_position_B(self,position_a, distance_d, angle_degrees):
        # Convert the angle from degrees to radians
        #print(angle_degrees);exit()
        angle_radians = math.radians(angle_degrees)
        
        #print("position_a",position_a)
        # Calculate the coordinates (x, y) of position B
        x_b = position_a[0] + distance_d * math.cos(angle_radians)
        y_b = position_a[1] + distance_d * math.sin(angle_radians)
        z_b=0

        return x_b, y_b,z_b
    
    def calculate_midpoint(self,point1, point2):
        x1, y1, z1 = point1
        x2, y2, z1 = point2

        # Calculate the midpoint
        midpoint_x = (x1 + x2) / 2
        midpoint_y = (y1 + y2) / 2

        midpoint = (midpoint_x, midpoint_y,z1)
        return midpoint
    
    def distance(self,point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)



    











