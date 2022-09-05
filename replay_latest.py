'''
Script used to display robot stuff while training (loads in save robot state)
'''
import glob
import time
from pathlib import Path
home = str(Path.home())
import pickle
import default_arguments

from os import listdir
from os.path import isfile, join

def run(args):
    print()
    if args.hpc:
        # path_home = home + "/hpc-home/ale"
        path_home = home + "/hpc-scratch-pet"
    else:
        path_home = "/scratch1/$USER"
        # path_home = home + "/ale"

    if args.folder == "":
        # Get latest experiment
        # folders = [folder.split("/")[-1] for folder in glob.glob(path_home + "/results/" + args.exp + "/*/")]
        # Glob update broke things
        folders = [folder.split("/")[-2] for folder in glob.glob(path_home + "/results/" + args.exp + "/*/")]
        latest_folder = "01_01_1900_01_01_01"
        latest_date_key = time.strptime(latest_folder, "%d_%m_%Y_%H_%M_%S")
        for folder in folders:
            new_date_key = time.strptime(folder, "%d_%m_%Y_%H_%M_%S")
            if new_date_key > latest_date_key:
                latest_date_key = new_date_key
                latest_folder = folder
    else:
        latest_folder = args.folder

    PATH = path_home + "/results/" + args.exp + "/" + latest_folder

    Env, args = default_arguments.get_env(args)   

    env = Env(PATH=PATH, args=args)

    if args.emitter != "":
        args.emitter += "_"
    while True:
        try:
            print("Loading terrain and sim data", PATH + "/" + args.emitter)
            if args.best:
                data = pickle.load(open(PATH + "/" + args.emitter + "sim_data_best", "rb"))
            else:
                data = pickle.load(open(PATH + "/" + args.emitter + "sim_data", "rb"))
            print(data.shape)
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
        
        
        env.terrain = terrain
        env.reset(terrain)
        
        for d in data:
            pos, orn, joints = d

            for j,m in zip(env.motor_names, joints):
                if "x" in j:
                    print(j,m)
            # print(pos)
            env.set_position(pos, orn, joints)
            time.sleep(args.sleep)


if __name__=="__main__":
    args = default_arguments.get_defaults() 
    args.render = True
    args.test = True
    args.record_data = False
    run(args)