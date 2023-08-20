import pickle 
import numpy as np
from copy import deepcopy
from mpi4py import MPI
comm = MPI.COMM_WORLD
from utils.plotter import Plotter

class EnvBase():
    def __init__(self, PATH):
        if self.args.use_perception:
            self.im_size = [1,48,48]
        self.all_log_things = {}
        if self.args.do_plot:
            self.plotter = Plotter(PATH=PATH)

    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        return_dict = {}
        return return_dict

    def get_image(self):
        return np.zeros(self.im_size)

    def get_env_state(self):
        save_dict = {}
        for state in self.__dict__:
            if state not in ["model", "data", "viewer", "writer", "low_lev_pol"]:
                save_dict[state] = self.__dict__[state]
        return deepcopy(save_dict)

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
            if additional_arguments is not None:
                self.sim_data.append(additional_arguments)
            pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data","wb"))
            if self.args.do_plot and self.episodes % 20 == 0:
                self.plotter.plot("plot")
            if test:
                pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data_test","wb"))
                if self.args.do_plot:
                    self.plotter.plot("plot_test")
            if test and best:
                pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data_best_test","wb"))
                if self.args.do_plot:
                    self.plotter.plot("plot_best_test")
            if best:
                pickle.dump(np.array(self.sim_data, dtype=object), open(self.PATH + "sim_data_best","wb"))            
                if self.args.do_plot and self.episodes % 20 == 0:
                    self.plotter.plot("plot_best")
            if self.args.do_plot:
                self.plotter.reset()
            self.sim_data = []

    def save_sim_state(self, save_things=None):
        if self.args.record_sim and self.rank == 0:
            if save_things is not None:
                self.sim_data.append([self.pos, self.orn, self.joints, save_things])  
            else:
                self.sim_data.append([self.pos, self.orn, self.joints])  

    def log_stuff(self, logger, writer, iters_so_far):
        log_things = self.get_log_things()
        for thing in log_things:
            if isinstance(log_things[thing], int) or isinstance(log_things[thing], float):
                self.all_log_things["all_" + thing] = MPI.COMM_WORLD.allgather(log_things[thing])
            else:
                self.all_log_things["all_" + thing] = MPI.COMM_WORLD.allgather(np.mean(log_things[thing]))
            if self.rank == 0:
                print(thing, self.all_log_things["all_" + thing])
                writer.add_scalar(thing, np.mean(self.all_log_things["all_" + thing]), iters_so_far)
                