import torch
import numpy as np
import glob
import time
from pathlib import Path
import default_arguments

home = str(Path.home())

def run(args): 

    args.env = "spot_pb"

    if args.hpc:
        path_home = home + "/hpc-scratch/" + home.split("/")[-1]
    else:
        path_home = "/scratch3/" + home.split("/")[-1]

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
    
    print("Loading from ", PATH)

    Env, args = default_arguments.get_env(args)   
    args.render = True
    args.record_sim = False
    env = Env(PATH=PATH, args=args)


    USE_SPOT = True
    # USE_SPOT = False
    if USE_SPOT:
        # SPOT_MODEL_PATH = "./resources/spot/2024_04_30_08_59_43/model.pt" 
        # SPOT_MODEL_PATH = "./resources/spot/2024_05_08_21_23_04/model.pt" 
        SPOT_MODEL_PATH = "./resources/spot/2024_05_13_11_11_30/model.pt" 
        pol = torch.load(SPOT_MODEL_PATH)

    else:
        print("loading from ", PATH)
        pol = torch.load(PATH + "/model.pt")

    # else:
        # pol = torch.jit.load("./logs/chuck/exported/Oct18_09-03-12_/policy_1.pt")

    obs = env.reset()
    if args.use_perception:
        im = env.get_image()

    n=0
    while True:
        if args.use_perception:
            print(im)
            action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), torch.tensor(np.array(im).astype(np.float32)), stochastic=False)[0]
        else:
            # action = pol(torch.tensor(np.array(obs).astype(np.float32))).detach().numpy()[0]
            action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=False)[0]
        obs, rew, done, _ = env.step(action)

        # start = 100
        # if env.steps < start:
        #     env.commands = np.array([0., 0.0, 0.0])
        # elif env.steps < start + 200:
        #     env.commands = np.array([0., 0.0, 1.5])
        # elif env.steps < start + 400:
        #     env.commands = np.array([0., 0.0, -1.5])
        # elif env.steps < start + 500:
        #     env.commands = np.array([1., 0.0, 0])
        # elif env.steps < start + 700:
        #     env.commands = np.array([-0.5, 0.0, 0])
        # elif env.steps < start + 800:
        #     env.commands = np.array([0., 0.5, 0])
        # elif env.steps < start + 900:
        #     env.commands = np.array([0., -0.5, 0])
         
        print(rew)
        print(env.commands)
        print(env.vx, env.vy, env.yaw_vel)
        print()
        if args.use_perception:
            im = env.get_image()

        if done==True or env.steps > args.max_ep_len:
            obs = env.reset()
            if args.use_perception:
                im = env.get_image()

if __name__== "__main__":
    args = default_arguments.get_defaults() 
    run(args)
