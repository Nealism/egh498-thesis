from assets.env_titan_pb_2 import Env as RobotEnv
import pybullet as p
from assets.env_base_pb import EnvBasePB
from mpi4py import MPI
comm = MPI.COMM_WORLD
from gym import spaces
import numpy as np



class Env(EnvBasePB):
    def __init__(self, PATH=None, args=None, writer=None):
    #def __init__(self, args.num_robots):
        self.rank = comm.Get_rank()
        self.args = args
        self.render = args.render and self.rank == 0
        self.PATH = PATH
        self.writer = writer
        self.master = True
        super().__init__(PATH)


        if "pumpkin" in self.args.env:
            self.ac_size = 22
            self.ob_size = 7
        else:
            self.ac_size = 2
            if self.args.num_robots > 1:
                self.ob_size = 18
            elif self.args.obstacle_avoidance:
                self.ob_size = 10
            else:
                self.ob_size = 6
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        self.load_simulator()
        
        objects = p.loadMJCF("./assets/xmls/ground.xml")
        self.worldId = objects[0]
        self.robots=[RobotEnv(PATH=PATH, args=args, writer=writer) for n in range(args.num_robots)]
        # for Robot in self.robots:


        # #self.robots=[RobotEnv() for n in [args.num_robots]]
        #     print("GOOOD PRINTTT",Robot.reset())


    def reset(self):
        res = []
        for Robot in self.robots:
            
            res.append(Robot.reset())
        print("GREAAATTTTTT", res)
        return res



    def step(self,actions):
        obs = []
        rews=[]
        dones=[]
        self.ob_dicts=[]
        for action,Robot in zip(actions,self.robots):
            ob,rew,done, self.ob_dict=Robot.step(action)
            # Robot.Id
            obs.append(ob)
            rews.append(rew)
            dones.append(done)

            self.ob_dicts.append(self.ob_dict)
        p.stepSimulation()

        return obs, rews, dones, self.ob_dict