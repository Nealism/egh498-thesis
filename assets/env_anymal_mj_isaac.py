import numpy as np
import torch
import os
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation
import mujoco_viewer
from pyquaternion import Quaternion
import glfw
from pathlib import Path

from .env_base_mj import EnvBaseMJ
from .env_anymal_mj import Env

BEH_TO_ISA = True
ISA_TO_BEH = False

class Env(Env):
    # Timestep for mujoco is set in the .xml, and shows up under self.model.opt.timestep
    # Default is 0.002, changing this might affect the contact model. 
    simStep = 1/500
    timeStep = 1/100

    rank = comm.Get_rank()
    Kp = 400
    initial_Kp = Kp

    def __init__(self, PATH=None, args=None, writer=None):
        """
        Defines a few other things required when loading/using an isaac policy as the llp
        """

        super().__init__(PATH=PATH, args=args, writer=writer)

        self.is_ob_size = 48  # isaac obs. vector size
        self.isaac_motor_names = self.correct_joint_order(self.motor_names, BEH_TO_ISA) # gives isaac ordering of joints
        self.isa_observation_space = spaces.Box(-10000*np.ones(self.is_ob_size), 10000*np.ones(self.is_ob_size), dtype=np.float32)

        # default initial joint positions used in isaac llp 
        self.isaac_default_joints = { 
            "LF_HAA": 0.0,
            "LH_HAA": 0.0,
            "RF_HAA": -0.0,
            "RH_HAA": -0.0,

            "LF_HFE": 0.4,
            "LH_HFE": -0.4,
            "RF_HFE": 0.4,
            "RH_HFE": -0.4,

            "LF_KFE": -0.8,
            "LH_KFE": 0.8,
            "RF_KFE": -0.8,
            "RH_KFE": 0.8,
        }

        #maps to default_dof_pos from isaac repo
        self.isaac_initial_joints = [self.isaac_default_joints[k] for k in self.isaac_motor_names]

        # scalers (for low-level policy obs. vector)
        self.lin_vel_scale = 2.0
        self.ang_vel_scale = 0.25
        self.dof_pos_scale = 1.0
        self.dof_vel_scale = 0.05
        self.commands_scale = torch.tensor([self.lin_vel_scale, self.lin_vel_scale, self.ang_vel_scale])
        
    def reset(self, test=False, model_path=None, restore_state=None):
        """
        Customised reset method for env_anymal_mj_isaac environment

        Changes:
            self.actions (third last line) initialised here (because state now depends on it)
            state (second last line) changed to llp-conformant format
        """

        if self.steps > 0:
            for key in self.reward_dict:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        if self.episodes > -1:
            self.success.append(self.get_success())
            target = None
            if self.args.tree_type:
                self.save_tree(best=self.total_return > self.best_return, test=test)
            self.record_sim_state(best=self.total_return > self.best_return, test=test, additional_arguments=target)
            if self.total_return > self.best_return:
                self.best_return = self.total_return
        self.total_return = 0
        self.paused = True

        if self.args.cur and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
                self.args.cur = False
            self.success = deque([0.0], maxlen=5)
        
        if model_path is not None:
            self.model_path = model_path 
        if self.args.tree_type or model_path is not None:
            self.load_robot()

        mujoco.mj_resetData(self.model, self.data)

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            # Rotate the base of the robot to simulate being on the back of a titan
            rot_range = 0.2
            # rot_range = 0.0
            self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), 0], degrees=False)
            self.orn = self.rot.as_quat()
            self.pos = [0,0,self.initial_z]
            self.set_position(pos=self.pos, orn=self.orn, joints=self.initial_joints)

        self.steps = 0
        self.episodes += 1

        # Step the simulation once to get the initial state
        mujoco.mj_forward(self.model, self.data)
        self.get_observation()

        # Maybe randomise which legs swing first?
        self.current_swing = "right"
        self.expert_target = self.right_swing if self.current_swing == "right" else self.left_swing
        self.get_trajectory(self.expert_target)

        self.prev_actions = self.joints

        #initialise actions vector
        self.actions = [0]*(self.ac_size)
        state = self.formulate_isaac_obs() # low level policy requires slightly different obs. vector
        return state

    def step(self, actions=None, replay_state=None, additional_stuff=None):
        """
        Customised step method for env_anymal_mj_isaac environment 

        Changes:
            self.actions (first line) changed to the correct llp order
            state (second last line) changed to llp-conformant format
        """
        # llp returns actions in isa order - convert self.actions back to beh order for consistency
        self.actions = self.correct_joint_order(actions, ISA_TO_BEH)
        if self.paused:
            self.target_vx = 0.0
            expert = self.initial_joints    
        else:
            self.target_vx = 1.0
            if self.steps % self.traj_size == 0:
                self.current_swing = "right" if self.current_swing == "left" else "left"
                self.expert_target = self.right_swing if self.current_swing == "right" else self.left_swing
                self.get_trajectory(self.expert_target)
            expert = self.expert_traj[self.traj_i]
            # expert = self.expert_target
            if self.traj_i < self.traj_size - 1:
                self.traj_i += 1
        
        # This might do something weird with mujoco contacts, and other things in the sim.
        for _ in range(int(np.rint(self.timeStep/self.simStep))):
            # self.set_position(pos=[0,0,0.5], orn=[0,0,0,1])

            if replay_state is not None:
                self.set_position(pos=replay_state[0], orn=replay_state[1])
            else:            
                if self.args.cur:
                    if self.args.just_expert:
                        self.data.ctrl[:self.ac_size] = (self.Kp / self.initial_Kp)*np.array(expert)
                    else:
                        self.data.ctrl[:self.ac_size] = self.action_multiplier*np.array(self.actions) + (self.Kp / self.initial_Kp) * np.array(expert)
                else:
                    self.data.ctrl[:self.ac_size] = self.action_multiplier*np.array(self.actions)
                            
            mujoco.mj_step(self.model, self.data)
        
        if self.render:
            self.viewer.render()

        self.get_observation()

        self.save_sim_state()
        reward, done = self.get_reward()
        self.prev_actions = self.actions
        self.total_return += reward
        self.steps += 1

        state = self.formulate_isaac_obs() # low-level policy requires slightly different obs. vector
        return np.array(state), reward, done, None

    def formulate_isaac_obs(self):
        """
        **Isaac low-levl policy takes 48-d obs. vector, whereas main net takes 51-d obs. vector** 

        Constructs and returns 48-d obs. vector for low-level policy
        """
        # NOTE: converted all to torch tensors because of need to vector multiply (is this slow?)
        # NOTE: hardcoded commands for now whilst testing isaac pol directly
        test_commands = [
            torch.tensor([0.1, 0.1, 0.1]),
            torch.tensor([-1.0, 0, 0]),
            torch.tensor([0, 1.0, 0]),
            torch.tensor([0, 0, 1.0]),
            torch.tensor([ 0.5153, -0.5045, -1.0192]) 
        ]

        gravity_vec = torch.tensor([[0, 0, -1.0]], dtype=torch.float64)
        dof_pos_default = torch.tensor(self.isaac_initial_joints) # use either: self.isaac_initial_joints OR self.initial_joints
        quat = torch.tensor([self.orn], dtype=torch.float64)
        clip_actions = 0.1

        #low-level policy obs. components (in order)
        lin_vel = torch.tensor(self.imu[5:8]) 
        ang_vel = torch.tensor(self.imu[2:5]) 
        proj_grav = self.quat_rotate_inverse(quat, gravity_vec)[0]
        commands = test_commands[1] # output of main net (Vx, Vy, Vz) - requested
        dof_pos_diff = torch.tensor(self.correct_joint_order(self.joints, BEH_TO_ISA)) - dof_pos_default 
        dof_vel = torch.tensor(self.correct_joint_order(self.joint_vel, BEH_TO_ISA))
        # self.actions = torch.clip(self.actions, -clip_actions, clip_actions)
        last_output = torch.tensor(self.correct_joint_order(self.actions, BEH_TO_ISA)) # last output of llp
        state = torch.cat((lin_vel*self.lin_vel_scale, ang_vel*self.ang_vel_scale, proj_grav*self.dof_vel_scale, commands*self.commands_scale, 
                               dof_pos_diff*self.dof_pos_scale, dof_vel*self.dof_vel_scale, last_output*self.dof_pos_scale), dim=-1)
        return state

    def correct_joint_order(self, joints, beh_to_isa):
        """
        **Joints for this repo are listed in different order to isaac repo's joints**

        Params:
            beh_to_isa : true if converting from beh_rl -> isaac, false if converting from isaac -> beh_rl

        Returns joints in correct order depending on policy

        """
        # hash table of form: mapping[beh_repo_index] = isaac_repo_index (or vice versa)
        mapping = [0, 1, 2, 6, 7, 8, 3, 4, 5, 9, 10, 11]
        new_joints = [None]*self.ac_size
        for beh_index, isaac_index in enumerate(mapping):
            if beh_to_isa:
                new_joints[isaac_index] = joints[beh_index]
            else:
                new_joints[beh_index] = joints[isaac_index]
        return new_joints
    
    def quat_rotate_inverse(self, q, v):
        """
        Returns vector v rotated using the given quaternion q.

        (Used to compute the projected gravity vector) 
        """
        shape = q.shape
        q_w = q[:, -1]
        q_vec = q[:, :3]
        a = v * (2.0 * q_w ** 2 - 1.0).unsqueeze(-1)
        b = torch.cross(q_vec, v, dim=-1) * q_w.unsqueeze(-1) * 2.0
        c = q_vec * \
        torch.bmm(q_vec.view(shape[0], 1, 3), v.view(
            shape[0], 3, 1)).squeeze(-1) * 2.0
        return a - b + c 


