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
    parser.add_argument('--perception', default=False, action="store_true")
    parser.add_argument('--apply_disturbances', default=False, action="store_true")
    parser.add_argument('--record_sim', default=True, action="store_false")
    parser.add_argument('--best', default=False, action="store_true")
    parser.add_argument('--use_ball', default=False, action="store_true")
    parser.add_argument('--emitter', default="")
    parser.add_argument('--folder', default="")
    parser.add_argument('--reward', default="")
    parser.add_argument('--exp', default="test")
    parser.add_argument('--sleep', type=float, default=0.01)

    # ========================================================================
    # Training
    # ========================================================================
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--save_freq', type=int, default=10)
    parser.add_argument('--steps', type=int, default=2048)
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
    # Not all fo these are implemented yet..
    if args.env == "humanoid_pb":
        from assets.env_humanoid_pb import Env
    elif args.env == "humanoid_pb_no_feet":
        from assets.env_humanoid_pb import Env
        args.no_feet = True
    elif args.env == "biped_pb":
        from assets.env_biped_pb import Env 
    elif args.env == "franka_ball_mj":
        from assets.env_franka_mj import Env
        args.use_ball = True
    elif args.env == "franka_reach_mj":
        from assets.env_franka_mj import Env
    elif args.env == "bi_franka_mj":
        from assets.env_bi_franka_mj import Env
    elif args.env == "anymal_mj":
        from assets.env_anymal_mj import Env
    elif args.env == "titan_gz":
        from assets.env_titan_gz import Env
        
    # args.test only loads simulator once, a bit nicer for debugging, but have to refresh for training else memory leak
    if "pb" in args.env and args.render:
        args.test = True    
    
    return Env, args