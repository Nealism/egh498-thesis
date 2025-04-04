import torch
import os
import numpy as np
import glob
import time
from pathlib import Path
import default_arguments
from utils.plotter import Plotter
import pandas as pd
import copy
from scipy.ndimage import label, generate_binary_structure

import time
import matplotlib.pyplot as plt
import os
import pandas as pd
from assets.env_multi_robot_pb import Env
from models import core
import matplotlib.pyplot as plt


success_robot1 = []
success_robot2 = []
epochs = []

home = str(Path.home())

args = default_arguments.get_defaults()

if args.hpc:
    path_home = "/hpc-scratch/" + home.split("/")[-1]
elif args.home:
    path_home = home 
else:
    path_home = "/scratch3/" + home.split("/")[-1]


if args.home:
    path_home += "/behaviour_rl/" +  args.exp + "/"

else:
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
args.render = False
# args.render = False
# if args.figure:
#     args.render = False
args.record_sim = False
env = Env(PATH=PATH, args=args)
actor_critic=core.MLPActorCriticPerception(None, env.observation_space, env.im_size, env.action_space)


# epoch_number=0
# checkpoint_dir="/scratch3/kom018/results/multi_robot_pb/test/2025_04_04_01_52_15/"
# checkpoint_dir="/hpc-scratch/kom018/results/multi_robot_pb/200203/E1r32G1E1/2025_04_04_04_19_17/"
checkpoint_dir="/hpc-scratch/kom018/results/multi_robot_pb/200203/E10r32G1E1/2025_04_04_05_08_36/"
checkpoint_files = sorted([f for f in os.listdir(checkpoint_dir) if f.endswith('.pt')], key=lambda x: int(x.split('_')[1].split('.')[0]))
   
for filename in checkpoint_files:
    epoch_number = int(filename.split('_')[1].split('.')[0])
    checkpoint_path = os.path.join(checkpoint_dir, filename)
    checkpoint = torch.load(checkpoint_path)
    model=checkpoint['model']
    # actor_critic.load_state_dict(checkpoint['state_dict'])
    # model=actor_critic
    # print("epcohno",checkpoint) 

    obs = env.reset()
    if args.use_perception:
        im = env.get_image()

    
    while True:
        if args.use_perception and not args.jit_model:
            if args.heterogeneous or args.titanheads:
                a_spot,a_titan, v, logp_spot, logp_titan =model.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)
            else:
                action = model.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]

        sp_ac=np.array([[0., 0.],[0., 0.]])
        obs, _, done,termination, _ = env.step(action,sp_ac)


        # print(obs[0],"obs?")
        if args.use_perception:
                im = env.get_image()

        if all(done) or all(termination) or env.steps > args.max_ep_len:
            
            obs = env.reset()
            if args.use_perception:
                im = env.get_image()
            print("epoch_number",epoch_number)
            success = env.success_list
            # print("success",success)
            print("rob",env.robots[0].ep_goal_success,env.robots[1].ep_goal_success,epoch_number)
            success_robot1.append(env.robots[0].ep_goal_success)
            success_robot2.append(env.robots[1].ep_goal_success)
            epochs.append(epoch_number)
            break


plt.figure(figsize=(14, 6))

# Plot for Robot 1
plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
plt.plot(epochs, success_robot1, marker='o', linestyle='-', color='blue')
plt.title('Success Rate of Robot 1 per Epoch')
plt.xlabel('Epoch')
plt.ylabel('Success Rate')
plt.grid(True)

# Plot for Robot 2
plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
plt.plot(epochs, success_robot2, marker='o', linestyle='-', color='red')
plt.title('Success Rate of Robot 2 per Epoch')
plt.xlabel('Epoch')
plt.ylabel('Success Rate')
plt.grid(True)

plt.tight_layout()
plt.show()

        
            