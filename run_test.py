import torch
import os
import numpy as np
import glob
import time
from pathlib import Path

home = str(Path.home())

import default_arguments
from utils.plotter import Plotter

def run(args): 

    if args.hpc:
        path_home = "/hpc-scratch/" + home.split("/")[-1]
    else:
        path_home = "/scratch1/" + home.split("/")[-1]

    path_home += "/results/" + args.env + "/" + args.exp + "/"

    if args.folder == "":
        # Get latest experiment (eg: latest model inside test folder)
        folders = [folder.split("/")[-2] for folder in glob.glob(path_home + "*/")]
        latest_folder = "1900_01_01_01_01_01"
        latest_date_key = time.strptime(latest_folder, "%Y_%m_%d_%H_%M_%S")
        for folder in folders:
            new_date_key = time.strptime(folder, "%Y_%m_%d_%H_%M_%S")
            if new_date_key > latest_date_key:
                latest_date_key = new_date_key
                latest_folder = folder
    else:
        latest_folder = args.folder

    PATH = path_home + latest_folder
    
    Env, args = default_arguments.get_env(args)   
    args.render = True
    args.record_sim = False
    env = Env(PATH=PATH, args=args)

    if "model.pt" not in os.listdir(PATH):
         print("----------")
         print("model.pt doesn't exist")
         print("----------")
         return -1
    # pol = torch.load(PATH + "/model.pt")

    #manually loading brendan's already trained walking gait
    pol = torch.load("/scratch1/rac018/results/anymal_mj/proper_trained/brendan_walking_gait" + "/model.pt")

    if args.do_plot:
        names_to_plot = ["joint_pos" + str(i) for i in range(env.ac_size)]
        names_to_plot += ["joint_vel" + str(i) for i in range(env.ac_size)]
        names_to_plot += ["joint_effort" + str(i) for i in range(env.ac_size)]
        names_to_plot += ["joint_cmd" + str(i) for i in range(env.ac_size)]
        plotter = Plotter(names_to_plot)

    obs = env.reset()
    while True:
        action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=False)[0]
        obs, _, done, _ = env.step(action)
        if args.do_plot:
            plotter.save_data({name:env.ob_dict[name] for name in names_to_plot})
        if done or env.steps > args.max_ep_len:
            obs = env.reset()
            if args.do_plot:
                plotter.plot()

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    run(args)