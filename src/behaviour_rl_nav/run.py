from datetime import datetime
from mpi4py import MPI
comm = MPI.COMM_WORLD
import tensorboardX
from utils.mpi_tools import mpi_fork
from utils.run_utils import setup_logger_kwargs
from models.ppo_perception import ppo
from assets.env_gz import Env
import default_arguments

def run(args):
    MY_WORKSPACE_NAME = "tid010"

    if args.render:
        args.test = True

    rank = comm.Get_rank()

    now = datetime.now()
    now = comm.bcast(now.strftime("%d_%m_%Y_%H_%M_%S"), root=0)  

    SAVE_PATH = "/scratch1/" + MY_WORKSPACE_NAME + "/results/"
    PATH = SAVE_PATH + "walker/" + args.exp + "/" + now + "/"

    if rank == 0:
        writer = tensorboardX.SummaryWriter(log_dir=PATH)
    else:
        writer = None
    
    logger_kwargs = setup_logger_kwargs(args.exp, args.seed)
    logger_kwargs["output_dir"] = PATH


    ppo(lambda : Env(PATH=PATH, args=args, writer=writer), ac_kwargs=dict(hidden_sizes=[64]*2), epochs=args.epochs, PATH=PATH, writer=writer, logger_kwargs=logger_kwargs, perception=args.perception)


if __name__=="__main__":
    args = default_arguments.get_defaults() 
    mpi_fork(args.cpu)

    run(args)