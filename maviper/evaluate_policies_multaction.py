import numpy as np
import joblib
import torch
import random
import models.core as core
import warnings
import os
import sys
import csv

from pathlib import Path
from contextlib import contextmanager
from datetime import datetime
from default_arguments import get_defaults, get_env
from heterogeneous_expert import HeterogeneousExpert

from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

home = str(Path.home())
# selected_model = "400182_E2_2025_06_06_12_53_28"
# model_path_int = home + "/multi-robot-collision-avoidance" + "/Saved_models/Spot_Titan/selected/"# + selected_model + "/"
# # folder = "2025_02_12_16_12_53" # test folder

# folder = "400182_E2_2025_06_06_12_53_28"

model_path_int = (
    home
    + "/multi-robot-collision-avoidance/"
    + "Saved_models/Spot_Titan/selected/"
    + "E13r32G1E1_104_Transfer_Hetero_85_BESTEST/"
)

folder = "2025_02_12_16_12_53"

tree_path = "maviper/saved_trees/"

#SEEDS = range(50)

random_SEEDS = []

x = 0
seed_count = 200
while x < seed_count: # seed count
    random_SEEDS.append(random.randint(0, 2**32-1))
    x += 1


POLICIES = [
    "ppo",
    "low_exp5",
    "mid_exp5",
    "high_exp5",
    "of_exp5",
    # "depth4_e_exp3",
    # "depth8_e_exp3", 
    # "high_fidelity_e_exp3",
]


def open_seeds():
    test_seeds = []
    with open("maviper/results/experiment4/experimental_seeds_2026_09_24_15_10_24.csv", 'r') as seeds: #TODO: CHANGE THIS

        for row in csv.reader(seeds):
            if row[0] == 'seed':
                continue
            else:
                test_seeds.append(int(row[0]))

    return test_seeds


warnings.filterwarnings("ignore")
@contextmanager
def suppress_output():
    with open(os.devnull, "w") as devnull:
        old_stdout_fd = os.dup(1)
        old_stderr_fd = os.dup(2)

        try:
            os.dup2(devnull.fileno(), 1)
            os.dup2(devnull.fileno(), 2)
            yield
        finally:
            os.dup2(old_stdout_fd, 1)
            os.dup2(old_stderr_fd, 2)
            os.close(old_stdout_fd)
            os.close(old_stderr_fd)

def save_to_csv(results, seeds):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    output_path = f"maviper/results/experiment7/policy_evaluation_{timestamp}.csv"
    seed_path = f"maviper/results/experiment7/experimental_seeds_{timestamp}.csv"

    os.makedirs("maviper/results/experiment7", exist_ok=True)

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

    with open(seed_path, "w", newline="") as csvfile_seed:
        writer = csv.writer(csvfile_seed)

        writer.writerow(["seed"])

        for seed in seeds:
            writer.writerow([seed])


    print(f"\nResults saved to {output_path}")


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

def run_seed(seed):
    torch.set_num_threads(1) # prevents pytorch from spawning lots of CPU threads itself

    seed_results = []

    for policy_name in POLICIES:
        with suppress_output():
            result = run_policy(
                seed=seed,
                policy_name=policy_name
            )

        seed_results.append(result)

    return seed, seed_results


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
    args.starting_gap_width = 1
    args.randomness = 2
    args.reward_fn = 27
    args.Pretrained_cur = False
    args.max_ep_len = 200

    args.render = False # for gui

    model_dir = model_path_int + folder

    core.args = args
    Env, args = get_env(args)

    env = Env(
        PATH=model_dir,
        args = args
    )

    obs = env.reset()

    return env, obs, args, model_dir

def load_tree_policy(tree_name):

    titan_linear_tree = joblib.load(tree_path+tree_name+"/titan_linear_tree.joblib")
    titan_angular_tree = joblib.load(tree_path+tree_name+"/titan_angular_tree.joblib")
    spot_linear_tree = joblib.load(tree_path+tree_name+"/spot_linear_tree.joblib")
    spot_lateral_tree = joblib.load(tree_path+tree_name+"/spot_lateral_tree.joblib")
    spot_angular_tree = joblib.load(tree_path+tree_name+"/spot_angular_tree.joblib")

    return titan_linear_tree, titan_angular_tree, spot_linear_tree, spot_lateral_tree, spot_angular_tree

def load_ppo_policy(model_dir):
    return HeterogeneousExpert(model_path=model_dir + "/model.pt")

def valid_initial_conditions(env):
    for robot in env.robots:
        robot_collision = bool(robot.intersection_r1_r)
        wall_collision = bool(np.asarray(robot.contacts).any())
        tipped = bool(robot.tipped)

        if robot_collision or wall_collision or tipped:
            return False
    return True

def check_seed_validity():
    for seed in random_SEEDS:
            env, obs, args, model_dir = create_env(seed)
            valid = valid_initial_conditions(env)
            print(f"Seed: {seed}, validity: {valid}")

def check_first_step_conditions():
    for seed in random_SEEDS:
        with suppress_output():
            env, obs, args, model_dir = create_env(seed)

        # Keep perception call consistent with normal evaluation
        im = env.get_image()

        zero_actions = [
            np.zeros(2, dtype=np.float32),  # Titan
            np.zeros(3, dtype=np.float32),  # Spot
        ]

        expert_acs = np.zeros((2, 2), dtype=np.float32)

        obs, rewards, dones, terminations, info = env.step(
            zero_actions,
            expert_acs
        )

        print(
            f"Seed {seed} | "
            f"Dones: {dones} | "
            f"Rewards: {rewards} | "
            f"Titan contact: {np.asarray(env.robots[0].contacts).any()} | "
            f"Spot contact: {np.asarray(env.robots[1].contacts).any()} | "
            f"Robot collision: "
            f"{env.robots[0].intersection_r1_r or env.robots[1].intersection_r1_r}"
        )

        env._p.disconnect()

def run_policy(seed, policy_name):

    

    env, obs, args, model_dir = create_env(seed)

    if not valid_initial_conditions(env):
        return {
            "seed": seed,
            "policy": policy_name,
            "valid_scenario": False,
        }
    expert = load_ppo_policy(model_dir)

    if policy_name != "ppo":
        titan_linear_tree, titan_angular_tree, spot_linear_tree, spot_lateral_tree, spot_angular_tree = load_tree_policy(policy_name)

    total_reward = 0.0

    titan_success = False
    spot_success = False

    titan_failed = False
    spot_failed = False

    titan_wall_collision = False
    spot_wall_collision = False

    titan_robot_collision = False
    spot_robot_collision = False

    titan_tipped = False
    spot_tipped = False

    min_robot_distance = float("inf")

    titan_goal_step = None
    spot_goal_step = None

    titan_action_errors = []
    spot_action_errors = []

    titan_linear_errors = []
    titan_angular_errors = []

    spot_linear_errors = []
    spot_lateral_errors = []
    spot_angular_errors = []

    for step in range(args.max_ep_len):
        im = env.get_image()

        # predict PPO action for same state for comparison

        model_obs = [
                        np.insert(obs[0], 0, 0),  # Titan
                        np.insert(obs[1], 0, 1)   # Spot
                    ]

        if policy_name == "ppo":
            actions, _, _ = expert.act(
                model_obs,
                im
            )

        else:

            titan_state = np.asarray(obs[0], dtype=np.float32)
            spot_state = np.asarray(obs[1], dtype=np.float32)

            titan_linear_action = titan_linear_tree.predict(titan_state)[0]
            titan_angular_action = titan_angular_tree.predict(titan_state)[0]

            titan_action = np.array([titan_linear_action, titan_angular_action], dtype=np.float32)

            spot_linear_action = spot_linear_tree.predict(spot_state)[0]
            spot_lateral_action = spot_lateral_tree.predict(spot_state)[0]
            spot_angular_action = spot_angular_tree.predict(spot_state)[0]

            spot_action = np.array([spot_linear_action, spot_lateral_action, spot_angular_action], dtype=np.float32)


            actions = [
                titan_action,
                spot_action
            ]

            ppo_actions, _, _ = expert.act(model_obs, im)

            titan_action_error = np.mean(np.abs(titan_action - ppo_actions[0]))
            spot_action_error = np.mean(np.abs(spot_action - ppo_actions[1]))

            titan_linear_error = np.mean(np.abs(titan_linear_action - ppo_actions[0][0]))
            titan_angular_error = np.mean(np.abs(titan_angular_action - ppo_actions[0][1]))

            spot_linear_error = np.mean(np.abs(spot_linear_action - ppo_actions[1][0]))
            spot_lateral_error =  np.mean(np.abs(spot_lateral_action - ppo_actions[1][1]))
            spot_angular_error = np.mean(np.abs(spot_angular_action - ppo_actions[1][2]))

            titan_action_errors.append(titan_action_error)
            spot_action_errors.append(spot_action_error)

            titan_linear_errors.append(titan_linear_error)
            titan_angular_errors.append(titan_angular_error)

            spot_linear_errors.append(spot_linear_error)
            spot_lateral_errors.append(spot_lateral_error)
            spot_angular_errors.append(spot_angular_error)

            

        # Required by env.step() because Pretrained_cur=False
        expert_acs = np.zeros(
            (2, 2),
            dtype=np.float32
        )

        obs, rewards, dones, terminations, info = env.step(
            actions,
            expert_acs
        )

        if env.robots[0].dist_to_wp < 1 and titan_goal_step is None:
            titan_goal_step = step + 1
            titan_success = True

        if env.robots[1].dist_to_wp < 1 and spot_goal_step is None:
            spot_goal_step = step + 1
            spot_success = True

        titan_pos = np.asarray(
            env.robots[0].pos[:2],
            dtype=np.float32
        )

        spot_pos = np.asarray(
            env.robots[1].pos[:2],
            dtype=np.float32
        )

        robot_distance = np.linalg.norm(
            titan_pos - spot_pos
        )

        min_robot_distance = min(
            min_robot_distance,
            float(robot_distance)
        )

        total_reward += float(np.sum(rewards))

        titan_failed = titan_failed or bool(dones[0])
        spot_failed = spot_failed or bool(dones[1])


        titan_robot_collision = (
            titan_robot_collision
            or bool(env.robots[0].intersection_r1_r)
        )

        spot_robot_collision = (
            spot_robot_collision
            or bool(env.robots[1].intersection_r1_r)
        )

        # collisions in Komol's model happen through bounding box intersections, not just robot intersections

        titan_wall_collision = (
            titan_wall_collision
            or bool(np.asarray(env.robots[0].contacts).any())
        )

        spot_wall_collision = (
            spot_wall_collision
            or bool(np.asarray(env.robots[1].contacts).any())
        )

        titan_tipped = (
            titan_tipped
            or bool(env.robots[0].tipped)
        )

        spot_tipped = (
            spot_tipped
            or bool(env.robots[1].tipped)
        )

        # print(
        #     f"Seed {seed} | "
        #     f"Policy {policy_name} | "
        #     f"Step {step} | "
        #     f"Reward {rewards} | "
        #     f"Dones {dones}"
        # )

        if all(dones) or all(terminations):
            break

    if titan_action_errors:
        titan_action_mae = float(np.mean(titan_action_errors))
    else:
        titan_action_mae = None

    if spot_action_errors:
        spot_action_mae = float(np.mean(spot_action_errors))
    else:
        spot_action_mae = None

    if titan_linear_errors:
        titan_linear_mae = float(np.mean(titan_linear_errors))
        titan_angular_mae = float(np.mean(titan_angular_errors))

        spot_linear_mae = float(np.mean(spot_linear_errors))
        spot_lateral_mae = float(np.mean(spot_lateral_errors))
        spot_angular_mae = float(np.mean(spot_angular_errors))

    else:
        titan_linear_mae = None
        titan_angular_mae = None

        spot_linear_mae = None
        spot_lateral_mae = None
        spot_angular_mae = None


    result = {
        "seed": seed,
        "policy": policy_name,
        "steps": step + 1,
        "total_reward": total_reward,
        "valid_scenario": True,

        "titan_success": titan_success,
        "spot_success": spot_success,
        "team_success": titan_success and spot_success,

        "titan_failed": titan_failed,
        "spot_failed": spot_failed,

        "titan_wall_collision": titan_wall_collision,
        "spot_wall_collision": spot_wall_collision,

        "titan_robot_collision": titan_robot_collision,
        "spot_robot_collision": spot_robot_collision,

        "titan_tipped": titan_tipped,
        "spot_tipped": spot_tipped,

        "titan_goal_step": titan_goal_step,
        "spot_goal_step": spot_goal_step,

        "titan_final_goal_distance": float(env.robots[0].dist_to_wp),
        "spot_final_goal_distance": float(env.robots[1].dist_to_wp),

        "min_robot_distance": min_robot_distance,

        "titan_action_mae": titan_action_mae,
        "spot_action_mae": spot_action_mae,

        "titan_linear_mae": titan_linear_mae,
        "titan_angular_mae": titan_angular_mae,

        "spot_linear_mae": spot_linear_mae,
        "spot_lateral_mae": spot_lateral_mae,
        "spot_angular_mae": spot_angular_mae,
    }

    env._p.disconnect()

    return result


def main():

    results = []

    test_seeds = random_SEEDS

    # test_seeds = open_seeds()

    max_workers = 8

    print(
        f"Running {len(test_seeds)} seeds "
        f"x {len(POLICIES)} policies "
        f"using {max_workers} workers"
    )

    completed = 0

    ctx = mp.get_context("spawn")

    with ProcessPoolExecutor(
        max_workers=max_workers,
        mp_context=ctx
    ) as executor:

        futures = {
            executor.submit(
                run_seed,
                seed
            ): seed
            for seed in test_seeds
        }

        for future in as_completed(futures):

            seed = futures[future]

            try:
                completed_seed, seed_results = future.result()

            except Exception as e:

                print(
                    f"\nSeed {seed} FAILED:"
                )

                print(e)

                continue

            results.extend(seed_results)

            completed += 1

            print(
                f"Completed seed "
                f"{completed}/{len(test_seeds)} "
                f"({completed_seed})"
            )

            for result in seed_results:

                print(
                    f"  {result['policy']}: "
                    f"Titan={result.get('titan_success')} "
                    f"Spot={result.get('spot_success')} "
                    f"Team={result.get('team_success')}"
                    f"Total reward={result.get('total_reward')}"
                    f"Steps={result.get('steps')}"
                )

    policy_order = {
        policy: i
        for i, policy in enumerate(POLICIES)
    }

    results.sort(
        key=lambda r: (
            test_seeds.index(r["seed"]),
            policy_order[r["policy"]]
        )
    )

    save_to_csv(
        results,
        test_seeds
    )


if __name__ == "__main__":
    main()