import glob
import time
from pathlib import Path
home = str(Path.home())
import pickle
import os

import default_arguments

def run(args):

    if args.hpc:
        path_home = "/hpc-scratch/" + home.split("/")[-1]
    else:
        path_home = "/scratch1/" + home.split("/")[-1]

    path_home += "/results/" + args.env + "/" + args.exp + "/"

    if args.folder == "":
        # Get latest experiment
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
    args.test = True
    args.record_sim = False
    args.replay = True
    env = Env(PATH=PATH, args=args)

    while True:
        try:
            print("Loading terrain and sim data", PATH)
            more = ""
            if args.best:
                more += "_best"
            if args.see_test:
                more += "_test"
            data = pickle.load(open(PATH + "/sim_data" + more, "rb"))
            additional_stuff = None
            if "mj" in args.env:
                print("Data len", len(data), len(data[-1]))
                # if len(data[-1]) != 5:
                # if len(data[-1]) != 3:
                    # additional_stuff = data[-1]
                    # data = data[:-1]
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
            data = None
        
        if data is not None:
            if "mj" in args.env:
                if os.path.exists(PATH + "/trees/replay_scene" + more + ".xml"):
                    env.reset(model_path = PATH + "/trees/replay_scene" + more + ".xml")
                else:
                    env.reset()
            else:
                env.terrain = terrain
                env.reset(terrain)
            
            for d in data:
                if "mj" in args.env:
                    env.step(replay_state=d)
                else:
                    pos, orn, joints = d
                    env.set_position(pos, orn, joints)
                    time.sleep(args.sleep)

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    run(args)