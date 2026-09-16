import numpy as np
import joblib
import models.core as core

from pathlib import Path
from default_arguments import get_defaults, get_env

home = str(Path.home())

model_path_int = home + "/multi-robot-collision-avoidance" + "/Saved_models/Spot_Titan/selected/E13r32G1E1_104_Transfer_Hetero_85_BESTEST" + "/"
folder = "2025_02_12_16_12_53" # test folder

tree_path = "maviper/saved_trees/"

def main():
    args = get_defaults()

    args.env = "multi_robot_pb"
    args.num_robots = 2
    args.cur_succ = 0
    args.gap_avoidance = True
    args.insert_wall = True
    args.occupancy_map = True
    args.use_perception = True
    args.experiment_1 = True
    args.heterogeneous = True
    args.gap_curr = True
    args.starting_gap_width = 0.85
    args.randomness = 2
    args.reward_fn = 27
    args.Pretrained_cur = False
    args.max_ep_len = 200

    args.render = True # for gui

    model_dir = model_path_int + folder

    core.args = args
    Env, args = get_env(args)

    env = Env(
        PATH=model_dir,
        args = args
    )

    titan_tree = joblib.load(tree_path + "high_fidelity_e/titan_tree.joblib")
    spot_tree = joblib.load(tree_path + "high_fidelity_e/spot_tree.joblib")

    obs = env.reset()

    total_reward = 0.0

    for step in range(args.max_ep_len):
        titan_action = titan_tree.predict(obs[0])[0]
        spot_action = spot_tree.predict(obs[1])[0]

        actions = [titan_action, spot_action]

        expert_acs = np.zeros((2,2), dtype=np.float32) # required by env.step, unused because pretrained_cur is false

        obs, rewards, dones, terminations, info = env.step(actions, expert_acs)

        total_reward += float(np.sum(rewards))

        print(
            f"Step {step} | "
            f"Titan Action: {titan_action} | "
            f"Spot Action: {spot_action} | "
            f"Reward: {rewards} | "
            f"Dones: {dones} | "
            f"Terminations: {terminations}"
        )

        if all(dones) or all(terminations):
            print(
                f"Episode Finished | "
                f"Dones: {dones} | "
                f"Terminations: {terminations}"
            )
            break


    print(f"\nSteps: {step+1}")
    print(f"Total reward: {total_reward:.3f}")

if __name__ == "__main__":
    main()