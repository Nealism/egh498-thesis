import pickle 
import numpy as np
from copy import deepcopy
from mpi4py import MPI
comm = MPI.COMM_WORLD

class EnvBase():
    def __init__(self):
        pass

    def record_sim_state(self, best=False):
        if self.rank == 0:
            if self.args.add_terrain:
                self.sim_data.append(self.terrain)
            if best:
                pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data_best","wb"))
            pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data","wb"))
            self.sim_data = []

    def save_sim_state(self):
        if self.rank == 0:
            self.sim_data.append([self.body_xyz, [self.qx, self.qy, self.qz, self.qw], self.joints])  

    # def restore_state(self, state):
    #     # self.set_position(self.pos, self.orn, self.joints, self.joint_vel)  
    #     self.set_position(state)  

    # def restore_env_state(self, params):
    #     for key in params:
    #         self.__dict__[key] = params[key]
    #     self.set_position(self.pos, self.orn, self.joints, self.joint_vel) 
        # self.restore_state()
        # self.set_position()

    # def set_position(self, pos, orn, joints, joint_vel):
    #     pass
