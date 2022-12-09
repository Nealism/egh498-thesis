import numpy as np
import default_arguments

# Currently Isaac environments don't support loading one after another
# from isaacgym import gymtorch
# from isaacgym import gymapi
# from isaacgym.torch_utils import *
all_envs = [
            "humanoid_pb",
            "biped_pb",
            "franka_ball_mj",
            "franka_reach_mj",
            "franka_reach_dm_mj",
            "franka_reach_pb",
            "anymal_mj",
            # "anymal_is",
            "titan_pb", 
            "pumpkin_pb",
            "titan_mj",
            # "titan_is",
            ]

def test(args):
    args.max_ep_len = 50
    errors = []
    for env_name in all_envs:
        try:
            print("Testing ", env_name)
            # Simple test
            args.env = env_name
            Env, args = default_arguments.get_env(args) 
            env = Env(PATH=None, args=args)
            env.reset()
            while True:
                actions = np.random.uniform(-1,1, env.ac_size)
                obs, rew, done, _ = env.step(actions)
                if done or env.steps > env.args.max_ep_len:
                    break
            # Test restoring state
            save_state = env.get_env_state()
            restore_state = [env.pos, env.orn, env.joints]
            env.args.cur = False
            env.args.disturbances = False
            env.args.record_sim = False
            env.reset()
            done = False
            while True:
                actions = np.random.uniform(-1,1, env.ac_size)
                obs, rew, done, _ = env.step(actions)
                if done or env.steps > env.args.max_ep_len:
                    break
            success = env.get_success()
            env.reset(test=True, restore_state=restore_state)
            env.restore_env_state(save_state)
        except Exception as e:
            errors.append([env_name, e])
    
    print()
    print("==========================")
    print(len(errors), " errors:")
    print("==========================")
    for error in errors:
        print(error)

    print()
    print("==========================")
    print("Known errors:")
    print("==========================")
    print("mujoco_py: no default __reduce__ due to non-trivial __cinit__")
    print("PyBullet (need to investigate): Not connected to physics server.")

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    test(args)