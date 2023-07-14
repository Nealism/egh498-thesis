from cmath import e
from copy import deepcopy
import numpy as np
import pybullet as p
import time
from gym import spaces
from collections import deque

from mpi4py import MPI
comm = MPI.COMM_WORLD
import math
import random

from assets.env_base_pb import EnvBasePB



#Currently, we are commenting our work on inlation radius. We will consider our inflation radius work before testing phase.
#Inflation radious code are specified some in reset, some in reward function and mostly in observation.

class Env(EnvBasePB):
	terrain_size = im_size = [1,100,100]
	
	def __init__(self, PATH=None, args=None, writer=None):

		self.rank = comm.Get_rank()
		self.args = args
		self.render = args.render and self.rank == 0
		self.PATH = PATH
		self.writer = writer
		self.master = True
		Initial_distance_to_goal=0
		
		self.prev_dist_to_goal= Initial_distance_to_goal

		
		

		super().__init__(PATH)

		self.reward_fn_name = f'get_reward_{self.args.reward_fn}'
		#self.obs_fn_name = f'get_hlp_obs_{self.args.obs_fn}'
		self.reset_fn_name = f'reset_{self.args.reset_fn}'
		self.step_fn_name = f'step_{self.args.step_fn}'

		self.simStep = 1/240
		self.timeStep = 1/120
		if "pumpkin" in self.args.env:
			self.ac_size = 22
			self.ob_size = 7
		else:
			self.ac_size = 2
			if self.args.num_robots > 1:
				self.ob_size = 18
			else:
				self.ob_size = 6
		self.Kp = 400
		self.initial_Kp = self.Kp
		# self.a=6.0
		# self.b=0.5

		self.a=0.0
		self.b=0.0
		
		self.action_multiplier = 0.1 

		# Needed if importing as Gym environment--  spaces.Discrete(self.ac_size) 
		self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
		self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
		
		self.steps = -1
		
		self.reward_names = ["Reward/goal", "Reward/heading", "Reward/heading_obs", "Reward/neg", "Distance to Goal Improved"]
		self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
		self.ep_reward_dict = {reward:0 for reward in self.reward_names} 
	
		self.env_exp = None
		self.target_speed = 1.0
		self.target_yaw = 0.0
		self.initial_joints = [0.0] * 15 + [ 0.5, -0.5, -1.5707] + [-0.5, 0.5, -1.5707]
		self.cur_success = deque([0.0], maxlen=5)
		self.success = deque([0.0], maxlen=1)
		self.ep_goal_success = 0.0
		self.ep_success = False

		if self.args.add_terrain:
			self.terrain_difficulty = self.args.initial_terrain_difficulty
		else:
			self.terrain_difficulty = 0
			self.terrain = None

		self.max_disturbance = 250
		self.final_disturbance = 1600
		self.episodes = -1
		self.total_steps = 0
		self.ob_dict = {}
		#self.done = False

		# States that we want to restore, for resuming training after running a test
		self.states_to_restore = ["pos", "orn", "joints", "base_vel", "joint_vel", "args", "episodes", "steps", "total_steps"]

		# Things we want to log each training step (print and add to tensorboard)
		self.log_things = {"Kp": self.Kp, "Success": self.cur_success, "Dist": self.max_disturbance, "Diffficulty": self.terrain_difficulty}

		self.load_robot()


	# def load_terrains(self):
	#     """
	#     Generates all Terrain objects for this environment and adds them to the terrains array.

	#     NOTE: By default, always load the ground truth
	#     NOTE: can optionally create other terrains 
	#     """
	#     # generate and load ground truth image
	#     gt_arr = self.terrain_generator.gen_rand_ground_truth(0, 255, self.cfg.terrain.gt_img_dim)
	#     gt_path = self.get_parent_dir(self.model_path)
	#     gt_name = f"ground_truth_{str(self.rank)}"
	#     gt_position = self.terr_cfg.hf_centre_pos
	#     gt_size = (*self.terr_cfg.gt_mj_dim, self.terr_cfg.hf_elev, self.terr_cfg.hf_depth)

	#     self.ground_truth = Hfield(gt_arr, gt_path, gt_name, gt_position, gt_size) 
	#     self.terrains.append(self.ground_truth)

	def load_specific_robot(self):

		if "pumpkin" in self.args.env:
			self.load_urdf_robot("./assets/urdfs/pumpkin.urdf")
			self.contact_list = ['pumpkin_chassis', 'pumpkin_lower_chassis']
		else:
			#state_object= [random.uniform(-4,4),random.uniform(4,1),0.00]
			robot1=self.load_urdf_robot("./assets/urdfs/dynamic_titan.urdf")
			self.contact_list = ['titan_chassis', 'left_11_wheel', 'right_11_wheel','left_1_wheel', 'right_1_wheel']
			if self.args.num_robots > 1 and self.args.insert_robot2:
				robot2=self.load_urdf_robot2("./assets/urdfs/dynamic_titan.urdf")
			#robot2=self.load_urdf_robot("./assets/urdfs/dynamic_titan.urdf")
			self.contact_list2 = ['titan_chassis', 'left_11_wheel', 'right_11_wheel','left_1_wheel', 'right_1_wheel']
			wall_dir= "Wall_URDF/"
			wallA = p.loadURDF(wall_dir + "Wall.urdf", [11.25,0,0], useFixedBase=True)
			wallB = p.loadURDF(wall_dir + "Wall.urdf", [-11.25,0,0], useFixedBase=True)
			wall2A = p.loadURDF(wall_dir + "Wall2.urdf", [0,11.25,0], useFixedBase=True)
			wall2A = p.loadURDF(wall_dir + "Wall2.urdf", [0,-11.25,0], useFixedBase=True)
			#wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [-2,0,0], useFixedBase=True)
			#wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [-2,1,0], useFixedBase=True)
			#wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [2,0,0], useFixedBase=True)
			#wall2A = p.loadURDF(wall_dir + "Wall2_small.urdf", [2,1,0], useFixedBase=True)
			# wall2A = p.loadURDF("/home/komol/00_STUDY_DRIVE/Codes/mobile_robot/Wall_URDF/Wall2_small.urdf", [2,-1,0], useFixedBase=True)
			#wall2A = p.loadURDF("/home/komol/00_STUDY_DRIVE/Codes/mobile_robot/Wall_URDF/Wall2_small.urdf", [-2,1,0], useFixedBase=True)
			#state_object= [random.uniform(-4,4),random.uniform(-4,1),0.00]
			#state_object=[-2,-3,0.00]
			state_object=[np.random.uniform(-2, 2),np.random.uniform(-3, -3.5),0.00]
			wall_dir= "Wall_URDF/"
			self.Goal = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=state_object)
			
			#p.setCollisionFilterPair(self.Id, self.Id2, -1, -1, 0)
			
			#print(aabbMin)

		self.left_track = []
		self.right_track = []
		self.contact_dict = {}
		self.wheel_dict = {}
		for j in range( p.getNumJoints(self.Id) ):
			info = p.getJointInfo(self.Id, j)
			link_name = info[12].decode("ascii")
			if "wheel" in link_name: self.wheel_dict[link_name] = j
			if link_name in self.contact_list: self.contact_dict[link_name] = j
			if info[2] != p.JOINT_REVOLUTE: continue
			jname = info[1].decode("ascii")
			if "left" in jname:
				self.left_track.append(j)
			elif "right" in jname:
				self.right_track.append(j)
		self.motors = []
		# Works much better if using husky wheel interias in the URDF
		# for key in self.wheel_dict:
		# 	p.changeDynamics(self.Id, self.wheel_dict[key], lateralFriction=0.9, spinningFriction=0.01, rollingFriction=0.01)


	def get_log_things(self):
		# Things we want to log each training step (print and add to tensorboard)
		# print("What the ", self.ep_goal_success); exit()

		return_dict = {"Kp": self.Kp, "Curriculum Success": self.cur_success, "static robot distance from trajectory": self.a-self.b, "Difficulty_increase": self.b, "Goal Success": self.ep_goal_success }
		return_dict.update(self.reward_dict)
		return return_dict

	

	def get_success(self):
		# dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
		#print("success_dist",dist_to_goal)
		# return dist_to_goal < 1.0
		return self.total_reward > 700
	

	def check_for_success(self):
		return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()

	def reset(self, terrain=None, test=False, restore_state=None):
		
		#self.load_simulator()
		#p.resetDebugVisualizerCamera(cameraDistance=10, cameraYaw=0, cameraPitch=-40, cameraTargetPosition=[0.55,-0.35,0.2])

		Initial_distance_to_goal=0
		
		self.prev_dist_to_goal= Initial_distance_to_goal

		if self.steps > 0:
			for key in self.reward_dict:
				self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
		self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

		if self.episodes > -1:

			self.success.append(self.get_success())
			# print(self.success)
			self.ep_success = self.get_success()
			# print(self.ep_success)			
			self.cur_success.append(self.ep_success)
			self.ep_goal_success = np.mean(self.goal_success) if self.goal_success else 0.0

		self.goal_success = []
			# print(self.cur_success)
		#print(self.body_xyz)
		

		#pos, orn = p.getBasePositionAndOrientation(self.Id)
		
		
		#Uncomment this part for static inflation radius. Not for dynamic inflation radius.
		#For dynamic inflation radious, this part is added in observation section. 

		# m=0.075 #value of inflation radius
		# x=(1.4/2)+m
		# y=(0.78/2)+m
		# z=0.235
		# # get the self.corners of the bounding box
		# self.corners1 = [(x, y, z),
		#   		(x,-y,z),
		#   		(-x,-y,z),
		#   		(-x,y,z),
		#   		(x,y,z)]
		
		# self.corners2 = [(x, y, z),
		#   		(x,-y,z),
		#   		(-x,-y,z),
		#   		(-x,y,z),
		#   		(x,y,z)]
		
		
		# self.lineId1 = [-1]*4  # initialize with an invalid ID for lines around robots
		# self.lineId2 = [-1]*4 
		p.removeAllUserDebugItems()		





		p.removeBody(self.Goal)
		#state_object= [random.uniform(-4,4),random.uniform(-4,0),0.00]
		#state_object=[-2,-3,0.00]


		# Goal
		# state_object=[np.random.uniform(-3, 3), np.random.uniform(-3, -3.5), 0.00]
		state_object=[np.random.uniform(-4, 4), np.random.uniform(-4, 4), 0.00]
		wall_dir= "Wall_URDF/"
		self.Goal = p.loadURDF(wall_dir + "simplegoal.urdf", basePosition=state_object)
		p.setCollisionFilterGroupMask(self.Goal, -1, collisionFilterGroup=0, collisionFilterMask=0)
		
		
		if self.rank == 0 and self.args.record_sim and self.episodes > 0:
			self.record_sim_state(best=self.check_for_success(), test=test)
		
		# if terrain is not None:
		#     self.load_terrain(terrain)
		# elif self.args.add_terrain:
		#     template = (np.random.random([int(self.terrain_size[2]/4),int(self.terrain_size[2]/4)]) + 1.0) * self.terrain_difficulty 
		#     # Make the edges smooth
			
		#     df = pd.DataFrame(template)
		#     df.to_csv("template.csv")
		#     #dj=pd.read_csv("template.csv")
		#     #template=dj.to_numpy()
		#     template[:, 0] = 0.0
		#     #print(type(template))
		#     template[:, -1] = 0.0
		#     template[0, :] = 1.0
		#     template[-1, :] = 0.0
		#     #print(self.terrain_size[1])
		#     terrain = cv2.resize(template, dsize=(self.terrain_size[1], self.terrain_size[2])).reshape(self.terrain_size)
		#     #print(template)
		#     #print(template[:, 0])
		#     self.load_terrain(terrain)


		self.steps = 0

		#Robot1
		# initial_x, initial_y = np.random.uniform(-3, 3), np.random.uniform(3, 3.5) 
		initial_x, initial_y = np.random.uniform(-4, 4), np.random.uniform(-4, 4) 
		#initial_x, initial_y = -2, -2 
		self.initial_yaw = np.random.uniform(-np.pi, np.pi) 
		self.initial_orn = p.getQuaternionFromEuler([0,0,self.initial_yaw])
		self.z_offset = 0

	
		
		if self.args.cur and self.Kp > 0 and self.check_for_success():
			self.Kp = 0.75*self.Kp
			if self.Kp < 5:
				self.Kp = 0
			self.cur_success = deque([0.0], maxlen=5)


		# self.a is the fixed value of unit ( how far from the line) and self.b is the step size ( Here, step size is 0.5 unit)
		#print("static robot distance from trajectory",self.a-self.b,"and cur_success", self.cur_success)
		#print("cur_success", self.cur_success)	
		if self.args.num_robots > 1 and self.args.cur and self.check_for_success():
			if self.a-self.b == 0:         # at each episode, step size will increase but when the static robot position is in the line, then step size will not change.
				self.b = self.a
				self.cur_success = deque([0.0], maxlen=5)
				#print("cur_success", self.cur_success)			
			else:
				self.b +=0.1			
				
				self.cur_success = deque([0.0], maxlen=5)
		
		
		
		

		#x = (np.random.uniform(1, 5) if np.random.randint(2) else np.random.uniform(-1, -5))
		#y = (np.random.uniform(1, 5) if np.random.randint(2) else np.random.uniform(-1, -5))
		#self.goal = (x, y)
		

		# Visual element of the goal
		#Goal(self.goal)

		if restore_state is not None:
			self.set_position(pos=restore_state[0], orn=restore_state[1])
			
		else:
			pos, orn, self.joints, self.base_vel, self.joint_vel = [initial_x, initial_y, self.z_offset+0.31],self.initial_orn, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
			# pos2, orn2, self.joints, self.base_vel, self.joint_vel = [initial_x2, initial_y2, self.z_offset+0.31],self.initial_orn2, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
			self.set_position(pos, orn, robot_id=self.Id)

		# Function to move the goal and the static robot
		self.move_goal_and_static_robot(initial_x=pos[0], initial_y=pos[1], yaw=self.initial_yaw)
		
		# print("robot_positions", pos2)
		# print("robot_state")
		# print(self.state_robot2)

		self.lineId1 = [-1]*4  # initialize with an invalid ID for lines around robots
		self.lineId2 = [-1]*4 
		self.ray_line = [-1]*2
		self.hit = False

		self.get_observation()
		
		self.episodes += 1

		self.cur_time = 0
		self.total_reward = 0

		# Time to take single step
		#print(list(self.pos))
		postuple= tuple(self.pos)
		allowance = 0.05 # allowance for flexibility in avoiding robot2
		if self.args.num_robots > 1:
			self.Initial_robot2_avoid_angle=self.robot2_avoid_angle + allowance #Set Robot 2 avoid angle in reset
		#print("Self_Robot2Ang",self.Initial_robot2_avoid_angle)
		#print("goal",_)
		#print(type(self.joint_vel))
		#return np.array(self.robot1_bbox[0] +self.robot1_bbox[1] +self.robot1_bbox[2] +self.robot1_bbox[3] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3] + self.contacts + self.contacts2+ list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+  list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped])
		# return np.array(list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped])
		return self.return_state()


	def move_goal_and_static_robot(self, initial_x, initial_y, yaw):

		# Get a new goal position, make sure it is far enough away from the robot. 
		state_object=[np.random.uniform(-4, 4), np.random.uniform(-4, 4), 0.00]
		dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)
		while dist < 3:
			state_object=[np.random.uniform(-4, 4), np.random.uniform(-4, 4), 0.00]
			dist = np.sqrt((state_object[0] - initial_x)**2 + (state_object[1] - initial_y)**2)

		# Estimate time to target, velocity in steps + time to turn + current steps + buffer for going around a robot / acceleration
		# Keep an eye on this, need to make sure there's enough time to get to the goal
		self.heading_error, _ = self.calc_angle_error(state_object, [initial_x, initial_y], yaw)
		self.time_to_target = dist / self.timeStep + abs(self.heading_error) / self.timeStep + self.steps + 500
		
		#Equation of the line trajectory from moving robot to goal

		#Slope
		M = (initial_y-state_object[1])/(initial_x-state_object[0])

		#Y-Intercept
		C = initial_y - (M * initial_x)
		
		#Robot2

		# initial_y2 = np.random.uniform(-2.5, 2.5)  # y position of static robot

		# Start from the midpoint:
		rand_x = (initial_x + state_object[0]) / 2
		rand_y = (initial_y + state_object[1]) / 2

		target_dist = self.a-self.b

		angle = np.arctan2((initial_y-state_object[1]), (initial_x-state_object[0]))
		# target_angle = angle - 90 
		target_angle = random.choice([90 + angle, angle - 90 ])
		initial_x2 = target_dist * np.cos(target_angle) + rand_x
		initial_y2 = target_dist * np.sin(target_angle) + rand_y

		if self.args.debug:
			p.addUserDebugLine((initial_x, initial_y, 0), (state_object[0], state_object[1], 0), lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=5)
			p.addUserDebugLine((rand_x, rand_y, 0), (initial_x2, initial_y2, 0), lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=5)

		#initial_y2 = np.random.uniform(0, 0.5)   
		#initial_x2, initial_y2 = 0,0
		
		self.initial_yaw2 = np.random.uniform(-1, 1)
		self.initial_orn2 = p.getQuaternionFromEuler([0,0,self.initial_yaw2])
		self.z_offset = 0
		self.pos2, self.orn2 = [initial_x2, initial_y2, self.z_offset+0.31],self.initial_orn2
		self.state_robot2 = self.pos2
		self.orn_robot2 = self.orn2
		self.roll2, self.pitch2, self.yaw2 = p.getEulerFromQuaternion(self.orn2)

		# Move the goal
		self.set_position(state_object, robot_id=self.Goal)
		self.state_goal, _ = p.getBasePositionAndOrientation(self.Goal)

		# Move the static robot
		if self.args.num_robots > 1 and self.args.insert_robot2:
			self.set_position(self.pos2, self.orn2, robot_id=self.Id2)
			self.state_robot2, self.orn_robot2 = p.getBasePositionAndOrientation(self.Id2)


	def twist_to_tracks(self, actions):
		radius = 0.14
		width = 0.78/2
		lin_vel = actions[0]
		ang_vel = actions[1]
		w_r = (lin_vel + ang_vel*width)/radius
		w_l = (lin_vel - ang_vel*width)/radius
		return [w_l, w_r]
	
	def step(self, actions):
		#print("AAA",actions)
		#print(self)
		# actions=[2.5,5]

		# actions = 0.5*actions
		# ===========================
		# This is an expert function
		# ===========================
		exp_actions = [0.0]*2

		# if self.args.num_robots > 1:
		# 	if abs(self.heading_error) < 0.5 and self.dist_r1_r2 >1.5 and self.dist_to_wp > 1.0:
		# 		exp_actions[0] = 0.25
		# 		exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
			
		# 	elif abs(self.heading_error) < 1.5 and self.dist_r1_r2 <1.5 and self.dist_to_wp > 1.0:
		# 		exp_actions[0] = 0.04
		# 		exp_actions[1] = -0.5*np.clip(self.heading_error_obs, -1, 1)
		# 	else:	
		# 		exp_actions[0] = 0.0
		# 		exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
      
		# else:
		if abs(self.heading_error) < 0.5 and self.dist_to_wp > 1.0:
			exp_actions[0] = 0.25
		else:	
			exp_actions[0] = 0.0
		exp_actions[1] = 0.5*np.clip(self.heading_error, -1, 1)
		
		if self.args.just_expert or self.args.cur:
			applied_actions = (self.Kp/self.initial_Kp) * np.array(exp_actions)
			if not self.args.just_expert:
				applied_actions += self.action_multiplier*actions
		else:
			applied_actions = self.action_multiplier*actions

		# Network now outputs a twist message
		track_actions = self.twist_to_tracks(applied_actions)

		for (a, tracks) in zip(track_actions,[self.left_track, self.right_track]):
			for track in tracks:
				p.setJointMotorControl2(self.Id, track, p.VELOCITY_CONTROL, targetVelocity=a*20, force=100)
		
		p.stepSimulation()
		if self.args.render:
			time.sleep(self.args.sleep)
		self.get_observation()
		self.save_sim_state()
		#reward, done = self.get_reward()
		reward, done = getattr(self, self.reward_fn_name)()

		# Move the waypoint and static robot if close the waypoint
		# print(self.ep_goal_success, self.time_to_target, self.steps, self.dist_to_wp)
		if self.dist_to_wp < 1.0:
			self.move_goal_and_static_robot(self.pos[0], self.pos[1], self.yaw)
			self.goal_success.append(True)

		elif self.time_to_target < self.steps or done:
			self.move_goal_and_static_robot(self.pos[0], self.pos[1], self.yaw)
			self.goal_success.append(False)

		self.prev_actions = actions
		self.steps += 1
		self.total_steps += 1
		self.total_reward += reward
		#return np.array(self.robot1_bbox[0] +self.robot1_bbox[1] +self.robot1_bbox[2] +self.robot1_bbox[3] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3] + self.contacts + self.contacts2 + list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped]), reward, done, self.ob_dict
		# return np.array(list(self.state_goal)+list(self.body_xyz)+ [self.roll] + [self.pitch] + [self.yaw] + list(self.body_vxyz)+ list(self.base_rot_vel)+ list(self.body_xyz2)+ [self.roll2] + [self.pitch2] + [self.yaw2] + list(self.body_vxyz2)+ list(self.base_rot_vel2)+ [self.tipped]), reward, done, self.ob_dict

		return self.return_state(), reward, done, self.ob_dict

	def return_state(self):
		if self.args.num_robots > 1:
			return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel] + self.robot2_bbox[0] + self.robot2_bbox[1] + self.robot2_bbox[2] + self.robot2_bbox[3])
		else:
			return np.array(self.wp_pos_robot + [self.roll, self.pitch, self.vx, self.yaw_vel])

	def get_reward_1(self):
		"""
		Reward Function 1
		"""
		#reward = 1.5*np.exp(-2.5*max(0, self.target_speed - self.vx)**2)
		#done = False
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
		#print(dist_to_goal)

		# if self.dist_to_robot2 < 2.0:                  #robot1 close to robot 2  distance < x
		# 	goal = np.exp(-0.5*self.dist_to_wp)
		# elif abs(self.heading_error) < 0.5:
		# 	goal = np.exp(-0.5*self.dist_to_wp)
		# else:	
		goal = 0
		if abs(self.heading_error) < 0.5:
			goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
		heading = 0.25*np.exp(-0.5*self.heading_error**2)
		#heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		neg = 0
		if self.vx < 0:
			neg = 0.25*self.vx 
		# if self.vx > 0 and self.heading_vx > 0:
			# goal = 0.5*np.clip(self.heading_vx, 0, 3)

		# goal = 1.5*np.exp(-10*(0.5 - self.heading_vx)**2)
		# goal = 1.5*np.exp(-10*(3.0 - self.heading_vx)**2)
		# neg = 0.25*self.vx if self.vx < 0 else 0
		# heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		#print("goal", goal, "h", heading, "hO", heading_obs, "ng", neg)
		# reward = 1.0 * goal + 0.2 * heading #- 0.2 * heading_obs
		reward = goal + neg + heading
		# reward = goal + heading 
		#print("reward", reward)
		

		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/neg"] += neg
		self.ep_reward_dict["Reward/heading"] += heading
		#self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		#print(state_object[0])
		#print("prev",self.prev_dist_to_goal)
		#print(self.prev_dist_to_goal)
		#print((self.steps * self.timeStep)+1)
		#TT= self.steps * self.timeStep + 1 # time travel per episode ( It is not travel time to goal. I want to stop the robot at the goal. So, I add time of whole episode)
		
		
		
		
		#print(dist_to_goal)
		#fixed_dist_goal=math.sqrt(((3 - self.state_goal[0]) ** 2 + (3 - self.state_goal[1]) ** 2))
		#print("dist_to_goal", dist_to_goal)
		#T= (fixed_dist_goal)*0.75 #Time to reach the goal where 0.75 is the velocity
		
		# reward = 0
		# if dist_to_goal < 0.5:
		#     reward = 100/TT

		#write me a reward function that define shortest possible distance in time

		#print(reward)
		#reward = self.prev_dist_to_goal - dist_to_goal
		
		
		distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
		self.ep_reward_dict["Distance to Goal Improved"] += distance_improve
		#print(distance_improve)
		# print(reward)
		# if dist_to_goal < .2:
		#     reward = 1000/TT
		#print(reward)
		#print((self.steps * self.timeStep)+1,"dist_to_goal", dist_to_goal,"time_to_goal",T, "reward", reward)
		#print("time",T)
		#reward = (max(self.prev_dist_to_goal - dist_to_goal, 0))/TT
		#print(reward)
		#print("difference_in_distance",self.prev_dist_to_goal - dist_to_goal)
		
		self.prev_dist_to_goal = dist_to_goal
		#print(dist_to_goal,self.prev_dist_to_goal)
		#print(self.pos)
		
		#if (self.pos[0] >= 4 or self.pos[0] <= -4 or self.pos[1] >= 4 or self.pos[1] <= -4):
			#done = True
		# Done by reaching goal
		#print("dist",dist_to_goal)
		#print("reward",reward)
		
		#print(self.contacts)


		#######################
		#uncomment this part if inlation radius is used
		if self.intersection:   #Multi RObot Collision
			done=True
			print("Multi_Robot_Collision",done)
		######################
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
			done=True
			#print("Hit_Obstacle",done)
		if self.tipped == True:
			done = True


		return reward, done

	def get_reward_2(self):
		"""
		Reward Function 1
		"""
		#reward = 1.5*np.exp(-2.5*max(0, self.target_speed - self.vx)**2)
		#done = False
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
		#print(dist_to_goal)

		# if self.dist_to_robot2 < 2.0:                  #robot1 close to robot 2  distance < x
		# 	goal = np.exp(-0.5*self.dist_to_wp)
		# elif abs(self.heading_error) < 0.5:
		# 	goal = np.exp(-0.5*self.dist_to_wp)
		# else:	
		goal = 0
		heading = 0.25*np.exp(-0.5*self.heading_error**2)
		if self.dist_r1_r2 < 1.5 and abs(self.heading_error) < 1.6:
			goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
			heading = -0.25*np.exp(-0.5*self.heading_error_obs**2)
		elif self.dist_r1_r2 > 1.5 and abs(self.heading_error) < 0.5:
			goal = np.exp(-0.5*(3.0 - self.heading_vx)**2) if self.vx > 0 else 0.0
			heading = 0.25*np.exp(-0.5*self.heading_error**2)
		#heading_obs = 0.25*np.exp(-0.5*self.heading_error_obs**2)
		neg = 0
		if self.vx < 0:
			neg = 0.25*self.vx 
		# if self.vx > 0 and self.heading_vx > 0:
			# goal = 0.5*np.clip(self.heading_vx, 0, 3)

		# goal = 1.5*np.exp(-10*(0.5 - self.heading_vx)**2)
		# goal = 1.5*np.exp(-10*(3.0 - self.heading_vx)**2)
		# neg = 0.25*self.vx if self.vx < 0 else 0
		# heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		#print("goal", goal, "h", heading, "hO", heading_obs, "ng", neg)
		# reward = 1.0 * goal + 0.2 * heading #- 0.2 * heading_obs
		reward = goal + neg + heading
		# reward = goal + heading 
		#print("reward", reward)
		

		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/neg"] += neg
		self.ep_reward_dict["Reward/heading"] += heading
		#self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		
		
		
		distance_improve = (max(self.prev_dist_to_goal - dist_to_goal, 0))
		self.ep_reward_dict["Distance to Goal Improved"] += distance_improve
		
		
		self.prev_dist_to_goal = dist_to_goal
		


		#######################
		#uncomment this part if inlation radius is used
		if self.intersection:   #Multi RObot Collision
			done=True
			print("Multi_Robot_Collision",done)
		######################
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls/anything
			done=True
			#print("Hit_Obstacle",done)
		if self.tipped == True:
			done = True


		return reward, done
	
	def get_reward_2_old(self):
		"""
		Reward Function 2
		"""
		#reward = 1.5*np.exp(-2.5*max(0, self.target_speed - self.vx)**2)
		#done = False
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
		
		reward = (max(self.prev_dist_to_goal - dist_to_goal, 0))
		
		
		self.prev_dist_to_goal = dist_to_goal
		

		if self.intersection:   #Multi RObot Collision
			done=True
			#print("Multi_Robot_Collision",done)
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls
			done=True
			#print("Hit_Obstacle",done)


		return reward, done
	
	def get_reward_3(self):
		"""
		Reward Function 3
		"""
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))

		if abs(self.heading_error) < 0.5:
			goal = np.exp(-0.5*self.dist_to_wp)
		else:
			goal = 0
		
		heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		heading = np.exp(-0.5*self.heading_error**2)
		#print(goal, heading, heading_obs)
		reward = 1.0 * goal + 0.2 * heading - 0.2 * heading_obs
		#print("reward", reward)
		
		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/heading"] += heading
		self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		self.prev_dist_to_goal = dist_to_goal
		
		if self.intersection:   #Multi RObot Collision
			done=True
			#print("Multi_Robot_Collision",done)
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls
			done=True
			#print("Hit_Obstacle",done)

		return reward, done
	
	def get_reward_4(self):
		"""
		Reward Function 4
		"""
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))

		if abs(self.heading_error) < 1.5708:
			goal = np.exp(-0.5*self.dist_to_wp)
		else:
			goal = 0
		
		heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		heading = np.exp(-0.5*self.heading_error**2)
		#print(goal, heading, heading_obs)
		reward = 1.0 * goal + 0.2 * heading - 0.2 * heading_obs
		#print("reward", reward)
		
		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/heading"] += heading
		self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		self.prev_dist_to_goal = dist_to_goal
		
		if self.intersection:   #Multi RObot Collision
			done=True
			#print("Multi_Robot_Collision",done)
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls
			done=True
			#print("Hit_Obstacle",done)

		return reward, done
	

	def get_reward_5(self):
		"""
		Reward Function 5
		"""
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))

		if abs(self.heading_error) < 1.5708 and abs(self.heading_error_obs) > 0.3:
			goal = np.exp(-0.5*self.dist_to_wp)
		else:
			goal = 0
		
		heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		heading = np.exp(-0.5*self.heading_error**2)
		#print(goal, heading, heading_obs)
		reward = 1.0 * goal + 0.2 * heading - 0.1 * heading_obs
		#print("reward", reward)
		
		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/heading"] += heading
		self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		self.prev_dist_to_goal = dist_to_goal
		
		if self.intersection:   #Multi RObot Collision
			done=True
			#print("Multi_Robot_Collision",done)
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls
			done=True
			#print("Hit_Obstacle",done)

		return reward, done
	
	def get_reward_6(self):
		"""
		Reward Function 6
		"""
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
		
		

		if abs(self.heading_error) < 0.5:
			if abs(self.heading_error_obs) > self.Initial_robot2_avoid_angle:
				goal = np.exp(-0.5*self.dist_to_wp)
			else:
				goal = 0
		else:
				goal = 0

		heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		heading = np.exp(-0.5*self.heading_error**2)
		#print(goal, heading, heading_obs)
		reward = 1.0 * goal + 0.2 * heading - 0.2 * heading_obs
		#print("reward", reward)
		

		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/heading"] += heading
		self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		
		self.prev_dist_to_goal = dist_to_goal
		

		if self.intersection:   #Multi RObot Collision
			done=True
			#print("Multi_Robot_Collision",done)
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls
			done=True
			#print("Hit_Obstacle",done)


		return reward, done
	
	def get_reward_7(self):
		"""
		Reward Function 7
		"""
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))

		if abs(self.heading_error) < 1.5708 and abs(self.heading_error_obs) < (2*self.Initial_robot2_avoid_angle):
			goal = np.exp(-0.5*self.dist_to_wp)
		else:
			goal = 0
		
		heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		heading = np.exp(-0.5*self.heading_error**2)
		#print(goal, heading, heading_obs)
		reward = 1.0 * goal + 0.2 * heading - 0.2 * heading_obs
		#print("reward", reward)
		
		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/heading"] += heading
		self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		self.prev_dist_to_goal = dist_to_goal
		
		if self.intersection:   #Multi RObot Collision
			done=True
			#print("Multi_Robot_Collision",done)
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls
			done=True
			#print("Hit_Obstacle",done)

		return reward, done
	
	def get_reward_8(self):
		"""
		Reward Function 8
		"""
		done=False
		
		dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))

		if abs(self.heading_error) < 1.5708 and abs(self.heading_error_obs) < (3*self.Initial_robot2_avoid_angle):
			goal = np.exp(-0.5*self.dist_to_wp)
		else:
			goal = 0
		
		heading_obs = np.exp(-0.5*self.heading_error_obs**2)
		heading = np.exp(-0.5*self.heading_error**2)
		#print(goal, heading, heading_obs)
		reward = 1.0 * goal + 0.4 * heading + 0.2 * heading_obs
		#print("reward", reward)
		
		self.ep_reward_dict["Reward/goal"] += goal
		self.ep_reward_dict["Reward/heading"] += heading
		self.ep_reward_dict["Reward/heading_obs"] += heading_obs
		
		self.prev_dist_to_goal = dist_to_goal
		
		if self.intersection:   #Multi RObot Collision
			done=True
			#print("Multi_Robot_Collision",done)
		
		if (np.array(self.contacts) == True).any():  #Collision with Walls
			done=True
			#print("Hit_Obstacle",done)

		return reward, done

	def get_observation(self):
		
		self.body_xyz, orn = p.getBasePositionAndOrientation(self.Id)
		self.pos = self.body_xyz

		if self.args.num_robots > 1 and self.args.insert_robot2:
			self.body_xyz2, orn2 = p.getBasePositionAndOrientation(self.Id2)
			self.pos2 = self.body_xyz2
			self.orn2 = list(orn2)
			self.qx2, self.qy2, self.qz2, self.qw2 = self.orn2
			self.roll2, self.pitch2, self.yaw2 = p.getEulerFromQuaternion(self.orn2)
			self.body_vxyz2, self.base_rot_vel2 = p.getBaseVelocity(self.Id2)

			self.roll_vel2 = self.base_rot_vel2[0]
			self.pitch_vel2 = self.base_rot_vel2[1]
			self.yaw_vel2 = self.base_rot_vel2[2]

		#print("pos_euler",self.pos)
		#print("self.body_xyz",self.body_xyz)
		#print("posx", self.pos[0],"posy", self.pos[1],"posz", self.pos[2])
		self.orn = list(orn)
		self.qx, self.qy, self.qz, self.qw = self.orn
		self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
		self.body_vxyz, self.base_rot_vel = p.getBaseVelocity(self.Id)
		#print(type(self.body_xyz))
		#print(self.body_xyz[2])
		#print(self.pos)
		# k=[self.body_xyz[0]+0.7,1.5*self.body_xyz[1],self.body_xyz[2]]
		# l=[self.body_xyz[0]-0.7,1.5*self.body_xyz[1],self.body_xyz[2]]
		# m=[0,0,0]
		# n=30
		# p.addUserDebugLine(k,l,m,n,.2)
		self.roll_vel = self.base_rot_vel[0]
		self.pitch_vel = self.base_rot_vel[1]
		self.yaw_vel = self.base_rot_vel[2]



		#dist_to_goal = math.sqrt(((self.pos[0] - self.state_goal[0]) ** 2 + (self.pos[1] - self.state_goal[1]) ** 2))
		#print(dist_to_goal)
		rot_speed = np.array(
		[[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
			[np.sin(-self.yaw), np.cos(-self.yaw), 0],
			[		0,			 0, 1]]
		)

		self.contacts = []
		self.contacts2 = []
		for contact in self.contact_dict:
			self.contacts.append(len(p.getContactPoints(self.Id, -1, self.contact_dict[contact], -1))>0)
			if self.args.num_robots > 1 and self.args.insert_robot2:
				self.contacts2.append(len(p.getContactPoints(self.Id2, -1, self.contact_dict[contact], -1))>0)
			#self.contacts.append(len(p.getContactPoints(self.Id, self.Id2, self.contact_dict[contact], -1))>0)
			#self.contacts.append(len(p.getContactPoints(self.Id2, -1, self.contact_dict[contact], -1))>0)
		#print(self.contacts, self.contacts2)
		self.vx, self.vy, self.vz = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))

		if self.args.num_robots > 1 and self.args.insert_robot2:
			rot_speed2 = np.array(
			[[np.cos(-self.yaw2), -np.sin(-self.yaw2), 0],
				[np.sin(-self.yaw2), np.cos(-self.yaw2), 0],
				[		0,			 0, 1]]
			)
			self.vx2, self.vy2, self.vz2 = np.dot(rot_speed2, (self.body_vxyz2[0],self.body_vxyz2[1],self.body_vxyz2[2]))
		
		if abs(self.orn[0]) > 0.35 or abs(self.orn[1]) > 0.35:
			self.tipped = True
		else:
			self.tipped = False

		#print(self.body_vxyz[0]+self.body_vxyz[1])


		########################
		#Do not use this part if you already used it in reset
		#Uncomment this part if you want to use dynamic inflation radius

		m= 0.075
		# m= 0.075+((abs(self.body_vxyz[0])+abs(self.body_vxyz[1]))*0.05)#0.075 #value of inflation radius
		
		
		x=(1.4/2)+m
		y=(0.78/2)+m
		z=0.235
		# get the self.corners of the bounding box
		self.corners1 = [(x, y, z),
		  		(x,-y,z),
		  		(-x,-y,z),
		  		(-x,y,z),
		  		(x,y,z)]
		
		self.corners2 = [(x, y, z),
		  		(x,-y,z),
		  		(-x,-y,z),
		  		(-x,y,z),
		  		(x,y,z)]

		
		# ########################
		self.intersection = False
		
		if self.args.num_robots > 1:

			# #This part is for setting inflation radious bounding box around robots
			self.robot1_bbox=[]
			self.robot2_bbox=[]
			


			for i in range(len(self.corners1)-1):
				
				
				start1 = p.multiplyTransforms(self.pos, self.orn, self.corners1[i], [0, 0, 0, 1])[0]
				#print(list(start1))
				#print(i, self.corners1[i])
				self.robot1_bbox.append(list(start1))
				#print(self.corners[i])
					
				#print(p.multiplyTransforms(pos, orn, self.corners[i], [0, 0, 0, 1]))
				end1 = p.multiplyTransforms(self.pos, self.orn, self.corners1[i+1], [0, 0, 0, 1])[0]
				if self.args.debug:
					self.lineId1[i]=p.addUserDebugLine(start1, end1, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=self.lineId1[i])
			
			

				#for j in range(len(self.corners2)-1):
				start2 = p.multiplyTransforms(self.pos2, self.orn2, self.corners2[i], [0, 0, 0, 1])[0]
				
				self.robot2_bbox.append(list(start2))
				#print(self.corners[i])
				#print(p.multiplyTransforms(pos, orn, self.corners[i], [0, 0, 0, 1]))
				end2 = p.multiplyTransforms(self.pos2, self.orn2, self.corners2[i+1], [0, 0, 0, 1])[0]
				if self.args.debug:
					self.lineId2[i]=p.addUserDebugLine(start2, end2, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=self.lineId2[i])
					#print("robotA", start1, "robotB",start2)

			self.robot1_bbox.append(self.robot1_bbox[0])
			self.robot2_bbox.append(self.robot2_bbox[0])
			# check for intersection between the two lines
			# print(self.intersection)
			for i in range(len(self.robot1_bbox)-1):
				for j in range(len(self.robot2_bbox)-1):

					#print(self.intersection)
					x1,y1,z1=self.robot1_bbox[i]     #Rotating start coordinates for Robot 1
					x2,y2,z2=self.robot1_bbox[i+1]   #Rotating end coordinates for Robot 1
					x3,y3,z3=self.robot2_bbox[j]     #Rotating start coordinates for Robot 2
					x4,y4,z4=self.robot2_bbox[j+1]   #Rotating end coordinates for Robot 2


					if (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1) == 0:
						
						self.intersection = True
						print("Denominator_Zero")
					else:
						uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
						uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))


					# uA = ((x2-x1)*(y4-y3) - (y2-y1)*(x4-x3)) / ((x2-x1)*(y4-y3) - (y2-y1)*(x4-x3))
					# uB = ((x3-x4)*(y1-y2) - (y3-y4)*(x1-x2)) / ((x2-x1)*(y4-y3) - (y2-y1)*(x4-x3))
					#uA = ((end2[0]-start2[0])*(start1[1]-start2[1]) - (end2[1]-start2[1])*(start1[0]-start2[0])) / ((end2[1]-start2[1])*(end1[0]-start1[0]) - (end2[0]-start2[0])*(end1[1]-start1[1]))
					#uB = ((end1[0]-start1[0])*(start1[1]-start2[1]) - (end1[1]-start1[1])*(start1[0]-start2[0])) / ((end2[1]-start2[1])*(end1[0]-start1[0]) - (end2[0]-start2[0])*(end1[1]-start1[1]))
					#print("line1",uA,"line2", uB)
						if 0 <= uA <= 1 and 0 <= uB <= 1:
							self.intersection = True

		#Uncomment above section if you want to use inflation radius
			   
		#print(tuple(self.robot1_bbox[0]))
		if self.args.num_robots > 1:
			#self.c_robot1 = [(tuple(self.robot1_bbox[0])),(tuple(self.robot1_bbox[1])),(tuple(self.robot1_bbox[2])),(tuple(self.robot1_bbox[3]))]
			self.c_robot1 = [(tuple(self.robot1_bbox[0])),(tuple(self.robot1_bbox[1]))]
			self.c_robot2 = [(tuple(self.robot2_bbox[0])),(tuple(self.robot2_bbox[1])),(tuple(self.robot2_bbox[2])),(tuple(self.robot2_bbox[3]))]
  
			self.dist_r1_r2 = self.min_distance_corners(self.c_robot1, self.c_robot2)
			#print("Minimum Distance between the corner points of robot1 and robot2:", self.dist_r1_r2)
  
  
  
		
		

		# print "Collision detected!" if the lines are intersecting
		# if self.intersection:
		# 	print("Collision detected!")


		#Between Goal and Robot 1
		self.wp_pos_robot = self.world_to_robot(self.yaw, self.pos, self.state_goal)
		#print(self.wp_pos_robot)
		#print("waypoint_pos", self.wp_pos_robot)
		self.heading_error, self.target_angle = self.calc_angle_error(self.state_goal, self.pos, self.yaw)
		#print("heading_error", self.heading_error)
		self.dist_to_wp = math.sqrt(self.wp_pos_robot[0]**2 + self.wp_pos_robot[1]**2)
		#print("distanc-to_wp", self.dist_to_wp)

		rot_speed = np.array(
		[[np.cos(-self.target_angle), -np.sin(-self.target_angle), 0],
			[np.sin(-self.target_angle), np.cos(-self.target_angle), 0],
			[		0,			 0, 1]]
		)
		self.heading_vx, _, _ = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))

		if self.args.num_robots > 1:
			#Between Robot 1 and Robot 2
			self.robot2_pos_robot1 = self.world_to_robot(self.yaw, self.pos, self.state_robot2)
			#print("self.robot2_pos_robot1",self.robot2_pos_robot1)
			self.dist_to_robot2 = math.sqrt(self.robot2_pos_robot1[0]**2 + self.robot2_pos_robot1[1]**2)
			#print("self.dist_to_robot2 ",self.dist_to_robot2 )
			self.heading_error_obs, self.target_angle_obs = self.calc_angle_error(self.state_robot2, self.pos, self.yaw)
			#print("heading_error_obs", self.heading_error_obs)
			#print("target_angle_obs", self.target_angle_obs)
			self.robot2_avoid_angle = np.arctan2(0.7, self.dist_to_robot2)
			#print("robot2_avoid_angle",self.robot2_avoid_angle*(180/np.pi),self.robot2_avoid_angle)
		
		# robot2_avoid_angle = np.arctan2(0.7*self.yaw2, self.dist_to_robot2)
		# print("robot2_avoid_angleyaw",robot2_avoid_angle*(180/np.pi))
		# robot2_avoid_angle = np.arctan2(math.sqrt(0.7**2 + self.yaw2**2), self.dist_to_robot2)
		# print("robot2_avoid_anglesqrt",robot2_avoid_angle*(180/np.pi))
		# print(self.yaw2)

		rayLen = 2
		mat = p.getMatrixFromQuaternion(self.orn)
		dir = [mat[0], mat[3], mat[6]]
		lines_from = []
		lines_to = []
		for n, line_from in enumerate(self.robot1_bbox[:2]):
			line_to = [line_from[0] + dir[0] * rayLen, line_from[1] + dir[1] * rayLen, line_from[2] + dir[2] * rayLen]
			line_from = [self.body_xyz[0] + dir[0] * 0.5, self.body_xyz[1] + dir[1] * 0.5, self.body_xyz[2] + dir[2] * 0.5]
			lines_from.append(line_from)
			lines_to.append(line_to)
		if self.args.debug:
			for n, (line_to, line_from) in enumerate(zip(lines_from, lines_to)):
				self.ray_line[n] = p.addUserDebugLine(line_from, line_to, lineColorRGB=[1, 0, 0], lineWidth=50, lifeTime=0.3, replaceItemUniqueId=self.ray_line[n])
		hits = p.rayTestBatch(lines_from, lines_to)
		self.hit = [hits[0][0] > 0, hits[1][0] > 0]


	def world_to_robot(self, robot_yaw, robot, world):
		x,y = world[0] - robot[0], world[1] - robot[1]                       #longitudinal distance
		rot_mat = np.array([[np.cos(robot_yaw), np.sin(robot_yaw)],          #rotational distance
							 [-np.sin(robot_yaw), np.cos(robot_yaw)]])
		return list(np.dot(rot_mat, np.array([x, y])))

	def calc_angle_error(self, world, robot, angle):
		target_angle = np.arctan2(world[1] - robot[1], world[0] - robot[0])
		#print("target",target_angle)
		if ( target_angle < 0 and angle > 0 ):
			angle_error = ( 2*np.pi + target_angle ) - angle
		elif ( target_angle > 0 and angle < 0 ):
			angle_error = target_angle - ( 2*np.pi + angle )
		else:
			angle_error = target_angle - angle

		if angle_error > np.pi:
			angle_error = np.pi - angle_error
		elif angle_error < -np.pi:
			angle_error = angle_error - np.pi

		return angle_error, target_angle

	def min_distance_corners(self, corners_robot1, corners_robot2):
	

		min_distance = float('inf')

		for corner1 in corners_robot1:
			for corner2 in corners_robot2:
				dist = math.sqrt((corner2[0] - corner1[0]) ** 2 + (corner2[1] - corner1[1]) ** 2)
				#print(dist)
				min_distance = min(min_distance, dist)

		return min_distance