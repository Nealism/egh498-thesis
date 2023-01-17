import numpy as np
import pybullet as p
from mpi4py import MPI
comm = MPI.COMM_WORLD

class Env():
    rank = comm.Get_rank()
    simStep = 1/120
    timeStep = 1/120
    ac_size = 7
    ob_size = 25
    def __init__(self, args, render):

        self.args = args
        self.render = render
        self.master = True 
        
        super().__init__()

        if self.args.render and self.master:
            self.physicsClientId = p.connect(p.GUI)
        else:
            self.physicsClientId = p.connect(p.DIRECT) 

        self.load()

    def get_success(self):
        return self.body_xyz[0] > 15

    def load(self):
        if self.master:
            # flags=p.URDF_MAINTAIN_LINK_ORDER + p.URDF_USE_SELF_COLLISION + p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS
            flags=p.URDF_USE_SELF_COLLISION + p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS
            self.Id = p.loadURDF("./assets/humanoid.urdf", [0, 0.889540259, 0], globalScaling=0.25, useFixedBase=False, flags=flags)
        else:
            self.Id = 1
        
        p.setTimeStep(self.simStep)
        p.setGravity(0,0,-9.8)
        # ======================================================================

        print(self.Id); exit()

        numJoints = p.getNumJoints(self.Id)
        self.model = p.loadXML("assets/humanoid.xml")
        self.sim = MjSim(self.model)
        if self.render:
            self.viewer = MjViewer(self.sim)

        # Actuator bounds
        # bounds = self.model.actuator_ctrlrange.copy().astype(np.float32)
        # low, high = bounds.T

    def reset(self):
        self.sim.reset()
        # state = self.sim.get_state()
        state = list(self.sim.data.qpos) + list(self.sim.data.qvel) + list(self.sim.data.actuator_force)
        return state

    def step(self, actions):
        self.sim.data.ctrl[:] = actions[:]
        self.sim.step()
        if self.render:
            self.viewer.render()
        # Need this?
        # state = self.sim.get_state()
        state = list(self.sim.data.qpos) + list(self.sim.data.qvel) + list(self.sim.data.actuator_force)
        # state = [state["qpos"] + state["qvel"]]
        # print(state["qpos"])
        self.body_xyz = self.get_body_xyz()

        # self.sim.data.ncon == 0
        reward = 1
        done = False
        return state, reward, done, None

    def set_position(self, pos, orn, joints):
        sim_state = self.sim.get_state()
        sim_state = self.sim.set_state()


    def get_body_xyz(self):
        mass = np.expand_dims(self.model.body_mass, 1)
        xpos = self.sim.data.xipos
        return (np.sum(mass * xpos, 0) / np.sum(mass))[0]

    # What's a marker?
        # viewer.add_marker(pos=np.array([x, y, 1]),
                # label=str(t))
    def set_target(self, x, y):
        self.viewer.add_marker(pos=np.array([x, y, 1]), label=str(t))