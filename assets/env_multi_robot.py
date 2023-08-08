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
        for action,Robot in zip(actions,self.robots):
            Robot.step(action)
            Robot.Id
        p.stepSimulation()