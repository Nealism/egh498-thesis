from cmath import e
from copy import deepcopy
import numpy as np
import pybullet as p
import time
from gym import spaces
from collections import deque
import cv2
from mpi4py import MPI
comm = MPI.COMM_WORLD

from assets.env_base_pb import EnvBasePB

class Env(EnvBasePB):

    def __init__(self, PATH=None, args=None, writer=None):

        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True 

        super().__init__(PATH)

        self.simStep = 1/240
        self.timeStep = 1/120
        if "pumpkin" in self.args.env:
            self.ac_size = 22
            self.ob_size = 7
        else:
            self.ac_size = 22
            self.ob_size = 6
        self.Kp = 400
        self.initial_Kp = self.Kp

        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        
        self.steps = -1
        
        self.env_exp = None
        self.target_speed = 1.0
        self.target_yaw = 0.0
        self.initial_joints = [0.0] * 15 + [ 0.5, -0.5, -1.5707] + [-0.5, 0.5, -1.5707]
        self.cur_success = deque([0.0], maxlen=5)

        if self.args.add_terrain:
            self.terrain_difficulty = self.args.initial_terrain_difficulty
        else:
            self.terrain_difficulty = 0
            self.terrain = None

        self.max_disturbance = 250
        self.final_disturbance = 1600
        self.episodes = 0
        self.total_steps = 0
        self.ob_dict = {}

        # States that we want to restore, for resuming training after running a test
        self.states_to_restore = ["pos", "orn", "joints", "base_vel", "joint_vel", "args", "episodes", "steps", "total_steps"]

        # Things we want to log each training step (print and add to tensorboard)
        self.log_things = {"Kp": self.Kp, "Success": self.cur_success, "Dist": self.max_disturbance, "Diffficulty": self.terrain_difficulty}

    def load_specific_robot(self):

        if "pumpkin" in self.args.env:
            self.load_urdf_robot("./assets/urdfs/pumpkin.urdf")
            self.contact_list = ['pumpkin_chassis', 'pumpkin_lower_chassis']
        else:
            self.load_urdf_robot("./assets/urdfs/dynamic_titan.urdf")
            self.contact_list = ['titan_chassis']

        self.left_track = []
        self.right_track = []
        self.contact_dict = {}
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            link_name = info[12].decode("ascii")
            if link_name in self.contact_list: self.contact_dict[link_name] = j
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            if "left" in jname:
                self.left_track.append(j)
            elif "right" in jname:
                self.right_track.append(j)
        self.motors = []

    def check_for_success(self):
        return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()

    def get_success(self):
        return self.body_xyz[0] > 15

    def reset(self, terrain=None, test=False, restore_state=None):
        self.load_robot()
        
        if self.rank == 0 and self.args.record_sim and self.episodes > 0:
            self.record_sim_state(best=self.check_for_success(), test=test)
        
        self.steps = 0
        initial_x, initial_y = 2, np.random.uniform(-0.5, 0.5)   
        self.initial_yaw = np.random.uniform(-0.5,0.5)
        self.initial_orn = p.getQuaternionFromEuler([0,0,self.initial_yaw])
        self.z_offset = 0

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1])
        else:
            pos, orn, self.joints, self.base_vel, self.joint_vel = [initial_x, initial_y, self.z_offset+0.31],self.initial_orn, [0]*self.ac_size, [[0,0,0],[0,0,0]], [0.]*self.ac_size
            self.set_position(pos, orn)
        self.get_observation()
        self.episodes += 1
        return np.array(self.orn + self.contacts + [self.tipped])

    def step(self, actions):
        for (a, tracks) in zip(actions,[self.left_track, self.right_track]):
            for track in tracks:
                p.setJointMotorControl2(self.Id, track, p.VELOCITY_CONTROL, targetVelocity=a*20, force=100)
        p.stepSimulation()
        if self.args.render:
            time.sleep(self.args.sleep)
        self.get_observation()
        self.save_sim_state()
        reward, done = self.get_reward()
        self.prev_actions = actions
        self.steps += 1
        self.total_steps += 1
        return np.array(self.orn + self.contacts + [self.tipped]), reward, done, self.ob_dict

    def get_reward(self):
        reward = 1.5*np.exp(-2.5*max(0, self.target_speed - self.vx)**2)
        done = False
        return reward, done

    def get_observation(self):
        self.body_xyz, orn = p.getBasePositionAndOrientation(self.Id)
        self.pos = self.body_xyz
        self.orn = list(orn)
        self.qx, self.qy, self.qz, self.qw = self.orn
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion(self.orn)
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