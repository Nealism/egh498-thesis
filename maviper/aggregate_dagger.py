import os
import numpy as np
from datetime import datetime



DATASET_PATHS = [
    "maviper/data/dagger_exp9_2026_10_01_00_20_28_dataset.npz",
    "maviper/data/experiment9_dagger_round1_T0_exp9_beta0.25_2026_10_01_00_50_22_dataset.npz",
    "maviper/data/experiment9_D2_T1_exp9_beta0.25_2026_10_01_01_22_11_dataset.npz"
]

OUTPUT_DIR = "maviper/data/"

OUTPUT_NAME = "experiment9_dagger_aggregated_round2"



def parse_date():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def load_dataset(path):

    print(f"Loading: {path}")

    data = np.load(
        path,
        allow_pickle=True
    )

    return data

def aggregate_datasets(dataset_paths):

    titan_obs_all = []
    titan_actions_all = []

    spot_obs_all = []
    spot_actions_all = []

    titan_im_all = []
    spot_im_all = []

    episode_ids_all = []

    dataset_source_all = []

    episode_offset = 0


    for dataset_index, path in enumerate(dataset_paths):

        data = load_dataset(path)

        print(
            f"\nDataset {dataset_index}:"
        )

        print(
            f"  titan_obs: "
            f"{data['titan_obs'].shape}"
        )

        print(
            f"  titan_actions: "
            f"{data['titan_actions'].shape}"
        )

        print(
            f"  spot_obs: "
            f"{data['spot_obs'].shape}"
        )

        print(
            f"  spot_actions: "
            f"{data['spot_actions'].shape}"
        )


        titan_obs_all.append(
            data["titan_obs"]
        )

        titan_actions_all.append(
            data["titan_actions"]
        )

        spot_obs_all.append(
            data["spot_obs"]
        )

        spot_actions_all.append(
            data["spot_actions"]
        )



        if "titan_im" in data.files:
            titan_im_all.append(
                data["titan_im"]
            )

        if "spot_im" in data.files:
            spot_im_all.append(
                data["spot_im"]
            )


        # Each source dataset usually begins again at episode 0.
        # Shift them so every episode is globally unique.


        original_episode_ids = (
            data["episode_ids"]
            .astype(np.int64)
        )

        unique_original = np.unique(
            original_episode_ids
        )

        # Remap the IDs cleanly rather than assuming
        # they are perfectly consecutive.
        id_map = {
            old_id: new_id + episode_offset
            for new_id, old_id
            in enumerate(unique_original)
        }

        adjusted_episode_ids = np.asarray(
            [
                id_map[episode_id]
                for episode_id
                in original_episode_ids
            ],
            dtype=np.int64
        )

        episode_ids_all.append(
            adjusted_episode_ids
        )


        # ----------------------------------------------------
        # RECORD WHICH DATASET EACH TIMESTEP CAME FROM
        #
        # 0 = D0
        # 1 = D1
        # 2 = D2
        # etc.
        # ----------------------------------------------------

        dataset_source_all.append(
            np.full(
                len(original_episode_ids),
                dataset_index,
                dtype=np.int32
            )
        )


        # Increase offset for next dataset.
        episode_offset += len(
            unique_original
        )

        print(
            f"  episodes: "
            f"{len(unique_original)}"
        )

        print(
            f"  adjusted episode range: "
            f"{adjusted_episode_ids.min()} "
            f"to "
            f"{adjusted_episode_ids.max()}"
        )


    aggregated = {

        "titan_obs":
            np.concatenate(
                titan_obs_all,
                axis=0
            ),

        "titan_actions":
            np.concatenate(
                titan_actions_all,
                axis=0
            ),

        "spot_obs":
            np.concatenate(
                spot_obs_all,
                axis=0
            ),

        "spot_actions":
            np.concatenate(
                spot_actions_all,
                axis=0
            ),

        "episode_ids":
            np.concatenate(
                episode_ids_all,
                axis=0
            ),

        "dataset_source":
            np.concatenate(
                dataset_source_all,
                axis=0
            )
    }


    if len(titan_im_all) == len(dataset_paths):

        aggregated["titan_im"] = (
            np.concatenate(
                titan_im_all,
                axis=0
            )
        )

    if len(spot_im_all) == len(dataset_paths):

        aggregated["spot_im"] = (
            np.concatenate(
                spot_im_all,
                axis=0
            )
        )


    return aggregated

def save_aggregated_dataset(
    dataset,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    np.savez_compressed(
        output_path,
        **dataset
    )

    print(
        f"\nAggregated dataset saved to:"
    )

    print(
        output_path
    )


def main():

    dataset = aggregate_datasets(
        DATASET_PATHS
    )


    output_path = (
        OUTPUT_DIR
        + OUTPUT_NAME
        + "_"
        + parse_date()
        + "_dataset.npz"
    )


    save_aggregated_dataset(
        dataset,
        output_path
    )

    print(
        "\nFinal aggregated dataset:"
    )

    for key, value in dataset.items():

        print(
            f"{key}: "
            f"{np.asarray(value).shape}"
        )


    print(
        "\nUnique episodes:",
        len(
            np.unique(
                dataset["episode_ids"]
            )
        )
    )


    print(
        "Total timesteps:",
        len(
            dataset["episode_ids"]
        )
    )


if __name__ == "__main__":
    main()