#!/usr/bin/env python

import pybullet as pb
import time
import numpy as np
import sys
import torch

import sys
sys.path.append('/home/kom018/behaviour_rl')

from spotmicro.OpenLoopSM.SpotOL import BezierStepper
from spotmicro.GymEnvs.spot_bezier_env import spotBezierEnv
from assets.env_base_pb import EnvBasePB
from assets.env_titan_pb_2 import Env as RobotEnv
from assets.env_multi_robot_pb import Env as MA_RobotEnv
import default_arguments

import torch
import os
import numpy as np
import glob
import time
from pathlib import Path
import default_arguments
from utils.plotter import Plotter
import pandas as pd
import copy

import run_test

home = str(Path.home())

start_time=time.time()







class GUI:
    def __init__(self, quadruped):

        time.sleep(0.5)
        actions = pd.read_csv("/home/kom018/behaviour_rl/action_test.csv")
        # print("titan_actions",actions.linear)
        self.linear_vel=0
        self.angular_vel=1
        self.angular_vel_above_half=0
        action_multiplier=1


        self.cyaw = 0
        self.cpitch = -7
        self.cdist = 0.66
        # print("check");exit()
        self.xId = pb.addUserDebugParameter("x", -0.10, 0.10, 0.)
        self.yId = pb.addUserDebugParameter("y", -0.10, 0.10, 0.)
        self.zId = pb.addUserDebugParameter("z", -0.10, 0.10, 0.)
        self.rollId = pb.addUserDebugParameter("roll", -np.pi / 4, np.pi / 4,
                                               0.)
        self.pitchId = pb.addUserDebugParameter("pitch", -np.pi / 4, np.pi / 4,
                                                0.)
        self.yawId = pb.addUserDebugParameter("yaw", -np.pi / 4, np.pi / 4, 0.)
        self.StepLengthID = pb.addUserDebugParameter("Step Length", -0.1, 0.1,
                                                     0.032)
        self.YawRateId = pb.addUserDebugParameter("Yaw Rate", -1.0, 1.0, self.angular_vel*action_multiplier)
        self.LateralFractionId = pb.addUserDebugParameter(
            "Lateral Fraction", -np.pi / 2.0, np.pi / 2.0, self.angular_vel_above_half*action_multiplier)
        self.StepVelocityId = pb.addUserDebugParameter("Step Velocity", 0.0001,
                                                       3., self.linear_vel*action_multiplier)
        # self.StepVelocityId = pb.addUserDebugParameter("Step Velocity", 0.001,
        #                                                3., 0.1)
        self.ClearanceHeightId = pb.addUserDebugParameter(
            "Clearance Height", 0.0, 0.1, 0.03)
        self.PenetrationDepthId = pb.addUserDebugParameter(
            "Penetration Depth", 0.0, 0.05, 0.005)

        self.quadruped = quadruped
        
        # args = default_arguments.get_defaults() 

        # run_test.run(args)

        # if __name__== "__main__":
        # args = default_arguments.get_defaults() 
        # run_test.run(args)
        # print("oajsodhsaiufb iasdbskfbksdjbfjksd bfkjsdb kjsdbfksdbfsdkfbkjsd")
        
        # args = default_arguments.get_defaults() 
        
        # Env, args = default_arguments.get_env(args)   
        # # argus.render = True
        # # #args.render = False
        # # argus.record_sim = False
        # args.render=True
        # args.record_sim=False
        # # env=MA_RobotEnv(RobotEnv)

        # self.observations=Env.reset()
        # self.im_ocupancy=Env.get_image()

        # mu_net = torch.load("/home/kom018/behaviour_rl/Saved_models/JIT_models/mu_net.jit")
        # z_net = torch.load("/home/kom018/behaviour_rl/Saved_models/JIT_models/z_net.jit")


        


        # a=torch.as_tensor(np.array(self.observations), dtype=torch.float32).unsqueeze(dim=0)
        # b=z_net(torch.as_tensor(self.im_ocupancy, dtype=torch.float32))

        # # print(a.shape)
        # # print(b.shape)
        # concatenate_part=torch.concat((a,b),-1)


        # actions = mu_net(concatenate_part)

        # print("Titan_actions",actions)

    def UserInput(self):

        quadruped_pos, _ = pb.getBasePositionAndOrientation(self.quadruped)
        pb.resetDebugVisualizerCamera(cameraDistance=self.cdist,
                                      cameraYaw=self.cyaw,
                                      cameraPitch=self.cpitch,
                                      cameraTargetPosition=quadruped_pos)
        keys = pb.getKeyboardEvents()
        # Keys to change camera
        if keys.get(100):  # D
            self.cyaw += 1
        if keys.get(97):  # A
            self.cyaw -= 1
        if keys.get(99):  # C
            self.cpitch += 1
        if keys.get(102):  # F
            self.cpitch -= 1
        if keys.get(122):  # Z
            self.cdist += .01
        if keys.get(120):  # X
            self.cdist -= .01
        if keys.get(27):  # ESC
            pb.disconnect()
            sys.exit()

        # Read Robot Transform from GUI
        pos = np.array([
            pb.readUserDebugParameter(self.xId),
            pb.readUserDebugParameter(self.yId),
            pb.readUserDebugParameter(self.zId)
        ])
        orn = np.array([
            pb.readUserDebugParameter(self.rollId),
            pb.readUserDebugParameter(self.pitchId),
            pb.readUserDebugParameter(self.yawId)
        ])
        StepLength = pb.readUserDebugParameter(self.StepLengthID)
        YawRate = pb.readUserDebugParameter(self.YawRateId)
        LateralFraction = pb.readUserDebugParameter(self.LateralFractionId)
        StepVelocity = pb.readUserDebugParameter(self.StepVelocityId)
        ClearanceHeight = pb.readUserDebugParameter(self.ClearanceHeightId)
        PenetrationDepth = pb.readUserDebugParameter(self.PenetrationDepthId)

        # args = default_arguments.get_defaults() 
        # run(args)

        # args = default_arguments.get_defaults() 

        # run_test.run(args)

        return pos, orn, StepLength, LateralFraction, YawRate, StepVelocity, ClearanceHeight, PenetrationDepth
