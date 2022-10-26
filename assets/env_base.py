import pickle 
import numpy as np
from copy import deepcopy
from mpi4py import MPI
comm = MPI.COMM_WORLD

class EnvBase():

    def get_env_state(self):
        # For some reason getting the entire class dict doesn't work with MPI, need specify what states to save/restore
        return deepcopy({state:self.__dict__[state] for state in self.states_to_restore if state in self.__dict__})

    def restore_env_state(self, params):
        if params:
            for key in params:
                self.__dict__[key] = params[key]
            self.set_position(self.pos, self.orn, self.joints, self.joint_vel) 
        else:
            print("Trying to restore without any saved parameters.")
            exit()

    def record_sim_state(self, best=False, test=False, additional_arguments=None):
        if self.args.record_sim and self.rank == 0:
            if additional_arguments:
                self.sim_data.append(additional_arguments)
            if test:
                pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data_test","wb"))
            if test and best:
                pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data_best_test","wb"))
            if best:
                pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data_best","wb"))
            pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data","wb"))
            self.sim_data = []

    def save_sim_state(self):
        if self.rank == 0:
            self.sim_data.append([self.pos, self.orn, self.joints])  

    def log_stuff(self, logger, writer, iters_so_far):
        log_things = self.get_log_things()
        for thing in log_things:
            if isinstance(log_things[thing], int) or isinstance(log_things[thing], float):
                things = MPI.COMM_WORLD.allgather(log_things[thing])
            else:
                things = MPI.COMM_WORLD.allgather(np.mean(log_things[thing]))
            if self.rank == 0:
                print(thing, things)
                writer.add_scalar(thing, np.mean(things), iters_so_far)