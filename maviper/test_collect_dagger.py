import random
import joblib
import models.core as core
import numpy as np
import torch

from pathlib import Path
from datetime import datetime

from default_arguments import get_defaults, get_env
from heterogeneous_expert import HeterogeneousExpert
from collect_dagger import DAggerCollector, save_dataset

from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp



home = str(Path.home())

model_path_int = (
    home
    + "/multi-robot-collision-avoidance/"
    + "Saved_models/Spot_Titan/selected/"
    + "E13r32G1E1_104_Transfer_Hetero_85_BESTEST/"
)

folder = "2025_02_12_16_12_53"

model_dir = model_path_int + folder


TREE_NAME = "T1_exp9"

tree_path = "maviper/saved_trees/" + TREE_NAME + "/"

titan_tree_path = tree_path + "titan_tree.joblib"
spot_tree_path = tree_path + "spot_tree.joblib"



N_EPISODES = 200

# Probability that PPO controls at each step.
#
# 1.0 = PPO always controls
# 0.5 = PPO controls 50% of steps
# 0.0 = tree always controls
BETA = 0.25


DAGGER_MASTER_SEED = 98765

DAGGER_ROUND = 2

MAX_WORKERS = 12


def parse_date():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def generate_dagger_seeds(
    n_episodes,
    master_seed
):

    rng = random.Random(
        master_seed
    )

    seeds = [
        rng.randint(
            0,
            2**32 - 1
        )
        for _ in range(n_episodes)
    ]

    return seeds


def collect_chunk(
    episode_start,
    seeds
):

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

    core.args = args


    Env, args = get_env(args)

    env = Env(
        PATH=model_dir,
        args=args
    )


    expert = HeterogeneousExpert(
        model_path=model_dir + "/model.pt"
    )


    titan_tree = joblib.load(
        titan_tree_path
    )

    spot_tree = joblib.load(
        spot_tree_path
    )


    collector = DAggerCollector(
        env=env,
        expert=expert,
        titan_tree=titan_tree,
        spot_tree=spot_tree,
        max_ep_len=args.max_ep_len
    )


    dataset = collector.collect(
        n_episodes=len(seeds),
        seeds=seeds,
        beta=BETA
    )


    dataset["episode_ids"] = (
        dataset["episode_ids"]
        + episode_start
    )


    try:
        env._p.disconnect()
    except Exception:
        pass


    return (
        episode_start,
        dataset
    )



def main():


    dagger_seeds = generate_dagger_seeds(
        n_episodes=N_EPISODES,
        master_seed=DAGGER_MASTER_SEED
    )

    print(
        f"\nGenerated {len(dagger_seeds)} "
        f"DAgger seeds."
    )

    print(
        f"Master seed: "
        f"{DAGGER_MASTER_SEED}"
    )

    print(
        f"First 5 seeds: "
        f"{dagger_seeds[:5]}"
    )


    print(
        f"\nStarting DAgger Round "
        f"{DAGGER_ROUND}"
    )

    print(
        f"Tree: {TREE_NAME}"
    )

    print(
        f"Episodes: {N_EPISODES}"
    )

    print(
        f"Beta: {BETA}"
    )

    print(
        "\nRemember:"
    )

    print(
        "Tree/PPO mixture controls the robot, "
        "but PPO actions are always saved "
        "as the training labels."
    )


    indexed_seeds = list(
        enumerate(dagger_seeds)
    )

    chunks = np.array_split(
        indexed_seeds,
        MAX_WORKERS
    )

    worker_inputs = []

    for chunk in chunks:

        if len(chunk) == 0:
            continue

        episode_start = int(
            chunk[0][0]
        )

        seeds = [
            int(seed)
            for _, seed in chunk
        ]

        worker_inputs.append(
            (
                episode_start,
                seeds
            )
        )


    datasets = []

    ctx = mp.get_context(
        "spawn"
    )


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
            for episode_start, seeds
            in worker_inputs
        }


        completed = 0


        for future in as_completed(
            futures
        ):

            episode_start = futures[
                future
            ]

            try:

                result = future.result()

            except Exception as e:

                print(
                    f"Chunk starting at episode "
                    f"{episode_start} FAILED:"
                )

                print(e)

                raise


            datasets.append(
                result
            )

            completed += 1

            print(
                f"Completed chunk "
                f"{completed} of "
                f"{len(worker_inputs)}"
            )


    datasets.sort(
        key=lambda x: x[0]
    )


    dataset = {}


    for key in datasets[0][1].keys():

        dataset[key] = np.concatenate(
            [
                chunk_dataset[key]
                for _, chunk_dataset
                in datasets
            ],
            axis=0
        )


    dataset["dagger_seeds"] = np.asarray(
        dagger_seeds,
        dtype=np.uint32
    )

    dataset["beta"] = np.asarray(
        [BETA],
        dtype=np.float32
    )

    dataset["dagger_round"] = np.asarray(
        [DAGGER_ROUND],
        dtype=np.int32
    )

    dataset["source_tree"] = np.asarray(
        [TREE_NAME]
    )

    dataset["dagger_master_seed"] = np.asarray(
        [DAGGER_MASTER_SEED],
        dtype=np.uint32
    )


    dataset_name = (
        f"experiment9_"
        f"D{DAGGER_ROUND}_"
        f"{TREE_NAME}_"
        f"beta{BETA}_"
        f"{parse_date()}_dataset.npz"
    )

    output_path = (
        "maviper/data/"
        + dataset_name
    )

    save_dataset(
        dataset,
        output_path
    )


    print(
        "\nDAgger collection successful."
    )

    print(
        f"Saved to:"
    )

    print(
        output_path
    )

    print(
        "\nDataset contents:"
    )

    for key, value in dataset.items():

        try:
            shape = value.shape
        except AttributeError:
            shape = (
                len(value)
                if hasattr(value, "__len__")
                else "scalar"
            )

        print(
            f"{key}: {shape}"
        )


if __name__ == "__main__":
    main()