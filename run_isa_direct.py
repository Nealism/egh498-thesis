import torch
import torch.nn as nn
import os
import numpy as np
import glob
import time
from pathlib import Path
import models.core as core
import copy

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

    #hardcoded model paths
    rough_no_height_1500_path =f"{PATH}/model_1500.pt"
    flat_1001_path = f"{PATH}/model_1001.pt"

    loaded_dict = torch.load(flat_1001_path, map_location=torch.device("cpu"))
    loaded_dict_copy = copy.deepcopy(loaded_dict)
    
    # change names of keys in state_dict (bit hacky but the alternative is importing an entire module from the isaac repo)
    for i, (k, _) in enumerate(loaded_dict['model_state_dict'].items()):
        print(i, k)
        if i == 0:
            loaded_dict_copy["model_state_dict"]["pi.log_std"] = loaded_dict_copy["model_state_dict"].pop("std")
        
        elif i > 0 and i < 9:
            loaded_dict_copy["model_state_dict"]["pi.mu_net." + k[6:]] = loaded_dict_copy["model_state_dict"].pop("actor." + k[6:])
        
        else:
            loaded_dict_copy["model_state_dict"]["v.v_net." + k[7:]] = loaded_dict_copy["model_state_dict"].pop("critic." + k[7:])

    actor_critic = core.MLPActorCritic
    isaac_obs_space = env.isa_observation_space
    isaac_action_space = env.action_space
    isaac_activation = nn.ELU
    isaac_rough_hidden_layers = [512, 256, 128]
    isaac_flat_hidden_layers = [128, 64, 32]
    ac_kwargs = dict(hidden_sizes=isaac_flat_hidden_layers, activation=isaac_activation)
    ac = actor_critic(isaac_obs_space, isaac_action_space, **ac_kwargs)
    ac.load_state_dict(loaded_dict_copy['model_state_dict'])
    ac.eval()

    # pol = torch.load(rough_no_height_1500_path)
    pol = torch.load(flat_1001_path)

    if args.do_plot:

        names_to_plot = ["joint_pos" + str(i) for i in range(env.ac_size)]
        names_to_plot += ["joint_vel" + str(i) for i in range(env.ac_size)]
        names_to_plot += ["joint_effort" + str(i) for i in range(env.ac_size)]
        names_to_plot += ["joint_cmd" + str(i) for i in range(env.ac_size)]
        plotter = Plotter(names_to_plot)

    obs = env.reset()
    
    while True:
        # action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=False)[0]
        distribution = ac.pi(torch.tensor(np.array(obs).astype(np.float32)))[0]
        action = distribution.sample()
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