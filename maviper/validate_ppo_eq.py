import numpy as np
import torch
import random
from pathlib import Path


import models.core as core

from default_arguments import get_defaults, get_env
from heterogeneous_expert import HeterogeneousExpert

home = str(Path.home())

model_path_int = (
    home
    + "/multi-robot-collision-avoidance/"
    + "Saved_models/Spot_Titan/selected/"
    + "E13r32G1E1_104_Transfer_Hetero_85_BESTEST/"
)

folder = "2025_02_12_16_12_53"

model_dir = model_path_int + folder

SEED = 42
NUM_STEPS = 20

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def create_env(seed):

    set_seed(seed)

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
    args.render = False

    core.args = args

    Env, args = get_env(args)

    env = Env(
        PATH=model_dir,
        args=args
    )

    obs = env.reset()

    return env, obs, args

def main():

    env,obs,args = create_env(SEED)

    direct_model = torch.load(
        model_dir + "/model.pt",
        weights_only=False
    )

    direct_model.eval()

    expert = HeterogeneousExpert(
        model_path=model_dir+"/model.pt"
    )

    print("Comparison of direct PPO against trained expert")
    print("="*50)

    max_titan_difference = 0.0
    max_spot_difference = 0.0

    for step in range(NUM_STEPS):
        im = env.get_image()

        model_obs = [
            np.insert(obs[0],0,0),
            np.insert(obs[1],0,1)
        ]

        obs_tensor = torch.as_tensor(
            np.asarray(model_obs),
            dtype=torch.float32
        )

        im_tensor = torch.as_tensor(
            np.asarray(im),
            dtype=torch.float32
        )

        # direct PPO
        with torch.no_grad():

            direct_output = direct_model.step(
                obs_tensor,
                im_tensor,
                stochastic=False
            )

        direct_spot_actions = direct_output[0]
        direct_titan_actions = direct_output[1]

        # expert wrapped PPO
        wrapped_actions, _, _ = expert.act(
            model_obs,
            im
        )

        if step == 0:
            print("\nRaw Direct Output:")
            print(direct_output)

            print("\nTitan Direct Actions")
            print(direct_titan_actions)

            print("\nSpot Direct Actions")
            print(direct_spot_actions)

            print("\nWrapped Actions:")
            print(wrapped_actions)

            print("\n" + "="*50)

        try:

            direct_titan = np.asarray(
                direct_titan_actions[0],
                dtype=np.float32
            )

            direct_spot = np.asarray(
                direct_spot_actions[1],
                dtype=np.float32
            )

            wrapped_titan = np.asarray(
                wrapped_actions[0],
                dtype=np.float32
            )

            wrapped_spot = np.asarray(
                wrapped_actions[1],
                dtype=np.float32
            )


            titan_diff = np.abs(
                direct_titan - wrapped_titan
            )

            spot_diff = np.abs(
                direct_spot - wrapped_spot
            )


            max_titan_difference = max(
                max_titan_difference,
                float(np.max(titan_diff))
            )

            max_spot_difference = max(
                max_spot_difference,
                float(np.max(spot_diff))
            )


            print(
                f"\nStep {step + 1}"
            )

            print(
                f"Titan direct : {direct_titan}"
            )

            print(
                f"Titan wrapper: {wrapped_titan}"
            )

            print(
                f"Titan diff   : {titan_diff}"
            )

            print()

            print(
                f"Spot direct  : {direct_spot}"
            )

            print(
                f"Spot wrapper : {wrapped_spot}"
            )

            print(
                f"Spot diff    : {spot_diff}"
            )


        except Exception as e:

            print(
                "\nCould not automatically compare "
                "the direct PPO output."
            )

            print("Error:", e)

            print(
                "\nSend me the RAW DIRECT OUTPUT "
                "printed above and we can map it correctly."
            )

            env._p.disconnect()
            return


        # =====================================
        # Advance environment using DIRECT PPO
        # =====================================

        actions = [
            direct_titan,
            direct_spot
        ]

        expert_acs = np.zeros(
            (2, 2),
            dtype=np.float32
        )

        obs, rewards, dones, terminations, info = env.step(
            actions,
            expert_acs
        )

        if all(dones) or all(terminations):
            print("\nEpisode terminated.")
            break


    print("\n" + "=" * 80)

    print(
        f"Maximum Titan difference: "
        f"{max_titan_difference}"
    )

    print(
        f"Maximum Spot difference: "
        f"{max_spot_difference}"
    )

    env._p.disconnect()


if __name__ == "__main__":
    main()