import torch
import os
import numpy as np
import glob
import time
from pathlib import Path
import default_arguments
from utils.plotter import Plotter

home = str(Path.home())

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

    if args.env == "anymal_cmd_mj":
        pol = torch.load("./resources/cmd_model/model.pt")
    else:
        pol = torch.load(PATH + "/model.pt")

    obs = env.reset()
    while True:
        action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=False)[0]
        if args.env == "anymal_cmd_mj":
            obs, _, done, _ = env.step(action, cmds=[0.8,0.0,0.0])
        else:
            obs, _, done, _ = env.step(action)
        if done or env.steps > args.max_ep_len:
            obs = env.reset()

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    run(args)
