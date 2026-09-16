import numpy as np
import joblib
import os


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from core.regression_dt import RegressionDTPolicy

FEATURE_NAMES = [
    "waypoint_x",
    "waypoint_y",
    "roll",
    "pitch",
    "forward_velocity",
    "yaw_angular_velocity",
]

def evaluate_tree(name, tree, x_test, y_test):
    predictions = tree.predict(x_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"Evaluation for {name}:")
    print(f"Depth: {tree.get_depth()}")
    print(f"Nodes: {tree.get_node_count()}")
    print(f"MAE: {mae:.6f}")
    print(f"MSE: {mse:.6f}")
    print(f"R2: {r2:.6f}")

def train_and_save_pair(
        name,
        titan_depth,
        spot_depth,
        titan_x_train,
        titan_y_train,
        spot_x_train,
        spot_y_train
):
    titan_tree = RegressionDTPolicy(max_depth=titan_depth)
    spot_tree = RegressionDTPolicy(max_depth=spot_depth)

    titan_tree.train(titan_x_train, titan_y_train)
    spot_tree.train(spot_x_train, spot_y_train)

    output_dir = f"maviper/saved_trees/{name}"
    os.makedirs(output_dir, exist_ok=True)

    joblib.dump(titan_tree, f"{output_dir}/titan_tree.joblib")
    joblib.dump(spot_tree, f"{output_dir}/spot_tree.joblib")
    print(f"Saved {name}")


def main():
    dataset_path = "maviper/data/episode_ids_2026_09_09_13_37_24_dataset.npz" # TODO: come back to this

    data = np.load(dataset_path)

    titan_obs = data["titan_obs"]
    titan_actions = data["titan_actions"]
    spot_obs = data["spot_obs"]
    spot_actions = data["spot_actions"]
    episode_ids = data["episode_ids"]
    unique_episodes = np.unique(episode_ids)

    train_episodes, test_episodes = train_test_split(
        unique_episodes,
        test_size=0.2,
        random_state=42
    )

    train_mask = np.isin(episode_ids, train_episodes)
    test_mask = np.isin(episode_ids, test_episodes)

    titan_x_train = titan_obs[train_mask]
    titan_y_train = titan_actions[train_mask]

    titan_x_test = titan_obs[test_mask]
    titan_y_test = titan_actions[test_mask]

    spot_x_train = spot_obs[train_mask]
    spot_y_train = spot_actions[train_mask]

    spot_x_test = spot_obs[test_mask]
    spot_y_test = spot_actions[test_mask]

    # titan_x_train, titan_x_test, titan_y_train, titan_y_test = train_test_split(
    #     titan_obs,
    #     titan_actions,
    #     test_size=0.2,
    #     random_state=42
    # )

    # spot_x_train, spot_x_test, spot_y_train, spot_y_test = train_test_split(
    #     spot_obs,
    #     spot_actions,
    #     test_size=0.2,
    #     random_state=42
    # )

    titan_tree = RegressionDTPolicy(max_depth=4)
    spot_tree = RegressionDTPolicy(max_depth=4)

    titan_tree.train(titan_x_train, titan_y_train)
    spot_tree.train(spot_x_train, spot_y_train)

    evaluate_tree(
        "Titan",
        titan_tree,
        titan_x_test,
        titan_y_test
    )

    evaluate_tree(
        "Spot",
        spot_tree,
        spot_x_test,
        spot_y_test
    )

    train_and_save_pair("depth4_e", 4,4, titan_x_train, titan_y_train, spot_x_train, spot_y_train)
    train_and_save_pair("depth6_e", 6,6, titan_x_train, titan_y_train, spot_x_train, spot_y_train)
    train_and_save_pair("high_fidelity_e", 6,9, titan_x_train, titan_y_train, spot_x_train, spot_y_train) # 10 and 9 had the highest r2 values for titan and spot respectively for Random-Timestep, 6 and 9 for Episodic Split

    # print("\nTitan Rules:")
    # print(titan_tree.export_rules(FEATURE_NAMES))

    # print("\nSpot Rules:")
    # print(spot_tree.export_rules(FEATURE_NAMES))


if __name__ == '__main__':
    main()