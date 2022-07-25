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
from assets.env_mocap_pb import EnvExp

class Env(EnvBasePB):

    def __init__(self, PATH=None, args=None, writer=None, frameless=True, with_feet=True):

        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True 
        self.frameless = frameless
        self.with_feet = with_feet

        self.simStep = 1/240
        self.timeStep = 1/120
        self.ac_size = 21
        self.ob_size = 57
        self.Kp = 400
        self.initial_Kp = self.Kp
        self.ROBOT_HEIGHT = 1.2

        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        
        self.steps = -1
        
        self.env_exp = EnvExp(args)
        self.target_speed = 1.0
        self.target_yaw = 0.0
        self.initial_joints = [0.0] * 15 + [ 0.5, -0.5, -1.5707] + [-0.5, 0.5, -1.5707]
        self.cur_success = deque([0.0], maxlen=5)

        if self.args.add_terrain:
            self.terrain_difficulty = self.args.initial_terrain_difficulty
        
        self.max_disturbance = 250
        self.final_disturbance = 1600

        self.states = ["joints", "pos", "orn", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]
        
    def check_for_success(self):
        return len(self.cur_success) == 5 and (np.array(self.cur_success) == True).all()

    def get_success(self):
        return self.body_xyz[0] > 15

    def reset(self, terrain=None):
        self.load_robot()

        # Wait until both feet are on the ground before starting walking
        self.paused = True

        if self.steps > -1:
            self.ep_success = self.get_success()
            self.cur_success.append(self.ep_success)  

        if self.rank == 0 and self.args.record_sim and self.steps > -1:
            self.record_sim_state(best=self.check_for_success())
        
        # Three curriculum stages, can swap the order of the first two
        # Stage 1
        if self.args.terrain_first:
            if self.args.add_terrain and self.terrain_difficulty < self.args.final_terrain_difficulty and self.check_for_success():
                self.terrain_difficulty += 0.05
                self.cur_success = deque([0.0], maxlen=5)

        if self.args.cur and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
            self.cur_success = deque([0.0], maxlen=5)

        # Stage 2
        if not self.args.terrain_first:
            if self.args.add_terrain and self.terrain_difficulty < self.args.final_terrain_difficulty and self.check_for_success():
                self.terrain_difficulty += 0.05
                self.cur_success = deque([0.0], maxlen=5)

        # Stage 3
        if self.args.apply_disturbances and self.max_disturbance < self.final_disturbance and self.check_for_success():
            self.max_disturbance += 250
            self.cur_success = deque([0.0], maxlen=5)

        if terrain is not None:
            self.load_terrain(terrain)
        elif self.args.add_terrain:
            template = (np.random.random([int(self.terrain_size[2]/4),int(self.terrain_size[2]/4)]) + 1.0) * self.terrain_difficulty 
            # Make the edges smooth
            template[:, 0] = 0.0
            template[:, -1] = 0.0
            template[0, :] = 0.0
            template[-1, :] = 0.0
            terrain = cv2.resize(template, dsize=(self.terrain_size[1], self.terrain_size[2])).reshape(self.terrain_size)
            self.load_terrain(terrain)

        self.steps += 1
        self.ep_steps = 0

        self.ob_dict = {'prev_right_foot_left_ground': False,'prev_left_foot_left_ground': False,'left_foot_left_ground': False,'right_foot_left_ground': False}
        
        self.ob_dict['prev_right_foot'] = self.ob_dict['right_foot'] = False
        self.ob_dict['prev_left_foot'] = self.ob_dict['left_foot'] = False
        
        self.initial_swing_foot = np.random.randint(2)
        if self.initial_swing_foot:
            self.ob_dict['swing_foot'] = True
        else: 
            self.ob_dict['swing_foot'] = False
        self.ob_dict['cur_swing_foot'] = self.ob_dict['swing_foot']

        self.ob_dict['right_foot_swing'] = False
        self.ob_dict['left_foot_swing'] = False
        self.first_step = True
        self.prev_step_count = self.step_count = 0
        self.z_offset = 0

        rand_scale = self.max_disturbance / self.final_disturbance
        pos = [0,0,1.5 + rand_scale * np.random.uniform(-0.2, 0.2)]
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

        self.cur_time = 0
        # Time to take single step
        self.time_of_step = int(135/2)
        self.step_count = 0

        self.internal_state = "paused"
        self.swing_right_first = np.random.choice([True, False])
        self.env_exp.reset(right_swing=self.swing_right_first)
        # self.prev_swing_foot = "right_foot" if s

        # Experimental for symmetry:
        self.all_actions = np.zeros([self.env_exp.sample_size, 6])
        self.indicies = [5,6,7,11,12,13]

        self.state = self.joints + self.joint_vel + self.body + self.contacts 
        return np.array(self.state)

    def step(self, actions):
        # Wait until both feet in contact with the ground before progressing the expert
        if self.paused:
            self.exp_body_xyz = [0,0,self.ROBOT_HEIGHT+self.z_offset]
            self.exp_body_rot = [0,0,0,1]
            self.exp_joints, self.exp_joint_vel = self.initial_joints, [0.0]*self.ac_size
            self.target_speed = 0.0
            if self.ob_dict["right_foot"] and self.ob_dict["left_foot"]:
                self.paused = False
                self.ob_dict['right_foot_swing'] = self.swing_right_first
                self.ob_dict['left_foot_swing'] = not self.ob_dict['right_foot_swing']
                if self.ob_dict['right_foot_swing']:
                    self.prev_swing_foot = "right_foot"
                else:
                    self.prev_swing_foot = "left_foot"
                self.reset_sample = False
                self.exp_body_xyz, self.exp_body_rot, self.exp_joints, self.exp_joint_vel = self.env_exp.get_sample()
                self.target_speed = 1.0
        else:
            self.exp_body_xyz, self.exp_body_rot, self.exp_joints, self.exp_joint_vel = self.env_exp.get_sample(reset=self.reset_sample,right_swing = self.ob_dict['right_foot_swing'])
            self.reset_sample = False

        if self.args.apply_disturbances and np.random.random() < 0.005:
            # print("adding disturbance")
            self.add_disturbance(max_dist=self.max_disturbance)

        forces = 30.0*np.array(actions)
        self.actions = actions
        
        if self.args.cur:
            if self.Kp > 0:
                exp_forces = self.apply_forces()
                forces = forces + (self.Kp/self.initial_Kp) * exp_forces
        
        # Visualise expert (mocap) 
        # self.set_position([self.exp_body_xyz[0], self.exp_body_xyz[1], self.exp_body_xyz[2]], self.exp_body_rot, self.exp_joints, joint_vel=self.exp_joint_vel, robot_id=self.Id)
        # p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.POSITION_CONTROL, targetPositions=self.exp_joints)
        # self.set_position([0,0,1.25], [0,0,0,1])
        
        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.TORQUE_CONTROL, forces=forces)

        for _ in range(int(self.timeStep/self.simStep)):
            p.stepSimulation()

        if self.args.render:
            time.sleep(0.01)

        self.get_observation()
        self.save_sim_state()
        reward, done = self.get_reward()
        self.ep_steps += 1

        self.state = self.joints + self.joint_vel + self.body + self.contacts 
        return self.state, reward, done, None

    def get_reward(self):
        
        goal = 1.5*np.exp(-2.5*max(0, self.target_speed - self.vx)**2)

        pos = 0.65*np.exp(-2.0*np.sum((np.array(self.exp_joints) - np.array(self.joints))**2))            
        vel = 0.05*np.exp(-0.1*np.sum((np.zeros(self.ac_size) - np.array(self.joint_vel))**2))
        com = 0.2*np.exp(-10*np.sum((np.array([self.roll, self.pitch, self.body_xyz[2], self.yaw]) - np.array([0.0, 0.0, self.ROBOT_HEIGHT+self.z_offset, self.target_yaw]))**2))
        
        neg = 0
        neg -= 0.2*sum([self.ob_dict[w] for w in self.shin_dict])
        neg -= 0.2*sum([self.ob_dict[w] for w in self.arm_dict])

        # If taken a new step, make step should have taken roughly the same time..
        if self.step_count != self.prev_step_count and self.step_count > 2:
            neg -= min(self.touchdown_pen/5, 5.0)  
        self.prev_step_count = self.step_count

        if not self.paused and self.steps > 100:
            if (self.ob_dict['right_foot_left_ground'] and self.ob_dict['left_foot_left_ground'] ):
                neg -= 1.0

        # Symmetry penalty, just on y joints (hip, knee, ankle), based on expert pointer
        sym = 0.0 if self.paused else -0.03*np.sum((self.all_actions[(self.env_exp.sample_pointer + int(self.env_exp.sample_size/2)) % self.env_exp.sample_size, :] - np.array(self.actions)[self.indicies])**2)
        self.all_actions[self.env_exp.sample_pointer, :] = np.array(self.actions)[self.indicies] 

        reward = goal + pos + vel + com  + neg + sym

        done = False
        
        if abs(self.body_xyz[1]) > 1.5:
            done = True

        if self.body_xyz[2] < 0.9 or np.sqrt(np.sum(np.array(self.body_vxyz)**2)) > 20:
            done = True
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

        self.ob_dict['prev_right_foot']  = self.ob_dict['right_foot'] 
        self.ob_dict['prev_right_left']  = self.ob_dict['left_foot'] 

        self.ob_dict['right_foot'] = len(p.getContactPoints(self.Id, -1, self.feet_dict['right_foot'], -1))>0
        self.ob_dict['left_foot'] = len(p.getContactPoints(self.Id, -1, self.feet_dict['left_foot'], -1))>0

        for w in self.shin_dict:
            self.ob_dict[w] = len(p.getContactPoints(self.Id, -1, self.shin_dict[w], -1))>0

        for w in self.arm_dict:
            self.ob_dict[w] = len(p.getContactPoints(self.Id, -1, self.arm_dict[w], -1))>0

        if not self.paused:
            self.cur_time += 1
            if (self.ob_dict['right_foot_swing'] and self.ob_dict['prev_right_foot_left_ground'] and self.ob_dict['right_foot']) \
                or (not self.ob_dict['right_foot_swing'] and self.ob_dict['prev_left_foot_left_ground'] and self.ob_dict['left_foot']):
                if self.ob_dict['right_foot_swing']:
                    self.prev_swing_foot = "right_foot"
                else:
                    self.prev_swing_foot = "left_foot"
                self.ob_dict['right_foot_swing'] = not self.ob_dict['right_foot_swing']
                self.ob_dict['left_foot_swing'] = not self.ob_dict['left_foot_swing']
                self.reset_sample = True
                self.touchdown_pen = abs(self.cur_time - self.time_of_step)
                self.cur_time = 0
                self.step_count += 1
                if self.ob_dict['right_foot_swing']: 
                    self.internal_state = "right_foot_swing"
                elif self.ob_dict['left_foot_swing']: 
                    self.internal_state = "left_foot_swing"

        else:
            self.ob_dict['right_foot_swing'] = False
            self.ob_dict['left_foot_swing'] = False

        # Update feet that have left the ground.
        self.ob_dict['prev_right_foot_left_ground'] = self.ob_dict['right_foot_left_ground']
        self.ob_dict['prev_left_foot_left_ground'] = self.ob_dict['left_foot_left_ground']
        self.ob_dict['right_foot_left_ground'] = not self.ob_dict['right_foot']
        self.ob_dict['left_foot_left_ground'] = not self.ob_dict['left_foot']
        
        self.ob_dict['right_full_foot_on_ground'] = self.ob_dict['right_foot']
        self.ob_dict['left_full_foot_on_ground'] = self.ob_dict['left_foot'] 
        
        self.ob_dict['right_foot_on_ground'] = not self.ob_dict['right_foot_left_ground']
        self.ob_dict['left_foot_on_ground'] = not self.ob_dict['left_foot_left_ground']
        
        right_contacts = [self.ob_dict['right_foot']]
        left_contacts = [self.ob_dict['left_foot']]
        prev_right_contacts = [self.ob_dict['prev_right_foot']]
        prev_left_contacts = [self.ob_dict['prev_left_foot']]

        self.foot_pos = {}
        self.foot_pos['left'] = np.array(p.getLinkState(self.Id, self.feet_dict['left_foot'])[0])
        self.foot_pos['right'] = np.array(p.getLinkState(self.Id, self.feet_dict['right_foot'])[0])

        # From old code, not needed yet
        # self.local_foot_pos = {}
        # self.local_foot_pos['left'] = self.global_to_local_2d(self.body_xyz, self.yaw, self.foot_pos['left'])
        # self.local_foot_pos['right'] = self.global_to_local_2d(self.body_xyz, self.yaw, self.foot_pos['right'])
        # self.x_min = min(self.body_xyz[0], self.foot_pos['left'][0], self.foot_pos['right'][0])
        # self.x_max = max(self.body_xyz[0], self.foot_pos['left'][0], self.foot_pos['right'][0])

        # if self.ob_dict['right_foot_swing']:
        #     swing = 'right'
        #     stance = 'left'
        # else: 
        #     swing = 'left'
        #     stance = 'right'

        # if self.time_of_step == 0:
        #     self.ob_dict['right_foot_swing'] = 0
        #     self.ob_dict['left_foot_swing'] = 0
        # else:
        #     if self.ob_dict['prev_' + swing + '_foot_left_ground'] and not self.ob_dict[swing + '_foot_left_ground']:
        #         self.swing_on_ground_time = self.steps

        self.swing_stance = [self.ob_dict['right_foot_swing'], self.ob_dict['left_foot_swing']]

        self.contacts = right_contacts + left_contacts + prev_right_contacts + prev_left_contacts + self.swing_stance

    def apply_forces(self):
        # z_force = 1.5*(self.Kp * ((self.ROBOT_HEIGHT + self.z_offset)-self.body_xyz[2]) + 0.1*self.Kp * self.vz * -1)
        z_force = 3.0*(self.Kp * ((self.ROBOT_HEIGHT + self.z_offset)-self.body_xyz[2]) + 0.1*self.Kp * self.vz * -1)
        x_force = 1.0*self.Kp * (self.target_speed - self.vx)
        y_force = 1.0*self.Kp*(0 - self.body_xyz[1]) + self.Kp*(0.0 - self.vy)
        p.applyExternalForce(self.Id,-1,[x_force,y_force,z_force],[0,0,0],p.LINK_FRAME)

        yaw_force = 1.0*self.Kp*(self.target_yaw - self.yaw) - 0.1*self.Kp*self.yaw_vel            
        roll_force = -1.0*self.Kp * self.roll        - 0.1*self.Kp*self.roll_vel
        pitch_force = -2.0*self.Kp * self.pitch    - 0.1*self.Kp*self.pitch_vel

        p.applyExternalTorque(self.Id,-1,[roll_force,pitch_force,yaw_force],p.WORLD_FRAME)

        return 240*(np.array(self.exp_joints) - np.array(self.joints)) + 0.5*(np.zeros(self.ac_size) - np.array(self.joint_vel))

    def add_disturbance(self, max_dist=None, forward_only=False):
        if forward_only:
            force_x = np.random.random()*max_dist/2
        else:
            force_x = (np.random.random() - 0.5)*max_dist
        force_y = (np.random.random() - 0.5)*max_dist
        force_z = (np.random.random() - 0.5)*(max_dist/4)
        # print("applying forces", force_x, force_y, force_z)
        p.applyExternalForce(self.Id,-1,[force_x,force_y,force_z],[0,0,0],p.LINK_FRAME)
        force_roll = (np.random.random() - 0.5)*max_dist/2
        force_pitch = (np.random.random() - 0.5)*max_dist/2
        force_yaw = (np.random.random() - 0.5)*(max_dist/2)
        p.applyExternalTorque(self.Id,-1,[force_roll,force_pitch,force_yaw],p.LINK_FRAME)

        forces = 20.0*(max_dist/self.final_disturbance)*np.random.random(self.ac_size)
        p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.TORQUE_CONTROL, forces=forces)

    def get_env_state(self):
        # For some reason getting the entire class dict doesn't work with MPI
        states = ["joints", "pos", "orn", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]
        return deepcopy({state:self.__dict__[state] for state in states})


    def log_stuff(self, logger, writer, iters_so_far):
        self.log_things = {"Kp": self.Kp, "Success": self.cur_success, "Dist": self.max_disturbance, "Diffficulty": self.terrain_difficulty}
        for thing in self.log_things:
            if thing == "Success":
                things = MPI.COMM_WORLD.allgather(np.mean(self.log_things[thing]))
            else:
                things = MPI.COMM_WORLD.allgather(self.log_things[thing])
            logger.log_tabular(thing, np.mean(things))
            if self.rank == 0:
                print(thing, things)
                writer.add_scalar(thing, np.mean(things), iters_so_far)
        
        # Kp = MPI.COMM_WORLD.allgather(self.Kp) 
        # success = MPI.COMM_WORLD.allgather(np.mean(self.cur_success))
        # disturbances = MPI.COMM_WORLD.allgather(self.max_disturbance)
        # terrain_difficulty = MPI.COMM_WORLD.allgather(self.terrain_difficulty)
        # # logger.store(Kp=np.mean(Kp))
        # logger.log_tabular("Kp", np.mean(Kp))
        # logger.log_tabular("Disturb", np.mean(disturbances))
        # logger.log_tabular("Success", np.mean(success))
        # logger.log_tabular("Terrain Difficulty", np.mean(terrain_difficulty))
        # if self.rank == 0:
        #     # Like to print the values from all processes for debugging
        #     print("Gain", Kp)
        #     print("Success", success)
        #     print("Disturb", disturbances)
        #     print("Terrain Difficulty", terrain_difficulty)
        #     writer.add_scalar("Kp", np.mean(Kp), iters_so_far)
        #     writer.add_scalar("Success", np.mean(success), iters_so_far)
        #     writer.add_scalar("Disturb", np.mean(disturbances), iters_so_far)
        #     writer.add_scalar("Difficulty", np.mean(terrain_difficulty), iters_so_far)

            # Might be worth adding these at some stage
            # writer.add_scalar("breakdown/goal", np.mean(self.reward_breakdown['goal']), self.iters_so_far)                
            # writer.add_scalar("breakdown/jump_length", np.mean(self.reward_breakdown['jump_length']), self.iters_so_far)                
            # writer.add_scalar("breakdown/force", np.mean(self.reward_breakdown['force']), self.iters_so_far)                
            # writer.add_scalar("breakdown/end_effector", np.mean(self.reward_breakdown['end_effector']), self.iters_so_far)                
            # writer.add_scalar("breakdown/pos", np.mean(self.reward_breakdown['pos']), self.iters_so_far)                
            # writer.add_scalar("breakdown/vel", np.mean(self.reward_breakdown['vel']), self.iters_so_far)     
            # writer.add_scalar("breakdown/tip", np.mean(self.reward_breakdown['tip']), self.iters_so_far)     
            # writer.add_scalar("breakdown/com", np.mean(self.reward_breakdown['com']), self.iters_so_far)     
            # writer.add_scalar("breakdown/neg", np.mean(self.reward_breakdown['neg']), self.iters_so_far)     
            # writer.add_scalar("breakdown/sym", np.mean(self.reward_breakdown['sym']), self.iters_so_far)     
            # writer.add_scalar("breakdown/act", np.mean(self.reward_breakdown['act']), self.iters_so_far)     
            # writer.add_scalar("breakdown/success", np.mean(self.reward_breakdown['success']), self.iters_so_far)     
            # writer.add_scalar("difficulty", self.min_difficulty, self.iters_so_far)     
            # writer.add_scalar("dist_difficulty", self.dist_difficulty, self.iters_so_far)     
            # writer.add_scalar("height", self.height_coeff, self.iters_so_far)     