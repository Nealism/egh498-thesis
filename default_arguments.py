import argparse

def get_defaults():
    
    parser = argparse.ArgumentParser()
    # ========================================================================
    # Sim
    # ========================================================================
    parser.add_argument('--render', default=False, action="store_true")
    parser.add_argument('--env', default="franka_reach_mj")
    parser.add_argument('--ident', default="tid010")
    parser.add_argument('--urdf', default=False, action="store_true")
    parser.add_argument('--cur', default=False, action="store_true")
    parser.add_argument('--hpc', default=False, action="store_true")
    parser.add_argument('--test', default=False, action="store_true")
    parser.add_argument('--just_expert', default=False, action="store_true")
    parser.add_argument('--perception', default=False, action="store_true")
    parser.add_argument('--apply_disturbances', default=False, action="store_true")
    parser.add_argument('--record_sim', default=True, action="store_false")
    parser.add_argument('--frameless', default=True, action="store_false")
    parser.add_argument('--best', default=False, action="store_true")
    parser.add_argument('--use_ball', default=False, action="store_true")
    parser.add_argument('--see_test', default=False, action="store_true")
    parser.add_argument('--replay', default=False, action="store_true")
    parser.add_argument('--control_type', default="torque")
    parser.add_argument('--emitter', default="")
    parser.add_argument('--folder', default="")
    parser.add_argument('--reward', default="")
    parser.add_argument('--exp', default="test")
    parser.add_argument('--tree_type', default="")
    parser.add_argument('--sleep', type=float, default=0.01)
    parser.add_argument('--max_joint_vel', type=float, default=2.0)
    parser.add_argument('--difficulty', type=int, default=1)

    # ========================================================================
    # Training
    # ========================================================================
    parser.add_argument('--training_on_hpc', default=False, action="store_true")
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--save_freq', type=int, default=10)
    parser.add_argument('--local_epoch_len', type=int, default=4096)
    parser.add_argument('--max_ep_len', type=int, default=1048)
    parser.add_argument('--epochs', type=int, default=8000)
    parser.add_argument('--cpu', type=int, default=1)
    parser.add_argument('--episodes', type=int, default=100)

    # ========================================================================
    # Terrain
    # ========================================================================
    parser.add_argument('--terrain_first', default=False, action="store_true")
    parser.add_argument('--add_terrain', default=False, action="store_true")
    parser.add_argument('--initial_terrain_difficulty', type=float, default=0.01)
    parser.add_argument('--final_terrain_difficulty', type=float, default=0.5)

    # knowns, unknowns = parser.parse_known_args()
    args = parser.parse_args()
    return args

def get_env(args):
    # Not all of these are implemented yet..
    if args.env == "humanoid_pb":
        from assets.env_humanoid_pb import Env
    elif args.env == "biped_pb":
        from assets.env_biped_pb import Env 
    elif args.env == "franka_ball_mj":
        from assets.env_franka_mj import Env
        args.use_ball = True
    elif args.env == "franka_reach_mj":
        from assets.env_franka_mj import Env
    elif args.env == "franka_reach_dm_mj":
        from assets.env_franka_dm_mj import Env
    elif args.env == "franka_reach_pb":
        from assets.env_franka_pb import Env
    elif args.env == "anymal_mj":
        from assets.env_anymal_mj import Env    
        args.control_type = "position"
    elif args.env in ["titan_pb", "pumpkin_pb"]:
        from assets.env_titan_pb import Env
        args.control_type = "velocity"
    elif args.env == "titan_mj":
        from assets.env_titan_mj import Env
        args.control_type = "velocity"
        args.max_ep_len = 256
    # TODOS:
    elif args.env == "bi_franka_mj":
        from assets.env_bi_franka_mj import Env
    elif args.env == "titan_gz":
        from assets.env_titan_gz import Env
    else:
        print("--env not in list of environments ", args.env); exit()

    # args.test only loads simulator once, a bit nicer for debugging, but have to refresh for training else memory leak
    if "pb" in args.env and args.render:
        args.test = True    
    
    return Env, args