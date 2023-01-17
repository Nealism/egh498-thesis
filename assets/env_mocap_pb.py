import numpy as np
# Why this vs this?
import pybullet as p
import time
from assets.env_base_pb import EnvBasePB
from mpi4py import MPI
import torch
comm = MPI.COMM_WORLD

class EnvExp(EnvBasePB):
    ROBOT_HEIGHT = 1.2
    rank = comm.Get_rank()
    simStep = 1/120
    timeStep = 1/120
    ac_size = 21
    ob_size = 57
    def __init__(self, PATH=None, args=None, render=False, with_feet=True, master=False):

        self.args = args
        self.render = render and self.rank == 0
        self.PATH = PATH
        self.with_feet = with_feet
        self.master = master 

        super().__init__(PATH)

        if self.master:
            self.load_robot()

        self.load_mocap()

    def load_mocap(self):
        subject = '02'
        file_name = '_01'
        self.samples = np.load('resources/' + subject + file_name + '_samples.npy')
        print('loaded samples from resources' + subject + file_name + '_samples.npy with shape: ', self.samples.shape)
        self.sample_size = self.samples.shape[0]

    def reset(self, right_swing=True):
        if right_swing:
            self.sample_pointer = 33
        else:
            self.sample_pointer = 100
        # self.sample_pointer = 0
    
        self.initial_xyz = self.samples[self.sample_pointer,:][:3]
        self.saved_xyz = np.zeros(3)


    def step_expert(self, obs):
        return self.policy(obs, stochastic=False)

    def get_sample(self, reset=False, right_swing=True):
        if reset:
            if right_swing:
                self.sample_pointer = 20
            else:
                self.sample_pointer = 87
        temp = self.samples[self.sample_pointer,:]
        exp_body_xyz, exp_joints, exp_joint_vel = temp[:3], temp[6:12+6], temp[12+6:]
        exp_body_xyz = exp_body_xyz + self.saved_xyz 

        # exp_body_xyz = [0,0,1.5]
        # exp_joints = list(exp_joints) + [0.0]*3 + [ 0.5, exp_joints[2] - 0.5, -1.5707 - exp_joints[3]] + [-0.5, exp_joints[8] + 0.5, -1.5707 - exp_joints[9]] 
        # self.motor_names += ["right_hip_x"] #1
        # self.motor_names += ["right_hip_z"] #0
        # self.motor_names += ["right_hip_y"] #2
        # self.motor_names += ["right_knee"]  #3
        # self.motor_names += ["right_ankle_y"] #5
        # self.motor_names += ["right_ankle_x"] #4
        # self.motor_names += ["left_hip_x"] #7
        # self.motor_names += ["left_hip_z"] #6
        # self.motor_names += ["left_hip_y"] #8
        # self.motor_names += ["left_knee"] #9
        # self.motor_names += ["left_ankle_y"] #11
        # self.motor_names += ["left_ankle_x"] #10
        # Remapping from my old urdf file that the mocap data was generated from
        joint_indicies = np.array([1,0,2,3,5,4,7,6,8,9,11,10])
        
        exp_joints = [0.0]*3 + list(np.array(exp_joints)[joint_indicies]) + [ 0.5, - 0.5, -1.5707] + [-0.5,  0.5, -1.5707] 
        exp_joint_vel = np.zeros(self.ac_size)
        # self.exp_body_rot =  p.getQuaternionFromEuler([temp[3], temp[4], temp[5]+np.random.uniform(-self.max_yaw, self.max_yaw)])
        exp_body_rot =  p.getQuaternionFromEuler([temp[3], temp[4], temp[5]])

        self.sample_pointer += 1 
        if self.sample_pointer >= self.sample_size:
            self.saved_xyz = exp_body_xyz.copy() 
            self.sample_pointer = 0

        return exp_body_xyz, exp_body_rot, exp_joints, exp_joint_vel

    def step(self):
        self.exp_body_xyz, self.exp_body_rot, self.exp_joints, self.exp_joint_vel = self.get_sample()

        self.set_position([self.exp_body_xyz[0], self.exp_body_xyz[1], self.exp_body_xyz[2] + self.ROBOT_HEIGHT], self.exp_body_rot, self.exp_joints, joint_vel=self.exp_joint_vel, robot_id=self.Id)
        
        for _ in range(int(self.timeStep/self.simStep)):
            p.stepSimulation()

        if self.args.render:
            # print(self.sample_pointer)
            time.sleep(self.args.sleep)