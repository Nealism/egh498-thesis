import numpy as np
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation
import mujoco_viewer

from .env_base_mj import EnvBaseMJ

class Env(EnvBaseMJ):
    # Timestep for mujoco is set in the .xml, and shows up under self.model.opt.timestep
    # Default is 0.002, changing this might affect the contact model.
    simStep = 1/500
    timeStep = 1/100
    rank = comm.Get_rank()
    Kp = 400
    initial_Kp = Kp
    def __init__(self, PATH=None, args=None, writer=None):

        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True 

        super().__init__(PATH)

        # Name of the base link in the xml, for setting the robot position on reset
        self.base_link = "base"
        self.model_path = "assets/urdfs/titan_meshes/scene.xml"
        self.robot_name = "dynamic_titan"
        self.mesh_dir = "assets/urdfs/titan_meshes"
        self.action_multiplier = 200.0
        
        if self.args.tree_type:
            self.set_up_xmls()
        
        self.viewer = None
        self.load_robot()
        
        self.ob_size = 11
        self.ac_size = 2

        self.motor_names = [side + "_" + str(n + 1) + "_wheel_joint" for side in ["left", "right"] for n in range(11)]
    
        self.joints = [0.0]*len(self.motor_names)
        self.joint_vel = self.joints
        
        self.target_vx = 1.0
        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        self.episodes = -1
        self.success = deque([0.0], maxlen=5)
        self.target_radius = 0.12
        self.sim_data = []
        self.best_return = 0

        # States that we want to restore, for resuming training after running a test
        self.states_to_restore = ["pos", "orn", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

    def load_robot(self):
      
        if not self.args.replay and self.args.tree_type:
            if self.args.tree_type == "grass":
                self.generate_tree(radius=0.02, height=0.4, damping=1, stiffness=2, pos=[0,0,0],rot=[1,0,0,0], num=300, segs_per_branch=4, spread=[[0.5, 4.0],[-2, 1]], z_height=-0.05)
            elif self.args.tree_type == "tree":
                self.generate_tree(spread=[[0.5, 4.0],[-0.5, 0.5]])
      
        self.model = mujoco.MjModel.from_xml_path(self.model_path)
        self.data = mujoco.MjData(self.model)

        # Mujoco_viewer doesn't work on the hpc, shouldn't render there anyway
        if not self.args.training_on_hpc:
            if isinstance(self.viewer, mujoco_viewer.MujocoViewer):
                # Replace model and data of an existing viewer
                self.viewer.model = self.model
                self.viewer.data = self.data
            elif self.render:
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data)
            else:
                # Offscreen might help getting images?
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data, 'offscreen')
        else:
            print("Can't view mujoco on the HPC.")

    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        return {"Kp": self.Kp, "Success": self.success, "Cur": self.args.cur}

    def get_success(self):
        return True

    def check_for_success(self):
        return len(self.success) == 5 and (np.array(self.success) == True).all()

    def reset(self, test=False, model_path=None, restore_state=None):

        if self.episodes > -1:
            self.success.append(self.get_success())
            target = None
            if self.args.tree_type:
                self.save_tree(best=self.total_return > self.best_return, test=test)
            self.record_sim_state(best=self.total_return > self.best_return, test=test, additional_arguments=target)
            if self.total_return > self.best_return:
                self.best_return = self.total_return
        self.total_return = 0

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

        # Rotate the base of the robot 
        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            rot_range = 0.0
            self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), 0.0], degrees=False)
            orn = self.rot.as_quat()
            pos = [0,0, 0.1]
            self.set_position(pos=pos, orn=orn)

        self.steps = 0
        self.episodes += 1

        # Step the simulation once to get the initial state
        mujoco.mj_forward(self.model, self.data)
        
        self.get_observation()
        state = self.imu 
        return state

    def step(self, actions=None, replay_state=None, additional_stuff=None):
        actions = [1,1]
        if actions is not None:
            self.actions = list(actions)
        else:
            self.actions = [0]*(self.ac_size)

        for _ in range(int(np.rint(self.timeStep/self.simStep))):
            if replay_state is not None:
                self.set_position(pos=replay_state[0], orn=replay_state[1])
            else:            
                for n,m in enumerate(self.motor_names):
                    if "left" in m:
                        self.data.ctrl[n] = self.action_multiplier*np.array(self.actions[0])
                    else:
                        self.data.ctrl[n] = self.action_multiplier*np.array(self.actions[1])
            mujoco.mj_step(self.model, self.data)
        
        if self.render:
            self.viewer.render()

        self.get_observation()
        self.save_sim_state()
        reward, done = self.get_reward()
        self.prev_actions = self.actions
        self.total_return += reward
        self.steps += 1

        state = self.imu 
        return np.array(state), reward, done, None
    
    def get_reward(self):
        done = False
        reward = 1.5*np.exp(-2.5*max(0, self.target_vx - self.data.joint("free").qvel[0])**2)
        return reward, done

    def close(self):
        self.viewer.close()
    
    def get_observation(self):
        # Keep an eye on these to make sure they are getting what you think
        # free_joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "free")
        # self.pos = self.data.qpos[free_joint_id:free_joint_id+3].copy()
        # orn = self.data.qpos[free_joint_id+3:free_joint_id+7]
        # self.orn = [orn[1],orn[2],orn[3],orn[0]]

        self.pos = self.data.body(self.base_link).xpos.copy()
        orn = self.data.body(self.base_link).xquat.copy()
        self.orn = [orn[1],orn[2],orn[3],orn[0]]


        # There is something wrong here, though this is what works with the franka
        # rot = Rotation.from_matrix(np.array(self.data.body(self.base_link).ximat).reshape(3,3))
        rot = Rotation(self.orn)
        self.roll, self.pitch, self.yaw = rot.as_euler('xyz', degrees=False)
        self.imu = [self.roll, self.pitch] + list(self.data.sensordata) 