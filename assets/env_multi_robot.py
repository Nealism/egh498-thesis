from assets.env_titan_pb_2 import Env as RobotEnv
import pybullet as p
from assets.env_base_pb import EnvBasePB
from mpi4py import MPI
comm = MPI.COMM_WORLD


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

        self.load_simulator()
        
        objects = p.loadMJCF("./assets/xmls/ground.xml")
        self.worldId = objects[0]
        self.robots=[RobotEnv() for n in args.num_robots]

    def reset(self):
        for Robot in self.robots:
            Robot.reset()

    def step(self,actions):
        obs = []
        rews=[]
        dones=[]
        self.ob_dicts=[]
        for action,Robot in zip(actions,self.robots):
            ob,rew,done, self.ob_dict=Robot.step(action)
            Robot.Id
        obs.append(ob)
        rews.append(rew)
        dones.append(done)
        self.ob_dicts.append(self.ob_dict)
        p.stepSimulation()

        return obs, rews, dones, self.ob_dict