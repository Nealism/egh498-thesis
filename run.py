from datetime import datetime
import tensorboardX
from mpi4py import MPI
comm = MPI.COMM_WORLD

from models.ppo import ppo
from utils.mpi_tools import mpi_fork
from utils.run_utils import setup_logger_kwargs
import default_arguments

def run(args): 

    Env, args = default_arguments.get_env(args)   

    rank = comm.Get_rank()

    now = datetime.now()
    now = comm.bcast(now.strftime("%d_%m_%Y_%H_%M_%S"), root=0)  

    MY_WORKSPACE_NAME = args.ident
    SAVE_PATH = "/scratch1/" + MY_WORKSPACE_NAME + "/results/"
    PATH = SAVE_PATH + "walker/" + args.exp + "/" + now + "/"

    if rank == 0:
        writer = tensorboardX.SummaryWriter(log_dir=PATH)
    else:
        writer = None
    
    logger_kwargs = setup_logger_kwargs(args.exp, args.seed)
    logger_kwargs["output_dir"] = PATH

    ppo(lambda : Env(PATH=PATH, args=args, writer=writer), ac_kwargs=dict(hidden_sizes=[64]*2), epochs=args.epochs, PATH=PATH, writer=writer, max_ep_len=args.max_ep_len, local_epoch_len=args.local_epoch_len, logger_kwargs=logger_kwargs, perception=args.perception)

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    mpi_fork(args.cpu)
    run(args)