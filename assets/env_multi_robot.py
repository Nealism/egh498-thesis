from env_titan_pb_2 import Env as RobotEnv
import pybullet as p


class Env():
    def __init__(self, args.num_robots):
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