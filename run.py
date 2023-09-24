from datetime import datetime
import tensorboardX
from mpi4py import MPI
comm = MPI.COMM_WORLD
from pathlib import Path
home = str(Path.home())
import numpy as np

from utils.mpi_tools import mpi_fork
import default_arguments

def run(args): 

    Env, args = default_arguments.get_env(args)   

    rank = comm.Get_rank()

    now = datetime.now()
    now = comm.bcast(now.strftime("%Y_%m_%d_%H_%M_%S"), root=0)  

    SAVE_PATH = "/scratch3/" + home.split("/")[-1] + "/results/"
    #SAVE_PATH = "~/scratch3/" + home.split("/")[-1] + "/results/"

    if args.folder:
        PATH = SAVE_PATH + args.env + "/" + args.exp + "/" + args.folder + "/"
    else:
        PATH = SAVE_PATH + args.env + "/" + args.exp + "/" + now + "/"

    if rank == 0:
        writer = tensorboardX.SummaryWriter(log_dir=PATH)
    else:
        writer = None

    env = Env(PATH=PATH, args=args, writer=writer)
    env.reset()
    #print("reset",env.reset())
    env.step(np.zeros(2))
    # Need to import Torch after Isaac (for isaac "is" envs) 
    from utils.run_utils import setup_logger_kwargs

    logger_kwargs = setup_logger_kwargs(args.exp, args.seed)
    logger_kwargs["output_dir"] = PATH

    if args.env == "multi_robot_pb":

        from models.ppo_MA import ppo
        ppo(env, ac_kwargs=dict(hidden_sizes=[args.num_nodes]*args.num_layers), seed=args.seed, epochs=args.epochs, PATH=PATH, writer=writer, local_epoch_len=args.local_epoch_len, logger_kwargs=logger_kwargs, use_perception=args.use_perception, load_path=args.load_path, robot_number=args.num_robots)

    else:

        from models.ppo import ppo
        ppo(env, ac_kwargs=dict(hidden_sizes=[args.num_nodes]*args.num_layers), seed=args.seed, epochs=args.epochs, PATH=PATH, writer=writer, local_epoch_len=args.local_epoch_len, logger_kwargs=logger_kwargs, use_perception=args.use_perception, load_path=args.load_path)

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    # TODO handle vectorised environments
    if not args.vec:
        mpi_fork(args.cpu)
    run(args)