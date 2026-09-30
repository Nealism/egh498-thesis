import numpy as np
import models.core as core
import torch

from default_arguments import get_defaults, get_env
from heterogeneous_expert import HeterogeneousExpert
from collect_rollouts import RolloutCollector, save_dataset
from pathlib import Path
from datetime import datetime
import random
import os
import csv

from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

NUM_EPISODES = 200
master_seed = 3500614 # DO NOT CHANGE THIS UNLESS WANT TO CHANGE ROLLOUT SEEDS  (6767420, exp5 - 8. 3500614 exp9 -)

MAX_WORKERS = 12

rollout_rng = random.Random(master_seed)

rollout_seeds = [rollout_rng.randint(0, 2**32-1) for _ in range(NUM_EPISODES)]

def save_seeds_to_csv(seeds):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    output_path = f"maviper/rollout_data/experiment9/rollout_seeds_{timestamp}.csv"

    os.makedirs("maviper/rollout_data/experiment9", exist_ok=True)


    with open(output_path, "w", newline="") as csvfile_seed:
        writer = csv.writer(csvfile_seed)

        writer.writerow(["seed"])

        for seed in seeds:
            writer.writerow([seed])


    print(f"\Seeds saved to {output_path}")



home = str(Path.home())
# selected_model = "400182_E2_2025_06_06_12_53_28"
# model_path_int = home + "/multi-robot-collision-avoidance" + "/Saved_models/Spot_Titan/selected/"# + selected_model + "/"
# # folder = "2025_02_12_16_12_53" # test folder

# folder = "400182_E2_2025_06_06_12_53_28"


# \\wsl.localhost\Ubuntu-24.04\home\nealism\multi-robot-collision-avoidance\Saved_models\Spot_Titan\Full_Train_0.85_200207E10_53
model_path_int = (
    home
    + "/multi-robot-collision-avoidance/"
    + "Saved_models/Spot_Titan/selected/"
    + "E13r32G1E1_104_Transfer_Hetero_85_BESTEST/"
)

folder = "2025_02_12_16_12_53"

# model_path_int = (
#     home 
#     + "/multi-robot-collision-avoidance"
#     + "/Saved_models/Spot_Titan/"
# )
# folder = "Full_Train_0.85_200207E10_53"


def parse_date():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def collect_chunk(episode_start, seeds):
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

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
    args.starting_gap_width = 1.0
    args.randomness = 2
    args.reward_fn = 27
    args.Pretrained_cur = False
    args.max_ep_len = 200

    args.render = False

    model_dir = model_path_int + folder

    core.args = args

    Env, args = get_env(args)

    env = Env(
        PATH=model_dir,
        args=args
    )

    expert = HeterogeneousExpert(
        model_path = model_dir + "/model.pt" # check here for slash, not always included 
    )

    collector = RolloutCollector(
        env=env,
        expert=expert,
        max_ep_len=args.max_ep_len
    )

    dataset = collector.collect(
        n_episodes=len(seeds),
        seeds=seeds
    )

    dataset["episode_ids"] = dataset["episode_ids"] + episode_start

    env._p.disconnect()

    return episode_start, dataset



def main():
    args = get_defaults()

    indexed_seeds = list(enumerate(rollout_seeds))

    chunks = np.array_split(
        indexed_seeds,
        MAX_WORKERS
    )

    worker_inputs = []

    for chunk in chunks:
        if len(chunk) == 0:
            continue

        episode_start = int(chunk[0][0])

        seeds = [
            int(seed)
            for _, seed in chunk
        ]

        worker_inputs.append(
            (episode_start, seeds)
        )

    datasets = []

    ctx = mp.get_context("spawn")

    with ProcessPoolExecutor(
        max_workers=MAX_WORKERS,
        mp_context=ctx
    ) as executor:

        futures = {
            executor.submit(
                collect_chunk,
                episode_start,
                seeds
            ): episode_start
            for episode_start, seeds in worker_inputs
        }

        completed = 0

        for future in as_completed(futures):
            episode_start = futures[future]

            try:
                result = future.result()

            except Exception as e:
                print(f"Chunk starting at episode {episode_start} FAILED:")
                print(e)
                raise

            datasets.append(result)

            completed += 1

            print(
                f"Completed chunk {completed} of {len(worker_inputs)}"
            )

    datasets.sort(
        key=lambda x: x[0]
    )

    dataset = {}

    for key in datasets[0][1].keys():
        dataset[key] = np.concatenate(
            [
                chunk_dataset[key]
                for _, chunk_dataset in datasets
            ],
            axis=0
        )

    if args.dataset_description:
        dataset_name = args.dataset_description + "_" + parse_date() + "_dataset.npz"
    else:
        dataset_name = "hetero_" + parse_date() + "_dataset.npz"

    save_dataset(dataset, "maviper/data/" + dataset_name)
    save_seeds_to_csv(rollout_seeds)

    print("\nCollection Successful")

    for key, value in dataset.items():
        print(f"{key}: {np.asarray(value).shape}")


if __name__ == "__main__":
    main()