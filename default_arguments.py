import argparse

def get_defaults():
    
    parser = argparse.ArgumentParser()
    # ========================================================================
    # Run arguments
    # ========================================================================
    parser.add_argument('--vec', default=False, action="store_true", help="Vectorised environment (GPU stuff) or MPI")
    # ========================================================================
    # Sim
    # ========================================================================
    parser.add_argument('--render', default=False, action="store_true")
    parser.add_argument('--env', default="franka_reach_mj")
    parser.add_argument('--urdf', default=False, action="store_true")
    parser.add_argument('--cur', default=False, action="store_true")
    parser.add_argument('--hpc', default=False, action="store_true")
    parser.add_argument('--test', default=False, action="store_true")
    parser.add_argument('--just_expert', default=False, action="store_true")
    parser.add_argument('--use_perception', default=False, action="store_true")
    parser.add_argument('--apply_disturbances', default=False, action="store_true")
    parser.add_argument('--record_sim', default=True, action="store_false")
    parser.add_argument('--frameless', default=True, action="store_false")
    parser.add_argument('--best', default=False, action="store_true")
    parser.add_argument('--tree_first', default=False, action="store_true")
    parser.add_argument('--use_ball', default=False, action="store_true")
    parser.add_argument('--see_test', default=False, action="store_true")
    parser.add_argument('--replay', default=False, action="store_true")
    parser.add_argument('--do_plot', default=False, action="store_true")
    parser.add_argument('--rand_rot', default=True, action="store_false")
    parser.add_argument('--control_type', default="torque")
    parser.add_argument('--emitter', default="")
    parser.add_argument('--folder', default="")
    parser.add_argument('--reward', type=int, default=1)
    parser.add_argument('--exp', default="test")
    parser.add_argument('--goal', default="end_effector")
    parser.add_argument('--tree_type', default="")
    parser.add_argument('--sleep', type=float, default=0.01)
    parser.add_argument('--action_multiplier', type=float, default=5.0)
    parser.add_argument('--jitter_scalar', type=float, default=0.0)
    parser.add_argument('--max_joint_vel', type=float, default=2.0)
    parser.add_argument('--difficulty', type=int, default=1)
    parser.add_argument('--cmd_ranges', type=str, default="(1, 1, 1)")
    parser.add_argument('--one_wp_per_ep', default=False, action="store_true")

    # ========================================================================
    # PyBullet biped environment - TODO: move to config and cleanup
    # ========================================================================
    parser.add_argument('--cur_num', type=int, default=3)
    parser.add_argument('--cur_len', type=int, default=3)
    parser.add_argument('--detection_dist', type=float, default=0.9)
    parser.add_argument('--dist_off_ground', type=float, default=1.25)
    parser.add_argument('--more_power', type=float, default=1.0)
    parser.add_argument('--num_artifacts', type=int, default=3)
    parser.add_argument('--initial_disturbance', type=float, default=0.0)
    parser.add_argument('--final_disturbance', type=float, default=0.0)
    parser.add_argument('--multi_robots', default=False, action="store_true")
    parser.add_argument('--e2e', default=False, action="store_true")
    parser.add_argument('--advantage2', default=False, action="store_true")
    parser.add_argument('--doa', default=False, action="store_true")
    parser.add_argument('--expert', default=False, action="store_true")
    parser.add_argument('--record_step', default=False, action="store_true")
    parser.add_argument('--early_stop', default=False, action="store_true")
    parser.add_argument('--debug', default=False, action="store_true")
    parser.add_argument('--ood', default=False, action="store_true")
    parser.add_argument('--dqn', default=False, action="store_true")
    parser.add_argument('--show_detection', default=False, action="store_true")
    parser.add_argument('--easy_flat', default=False, action="store_true")
    parser.add_argument('--MASTER', default=True, action="store_false")
    parser.add_argument('--disturbances', default=True, action="store_false")
    parser.add_argument('--obstacle_type', default="gaps")
    parser.add_argument('--vis_type', default="depth")
    parser.add_argument('--run_state', default="")
    parser.add_argument('--comparison', default="")

    # ========================================================================
    # Network
    # ========================================================================
    parser.add_argument('--num_nodes', default=256, type=int)
    parser.add_argument('--num_layers', default=2, type=int)

    # ========================================================================
    # Training
    # ========================================================================
    parser.add_argument('--training_on_hpc', default=False, action="store_true")
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--save_freq', type=int, default=10)
    parser.add_argument('--local_epoch_len', type=int, default=4096)
    parser.add_argument('--max_ep_len', type=int, default=1024)
    parser.add_argument('--epochs', type=int, default=8000)
    parser.add_argument('--cpu', type=int, default=1)
    parser.add_argument('--episodes', type=int, default=100)
    parser.add_argument('--reward_fn', type=int, default=3)
    parser.add_argument('--obs_fn', type=int, default=3)
    parser.add_argument('--cmd_scaling', type=float, default=1.0)

    # ========================================================================
    # Terrain
    # ========================================================================
    parser.add_argument('--terrain_first', default=False, action="store_true")
    parser.add_argument('--add_terrain', default=False, action="store_true")
    parser.add_argument('--initial_terrain_difficulty', type=float, default=0.01)
    parser.add_argument('--final_terrain_difficulty', type=float, default=0.5)
    parser.add_argument('--rand_dz_mult', type=float, default=0.01)
    parser.add_argument('--undul_patches', type=int, default=0)

    # ========================================================================
    # Map
    # ========================================================================
    parser.add_argument('--show_map', default=False, action="store_true")

    # ========================================================================
    # Height map
    # ========================================================================
    parser.add_argument('--hm_size', type=int, default=8)

    # ========================================================================
    # Way point
    # ========================================================================
    parser.add_argument("--wp_time_scalar", type=float, default=2.0)

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
        # args.max_ep_len = 256
    elif args.env == "franka_reach_pb":
        from assets.env_franka_pb import Env
    elif args.env == "anymal_mj":
        from assets.env_anymal_mj import Env    
        if args.tree_type == "tree":
            args.max_ep_len = 256
    elif args.env == "anymal_cmd_mj":
        from assets.env_anymal_cmd_mj import Env    
        args.control_type = "position"
    elif args.env == "anymal_is":
        from assets.env_anymal_is import Env    
    elif args.env == "anymal_is":
        from assets.env_anymal_is import Env   
        args.control_type = "position"
    elif args.env in ["titan_pb", "pumpkin_pb"]:
        from assets.env_titan_pb import Env
        args.control_type = "velocity"
    elif args.env == "titan_mj":
        from assets.env_titan_mj import Env
        args.control_type = "velocity"
        if args.tree_type == "grass":
            args.max_ep_len = 512
        elif args.tree_type == "tree":
            args.max_ep_len = 256
    elif args.env == "titan_is":
        from assets.env_titan_is import Env
        args.control_type = "velocity"
        args.max_ep_len = 256
    # TODOS:
    elif args.env == "bi_franka_mj":
        from assets.env_bi_franka_mj import Env
    elif args.env == "titan_gz":
        from assets.env_titan_gz import Env
    else:
        print("--env not in list of environments ", args.env); exit()

    if args.tree_type:
       args.local_epoch_len = 1024

    # args.test only loads simulator once, a bit nicer for debugging, but have to refresh for training else memory leak
    if "pb" in args.env and args.render:
        args.test = True    
    
    return Env, args