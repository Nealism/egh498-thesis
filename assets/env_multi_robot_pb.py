from assets.env_titan_pb_2 import Env as TitanEnv
from assets.env_spot_pb_2 import Env as SpotEnv
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
import time
import matplotlib.pyplot as plt
import os
import pandas as pd
from scipy.ndimage import label, generate_binary_structure



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
        self.rectangle_id3=0
        self.rectangle_id4=0
        self.start_time=time.time()

        
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
                self.ob_size = 7+5 *(self.args.num_robots-1)

            elif self.args.gap_avoidance and self.args.experiment_3:

                self.ob_size = 27+5*(self.args.num_robots-1)
                
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
        

        if self.args.multi_spots:
            self.robots=[SpotEnv(PATH=PATH, args=args, writer=writer) for n in range(args.num_robots)]
            self.z_position=0.4555
        elif self.args.multi_titans:
            self.robots=[TitanEnv(PATH=PATH, args=args, writer=writer) for n in range(args.num_robots)]
            self.z_position=0.031
        elif self.args.heterogeneous:
            self.robots=[TitanEnv(PATH=PATH, args=args, writer=writer),SpotEnv(PATH=PATH, args=args, writer=writer) ]
            self.z_position=0.4555
        # self.robots=[SpotEnv(PATH=PATH, args=args, writer=writer) for n in range(args.num_robots)]
        # print("ronots",self.robots)

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
            # print("Im",self.im_size,"local",self.local_map.shape);exit()
    def reset(self):
        res = []
        if self.args.map_noise:
            self.noise=np.random.choice([0.0,0.3])
        else:
            self.noise=0.0
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

        self.side_walls1_centre=[]
        self.side_walls2_centre=[]

        self.external_goals_states=[]
        self.external_goals_states_with_IDx=[]
        self.wall1_corners=[]
        self.wall2_corners=[]
        self.All_Robot_ID=[]

        self.robots_orn_with_IDx=[]
        self.robots_vx_with_IDx=[]
        self.robots_angular_vx_with_IDx=[]


        self.buffer_linear_action=[]
        self.buffer_angular_action=[]

        self.buffer_linear_obs=[]
        self.buffer_angular_obs=[]

        self.buffer_time=[]

        self.random_robot_init=np.random.choice([6,8,9,10])
        
        # self.wall_length=3.7
        self.wall_length=1.7

        if self.args.gap_offset:
            self.gap_offset=np.random.uniform(-0.5,0.5)
        else:
            self.gap_offset=0
        # self.gap_offset=-1.5
        

        bodies_to_remove = [self.rectangle_id1, self.rectangle_id2]
        
        random_0_10=random.uniform(0,10),random.uniform(0,10),self.z_position
        # print("random_0_10",random_0_10)

        for Robot in self.robots:
            self.initial_goal_distances.append(Robot.initial_goal_dist)
            self.All_Robot_ID.append(Robot)
            
            
            # 
            # self.gap_walls_length.append(Robot.each_wall_length)

        if self.args.gap_avoidance and self.args.insert_wall:
            
            p.removeBody(self.rectangle_id1)
            p.removeBody(self.rectangle_id2)
            p.removeBody(self.rectangle_id3)
            p.removeBody(self.rectangle_id4)
            
             
            

        if self.args.num_robots ==4:
            self.robottogoal_angles=[(self.robots[0],0),(self.robots[1],0),(self.robots[2],0),(self.robots[3],0)]
            self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+2,self.z_position]),(self.robots[2],[list(random_0_10)[0]+0,list(random_0_10)[1]-2,self.z_position]),(self.robots[3],[list(random_0_10)[0]+0,list(random_0_10)[1]-4,self.z_position])]
            # self.external_robots_pos=[(self.robots[0],[1,1,self.z_position]),(self.robots[1],[2.5,2.5,self.z_position]),(self.robots[2],[4,4,self.z_position])]
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                self.external_goals_states.append(self.external_goal_state)
                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))

        elif self.args.num_robots ==3:
            self.robottogoal_angles=[(self.robots[0],0),(self.robots[1],0),(self.robots[2],0)]
            self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+2,self.z_position]),(self.robots[2],[list(random_0_10)[0]+0,list(random_0_10)[1]-2,self.z_position])]
            # self.external_robots_pos=[(self.robots[0],[1,1,self.z_position]),(self.robots[1],[2.5,2.5,self.z_position]),(self.robots[2],[4,4,self.z_position])]
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                self.external_goals_states.append(self.external_goal_state)
                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        elif self.args.num_robots ==2:
            synchoniser_value=np.random.uniform(1.5, 3)
            if self.args.generalise:
                goal_offset_cross=np.random.uniform(6.0, 7.5)
                goal_offset_front=np.random.uniform(0.5, 2.0)
                goal_offset=np.random.choice([goal_offset_cross,goal_offset_front])
            else:
                goal_offset=7.5
            self.robot_goal_synchroniser=np.random.choice([-synchoniser_value,synchoniser_value]) #change value to increase gap between robots #This synchroniser ensire robots and goals are crossing to each other even when external robot position are swapping
            if self.args.collision_likelihood_curr:
                self.robottogoal_angles=[(self.robots[0],self.robot_goal_synchroniser*-2.5),(self.robots[1],self.robot_goal_synchroniser*2.5)]
            elif not self.args.collision_likelihood_curr:
                # self.robottogoal_angles=[(self.robots[0],self.robot_goal_synchroniser*7.5),(self.robots[1],self.robot_goal_synchroniser*-7.5)]
                # self.robottogoal_angles=[(self.robots[0],self.robot_goal_synchroniser*7.5),(self.robots[1],self.robot_goal_synchroniser*-7.5)]
                self.robottogoal_angles=[(self.robots[0],self.robot_goal_synchroniser*goal_offset),(self.robots[1],self.robot_goal_synchroniser*-goal_offset)]


            if self.args.randomness==0:
                self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+2,self.z_position])]
            elif self.args.randomness==1:
                # self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+self.robot_goal_synchroniser,self.z_position])]
                self.external_robots_pos=[(self.robots[0],list((random_0_10))),(self.robots[1],[list(random_0_10)[0]+0,list(random_0_10)[1]+self.robot_goal_synchroniser,self.z_position])]
            elif self.args.randomness==2:
                self.external_robots_pos=[(self.robots[0],list(random_0_10)),(self.robots[1],[list(random_0_10)[0]+np.random.choice([-1,0,-0,1]),list(random_0_10)[1]+self.robot_goal_synchroniser,self.z_position])]
            # self.external_robots_pos=[(self.robots[0],[0,0,self.z_position]),(self.robots[1],[-2,-1.5,self.z_position])]
            # print("list(random_0_10)[1]-2",list(random_0_10)[1]-2)
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                self.external_goals_states.append(self.external_goal_state)

                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        else:
            self.robottogoal_angles=[(self.robots[0],0)]
            self.external_robots_pos=[(self.robots[0],list(random_0_10))]
            # print("self.external_robots_pos",self.external_robots_pos)
            #self.external_robots_pos=[(self.robots[0],[0,1,self.z_position])]
            
            for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
                self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
                # print("robot_pos[1]",robot_pos[1])
                # self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, np.random.uniform(5,-5))
                self.external_goals_states.append(self.external_goal_state)
                self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))

        # self.mid_point_of_goals=self.calculate_midpoint(self.external_goals_states[0],self.external_goals_states[-1])
        #print("self.mid_point_of_goals",self.mid_point_of_goals)
        # print("rob_poses",self.external_robots_pos)
        
            
        

        self.steps = 0
        self.occupancy_maps=[]

        # shape = (2, 1, 80, 80)
        # self.prev_occupancy_maps=[[[[random.random() for _ in range(shape[3])] for _ in range(shape[2])] for _ in range(shape[1])] for _ in range(shape[0])]
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
            
            Robot.set_random_robotinit(self.random_robot_init)

            if self.args.obstacle_avoidance:
                Robot.set_obstacles(self.obstacles)
            
            res.append(Robot.reset())


            if self.args.gap_avoidance:
                self.gap_walls1_centre.append(Robot.rectangle1_centre)
                self.gap_walls2_centre.append(Robot.rectangle2_centre)
                self.side_walls1_centre.append(Robot.rectangle3_centre)
                self.side_walls2_centre.append(Robot.rectangle4_centre)
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

            
            self.rectangle_id1=self.create_rectangle(ID=1,corners=Robot.gap[0],wall_length=self.wall_length+self.gap_offset,wall_width=Robot.tunnel_depth,wall_height=1,orientation=Robot.gap_orn)
            self.rectangle_id2=self.create_rectangle(ID=2,corners=Robot.gap[1],wall_length=self.wall_length-self.gap_offset,wall_width=Robot.tunnel_depth,wall_height=1,orientation=Robot.gap_orn)


            perpendicular_direction = [Robot.gap_orn[1], -Robot.gap_orn[0], 0]

            

            # Given orientation (orn)
            orn_wallright = Robot.gap_orn
            perpendicular_orn = p.getQuaternionFromEuler((0, 0, p.getEulerFromQuaternion(Robot.gap_orn)[2] + (math.pi / 2)))
            # perpendicular_orn = p.getQuaternionFromEuler((0, 0, np.random.randint(1,3)))
            


            self.rectangle_id3=self.create_rectangle(ID=3,corners=Robot.sidewalls[0],wall_length=25,wall_width=Robot.tunnel_depth,wall_height=2,orientation=perpendicular_orn)
            self.rectangle_id4=self.create_rectangle(ID=4,corners=Robot.sidewalls[1],wall_length=25,wall_width=Robot.tunnel_depth,wall_height=2,orientation=perpendicular_orn)

            

            
                # self.gap_walls_length.append(Robot.each_wall_length)
        self.get_observation()


        #print("GREAAATTTTTT", self.initial_goal_distances)
        return res



    def step(self,actions):
        obs = []
        rews=[]
        dones=[]
        terminations=[]
        self.Both_Robots_stuck=[]
        self.turn_both=False
        # self.ob_dicts=[]
        # actions=[[0.0,1.5]]

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

        # for action,Robot in zip(actions,self.robots):
            
        #     Robot.motor_action(action)

        #     if self.args.gap_avoidance:
        #         self.Both_Robots_stuck.append(Robot.robot1_near_robot2)


        #     # print("self.Both_Robots_stuck",self.Both_Robots_stuck,len(self.Both_Robots_stuck))
        #     if all(self.Both_Robots_stuck) and len(self.Both_Robots_stuck)==2:
                
        #         self.turn_both=True
        #         # print("turn_both",self.turn_both)
        # print(actions[0],"a")
        if self.args.train_figure:
            clipped_linear_vel_command=round(np.clip(actions[0][0], -0.5, 1),2)
            clipped_angular_vel_command=round(np.clip(actions[0][1], -1.5, 1.5),2)

            self.clipped_applied_actions=[clipped_linear_vel_command,clipped_angular_vel_command]
            
            self.buffer_linear_action.append(clipped_linear_vel_command)
            self.buffer_angular_action.append(clipped_angular_vel_command)
            ttg=round(self.steps*self.timeStep_10Hz,2)
            self.buffer_time.append(ttg)


            output_dir ="/home/kom018/behaviour_rl/Results_plots/Action_plots/Pybullet/train_plots"

            plt.figure()
            plt.plot(self.buffer_time, self.buffer_linear_action, label='Command Linear Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Command Linear Velocity')
            plt.title('Command Linear Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'Command_Linear_Velocity_plot.png'))

            # Plot the angular velocity actions over time
            plt.figure()
            plt.plot(self.buffer_time, self.buffer_angular_action, label='Command Angular Velocity')
            plt.xlabel('Time (s)')
            plt.ylabel('Command Angular Velocity')
            plt.title('Command Angular Velocity over Time')
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'Command_angular_velocity_plot.png'))


            # print("self.buffer_linear_action",self.buffer_linear_action,"self.buffer_angular_action",self.buffer_angular_action)
        if self.args.multi_titans or self.args.multi_spots:
            for action,Robot in zip(actions,self.robots):
            
                Robot.motor_action(action)

                if self.args.gap_avoidance:
                    self.Both_Robots_stuck.append(Robot.robot1_near_robot2)


                # print("self.Both_Robots_stuck",self.Both_Robots_stuck,len(self.Both_Robots_stuck))
                if all(self.Both_Robots_stuck) and len(self.Both_Robots_stuck)==2:
                    
                    self.turn_both=True
                    # print("turn_both",self.turn_both)

        if self.args.multi_titans:
            for _ in range(int(self.timeStep_10Hz/self.simStep)):
                # print("self.steps",self.steps,self)
                p.stepSimulation()
        
        # print("OUTSIDELOOOOP",int(self.timeStep_10Hz/self.timeStep_50Hz))
        if self.args.multi_spots:

            for _ in range(int(self.timeStep_10Hz/self.timeStep_50Hz)):
                # print("LOOOOOP111111111111111111")
                for action,Robot in zip(actions,self.robots):
                    Robot.motor_action_LL()
                for _ in range(int(self.timeStep_50Hz/self.simStep)):
                    # print("LOOOOOP___________222222222heteroheterohetero22")
                    for action,Robot in zip(actions,self.robots):

                        Robot.step2()
                    p.stepSimulation()
                    # print("ANything")
                for action,Robot in zip(actions,self.robots):
                    Robot.get_observation2()


        if self.args.heterogeneous:

            for action,Robot in zip(actions,self.robots):
            
                Robot.motor_action(action)

                if self.args.gap_avoidance:
                    self.Both_Robots_stuck.append(Robot.robot1_near_robot2)


                # print("self.Both_Robots_stuck",self.Both_Robots_stuck,len(self.Both_Robots_stuck))
                if all(self.Both_Robots_stuck) and len(self.Both_Robots_stuck)==2:
                    
                    self.turn_both=True
                    # print("turn_both",self.turn_both)
                # if self.args.multi_titans:
                #     for _ in range(int(self.timeStep_10Hz/self.simStep)):
                #         p.stepSimulation()
                
                # print("OUTSIDELOOOOP",int(self.timeStep_10Hz/self.timeStep_50Hz))
                # if self.args.multi_spots:

            for _ in range(int(self.timeStep_10Hz/self.timeStep_50Hz)):
                # print("LOOOOOP111111111111111111")
                # for action,Robot in zip(actions,self.robots):
                self.robots[1].motor_action_LL()
                for _ in range(int(self.timeStep_50Hz/self.simStep)):
                    # print("LOOOOOP___________22222222222")
                    # for action,Robot in zip(actions,self.robots):

                    self.robots[1].step2()
                    p.stepSimulation()
                    # print("ANything")
                # for action,Robot in zip(actions,self.robots):
                self.robots[1].get_observation2()
        # p.stepSimulation()
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
            
                
            ob,rew,done,termination, self.ob_dict=Robot.return_step(action)
            #print("action_length",action,"robot",Robot)
            if self.args.train_figure:
                # print(ob)
                ob_lin=round(ob[4],4)
                ob_ang=round(ob[5],4)
                self.buffer_linear_obs.append(ob_lin)
                self.buffer_angular_obs.append(ob_ang)
                output_dir ="/home/kom018/behaviour_rl/Results_plots/Action_plots/Pybullet/train_plots"

                plt.figure()
                plt.plot(self.buffer_time, self.buffer_linear_obs, label='Robot\'s Linear Velocity')
                plt.xlabel('Time (s)')
                plt.ylabel('Robot\'s Linear Velocity')
                plt.title('Robot\'s Linear Velocity over Time')
                plt.legend()
                plt.grid(True)
                plt.savefig(os.path.join(output_dir, 'Robot\'s_Linear_Velocity_plot.png'))

                # Plot the angular velocity actions over time
                plt.figure()
                plt.plot(self.buffer_time, self.buffer_angular_obs, label='Robot\'s Angular Velocity')
                plt.xlabel('Time (s)')
                plt.ylabel('Robot\'s Angular Velocity')
                plt.title('Robot\'s Angular Velocity over Time')
                plt.legend()
                plt.grid(True)
                plt.savefig(os.path.join(output_dir, 'Robot\'s_Angular_Velocity_plot.png'))

                data = {
                    "Time": self.buffer_time,
                    "Command Linear Velocity": self.buffer_linear_action,
                    "Command Angular Velocity": self.buffer_angular_action,
                    "Robot's Linear Velocity": self.buffer_linear_obs,
                    "Robot's Angular Velocity": self.buffer_angular_obs
                }
                df = pd.DataFrame(data)
                csv_path = os.path.join(output_dir, 'actions_data.csv')
                df.to_csv(csv_path, index=False)
                print(ttg)
                if self.steps*self.timeStep_10Hz>10:
                    print("THAM");exit()

                
            obs.append(ob)
            rews.append(rew)
            dones.append(done)
            terminations.append(termination)
            #print("inside_rewards",rews)

            self.ob_dicts.append(self.ob_dict)

        
            #self.local_map = np.zeros((self.local_num_rows, self.local_num_cols), dtype=np.float32)
        # print()
        self.steps += 1
        self.get_observation()

        # print("obs_multi_env",obs)

        return obs, rews, dones, terminations, self.ob_dict
    
    def get_image(self):
        
        # print("step",self.steps)
        if self.args.occupancy_map and self.steps % 2 == 0:
        # if self.args.occupancy_map and (self.steps >20 or self.steps  == 0):
            # print("step_after",self.steps)

            # # p.setTimeStep(1/50)
             
            # for _ in range(int(50/10)):
            #     p.stepSimulation()
            # timestep = p.getPhysicsEngineParameters()["fixedTimeStep"]
            # print(timestep)
            #self.occupancy_maps=[]

            turtlebot_data=[]
            local_heightmaps=[]
            local_heightmap_positions=[]



            for robot_pos,robot_orn in zip(self.robots_pos,self.robots_orn):
                # print(robot_pos)
                local_heightmap, local_heightmap_position = self.get_heightmap(robot_pos,robot_orn)
                local_heightmaps.append(local_heightmap)
                local_heightmap_positions.append(local_heightmap_position)
                turtlebot_data.append((local_heightmap, local_heightmap_position, robot_pos))
                
                # array_shape = (65,75)
                # local_heightmap = np.zeros(array_shape)
                
                # print("in_function",local_heightmap.shape)
                # print("in_function_pos",local_heightmap_position)
            self.Occupancy_map=self.visualize_maps(self.global_map_list, local_heightmaps,local_heightmap_positions,self.robots_pos,self.Goals_pos,self.Obstacles_pos,self.gap_walls1_centre,self.gap_walls2_centre,self.side_walls1_centre,self.side_walls2_centre)
            # self.occupancy_maps=deepcopy(local_heightmaps)
            

                

            # print("self.local_heightmaps",np.array(local_heightmaps).shape)
            # print("self.global_Map",np.array(self.global_map_list).shape)
            #N=self.visualize_maps(self.global_map2, self.local_heightmaps,self.local_heightmap_positions,self.robots_pos,self.Goals_pos,self.Obstacles_pos)
            # print(np.array(self.global_map_list).shape,self.im_size)
            # gm=np.array(self.global_map_list).reshape([self.args.num_robots]+[1,1000,1000])

            
            
            # self.h1=np.savetxt('occupancy_map1.txt', self.local_heightmaps[0])
            # self.h2=np.savetxt('occupancy_map2.txt', self.local_heightmaps[1])
            # current_time = time.time()
            # print("current",current_time-self.start_time)
            # print("local_hmap",np.array(self.local_heightmaps).shape)
            # print("reshape",[self.args.num_robots]+self.im_size)
            
            # self.occupancy_maps_reshaped=np.array(self.occupancy_maps).reshape([self.args.num_robots]+self.im_size)

            # if current_time-self.start_time==0.2:
            #     self.occupancy_maps=deepcopy(self.local_heightmaps)
            #     self.occupancy_maps_reshaped=np.array(self.occupancy_maps).reshape([self.args.num_robots]+self.im_size)
            #     print("td",time.time()-current_time)
            
            # else:
            #     self.occupancy_maps_reshaped=self.prev_occupancy_maps
            # print(np.array(self.occupancy_maps).reshape([self.args.num_robots]+self.im_size).shape)
            self.global_map_list=[np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32) for _ in range(self.args.num_robots)]
            # self.prev_occupancy_maps=deepcopy(self.local_heightmaps)

            # for r in range(self.args.num_robots):
            #     self.global_map = np.zeros((self.global_num_rows, self.global_num_cols), dtype=np.float32)
            #     self.global_map_list.append(self.global_map)
        #print(self.occupancy_maps);exit()
        # else:
        #     pass
        # print("imsize",self.im_size,"occ_size",np.array(self.occupancy_maps[0]).shape,np.array(self.occupancy_maps[1]).shape)
        # print([self.args.num_robots]+self.im_size,np.array(self.occupancy_maps).shape)
        # print([self.args.num_robots]+self.im_size,np.array(self.occupancy_maps).shape)
        # print(np.array(self.occupancy_maps).shape,np.array(self.occupancy_maps).reshape([self.args.num_robots]+self.im_size).shape,self.im_size)

        # robot1_occupancy_map = np.zeros((80, 80), dtype=int)
        # robot1_occupancy_map[30:50, 30:50] = 1  # Creating a 20x20 block of 1s in the middle

        # # Generate a random occupancy map for Robot 2
        # robot2_occupancy_map = np.random.randint(0, 2, (80, 80))

        # # Combine them into the final array
        # example_occupancy_map = np.array([
        #     [robot1_occupancy_map],
        #     [robot2_occupancy_map]
        # ])

        


        

        # return np.array(self.occupancy_maps).reshape([self.args.num_robots]+self.im_size)
        return self.Occupancy_map
        # return np.array(self.global_map_list).reshape([self.args.num_robots]+self.im_size)
        # return example_occupancy_map
    
    # def get_image(self):
    #     # if self.args.occupancy_map and self.steps % 2 == 0:
    #     if self.args.occupancy_map:
    #         turtlebot_data = []
    #         self.local_heightmaps = []
    #         self.local_heightmap_positions = []
    #         for robot_pos, robot_orn in zip(self.robots_pos, self.robots_orn):
    #             local_heightmap, local_heightmap_position = self.get_heightmap(robot_pos, robot_orn)
    #             self.local_heightmaps.append(local_heightmap)
    #             self.local_heightmap_positions.append(local_heightmap_position)
    #             turtlebot_data.append((local_heightmap, local_heightmap_position, robot_pos))

    #         M = self.visualize_maps(self.global_map_list, self.local_heightmaps, self.local_heightmap_positions, self.robots_pos, self.Goals_pos, self.Obstacles_pos, self.gap_walls1_centre, self.gap_walls2_centre, self.side_walls1_centre, self.side_walls2_centre)

    #         self.occupancy_maps = []
    #         for hmap in self.local_heightmaps:
    #             if isinstance(hmap, np.ndarray):
    #                 self.occupancy_maps.append(hmap)
    #             else:
    #                 self.occupancy_maps.append(np.array(hmap))
    #         # self.args.num_robots=[2]
    #         # self.im_size
    #         print("imsize",self.im_size,type(self.im_size),np.array(self.occupancy_maps).shape)
    #         # Check if all elements are numpy arrays
    #         if all(isinstance(hmap, np.ndarray) for hmap in self.occupancy_maps):
    #             return np.array(self.occupancy_maps).reshape([self.args.num_robots] + self.im_size)
    #         else:
    #             print("Error: Some elements in occupancy_maps are not numpy arrays.")
    #             return None
    #     else:
    #         return None

    
    
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
        #     self.external_robots_pos=[(self.robots[0],[1,1,self.z_position]),(self.robots[1],[2.5,2.5,self.z_position]),(self.robots[2],[4,4,self.z_position])]
        #     for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
        #         self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
        #         self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        # elif self.args.num_robots ==2:
        #     self.robottogoal_angles=[(self.robots[0],0),(self.robots[1],0)]
        #     self.external_robots_pos=[(self.robots[0],[0,0,self.z_position]),(self.robots[1],[0,2.5,self.z_position])]
        #     for robot_pos,initial_goal_dist,robotgoal_angle in zip(self.external_robots_pos,self.initial_goal_distances,self.robottogoal_angles):
        #         self.external_goal_state=self.find_position_B(robot_pos[1], initial_goal_dist, robotgoal_angle[1])
        #         self.external_goals_states_with_IDx.append((Robot,self.external_goal_state))
        # else:
        #     self.robottogoal_angles=[(self.robots[0],0)]
        #     self.external_robots_pos=[(self.robots[0],[1,1,self.z_position])]
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
    # def get_heightmap(self,robot_position,robot_orientation):
    #     # Calculate the boundaries of the local map based on robot_position and local_map_size
    #     local_x_min = robot_position[0] - self.local_map_size_x / 2
    #     local_x_max = robot_position[0] + self.local_map_size_x / 2
    #     local_y_min = robot_position[1] - self.local_map_size_y / 2
    #     local_y_max = robot_position[1] + self.local_map_size_y / 2

    #     # Calculate grid indices for the local map within the global map
    #     local_x_indices = np.clip(
    #         np.array(((local_x_min + self.global_map_size_x / 2) / self.global_resolution), dtype=int), 0, self.global_num_rows - 1
    #     )
    #     local_y_indices = np.clip(
    #         np.array(((local_y_min + self.global_map_size_y / 2) / self.global_resolution), dtype=int), 0, self.global_num_cols - 1
    #     )

    #     for global_map in self.global_map_list:
    #         # Extract the local heightmap from the global map
    #         local_heightmap = global_map[
    #             local_x_indices:local_x_indices + self.local_num_rows, local_y_indices:local_y_indices + self.local_num_cols
    #         ]


        

    #         # Calculate the position of the local heightmap within the local map
    #         local_heightmap_x_min = local_x_min
    #         local_heightmap_x_max = local_x_max
    #         local_heightmap_y_min = local_y_min
    #         local_heightmap_y_max = local_y_max

    #         #print("local_heightmap", local_heightmap,local_heightmap.shape)
    #         # Rotate the local heightmap based on the robot's orientation
    #         local_heightmap = np.rot90(local_heightmap, k=int(math.degrees(robot_orientation) / 90))

    #         # array_shape = (65,75)
    #         # local_heightmap = np.zeros(array_shape)
    #         print("before_Lmap",local_heightmap.shape)

    #         # Pad heightmaps if their shape is less than (80, 80)
    #             # Calculate padding
    #         pad_height = max(80 - local_heightmap.shape[0], 0)
    #         pad_width = max(80 - local_heightmap.shape[1], 0)
            
    #         # Pad heightmaps if their shape is less than (80, 80)
    #         local_heightmap = np.pad(local_heightmap, ((0, pad_height), (0, pad_width)), mode='constant', constant_values=0)

    #         print("after_Lmap",local_heightmap.shape)

    #     return local_heightmap, (local_heightmap_x_min, local_heightmap_x_max, local_heightmap_y_min, local_heightmap_y_max)

    def get_heightmap(self, robot_position, robot_orientation):

        # robot_position=(50,50)
        robot_position=list(robot_position)
        # print(robot_position,"list")
        if robot_position[0] > 40:
            robot_position[0]=40
        elif robot_position[0] < -40:
            robot_position[0]=-40
        # else:
        #     robot_position[0]=robot_position[0]

        if robot_position[1] > 40:
            robot_position[1]=40
        elif robot_position[1] < -40:
            robot_position[1]=-40
        # else:
        #     robot_position[1]=robot_position[1]

        # print("robot_position[0]",robot_position[0],"robot_position[1]",robot_position[1])
        # Calculate the boundaries of the local map based on robot_position and local_map_size
        local_x_min = robot_position[0] - self.local_map_size_x / 2
        local_x_max = robot_position[0] + self.local_map_size_x / 2
        local_y_min = robot_position[1] - self.local_map_size_y / 2
        local_y_max = robot_position[1] + self.local_map_size_y / 2

        # print(" self.local_num_rows", self.local_num_rows," self.local_num_cols", self.local_num_cols)

        # Calculate grid indices for the local map within the global map
        local_x_indices = np.clip(
            np.array(((local_x_min + self.global_map_size_x / 2) / self.global_resolution), dtype=int), 0, self.global_num_rows - 1
        )
        local_y_indices = np.clip(
            np.array(((local_y_min + self.global_map_size_y / 2) / self.global_resolution), dtype=int), 0, self.global_num_cols - 1
        )

        # print("local_x_indices",local_x_indices,"local_y_indices",local_y_indices)
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

            # Rotate the local heightmap based on the robot's orientation
            # local_heightmap = np.rot90(local_heightmap, k=int(math.degrees(robot_orientation) / 90))

        #     # Pad heightmaps if their shape is less than (80, 80)
        #     # Calculate padding
        #     pad_height = max(80 - local_heightmap.shape[0], 0)
        #     pad_width = max(80 - local_heightmap.shape[1], 0)
        #     # print("before_hm",local_heightmap.shape)
        #     # Pad heightmaps if their shape is less than (80, 80)
        #     local_heightmap_final = np.pad(local_heightmap, ((0, pad_height), (0, pad_width)), mode='constant', constant_values=0)

        #     # Update the positions after padding
        #     local_heightmap_x_max += pad_height * self.global_resolution
        #     local_heightmap_y_max += pad_width * self.global_resolution
        # # print("after_hm",local_heightmap_final.shape)
        # print((local_heightmap_x_min, local_heightmap_x_max, local_heightmap_y_min, local_heightmap_y_max),self)

        return local_heightmap, (local_heightmap_x_min, local_heightmap_x_max, local_heightmap_y_min, local_heightmap_y_max)



    # Function to visualize the maps using OpenCV
    
    def visualize_maps(self,global_map_list, local_heightmaps, local_heightmap_positions, robot_positions,goal_positions,obstalce_positions,gap_walls1_centre,gap_walls2_centre,side_walls1_centre,side_walls2_centre):
        

        #
        #print("len",len(self.robots_pos))
        

        x_min,x_max,y_min,y_max=[],[],[],[]
        turtlebots_x_index,turtlebots_y_index=[],[]

        obstacles_x_index,obstacles_y_index=[],[]

        gap_wall1s_x_index,gap_wall1s_y_index,gap_wall2s_x_index,gap_wall2s_y_index=[],[],[],[]
        side_wall1s_x_index,side_wall1s_y_index,side_wall2s_x_index,side_wall2s_y_index=[],[],[],[]
        
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

        if self.args.gap_avoidance:
            for side_wall1_centre,side_wall2_centre in zip(side_walls1_centre,side_walls2_centre):
                
                side_wall1_x_index = int((side_wall1_centre[0] + self.global_map_size_x / 2) / self.global_resolution)
                side_wall1_y_index = int((side_wall1_centre[1] + self.global_map_size_y / 2) / self.global_resolution)

                side_wall2_x_index = int((side_wall2_centre[0] + self.global_map_size_x / 2) / self.global_resolution)
                side_wall2_y_index = int((side_wall2_centre[1] + self.global_map_size_y / 2) / self.global_resolution)

                # print(side_wall1_x_index,side_wall1_y_index,side_wall2_x_index,side_wall2_x_index)
                
                side_wall1s_x_index.append(side_wall1_x_index)
                side_wall1s_y_index.append(side_wall1_y_index)

                side_wall2s_x_index.append(side_wall2_x_index)
                side_wall2s_y_index.append(side_wall2_y_index)

        for robot_position, goal_position,local_heightmap,local_heightmap_position, obstalce_position,global_map in zip(robot_positions,goal_positions, local_heightmaps,local_heightmap_positions,obstalce_positions,global_map_list):
            #Scale the maps for visualization
            # print( (np.max(global_map) - np.min(global_map)))
            scaled_global_map = (global_map - np.min(global_map))  * 200
            # Convert to uint8 and create color images
            scaled_global_map = scaled_global_map.astype(np.uint8)
            global_map_image = cv2.cvtColor(scaled_global_map, cv2.COLOR_GRAY2BGR)
            # Set colors: Blue for global map, Green for local heightmap, Red for obstacles
            global_map_image[:, :, :] = 128  # Blue channel to 255 for global map (blue color)
            
            #print("WEW",local_heightmaps,len(local_heightmaps), local_heightmap_positions,len(local_heightmap_positions))
            # print(local_heightmap)
            # print((np.max(local_heightmap) - np.min(local_heightmap)))
            scaled_heightmap = (local_heightmap - np.min(local_heightmap))  * 200
            scaled_heightmap = scaled_heightmap.astype(np.uint8)
            heightmap_image = cv2.cvtColor(scaled_heightmap, cv2.COLOR_GRAY2BGR)
            heightmap_image[:, :, 1] = 155  # Green channel to 255 for local heightmap (green color)
            
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

            local_region = global_map[local_map_x_min_index:local_map_x_max_index, local_map_y_min_index:local_map_y_max_index]

            # Overlay the obstacles on the local heightmap
            obstacle_indices = np.where(local_region == 1.0)
            for f, g in zip(obstacle_indices[0], obstacle_indices[1]):
                heightmap_image[f, g] = (0, 0, 255)  # Red color for obstacles

            
            heightmap_images.append(heightmap_image)
         
        # # HM=list(heightmap_images)
        # print(type(heightmap_image),"tuple?")
        # print(np.array(heightmap_images),"HM",type(heightmap_images))
        # print("HP",np.array(heightmap_images).shape)

        
        #print("aa",heightmap_images)
        # print(len(global_map_image),len(globalmap_images[0]))
        for global_map_image in globalmap_images:
            for i in range (len(self.robots_pos)):
                # print(len(self.robots_pos))
                # print(len(global_map_image),len(heightmap_images[i]),x_min[i],x_max[i],y_min[i],y_max[i])
                # print("globals",np.array(global_map_image).shape,np.array(global_map_image[0]).shape,np.array(global_map_image[1]).shape)
                # print("locals",np.array(heightmap_images[i]).shape,np.array(heightmap_images[i][0]).shape,np.array(heightmap_images[i][1]).shape)
                # print(x_min[i],x_max[i],y_min[i],y_max[i])
                
                # global_map_image[
                # x_min[i]:x_max[i],
                # y_min[i]:y_max[i],] = heightmap_images[i]

                if heightmap_images[i].shape == (80, 80, 3):
                    global_map_image[
                        x_min[i]:x_max[i],
                        y_min[i]:y_max[i],:] = heightmap_images[i]
                else:
                    print("Skipping assignment due to shape mismatch.")


                # # Calculate padding
                # # Calculate padding
                # pad_height = max(80 - local_heightmap.shape[0], 0)
                # pad_width = max(80 - local_heightmap.shape[1], 0)

                # # Adjust x_min, x_max, y_min, y_max if they are less than 80
                # x_min_adjusted = max(x_min[i], 80 - pad_height)
                # x_max_adjusted = min(x_max[i], 80 + local_heightmap.shape[0])
                # y_min_adjusted = max(y_min[i], 80 - pad_width)
                # y_max_adjusted = min(y_max[i], 80 + local_heightmap.shape[1])

                # # Adjust heightmap size to match the region
                # heightmap_shape = (max(x_max_adjusted - x_min_adjusted, 1), max(y_max_adjusted - y_min_adjusted, 1))
                # local_heightmap_resized = cv2.resize(local_heightmap, heightmap_shape[::-1], interpolation=cv2.INTER_AREA)

                # # Create an empty image with the same shape as global_map_image
                # heightmap_image = np.zeros((heightmap_shape[0], heightmap_shape[1], 3), dtype=np.uint8)

                # # Insert the resized heightmap into the empty image
                # heightmap_image[
                #     :local_heightmap_resized.shape[0],
                #     :local_heightmap_resized.shape[1], :] = cv2.cvtColor(local_heightmap_resized, cv2.COLOR_GRAY2BGR)

                # # Overlay the heightmap image onto the global map image
                # global_map_image[
                #     x_min_adjusted:x_min_adjusted + heightmap_shape[0],
                #     y_min_adjusted:y_min_adjusted + heightmap_shape[1],:] = heightmap_image






                # # Adjust heightmap size to match the region
                # heightmap_shape = (x_max[i] - x_min[i], y_max[i] - y_min[i])
                # local_heightmap_resized = cv2.resize(local_heightmap, heightmap_shape[::-1], interpolation=cv2.INTER_AREA)

                # # Create an empty image with the same shape as global_map_image
                # heightmap_image = np.zeros_like(global_map_image)

                # print("local_heightmap_resized",local_heightmap_resized.shape)
                # # Insert the resized heightmap into the empty image
                # heightmap_image[
                #     x_min[i]:x_max[i],
                #     y_min[i]:y_max[i],:] = cv2.cvtColor(local_heightmap_resized, cv2.COLOR_GRAY2BGR)

                # # Overlay the heightmap image onto the global map image
                # global_map_image = cv2.addWeighted(global_map_image, 1, heightmap_image, 0.5, 0)

                # global_map_image[
                # x_min[i]:x_max[i],
                # y_min[i]:y_max[i],] = heightmap_images[i]
                # print(len(global_map_image),len(self.robots_pos[0:1]),len(self.robots_pos))
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
                    half_width_cells = int(self.wall_length / (2 * self.global_resolution))
                    half_gapoffset_cells = int(self.gap_offset / (2 * self.global_resolution))
                    #half_width_cells = int(self.gap_walls_length[0] / (2 * self.global_resolution))
                    
                    #side walls
                    sides_half_length_cells = int(25 / (2 * self.global_resolution))#int(self.gap_walls_thickness[0] / (2 * self.global_resolution))
                    sides_half_width_cells = int(self.gap_walls_thickness[0] / (2 * self.global_resolution))#int(25 / (2 * self.global_resolution))
                    
                    #print("rr",self.gap_walls1_centre);exit
                    wall1_x_center=gap_wall1s_x_index[i]
                    wall1_y_center=gap_wall1s_y_index[i]

                    wall2_x_center=gap_wall2s_x_index[i]
                    wall2_y_center=gap_wall2s_y_index[i]


                    side_wall1_x_center=side_wall1s_x_index[i]
                    side_wall1_y_center=side_wall1s_y_index[i]

                    side_wall2_x_center=side_wall2s_x_index[i]
                    side_wall2_y_center=side_wall2s_y_index[i]


                    # Wall 1 Set the obstacle region in the global map to a higher value for visualization
                    for p in range(wall1_x_center - half_length_cells, wall1_x_center + half_length_cells + 1):
                        for q in range(wall1_y_center - (half_width_cells+half_gapoffset_cells), wall1_y_center + (half_width_cells+half_gapoffset_cells) + 1):
                            if 0 <= p < self.global_num_rows and 0 <= q < self.global_num_cols:
                                global_map[p, q] = 1.0

                    # Wall 2 Set the obstacle region in the global map to a higher value for visualization
                    for p in range(wall2_x_center - half_length_cells, wall2_x_center + half_length_cells + 1):
                        for q in range(wall2_y_center - (half_width_cells-half_gapoffset_cells), wall2_y_center + (half_width_cells-half_gapoffset_cells) + 1):
                            if 0 <= p < self.global_num_rows and 0 <= q < self.global_num_cols:
                                global_map[p, q] = 1.0

                    # Side Wall 1Set the obstacle region in the global map to a higher value for visualization
                    for p in range(side_wall1_x_center - sides_half_length_cells, side_wall1_x_center + sides_half_length_cells + 1):
                        for q in range(side_wall1_y_center - sides_half_width_cells, side_wall1_y_center + sides_half_width_cells + 1):
                            if 0 <= p < self.global_num_rows and 0 <= q < self.global_num_cols:
                                global_map[p, q] = 1.0

                    # Side Wall 2 Set the obstacle region in the global map to a higher value for visualization
                    for p in range(side_wall2_x_center - sides_half_length_cells, side_wall2_x_center + sides_half_length_cells + 1):
                        for q in range(side_wall2_y_center - sides_half_width_cells, side_wall2_y_center + sides_half_width_cells + 1):
                            if 0 <= p < self.global_num_rows and 0 <= q < self.global_num_cols:
                                global_map[p, q] = 1.0

        
        for index,(global_map,global_map_image) in enumerate(zip(global_map_list,globalmap_images)):
            for i in range(self.args.num_robots):
                global_map_image = cv2.circle(global_map_image, (turtlebots_y_index[i], turtlebots_x_index[i]), 5, (255, 0, 0), -1)
                global_map_image = cv2.circle(global_map_image, (Goals_y_index[i], Goals_x_index[i]), 5, (0, 255, 0), -1)
                # print(self.global_resolution)
                # print("index",index,"i",i)
                # if index!=i or index==i:
                # for index_hm,local_heightmap in enumerate(local_heightmaps):
                #     print("ind",index,i,index_hm)
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

                # if index==i:
                # #     print("True")
                #     # Calculate robot-length and robot-width in grid cells
                #     robot_length = int(1.4 / (2 * self.global_resolution))
                #     robot_width = int(0.7 / (2 * self.global_resolution))
                #     x_index=turtlebots_x_index[i]
                #     y_index=turtlebots_y_index[i]
                    
                #     # Set the obstacle region in the global map to a higher value for visualization
                #     for k in range(x_index - robot_length, x_index + robot_length + 1):
                #         for l in range(y_index - robot_width, y_index + robot_width + 1):
                #             if 0 <= k < self.global_num_rows and 0 <= l < self.global_num_cols:
                #                 global_map[k, l] = 1.0  # Mark the obstacle as occupied with a value of 1
                
              
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
        for local_heightmap, local_heightmap_position, global_map in zip(local_heightmaps, local_heightmap_positions, global_map_list):
            # Scale the local heightmap for visualization
            scaled_heightmap = (local_heightmap - np.min(local_heightmap)) * 200
            scaled_heightmap = scaled_heightmap.astype(np.uint8)

            # Convert to a color image with green channel
            heightmap_image = cv2.cvtColor(scaled_heightmap, cv2.COLOR_GRAY2BGR)
            heightmap_image[:, :, 1] = 255  # Green channel to 255 for local heightmap

            # Extract the local region from the global map
            local_map_x_min = local_heightmap_position[0]
            local_map_x_max = local_heightmap_position[1]
            local_map_y_min = local_heightmap_position[2]
            local_map_y_max = local_heightmap_position[3]

            local_map_x_min_index = int((local_map_x_min + self.global_map_size_x / 2) / self.global_resolution)
            local_map_x_max_index = int((local_map_x_max + self.global_map_size_x / 2) / self.global_resolution)
            local_map_y_min_index = int((local_map_y_min + self.global_map_size_y / 2) / self.global_resolution)
            local_map_y_max_index = int((local_map_y_max + self.global_map_size_y / 2) / self.global_resolution)

            local_region = global_map[local_map_x_min_index:local_map_x_max_index, local_map_y_min_index:local_map_y_max_index]

            # Overlay the obstacles on the local heightmap
            obstacle_indices = np.where(local_region == 1.0)
            for f, g in zip(obstacle_indices[0], obstacle_indices[1]):
                heightmap_image[f, g] = (0, 0, 255)  # Red color for obstacles

            heightmap_images.append(heightmap_image)

        from scipy.ndimage import gaussian_filter

        def add_partial_detection(image, blur_sigma=1):
            blurred_image = gaussian_filter(image, sigma=blur_sigma)
            return blurred_image
        
        def add_intermittent_visibility(image, drop_prob=0.1):
            mask = np.random.rand(*image.shape[:2]) > drop_prob
            noisy_image = image.copy()
            noisy_image[~mask] = 0  # Set pixels to black
            return noisy_image

        def add_sparse_representation(image, sparsity=0.2):
            mask = np.random.rand(*image.shape[:2]) > sparsity
            noisy_image = image.copy()
            noisy_image[~mask] = 0  # Set pixels to black
            return noisy_image

        def add_trailing_effect(image, trail_length=5):
            height, width = image.shape[:2]
            trail_image = image.copy()
            for _ in range(trail_length):
                shift_x = np.random.randint(-2, 3)  # Random horizontal shift
                shift_y = np.random.randint(-2, 3)  # Random vertical shift
                shifted_image = np.roll(image, (shift_y, shift_x), axis=(0, 1))
                trail_image = np.maximum(trail_image, shifted_image)
            return trail_image
        
        def add_all_noises(image, drop_prob=0.1, blur_sigma=1, sparsity=0.2, trail_length=5):
            noisy_image = add_intermittent_visibility(image, drop_prob=drop_prob)
            noisy_image = add_partial_detection(noisy_image, blur_sigma=blur_sigma)
            noisy_image = add_sparse_representation(noisy_image, sparsity=sparsity)
            noisy_image = add_trailing_effect(noisy_image, trail_length=trail_length)
            return noisy_image

        
        #HEREHRHEHHRHOASHDJSDHJ

        # Step 1: Select the last two images
        last_two_images = heightmap_images[-self.args.num_robots:]

        

        def convert_heightmap_images(heightmap_images):
            # Result array with shape (2, 1, 80, 80)
            converted_images = np.zeros((self.args.num_robots, 1, 80, 80), dtype=np.uint8)
            
            # Only process the last two heightmaps
            for index in range(self.args.num_robots):
                heightmap_image = heightmap_images[index + self.args.num_robots]
                
                # Convert RGB to grayscale by isolating the red channel
                red_channel = heightmap_image[:, :, 2]
                
                # Create a binary image where red obstacles are marked as 1, all others as 0
                binary_image = (red_channel == 255).astype(np.uint8)
                
                # Place the binary image in the converted_images array
                converted_images[index, 0] = binary_image
            
            return converted_images

        # Convert heightmap images
        occupancy_map_locals = convert_heightmap_images(heightmap_images)

        def mark_edge_cells(occupancy_map):
            # Define a structure for connected components (8-connected neighborhood)
            structure = generate_binary_structure(2, 1)
            
            # Label connected components
            labeled_map, num_labels = label(occupancy_map, structure)
            
            # Find the unique labels (excluding background label 0)
            unique_labels = np.unique(labeled_map)[1:]
            
            # Create a new array for the modified occupancy map
            modified_occupancy_map = np.zeros_like(occupancy_map)
            
            # Iterate over each unique label (connected component)
            for labela in unique_labels:
                # Extract the mask for the current connected component
                component_mask = (labeled_map == labela).astype(np.uint8)
                # component_mask = add_sparse_representation(component_mask, sparsity=0.3)
                #Apply all noises
                
                # print("labela",unique_labels.shape,type(unique_labels))
                # Find edge cells that are adjacent to unoccupied cells (0)
                edge_mask = np.zeros_like(component_mask)

                
                # # print("component_mask",component_mask,type(component_mask),component_mask.shape)
                # edge_mask[1:-1, 1:-1] = (component_mask[1:-1, 1:-1] > 0) & \
                #                         ((component_mask[:-2, 1:-1] == 0) | (component_mask[2:, 1:-1] == 0) | \
                #                         (component_mask[1:-1, :-2] == 0) | (component_mask[1:-1, 2:] == 0))
                
                edge_mask[1:-1, 1:-1] = (component_mask[1:-1, 1:-1] > 0) & \
                                        ((component_mask[:-2, 1:-1] == 0) | (component_mask[2:, 1:-1] == 0) | \
                                        (component_mask[1:-1, :-2] == 0) | (component_mask[1:-1, 2:] == 0))

                edge_mask = add_all_noises(
                    edge_mask,
                    drop_prob=self.noise,
                    blur_sigma=0,
                    sparsity=0.0,
                    trail_length=0)
                
                # Mark edge cells as 1 in the modified map

                # print("EDGEMASK",edge_mask,type(edge_mask),edge_mask.shape)
                # edge_mask = add_sparse_representation(edge_mask, sparsity=0.2)

                modified_occupancy_map[edge_mask > 0] = 1
                # modified_occupancy_map[image_with_sparse_representation > 0] = 1
                # print("modified_occupancy_map",modified_occupancy_map,type(modified_occupancy_map),modified_occupancy_map.shape)

                
            return modified_occupancy_map
            # return component_mask

        # Iterate over the converted heightmap images and mark edge cells
        Hollowed_Occupancy_maps=[]
        for index in range(self.args.num_robots):
            occupancy_map_local = occupancy_map_locals[index, 0]
            modified_occupancy_map = mark_edge_cells(occupancy_map_local)
            Hollowed_Occupancy_maps.append(modified_occupancy_map)


        # hollow_images = np.array(Hollowed_Occupancy_maps).reshape(2, 80, 80, 1).repeat(3, axis=3)
        # # Step 2: Convert RGB images to grayscale
        # last_two_images_gray = np.array([cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in last_two_images])
        # print("HMM",np.array(Hollowed_Occupancy_maps).shape)
        # listing=np.array(listing).reshape(self.args.num_robots,self.im_size)
        # print("Hollowed_Occupancy_maps[-2:]",type(Hollowed_Occupancy_maps[-2:]),np.array(Hollowed_Occupancy_maps).shape)
        if self.args.map_show:

            # # Create separate OpenCV windows for each global map
            # cv2.namedWindow("Global Map with Local Heightmaps1", cv2.WINDOW_NORMAL)
            # cv2.namedWindow("Global Map with Local Heightmaps2", cv2.WINDOW_NORMAL)\



            # for index,global_map_image in enumerate(globalmap_images):
            #     # print(type(global_map_image),global_map_image.shape)
                
            #     image_with_intermittent_visibility = add_intermittent_visibility(global_map_image, drop_prob=0.1)
            #     image_with_partial_detection = add_partial_detection(global_map_image, blur_sigma=1)
            #     image_with_sparse_representation = add_sparse_representation(global_map_image, sparsity=0.2)
            #     image_with_trailing_effect = add_trailing_effect(global_map_image, trail_length=5)

            #     # Apply all noises
            #     noisy_global_map_image = add_all_noises(
            #         global_map_image,
            #         drop_prob=0.3,
            #         blur_sigma=0,
            #         sparsity=0.0,
            #         trail_length=0
            #     )
            #     #cv2.imshow("Global Map with Local Heightmaps"+str(index), globalmap_images)
            #     window_name = "Global Map with Local Heightmaps" + str(index)
            #     # cv2.imshow(window_name, global_map_image)
            #     cv2.imshow(window_name, global_map_image)
            # # print("local_heightmaps[-2:]",type(local_heightmaps[-2:]),np.array(local_heightmaps)[-2:].shape)
            # # print("OWOWHollowed",np.array(Hollowed_Occupancy_maps).shape)
            # # Display the local heightmaps using OpenCV
            for index, heightmap_image in enumerate(Hollowed_Occupancy_maps):
                window_name = "Local Heightmap " + str(index)
                # print("heightmap_image",heightmap_image.shape)
                image_with_intermittent_visibility = add_intermittent_visibility(heightmap_image, drop_prob=0.1)
                image_with_partial_detection = add_partial_detection(heightmap_image, blur_sigma=1)
                image_with_sparse_representation = add_sparse_representation(heightmap_image, sparsity=0.2)
                image_with_trailing_effect = add_trailing_effect(heightmap_image, trail_length=5)
                # print("HHHHMM",np.array(heightmap_images))

                # Apply all noises
                noisy_local_map_image = add_all_noises(
                    heightmap_image,
                    drop_prob=0.0,
                    blur_sigma=0.0,
                    sparsity=0.3,
                    trail_length=0
                )
                # unique_values = np.unique(heightmap_image)

                occupancy_map_array = np.array(heightmap_image)
                # print("occupancy_map_array.shape",occupancy_map_array.shape)
                # Determine the dimensions of the occupancy map
                rows, cols = occupancy_map_array.shape
                
                # Create an empty image with the same dimensions as the occupancy map
                image = np.zeros((rows, cols, 3), dtype=np.uint8)
                # Assign grey color where occupancy_map is 0
                image[occupancy_map_array == 0] = (128, 128, 128)  # Grey
                
                # Assign red color where occupancy_map is 1
                image[occupancy_map_array == 1] = (0, 0, 255)  # Red
                # print(f"Unique values in heightmap_image {index}: {unique_values}")
                # cv2.imshow(window_name, heightmap_image)
                resized_image = cv2.resize(image, (800, 600))
                cv2.imshow(window_name, resized_image)

            # cv2.imshow("Global Map with Local Heightmaps1", globalmap_images[0])
            # cv2.imshow("Global Map with Local Heightmaps2", globalmap_images[1])
            # Wait for a short delay to ensure the first window is initialized
            #cv2.waitKey(100)    
            #cv2.imshow("Global Map with Local Heightmaps2", globalmap_images[1])
            cv2.waitKey(10)
                #cv2.destroyAllWindows()
        Hollowed_Occupancy_maps=np.array(Hollowed_Occupancy_maps).reshape([self.args.num_robots]+self.im_size)
        # # # Step 3: Reshape the images to (2, 1, 80, 80)
        # # reshaped_images = np.array(occupancy_map_local).reshape(2, 1, 80, 80)
        # # hm=np.array(heightmap_images).reshape([self.args.num_robots]+self.im_size)
        # r1_occupancy_map = occupancy_map_local[0,0,:, :]
        # r2_occupancy_map = occupancy_map_local[1,0,:, :]

        # # r1_occupancy_map = next_im[0, :, :]
        # # r2_occupancy_map = next_im[1, :, :]

        # # r1_occupancy_map=next_im[0, 0, :, :]
        # # # r2_occupancy_map=next_im[1, 0, :, :]

        # r1_occupancy_map_array = np.array(r1_occupancy_map)
        # # print("r1_occupancy_map_array.shape",r1_occupancy_map_array.shape)
        # # Determine the dimensions of the occupancy map
        # rows, cols = r1_occupancy_map_array.shape
        
        # # Create an empty image with the same dimensions as the occupancy map
        # image_r1 = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        # # Assign grey color where occupancy_map is 0
        # image_r1[r1_occupancy_map_array == 0] = (128, 128, 128)  # Grey
        
        # # Assign red color where occupancy_map is 1
        # image_r1[r1_occupancy_map_array == 1] = (0, 0, 255)  # Red

        # image_r1 = image_r1 #occupancy_map_to_image(im_ocupancy)


        # # # Create a window with the specified name
        # cv2.namedWindow("R1 Occupancy Map", cv2.WINDOW_NORMAL)

        # # Resize the window to a desired size
        # cv2.resizeWindow("R1 Occupancy Map", 800, 600)
        # # Display the image
        # cv2.imshow("R1 Occupancy Map", image_r1)

        # r2_occupancy_map_array = np.array(r2_occupancy_map)
        # # print("r2_occupancy_map_array.shape",r2_occupancy_map_array.shape)
        # # Determine the dimensions of the occupancy map
        # rows_r2, cols_r2 = r2_occupancy_map_array.shape
        
        # # Create an empty image with the same dimensions as the occupancy map
        # image_r2 = np.zeros((rows_r2, cols_r2, 3), dtype=np.uint8)
        
        # # Assign grey color where occupancy_map is 0
        # image_r2[r2_occupancy_map_array == 0] = (128, 128, 128)  # Grey
        
        # # Assign red color where occupancy_map is 1
        # image_r2[r2_occupancy_map_array == 1] = (0, 0, 255)  # Red

        # image_r2 = image_r2 #occupancy_map_to_image(im_ocupancy)


        # # # Create a window with the specified name
        # cv2.namedWindow("R2 Occupancy Map", cv2.WINDOW_NORMAL)

        # # Resize the window to a desired size
        # cv2.resizeWindow("R2 Occupancy Map", 800, 600)
        # # Display the image
        # cv2.imshow("R2 Occupancy Map", image_r2)
        

        # cv2.waitKey(1)  
        return Hollowed_Occupancy_maps     
        # return np.array(listing)     


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
        # print("c",center)
        # center=[center[0],center[1]+1,center[2]]
        # print("ac",center)

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
    

    



    











