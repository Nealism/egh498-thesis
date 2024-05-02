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

home = str(Path.home())

start_time=time.time()


def run(args): 

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
    args.render = True
    # args.render = False
    args.record_sim = False
    env = Env(PATH=PATH, args=args)

    pol = torch.load(PATH + "/model.pt")
    # print(pol)
    obs = env.reset()
    # print(obs)

    

    n=0
    # print(pol)
    if args.use_perception:
        im = env.get_image()




    # print(pol)
    time_saving=[]
    action_saving1=[]
    action_saving2=[]

    model1 = copy.deepcopy(pol.pi.mu_net).to('cpu')
    traced_script_module1 = torch.jit.script(model1)
    traced_script_module1.save("/home/kom018/behaviour_rl/Saved_models/JIT_models/mu_net.jit")

    model2 = copy.deepcopy(pol.pi.z_net).to('cpu')
    traced_script_module2 = torch.jit.script(model2)
    traced_script_module2.save("/home/kom018/behaviour_rl/Saved_models/JIT_models/z_net.jit")


    # print("traced_script_module1",traced_script_module1)
    # print("traced_script_module2",traced_script_module2)
    st=time.time()
    action_saving1=[]
    action_saving2=[]

    while True:

        if args.use_perception:
            # print(torch.as_tensor(np.array(obs), dtype=torch.float32))
            action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]

        else:
            action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=False)[0]

        # print ("action", action);exit()

        # action_saving1.append(action[0][0])
        # action_saving2.append(action[0][1])
        # accc1=pd.DataFrame(action_saving1)
        # accc2=pd.DataFrame(action_saving2)
        # accc = pd.concat([accc1, accc2], axis=1)
        # # print(accc,type(accc))
        # accc.to_csv("action_test.csv")
        current_time = time.time() - st
        # print(current_time)
        st=time.time()
        # time_saving.append(current_time)
        
        obs, _, done, _ = env.step(action)

        if args.use_perception:
                im = env.get_image()
        

        if done==[True] or env.steps > args.max_ep_len:
            obs = env.reset()
            if args.use_perception:
                im = env.get_image()
            n=n+1
            if n==100:
                print("100 Iteration Done")
            for a in done:
                if a:
                    print(n,a)
        
            #print(obs)

if __name__== "__main__":
    args = default_arguments.get_defaults() 
    run(args)
