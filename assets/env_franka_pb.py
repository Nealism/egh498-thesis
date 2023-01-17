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
        self.ac_size = 7
        self.ob_size = 23
        self.Kp = 400
        self.initial_Kp = self.Kp
        self.ROBOT_HEIGHT = 1.2

        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        
        self.episodes = -1
        
        self.target_speed = 1.0
        self.target_yaw = 0.0
        self.cur_success = deque([0.0], maxlen=5)
        self.ep_success = deque([0.0], maxlen=5)

        if self.args.add_terrain:
            self.terrain_difficulty = self.args.initial_terrain_difficulty
        else:
            self.terrain_difficulty = 0
            self.terrain = None

        self.max_disturbance = 250
        self.final_disturbance = 1600

        self.states_to_save = ["joints", "pos", "orn", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "episodes", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance"]

        self.log_things = {"Kp": self.Kp, "Success": self.cur_success, "Dist": self.max_disturbance, "Diffficulty": self.terrain_difficulty}

    def load_specific_robot(self):
        
        self.load_urdf_robot("assets/urdfs/franka_panda/panda.urdf")

        self.jdict = {}
        self.ordered_joints = []
        self.ordered_joint_indices = []
        self.motor_names = []
        self.motor_power = []
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            link_name = info[12].decode("ascii")
            self.ordered_joint_indices.append(j)
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            lower, upper = (info[8], info[9])
            self.ordered_joints.append( (j, lower, upper) )
            self.jdict[jname] = j
            self.motor_names += [jname]
            self.motor_power += [10]

        self.motors = [self.jdict[n] for n in self.motor_names]
            
        forces = np.ones(len(self.motors))*240
        self.actions = {key:0.0 for key in self.motor_names}

        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(self.motor_names))

    def check_for_success(self):
        return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()

    def get_success(self):
        return self.body_xyz[0] > 15

    def reset(self, terrain=None, test=False, restore_state=None):
        self.load_robot()   
        self.paused = False
        self.ob_dict = {}
        self.contacts = []
        if self.episodes > -1:
            self.ep_success = self.get_success()
            self.cur_success.append(self.ep_success)  

        if self.rank == 0 and self.args.record_sim and self.episodes > -1:
            self.record_sim_state(best=self.check_for_success(), test=test)

        self.initial_joints = [0.0] * (self.ac_size + 1)
        self.initial_joints[3] = -np.pi/2
        self.initial_joints[5] = np.pi/2
        self.initial_joints[6] = np.pi/4
        
        self.steps = 0
        self.episodes += 1

        self.first_step = True
        self.prev_step_count = self.step_count = 0
        self.z_offset = 0

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            rand_scale = self.max_disturbance / self.final_disturbance
            pos = [0,0,0]
            orn = p.getQuaternionFromEuler([rand_scale * 0.25 * np.random.random(), rand_scale * 0.25 * np.random.random(), 0.0])
            # orn = [0,0,0,1]
            base_vel = [0,0,0]
            # joints = [0]*len(self.motors)
            joints = []
            for j in self.ordered_joints:
                joints.append(np.clip(np.random.random() * rand_scale * 0.25 , j[1], j[2]))
            joint_vel = [0]*len(self.motors)
            self.set_position(pos, orn, joints, base_vel, joint_vel)
        self.get_observation()

        self.state = self.joints + self.joint_vel + self.body + self.contacts 
        return np.array(self.state)

    def step(self, actions):
        # Wait until both feet in contact with the ground before progressing the expert
        forces = 30.0*np.array(actions)
        self.actions = actions
        
        if self.args.cur:
            if self.Kp > 0:
                exp_forces = self.apply_forces()
                forces = forces + (self.Kp/self.initial_Kp) * exp_forces
                
        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.TORQUE_CONTROL, forces=forces)

        for _ in range(int(self.timeStep/self.simStep)):
            p.stepSimulation()

        if self.args.render:
            time.sleep(0.01)

        self.get_observation()
        self.save_sim_state()
        reward, done = self.get_reward()
        self.steps += 1
        self.state = self.joints + self.joint_vel + self.body + self.contacts 
        return self.state, reward, done, None

    def get_reward(self):
        reward = 1.5
        done = False
        return reward, done

    def get_observation(self):
        jointStates = p.getJointStates(self.Id,self.ordered_joint_indices)
        self.joints = list(np.array([jointStates[j[0]][0] for j in self.ordered_joints[:int(self.ac_size)]]))
        
        # Scale vels 
        self.joint_vel = list(np.array([jointStates[j[0]][1] for j in self.ordered_joints[:int(self.ac_size)]]) / 10) 
        
        self.ob_dict.update({n + '_pos':j for n,j in zip(self.motor_names, self.joints)})


        self.body_xyz, (self.qx, self.qy, self.qz, self.qw) = p.getBasePositionAndOrientation(self.Id)
        self.pos = self.body_xyz
        self.orn = [self.qx, self.qy, self.qz, self.qw]
        self.roll, self.pitch, self.yaw = p.getEulerFromQuaternion([self.qx, self.qy, self.qz, self.qw])

        self.body_vxyz, self.base_rot_vel = p.getBaseVelocity(self.Id)
        
        self.roll_vel = self.base_rot_vel[0]
        self.pitch_vel = self.base_rot_vel[1]
        self.yaw_vel = self.base_rot_vel[2]

        rot_speed = np.array(
        [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
            [np.sin(-self.yaw), np.cos(-self.yaw), 0],
            [		0,			 0, 1]]
        )

        self.vx, self.vy, self.vz = np.dot(rot_speed, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
        
        # Policy shouldn't know yaw
        self.body = [self.vx, self.vy, self.vz, self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel, self.body_xyz[2] - self.z_offset]

        # self.viewer.add_marker(pos=np.array(target), type=2, label="", size=np.array([0.05, 0.05, 0.05]), rgba=np.array([0.0, 0.0, 1.0, 1.0]))
        # self.viewer.add_marker(pos=np.array(target), type=2, label="", size=np.array([self.target_radius, self.target_radius, self.target_radius]), rgba=np.array([0.0, 1.0, 0.0, 0.2]))
        # self.viewer.add_marker(pos=np.array(target_point), type=2, label="", size=np.array([0.01, 0.01, 0.01]), rgba=np.array([1.0, 0.0, 0.0, 1.0]))
        # self.viewer.add_marker(pos=np.array(target_point2), type=2, label="", size=np.array([0.01, 0.01, 0.01]), rgba=np.array([1.0, 0.0, 0.0, 1.0]))

    def insert_sphere(self, lifetime=2.0):
        target = [np.random.uniform(0.3, 0.4),np.random.uniform(-0.3, 0.3), np.random.uniform(0.5, 0.8)] 
        # theta = np.random.uniform(0, 2*np.pi)
        # phi = np.random.uniform(0, np.pi)
        # phi = np.pi
        theta = 0
        phi = 0
        target_radius = 0.12
        target_point =  [target[0] + (target_radius * np.cos(theta) * np.sin(phi)),
                                target[1] + (target_radius * np.sin(theta) * np.sin(phi)), 
                                target[2] + (target_radius * np.cos(phi))]
        target_point2 = [target[0] + ((0.1654 + target_radius) * np.cos(theta) * np.sin(phi)),
                                target[1] + ((0.1654 + target_radius) * np.sin(theta) * np.sin(phi)), 
                                target[2] + ((0.1654 + target_radius) * np.cos(phi))]
        p.removeAllUserDebugItems()
        p.addUserDebugLine(target_point, target_point2, lineColorRGB=[1.0, 0.0, 0.0], lineWidth=10.0)
        p.addUserDebugPoints([target], pointColorsRGB=[[0.0, 0.0, 1.0]], pointSize=20)
        # p.addUserDebugPoints([target_point], pointColorsRGB=[[0.0, 0.0, 1.0]], pointSize=0.01, lifeTime=lifetime)
        # p.addUserDebugPoints([target_point2], pointColorsRGB=[[0.0, 0.0, 1.0]], pointSize=0.01, lifeTime=lifetime)
        # p.addUserDebugPoints(points, pointColorsRGB=colours, pointSize=size, lifeTime=lifetime)

    def get_env_state(self):
        return deepcopy({state:self.__dict__[state] for state in self.states_to_save})
