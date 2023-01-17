import numpy as np
from mujoco_py import load_model_from_path, MjSim, MjViewer
from gym import spaces
import pickle
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD

from .env_base_mj import EnvBaseMJ

class Env(EnvBaseMJ):
    simStep = 0.002
    timeStep = 1/120
    rank = comm.Get_rank()
    ac_size = 7
    Kp = 400
    initial_Kp = Kp
    def __init__(self, PATH=None, args=None, writer=None):

        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True 

        super().__init__(PATH)

        if self.args.use_ball:
            self.model = load_model_from_path("assets/xmls/franka_panda_ball.xml")  
            self.ob_size = 44
        else:
            self.model = load_model_from_path("assets/xmls/franka_panda_reach.xml")
            self.ob_size = 31

        self.sim = MjSim(self.model)
        if self.render:
            self.viewer = MjViewer(self.sim)

        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        self.episodes = 0
        self.states = ["joints", "pos", "orn", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

        self.steps = 0
        self.success = deque([0.0], maxlen=5)

    @property
    def dt(self):
        return self.sim.model.opt.timestep * self.sim.nsubsteps

    def get_success(self):
        return np.sqrt(np.sum((np.array(self.end_effector) - np.array(self.target_point))**2)) < 0.1

    def reset(self, timeout=False):
        
        if self.steps > 0:
            self.success.append(self.get_success())

        self.sim.reset()        
        self.steps = 0
        # state = self.sim.get_state()
        # state = list(self.sim.data.qpos) + list(self.sim.data.qvel) + list(self.sim.data.actuator_force)
        
        self.record_sim_state(timeout)
        self.episodes += 1

        self.get_target()
        self.get_observation()

        state = self.joints + self.joint_vel + self.joint_force + self.end_effector + self.target
        return state

    def step(self, actions=None, replay_state=None, target=None, target_point=None):

        if replay_state is not None:
            if not self.args.use_ball:
                self.set_target(target, target_point)
            self.set_position(replay_state)
        else:
            if self.render:
                if not self.args.use_ball:
                    self.set_target(self.target, self.target_point)
            self.sim.data.ctrl[:] = actions[:]
        
        if self.render:
            self.viewer.render()
        for _ in range(int(np.rint(self.timeStep/self.simStep))):
            self.sim.step()
        
        # state = list(self.sim.data.qpos) + list(self.sim.data.qvel) + list(self.sim.data.actuator_force) + self.end_effector + self.target
        # state = [state["qpos"] + state["qvel"]]
        # sim_state = self.sim.get_state()
        # self.sim.data.set_joint_qpos('{}:joint'.format(obj_name), object_qpos)
        # self.sim.data.get_site_xpos('robot0:grip').copy()
        # object_qpos = self.sim.data.get_joint_qpos('{}:joint'.format(obj_name))
        # self.body_xyz = self.get_body_xyz()

        # self.sim.data.ncon == 0
        self.get_observation()
        self.save_sim_state()
        reward, done = self.get_reward()
        self.steps += 1
        state = self.joints + self.joint_vel + self.joint_force + self.end_effector + self.target

        return np.array(state), reward, done, None
    
    def get_reward(self):
        done = False
        if self.args.use_ball:
            reward = 1.0
            if self.target[2] < 0.3:
                done = True
        else:
            end_effector_error = np.sqrt(np.sum((np.array(self.end_effector) - np.array(self.target_point))**2))
            reward = np.exp(-5*end_effector_error)
        return reward, done

    
    def get_observation(self):
        self.end_effector = list(self.sim.data.get_site_xpos('end_effector'))
        self.joints = list(self.sim.data.qpos)
        self.joint_vel = list(self.sim.data.qvel)
        self.joint_force = list(self.sim.data.actuator_force)

        if self.args.use_ball:
            self.target = list(self.sim.data.get_joint_qpos("ball")[:3])
        # if self.sim.data.qpos is not None and self.sim.model.joint_names:
        #     print(self.sim.model.joint_names)
            # names = [n for n in self.sim.model.joint_names if n.startswith('robot')]
            # return (
                # np.array([sim.data.get_joint_qpos(name) for name in names]),
            #     np.array([sim.data.get_joint_qvel(name) for name in names]),
            # )

    def get_body_xyz(self):
        mass = np.expand_dims(self.model.body_mass, 1)
        xpos = self.sim.data.xipos
        return (np.sum(mass * xpos, 0) / np.sum(mass))[0]

    def get_target(self):
        if self.args.use_ball:
            dist, angle = np.random.uniform(0.2, 0.4), np.random.uniform(-0.5, 0.5)
            self.target = [dist*np.cos(angle), dist*np.sin(angle), 2.0]
            self.target_point = [0,0,0] 
            self.sim.data.set_joint_qpos("ball", self.target + [1.0, 0, 0, 0])
        else:
            # self.target = [np.random.uniform(0.25, 0.5),np.random.uniform(-0.5, 0.5), np.random.uniform(0.2, 0.8)] 
            self.target = [np.random.uniform(0.3, 0.4),np.random.uniform(-0.3, 0.3), np.random.uniform(0.5, 0.8)] 
            self.target_point = [self.target[0] + np.random.uniform(-0.1, 0.1), self.target[1] + np.random.uniform(-0.1, 0.1), self.target[2] + np.random.uniform(-0.1, 0.1)] 

    def set_target(self, target=[0.5,0,0.5], target_point=[0.1, 0.1, 0.1]):
        self.viewer.add_marker(pos=np.array(target), type=2, label="", size=np.array([0.05, 0.05, 0.05]), rgba=np.array([0.0, 0.0, 1.0, 1.0]))
        self.viewer.add_marker(pos=np.array(target), type=2, label="", size=np.array([0.1, 0.1, 0.1]), rgba=np.array([0.0, 1.0, 0.0, 0.2]))
        self.viewer.add_marker(pos=np.array(target_point), type=2, label="", size=np.array([0.01, 0.01, 0.01]), rgba=np.array([1.0, 0.0, 0.0, 1.0]))

    def record_sim_state(self, timeout):
        if self.args.record_sim and self.rank == 0:
            if self.episodes > 0 and not timeout:
                self.sim_data.append(self.target + self.target_point)
                # pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data","wb"))
                pickle.dump(self.sim_data, open(self.PATH + "sim_data","wb"))
            self.sim_data = []

    def save_sim_state(self):
        if self.args.record_sim and self.rank == 0:  
            # self.sim_data.append(self.self.joints) 
            self.sim_data.append(self.sim.get_state())     

    def log_stuff(self, logger, writer, iters_so_far):
        # Dictionary of things we want logged, printed and added to tensorboard, TODO: move this to env or outside?
        self.log_things = {"Kp": self.Kp, "Success": self.success}
        for thing in self.log_things:
            if thing == "Success":
                things = MPI.COMM_WORLD.allgather(np.mean(self.log_things[thing]))
            else:
                things = MPI.COMM_WORLD.allgather(self.log_things[thing])
            logger.log_tabular(thing, np.mean(things))
            if self.rank == 0:
                print(thing, things)
                writer.add_scalar(thing, np.mean(things), iters_so_far)

    # little gems:
                  
        # TO delete markers
        # del viewer._markers[:]

        # get num contacts
        # self.sim.data.ncon

        # Need this?
        # state = self.sim.get_state()
        # import utils.rotations
        # object_i_pos = self.sim.data.get_site_xpos(self.object_names[i])
        # # rotations
        # object_i_rot = rotations.mat2euler(self.sim.data.get_site_xmat(self.object_names[i]))
        # # velocities
        # object_i_velp = self.sim.data.ge  t_site_xvelp(self.object_names[i]) * dt
        # object_i_velr = self.sim.data.get_site_xvelr(self.object_names[i]) * dt

        # body_id = self.sim.model.body_name2id('robot0:gripper_link')
        # lookat = self.sim.data.body_xpos[body_id]

# def robot_get_obs(sim):
#     """Returns all joint positions and velocities associated with
#     a robot.
#     """
#     if sim.data.qpos is not None and sim.model.joint_names:
#         names = [n for n in sim.model.joint_names if n.startswith('robot')]
#         return (
#             np.array([sim.data.get_joint_qpos(name) for name in names]),
#             np.array([sim.data.get_joint_qvel(name) for name in names]),
#         )
#     return np.zeros(0), np.zeros(0)

#    def _get_obs(self):
#         # positions
#         grip_pos = self.sim.data.get_site_xpos('robot0:grip')
#         dt = self.sim.nsubsteps * self.sim.model.opt.timestep
#         grip_velp = self.sim.data.get_site_xvelp('robot0:grip') * dt
#         robot_qpos, robot_qvel = utils.robot_get_obs(self.sim)

#         gripper_state = robot_qpos[-2:]
#         gripper_vel = robot_qvel[-2:] * dt  # change to a scalar if the gripper is made symmetric


    # def get_xyz(self, name, object_type="body"):
    #     """Returns the xyz position of the specified object
    #     name: string
    #         name of the object you want the xyz position of
    #     object_type: string
    #         type of object you want the xyz position of
    #         Can be: mocap, body, geom, site
    #     """
    #     if object_type == "mocap":  # commonly queried to find target
    #         xyz = self.sim.data.get_mocap_pos(name)
    #     elif object_type == "body":
    #         xyz = self.sim.data.get_body_xpos(name)
    #     elif object_type == "geom":
    #         xyz = self.sim.data.get_geom_xpos(name)
    #     elif object_type == "site":
    #         xyz = self.sim.data.get_site_xpos(name)
    #     else:
    #         raise Exception(f"get_xyz for {object_type} object type not supported")

    #     return np.copy(xyz)
        