'''
Script used to display robot stuff while training (loads in save robot state)
'''
import numpy as np
import glob
import time
from pathlib import Path
home = str(Path.home())
import pickle
import default_arguments

from os import listdir
from os.path import isfile, join

def run(args):

    if args.hpc:
        path_home = home + "/hpc-scratch-pet"
    else:
        path_home = "/scratch1/" + home.split("/")[-1]

    path_home += "/results/" + args.env + "/" + args.exp + "/"

    if args.folder == "":
        # Get latest experiment
        folders = [folder.split("/")[-2] for folder in glob.glob(path_home + "*/")]
        latest_folder = "01_01_1900_01_01_01"
        latest_date_key = time.strptime(latest_folder, "%d_%m_%Y_%H_%M_%S")
        for folder in folders:
            new_date_key = time.strptime(folder, "%d_%m_%Y_%H_%M_%S")
            if new_date_key > latest_date_key:
                latest_date_key = new_date_key
                latest_folder = folder
    else:
        latest_folder = args.folder

    PATH = path_home + latest_folder

    Env, args = default_arguments.get_env(args)   

    args.render = True
    args.test = True
    args.record_data = False

    env = Env(PATH=PATH, args=args)

    while True:
        try:
            print("Loading terrain and sim data", PATH)
            if args.best:
                data = pickle.load(open(PATH + "/sim_data_best", "rb"))
            else:
                data = pickle.load(open(PATH + "/sim_data", "rb"))
            if "mj" in args.env:
                print("Data len", len(data))
                if len(data[-1]) != 5:
                    target = data[-1]
                    data = data[:-1]
            else:
                print("Data shape", data.shape)
                if len(data[-1]) != 3:
                    terrain = data[-1]
                    data = data[:-1]
                    print("loaded ", data.shape, terrain.shape)
                else:
                    terrain = None
                    print("loaded ", data.shape)

        except Exception as e:
            print("couldn't load terrain or data")
            print(e)
            exit()
        
        if "mj" in args.env:
            env.reset()
        else:
            env.terrain = terrain
            env.reset(terrain)
        
        for d in data:
            if "mj" in args.env:
                env.step(replay_state=d, target=target[:3], target_point=target[3:])
            else:
                pos, orn, joints = d
                env.set_position(pos, orn, joints)
                time.sleep(args.sleep)

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    run(args)