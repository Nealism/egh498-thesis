import numpy as np
import models.core as core

from default_arguments import get_defaults, get_env
from heterogeneous_expert import HeterogeneousExpert
from collect_rollouts import RolloutCollector, save_dataset
from pathlib import Path
from datetime import datetime



home = str(Path.home())
model_path_int = home + "/multi-robot-collision-avoidance" + "/Saved_models/Spot_Titan/selected/E13r32G1E1_104_Transfer_Hetero_85_BESTEST" + "/"
folder = "2025_02_12_16_12_53" # test folder



def parse_date():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")



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

    model_dir = model_path_int + folder

    core.args = args

    Env, args = get_env(args)

    env = Env(
        PATH=model_dir,
        args=args
    )

    expert = HeterogeneousExpert(
        model_path = model_dir + "/model.pt"
    )

    collector = RolloutCollector(
        env=env,
        expert=expert,
        max_ep_len=args.max_ep_len
    )

    dataset = collector.collect(n_episodes=50)
    if args.dataset_description:
        dataset_name = args.dataset_description + "_" + parse_date() + "_dataset.npz"
    else:
        dataset_name = "hetero_" + parse_date() + "_dataset.npz"

    save_dataset(dataset, "maviper/data/" + dataset_name)

    print("\nCollection Successful")

    for key, value in dataset.items():
        print(f"{key}: {np.asarray(value).shape}")


if __name__ == "__main__":
    main()
