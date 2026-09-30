import numpy as np
import joblib
import os
import csv


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from core.regression_dt import RegressionDTPolicy
from datetime import datetime

FEATURE_NAMES = [
    "waypoint_x",
    "waypoint_y",
    "roll",
    "pitch",
    "forward_velocity",
    "yaw_angular_velocity",
]

depths = range(1,50)

def save_to_csv(results):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_path = f"maviper/results/regression_trees_{timestamp}.csv"

    os.makedirs("maviper/results", exist_ok=True)

    if not results:
            print("No results to save")
            return
    
    fieldnames = results[0].keys()

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {output_path}")

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

    result = {
         "robot": name,
         "depth": tree.get_depth(),
         "nodes": tree.get_node_count(),
         "mae": mae,
         "mse": mse,
         "r2": r2
    }

    return result

def train_and_save_trees(
        name,
        titan_linear_depth,
        titan_angular_depth,

        spot_linear_depth,
        spot_lateral_depth,
        spot_angular_depth,

        titan_x_train,
        titan_linear_y_train,
        titan_angular_y_train,

        spot_x_train,
        spot_linear_y_train,
        spot_lateral_y_train,
        spot_angular_y_train
):
    titan_linear_tree = RegressionDTPolicy(max_depth=titan_linear_depth)
    titan_angular_tree = RegressionDTPolicy(max_depth=titan_angular_depth)
    spot_linear_tree = RegressionDTPolicy(max_depth=spot_linear_depth)
    spot_lateral_tree = RegressionDTPolicy(max_depth=spot_lateral_depth)
    spot_angular_tree = RegressionDTPolicy(max_depth=spot_angular_depth)


    titan_linear_tree.train(titan_x_train, titan_linear_y_train)
    titan_angular_tree.train(titan_x_train, titan_angular_y_train)
    spot_linear_tree.train(spot_x_train, spot_linear_y_train)
    spot_lateral_tree.train(spot_x_train, spot_lateral_y_train)
    spot_angular_tree.train(spot_x_train, spot_angular_y_train)



    output_dir = f"maviper/saved_trees/{name}"
    os.makedirs(output_dir, exist_ok=True)

    # joblib.dump(titan_tree, f"{output_dir}/titan_tree.joblib")
    # joblib.dump(spot_tree, f"{output_dir}/spot_tree.joblib")

    joblib.dump(titan_linear_tree, f"{output_dir}/titan_linear_tree.joblib")
    joblib.dump(titan_angular_tree, f"{output_dir}/titan_angular_tree.joblib")
    joblib.dump(spot_linear_tree, f"{output_dir}/spot_linear_tree.joblib")
    joblib.dump(spot_lateral_tree, f"{output_dir}/spot_lateral_tree.joblib")
    joblib.dump(spot_angular_tree, f"{output_dir}/spot_angular_tree.joblib")
    print(f"Saved {name}")


def main():
    dataset_path = "maviper/data/experiment5_2026_09_27_01_23_32_dataset.npz" # TODO: come back to this

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
    titan_x_test = titan_obs[test_mask]

    titan_linear_y_train = titan_actions[train_mask, 0]
    titan_linear_y_test = titan_actions[test_mask, 0]

    titan_angular_y_train = titan_actions[train_mask, 1]
    titan_angular_y_test = titan_actions[test_mask, 1]

    spot_x_train = spot_obs[train_mask]
    spot_x_test = spot_obs[test_mask]

    spot_linear_y_train = spot_actions[train_mask, 0]
    spot_linear_y_test = spot_actions[test_mask, 0]

    spot_lateral_y_train = spot_actions[train_mask, 1]
    spot_lateral_y_test = spot_actions[test_mask, 1]

    spot_angular_y_train = spot_actions[train_mask, 2]
    spot_angular_y_test = spot_actions[test_mask, 2]


  

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

    # results = []

    # for depth in depths:

    #     titan_linear_tree = RegressionDTPolicy(max_depth=depth)
    #     titan_angular_tree = RegressionDTPolicy(max_depth=depth)
    #     spot_linear_tree = RegressionDTPolicy(max_depth=depth)
    #     spot_lateral_tree = RegressionDTPolicy(max_depth=depth)
    #     spot_angular_tree = RegressionDTPolicy(max_depth=depth)

    #     titan_linear_tree.train(titan_x_train, titan_linear_y_train)
    #     titan_angular_tree.train(titan_x_train, titan_angular_y_train)
    #     spot_linear_tree.train(spot_x_train, spot_linear_y_train)
    #     spot_lateral_tree.train(spot_x_train, spot_lateral_y_train)
    #     spot_angular_tree.train(spot_x_train, spot_angular_y_train)

    #     result_tl = evaluate_tree(
    #          "Titan_Linear",
    #          titan_linear_tree,
    #          titan_x_test,
    #          titan_linear_y_test
    #     )

    #     result_ta = evaluate_tree(
    #          "Titan_Angular",
    #          titan_angular_tree,
    #          titan_x_test,
    #          titan_angular_y_test
    #     )

    #     result_sl = evaluate_tree(
    #          "Spot_Linear",
    #          spot_linear_tree,
    #          spot_x_test,
    #          spot_linear_y_test
    #     )

    #     result_sla = evaluate_tree(
    #          "Spot_Lateral",
    #          spot_lateral_tree,
    #          spot_x_test,
    #          spot_lateral_y_test
    #     )

    #     result_sa = evaluate_tree(
    #          "Spot_Angular",
    #          spot_angular_tree,
    #          spot_x_test,
    #          spot_angular_y_test
    #     )
    #     results.append(result_tl)
    #     results.append(result_ta)
    #     results.append(result_sl)
    #     results.append(result_sla)
    #     results.append(result_sa)

    # save_to_csv(results)


    train_and_save_trees("low_exp5",
                          2, # Titan linear
                          2, # Titan angular
                          2, # Spot linear
                          3, # Spot lateral
                          3, # Spot angular
                          titan_x_train,
                          titan_linear_y_train,
                          titan_angular_y_train,
                          spot_x_train,
                          spot_linear_y_train,
                          spot_lateral_y_train,
                          spot_angular_y_train)

    train_and_save_trees("mid_exp5",
                        4, # Titan linear
                        4, # Titan angular
                        5, # Spot linear
                        6, # Spot lateral
                        7, # Spot angular
                        titan_x_train,
                        titan_linear_y_train,
                        titan_angular_y_train,
                        spot_x_train,
                        spot_linear_y_train,
                        spot_lateral_y_train,
                        spot_angular_y_train)

    train_and_save_trees("high_exp5",
                        11, # Titan linear
                        12, # Titan angular
                        8, # Spot linear
                        11, # Spot lateral
                        14, # Spot angular
                        titan_x_train,
                        titan_linear_y_train,
                        titan_angular_y_train,
                        spot_x_train,
                        spot_linear_y_train,
                        spot_lateral_y_train,
                        spot_angular_y_train)

    train_and_save_trees("of_exp5",
                    25, # Titan linear
                    25, # Titan angular
                    30, # Spot linear
                    30, # Spot lateral
                    30, # Spot angular
                    titan_x_train,
                    titan_linear_y_train,
                    titan_angular_y_train,
                    spot_x_train,
                    spot_linear_y_train,
                    spot_lateral_y_train,
                    spot_angular_y_train)

    # train_and_save_pair("depth4_e_exp4", 4,4, titan_x_train, titan_y_train, spot_x_train, spot_y_train)
    # train_and_save_pair("depth8_e_exp4", 8,8, titan_x_train, titan_y_train, spot_x_train, spot_y_train)
    # train_and_save_pair("high_fidelity_e_exp4", 9,10, titan_x_train, titan_y_train, spot_x_train, spot_y_train) # 10 and 9 had the highest r2 values for titan and spot respectively for Random-Timestep, 6 and 9 for Episodic Split

    # print("\nTitan Rules:")
    # print(titan_tree.export_rules(FEATURE_NAMES))

    # print("\nSpot Rules:")
    # print(spot_tree.export_rules(FEATURE_NAMES))


if __name__ == '__main__':
    main()