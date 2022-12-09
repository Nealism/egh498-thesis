import matplotlib.pyplot as plt
import numpy as np

class Plotter():
    def __init__(self, PATH, plot_dict=None):
        self.PATH = PATH
        self.plot_dict = plot_dict

    def reset(self):
        self.data = {}
        for dl in self.plot_dict:
            if isinstance(self.plot_dict[dl], dict):
                self.data[dl] = {}
                for d in self.plot_dict[dl]:
                    self.data[dl][d] = []
            else:
                self.data[dl] = []

    def update(self, data, extra=None):
        if self.plot_dict is None:
            self.plot_dict = data
            self.reset()
        for dl in self.data:
            if isinstance(self.plot_dict[dl], dict):
                for d in self.data[dl]:
                    self.data[dl][d].append(data[dl][d])
            else:
                self.data[dl].append(data[dl])
        self.extra = extra

    def plot(self, tag=""):
        # print("Plotting")
        num_axes = len(self.data)
        fig, axes = plt.subplots(num_axes, figsize=(10, 3*num_axes))
        for i,dl in enumerate(self.data):
            if isinstance(self.data[dl], dict):
                for d in self.data[dl]:
                    axes[i].plot([_ for _ in range(len(self.data[dl][d]))], self.data[dl][d], alpha=1.0)    
                axes[i].legend([d for d in self.data[dl]])
            else:
                axes[i].plot([_ for _ in range(len(self.data[dl]))], self.data[dl], alpha=1.0)    
                if dl == "std1":
                    axes[i].plot([_ for _ in range(len(self.data[dl]))], [self.extra["thres1"] for _ in range(len(self.data[dl]))], alpha=1.0)    
            axes[i].set_title(dl, loc='left')
        # plt.savefig(self.PATH + "ep" + tag + str(ep_count) + ".png", bbox_inches="tight")
        plt.savefig(self.PATH + tag + ".png", bbox_inches="tight")
        plt.close()
        
        # e.g.:
        # plots.update({"current_pol":obstacle_types.index(eval_current_pol),
        # "terrain":{"z":env.box_info[1][env.box_num][2] + env.box_info[2][env.box_num][2],"robot_z":env.body_xyz[2]},"qvalue":{"q0_mean":means[0],"q1_mean":means[1],"q0_std":stds[0],"q1_std":stds[1]}, "std1":stds[0], "std2":stds[1]}, {"thres1":pols[0].train_model.thres[0],"thres2":pols[0].train_model.thres[1]})