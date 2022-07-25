import sys
sys.path.append('../../brendan')
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
import pybullet as p
import time
import numpy as np
from assets.obstacles_pb import Obstacles
import gym
from heightmap import HeightMap
from mpi4py import MPI
comm = MPI.COMM_WORLD
from collections import deque

class Env(gym.Env):
    ob_size = 4
    #   ob_size = 12
    ac_size = 2
    # im_size = [120,120,1]
    # resolution = 0.1
    # im_size = [60,60,1]
    im_size = [40,40,1]
    resolution = 0.1
    #   timeStep = 1/240
    # timeStep = 1/120
    timeStep = 1/10
    #   timeStep = 1/60
    #   timeStep = 1/10
    target_xv = 0.0
    target_yawv = 0.0
    episodes = 0
    y_offset = 0
    total_steps = 0
    difficulty = 1
    def __init__(self, PATH=None, args=None, rank=0):
        self.PATH = PATH
        self.args = args
        self.rank = rank

        self.state = ['left_motor_pos', 'right_motor_pos']
        self.state += ['left_motor_vel', 'right_motor_vel']
        # self.state += ['left_motor_vel', 'right_motor_vel']
        
        self.obstacles = Obstacles()
        
        if self.args.render and self.rank == 0:
            self.physicsClientId = p.connect(p.GUI)
        else:
            self.physicsClientId = p.connect(p.DIRECT) 
        p.setTimeStep(self.timeStep)
        p.setGravity(0,0,-9.8)
        self.load_model()

    def load_model(self):
        p.loadMJCF(currentdir + "/ground.xml")
        # Titan urdf doesn't have motors, for now can only use pumpkin
        if self.args.robot == 'dynamic':
            self.Id = p.loadURDF(currentdir + "/dynamic_titan.urdf")
            self.left_track = []
            self.right_track = []
            self.contact_list = ['pumpkin_chassis', 'pumpkin_lower_chassis']
            self.contact_dict = {}
            for j in range( p.getNumJoints(self.Id) ):
                info = p.getJointInfo(self.Id, j)
                link_name = info[12].decode("ascii")
                # print(link_name)
                if link_name in self.contact_list: self.contact_dict[link_name] = j
                if info[2] != p.JOINT_REVOLUTE: continue
                jname = info[1].decode("ascii")
                if "left" in jname:
                    self.left_track.append(j)
                elif "right" in jname:
                    self.right_track.append(j)

            # self.tracks = [[2,3,4], [5,6,7]]
            self.tracks = [self.left_track, self.right_track]
        elif self.args.robot == 'pumpkin':
            self.Id = p.loadURDF(currentdir + "/pumpkin.urdf")
            self.left_track = []
            self.right_track = []
            self.contact_list = ['pumpkin_chassis', 'pumpkin_lower_chassis']
            self.contact_dict = {}
            for j in range( p.getNumJoints(self.Id) ):
                info = p.getJointInfo(self.Id, j)
                link_name = info[12].decode("ascii")
                # print(link_name)
                if link_name in self.contact_list: self.contact_dict[link_name] = j
                if info[2] != p.JOINT_REVOLUTE: continue
                jname = info[1].decode("ascii")
                if "left" in jname:
                    self.left_track.append(j)
                elif "right" in jname:
                    self.right_track.append(j)

            # self.tracks = [[2,3,4], [5,6,7]]
            self.tracks = [self.left_track, self.right_track]
        elif self.args.robot == 'titan':
            self.Id = p.loadURDF(currentdir + "/titan.urdf")
            self.jdict = {}
            self.ordered_joints = []
            self.ordered_joint_indices = []
            for j in range( p.getNumJoints(self.Id) ):
                info = p.getJointInfo(self.Id, j)
                link_name = info[12].decode("ascii")
                self.ordered_joint_indices.append(j)
                # print(info, info[2])
                if info[2] != p.JOINT_REVOLUTE: continue
                jname = info[1].decode("ascii")
                print(jname)
                lower, upper = (info[8], info[9])
                self.ordered_joints.append( (j, lower, upper) )
                self.jdict[jname] = j
            self.motor_names = ['left_motor', 'right_motor']
            self.motors = [self.jdict[n] for n in self.motor_names]
        # Disable motors to use torque control:
        # p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(self.motor_names))
        self.pos = [0,0,0] 
        self.ep_success = deque(maxlen=3)
    

    def reset(self, box_info=None):
        self.steps = 0
        self.prev_actions = [0,0]

        # if self.episodes == 0:
        # p.resetSimulation()
        # self.load_model()
        # self.box_info = self.obstacles.add_straight_world(self, difficulty=10, height_coeff=0.07, terrain_type='mix', base=False, base_before=False, initial_pos=[0,0,0], baseline=False, num_artifacts=1, rand_flat=False, args=None, obstacle_types=None, dqn=False):
        if self.episodes > 0 and self.args.record_step:
            self.save_sim_data()
        else:
            self.sim_data = []
            self.im_data = []

        self.ep_success.append(self.pos[0] > 15)
        if (np.array(self.ep_success) > 0).all() and self.difficulty < 10:
            self.difficulty += 1

        if box_info is None:
            self.obstacles.remove_obstacles()
            self.box_info = self.obstacles.add_doors(self.difficulty)
        else:
            self.obstacles.remove_obstacles()
            self.box_info = box_info
            for pos, size, colour in zip(self.box_info[1], self.box_info[2], self.box_info[3]):
                self.obstacles.add_box(pos=pos[:3], orn=pos[3:], size=np.array(size)/2, colour=colour)

        # min_x, max_x, min_y, max_y = self.heightmap.map_extents
        # initial_x, initial_y = np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)
        initial_x, initial_y = 2, np.random.uniform(-0.5, 0.5)   
        self.initial_yaw = np.random.uniform(-0.5,0.5)
        self.initial_orn = p.getQuaternionFromEuler([0,0,self.initial_yaw])
        self.heightmap = HeightMap(self.box_info, self.im_size, grid_size=self.resolution, initial_yaw=self.initial_yaw, robot_pos=[initial_x, initial_y])
        self.heightmap.map_extents
        self.z_offset = self.heightmap.z_offset

        pos, orn, joints, base_vel, joint_vel = [initial_x, initial_y, self.z_offset+0.31],self.initial_orn, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size

        # pos, orn, joints, base_vel, joint_vel = [0,0,self.z_offset+0.31],[0,0,0,1], [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
        self.set_position(pos, orn)
        self.ob_dict = {}
        self.ob_dict.update({'left_motor_pos':0, 'right_motor_pos':0, 'left_motor_vel':0, 'right_motor_vel':0})
        self.get_observation()
        self.episodes += 1
        
        # return np.array([self.ob_dict[s] for s in self.state] + [self.target_xv, self.target_yawv])
        # return np.array([self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel, self.vx, self.vy, self.vz, self.pos[0],self.pos[1],self.pos[2], self.yaw])
        return np.array(self.orn)

    def step(self, actions=None, set_position=None):
        # actions = np.array([1.0, 1.0])
        # print(actions)
        if set_position is not None:
            self.set_position(pos=set_position[0], orn=set_position[1])
        else:
            for (a, tracks) in zip(actions,[self.left_track, self.right_track]):
                for track in tracks:
                    p.setJointMotorControl2(self.Id, track, p.VELOCITY_CONTROL, targetVelocity=a*100, force=100)
            p.stepSimulation()
        if self.args.render:
            time.sleep(self.args.sleep)
        self.get_observation()
        reward, done = self.get_reward(actions)
        self.prev_actions = actions
        if self.args.record_step: 
            self.record_sim_data()
        self.steps += 1
        self.total_steps += 1
        # return np.array([self.ob_dict[s] for s in self.state] + [self.target_xv, self.target_yawv]), reward, done, self.ob_dict
        # return np.array([self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel, self.vx, self.vy, self.vz, self.pos[0],self.pos[1],self.pos[2], self.yaw]), reward, done, self.ob_dict
        return np.array(self.orn), reward, done, self.ob_dict
    
    def get_reward(self, actions):
        done = False
        # print("rew", self.vx)
        # reward = np.exp(-2.5*abs(max(0, 0.5 - self.vx)))
        # reward = np.exp(-2.5*abs(max(0, 1.0 - self.vx)))
        # reward = np.exp(-2.5*abs(max(0, 0.75 - self.vx)))
        reward = np.exp(-2.5*abs(0.75 - self.vx))
        # print(self.yaw)
        # reward -= 0.1*np.exp(-2.5*abs(max(0, 0.75 - self.vx)))
        # if self.use_wp:
        #     # reward = np.exp(-2.5*abs(max(0, 0.5 - actions[0])))
        #     # reward -= 0.05*actions[1]**2
        #     reward += 0.1*np.exp(-2.5*np.sum(abs(np.array(self.orn) - np.array(self.waypoint_orn))))
        #     reward += 0.1*np.exp(-2.5*self.dist_to_waypoint)
        reward -= 0.001*np.sum((np.array(actions) - np.array(self.prev_actions))**2)
        # reward += np.exp(-2.5*abs(max(0, np.array([]) 1.0 - self.vx)))
        # print(self.orn, self.waypoint_orn)
        if self.steps > self.args.horizon or self.tipped or abs(self.yaw) > 1.4:
            # print(abs(self.yaw))
            done = True
        return reward, done

    def get_observation(self):
        self.pos, self.orn = p.getBasePositionAndOrientation(self.Id)
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(list(self.orn))
        self.body_vxyz, self.base_rot_vel = p.getBaseVelocity(self.Id)
        
        self.roll_vel = self.base_rot_vel[0]
        self.pitch_vel = self.base_rot_vel[1]
        self.yaw_vel = self.base_rot_vel[2]

        rot_speed = np.array(
        [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
            [np.sin(-self.yaw), np.cos(-self.yaw), 0],
            [		0,			 0, 1]]
        )

        self.contacts = []
        for contact in self.contact_dict:
            self.contacts.append(len(p.getContactPoints(self.Id, -1, self.contact_dict[contact], -1))>0)

        self.vx, self.vy, self.vz = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        if abs(self.orn[0]) > 0.35 or abs(self.orn[1]) > 0.35:
            self.tipped = True
        else:
            self.tipped = False

    def get_im(self, cam=None):
        # self.costmap = get_hm(self.pos, self.box_info, self.im_size, self.resolution)

        # self.costmap = self.heightmap.get_hm(self.pos, robot_yaw=None, display=self.args.display_im)
        self.hm = self.heightmap.get_hm(self.pos, robot_yaw=self.yaw, display=self.args.display_im)
        return self.hm

    def set_position(self, pos, orn, joints=None, velocities=None, joint_vel=None):
        pos = [pos[0], pos[1]+self.y_offset, pos[2]]
        p.resetBasePositionAndOrientation(self.Id, pos, orn)
        if joints is not None:
            if joint_vel is not None:
                for j, jv, m in zip(joints, joint_vel, self.motors):
                    p.resetJointState(self.Id, m, targetValue=j, targetVelocity=jv)
            else:
                for j, m in zip(joints, self.motors):
                    p.resetJointState(self.Id, m, targetValue=j)
        if velocities is not None:
            p.resetBaseVelocity(self.Id, velocities[0], velocities[1])

    def save_sim_data(self, PATH=None, last_steps=False):  
        if self.rank == 0 or last_steps:
            if PATH is not None:
                path = PATH
            else:
                path = self.PATH
            try:
                if last_steps:
                # print("saving to ", path + 'sim_data.npy')
                    np.save(path + 'sim_data.npy', np.array(self.sim_data, dtype='object')[-300:,:])     
                    np.save(path + 'im_data.npy', np.array(self.im_data, dtype='object')[-300:,:])     
                else:
                # print(np.array(self.sim_data).shape)
                    np.save(path + 'sim_data.npy', np.array(self.sim_data, dtype='object'))     
                    np.save(path + 'im_data.npy', np.array(self.im_data, dtype='object'))     
                self.sim_data = []
                self.im_data = []
            except Exception as e:
                print("Save sim data error:")
                print(e)    
            try:
                if self.box_info is not None:
                    np.save(path + 'box_info.npy', np.array(self.box_info, dtype=object))
            except Exception as e:
                print("trying to save box info", e)

    def record_sim_data(self):
        if len(self.sim_data) > 100000: return
        pos, orn = p.getBasePositionAndOrientation(self.Id)
        data = [pos, orn]
        self.sim_data.append(data)
        self.im_data.append(self.hm)


    def log_stuff(self, logger, writer, iters_so_far):
        
        difficulty = MPI.COMM_WORLD.allgather(self.difficulty)
        self.min_difficulty = np.min(difficulty)
        self.iters_so_far = iters_so_far
        if self.rank == 0:
            print("difficulty", difficulty, self.difficulty)
            writer.add_scalar("difficulty", self.min_difficulty, self.iters_so_far)   
            logger.record_tabular("difficulty", self.min_difficulty)


if __name__=="__main__":
  import argparse

  env = Env(render=True)
  ob = env.reset()
  # pid =  p.loadPlugin(PATH, postfix)
  # p.executePluginCommand(pid, textArg, intArgs, floatArgs)
  while True:
    ob, rew, done, _ = env.step(actions)
    if done:
      ob = env.reset()

