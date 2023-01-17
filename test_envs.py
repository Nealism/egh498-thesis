import numpy as np
import os
from pathlib import Path
home = str(Path.home())

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
            "anymal_cmd_mj",
            # "anymal_mj_isaac",
            # "anymal_is",
            "titan_pb", 
            "pumpkin_pb",
            "titan_mj",
            # "titan_is",
            ]

def test(args):
    SAVE_PATH = "/scratch1/" + home.split("/")[-1] + "/results/"
    PATH = SAVE_PATH + args.env + "/test/test/"
    if not os.path.exists(PATH):
        os.mkdirs(PATH)
    errors = {env:[] for env in all_envs}
    test_error = {env:[] for env in all_envs}
    for i in ["Initial", "Perception", "Position Control", "Torque Control", "Grass", "Trees"]:
        print("================================================")
        print("Testing " + i + ":")
        print("================================================")
        for env_name in all_envs:
            try:
                args.env = env_name
                Env, args = default_arguments.get_env(args) 
                if i in ["Grass", "Trees"] and "mj" not in args.env:
                    continue
                if i in ["Position Control", "Torque Control"] and "anymal" not in args.env:
                    continue
                if i == "Perception":
                    args.use_perception = True
                elif i == "Position Control":
                    args.control_type = "position"
                elif i == "Torque Control":
                    args.control_type = "torque"
                elif i == "Grass":
                    args.tree_type = "grass"
                elif i == "Trees":
                    args.tree_type = "tree"
                print("Testing ", env_name)
                args.max_ep_len = 50
                env = Env(PATH=PATH, args=args)
                env.reset()
                if args.use_perception:
                    im = env.get_image()
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
                if str(e) not in errors[env_name]:
                    errors[env_name].append(str(e))
                    test_error[env_name].append(i)
    print()
    print("==========================")
    print(sum([len(errors[env]) for env in errors]), " errors:")
    print("==========================")
    for error in errors:
        if errors[error]:
            print(error, ": ", [(e,z) for e,z in zip(test_error[error], errors[error])])

    print()
    print("==========================")
    print("Known errors: ")
    print("==========================")
    print("mujoco_py: no default __reduce__ due to non-trivial __cinit__")
    print("PyBullet (need to investigate): Not connected to physics server.")

if __name__=="__main__":
    args = default_arguments.get_defaults() 
    test(args)