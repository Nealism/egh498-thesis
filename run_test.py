import torch
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
import default_arguments

MY_WORKSPACE_NAME = "tid010"

def run(args): 

    Env, args = default_arguments.get_env(args)   

    PATH = "/home/" + MY_WORKSPACE_NAME + "/hpc-scratch-pet/results/walker/"
    
    env = Env(PATH=PATH, args=args)
    
    # EXP = "disturb/30_06_2022_16_53_21"
    # EXP = "no_disturb/30_06_2022_16_53_21"

    EXP = args.exp +  "no_disturb4/01_07_2022_12_30_29"
    
    # EXP = "disturb4/01_07_2022_12_30_26"

    pol = torch.load(PATH + EXP + "/model.pt")

    obs = env.reset()
    while True:
        action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=True)[0]
        obs, _, done, _ = env.step(action)
        if done:
            obs = env.reset()

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    args.render = True
    args.record_sim = False
    run(args)