from assets.env_anymal_cmd_mj import Env
import default_arguments
from pathlib import Path
import time
import glob

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
    env = Env(PATH=PATH, args=args)
    env.reset()
    while True:
        env.step([0]*12)
        
if __name__ == "__main__":
    args = default_arguments.get_defaults()
    run(args)