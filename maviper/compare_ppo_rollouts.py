import numpy as np
import torch
import random
from pathlib import Path

import models.core as core

from default_arguments import get_defaults, get_env
from heterogeneous_expert import HeterogeneousExpert


# ============================================================
# SETTINGS
# ============================================================

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
MAX_STEPS = 200

TOLERANCE = 1e-6


# ============================================================
# REPRODUCIBILITY
# ============================================================

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


# ============================================================
# ENVIRONMENT
# ============================================================

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


# ============================================================
# HELPER: RECORD CURRENT STATE
# ============================================================

def record_step(
    step,
    obs,
    actions,
    rewards,
    dones,
    terminations,
    env
):

    return {
        "step": step,

        "titan_obs": np.asarray(
            obs[0],
            dtype=np.float32
        ).copy(),

        "spot_obs": np.asarray(
            obs[1],
            dtype=np.float32
        ).copy(),

        "titan_action": np.asarray(
            actions[0],
            dtype=np.float32
        ).copy(),

        "spot_action": np.asarray(
            actions[1],
            dtype=np.float32
        ).copy(),

        "rewards": np.asarray(
            rewards,
            dtype=np.float32
        ).copy(),

        "dones": np.asarray(
            dones
        ).copy(),

        "terminations": np.asarray(
            terminations
        ).copy(),

        "titan_pos": np.asarray(
            env.robots[0].pos,
            dtype=np.float32
        ).copy(),

        "spot_pos": np.asarray(
            env.robots[1].pos,
            dtype=np.float32
        ).copy(),

        "titan_goal_distance": float(
            env.robots[0].dist_to_wp
        ),

        "spot_goal_distance": float(
            env.robots[1].dist_to_wp
        ),

        "titan_robot_collision": bool(
            env.robots[0].intersection_r1_r
        ),

        "spot_robot_collision": bool(
            env.robots[1].intersection_r1_r
        ),

        "titan_contact": bool(
            np.asarray(
                env.robots[0].contacts
            ).any()
        ),

        "spot_contact": bool(
            np.asarray(
                env.robots[1].contacts
            ).any()
        ),

        "titan_tipped": bool(
            env.robots[0].tipped
        ),

        "spot_tipped": bool(
            env.robots[1].tipped
        ),
    }


# ============================================================
# ORIGINAL / DIRECT PPO STYLE
# ============================================================

def run_direct(seed):

    env, obs, args = create_env(seed)

    model = torch.load(
        model_dir + "/model.pt",
        weights_only=False
    )

    model.eval()

    trajectory = []

    titan_success = False
    spot_success = False

    for step in range(MAX_STEPS):

        im = env.get_image()

        model_obs = [
            np.insert(obs[0], 0, 0),
            np.insert(obs[1], 0, 1)
        ]

        obs_tensor = torch.as_tensor(
            np.asarray(model_obs),
            dtype=torch.float32
        )

        im_tensor = torch.as_tensor(
            np.asarray(im),
            dtype=torch.float32
        )

        with torch.no_grad():

            output = model.step(
                obs_tensor,
                im_tensor,
                stochastic=False
            )

        # Heterogeneous mapping:
        #
        # output[0] = Spot action head
        # output[1] = Titan action head

        spot_actions = output[0]
        titan_actions = output[1]

        actions = [
            np.asarray(
                titan_actions[0],
                dtype=np.float32
            ),
            np.asarray(
                spot_actions[1],
                dtype=np.float32
            )
        ]

        expert_acs = np.zeros(
            (2, 2),
            dtype=np.float32
        )

        obs, rewards, dones, terminations, info = env.step(
            actions,
            expert_acs
        )

        if env.robots[0].dist_to_wp < 1:
            titan_success = True

        if env.robots[1].dist_to_wp < 1:
            spot_success = True

        trajectory.append(
            record_step(
                step=step + 1,
                obs=obs,
                actions=actions,
                rewards=rewards,
                dones=dones,
                terminations=terminations,
                env=env
            )
        )

        # Original run_test-style stopping logic
        if (
            all(dones)
            or all(terminations)
            or env.steps > args.max_ep_len
        ):
            break

    summary = {
        "steps": len(trajectory),
        "titan_success": titan_success,
        "spot_success": spot_success,
        "team_success": (
            titan_success and spot_success
        ),
    }

    env._p.disconnect()

    return trajectory, summary


# ============================================================
# CURRENT EVALUATOR STYLE
# ============================================================

def run_wrapper(seed):

    env, obs, args = create_env(seed)

    expert = HeterogeneousExpert(
        model_path=model_dir + "/model.pt"
    )

    trajectory = []

    titan_success = False
    spot_success = False

    for step in range(MAX_STEPS):

        im = env.get_image()

        model_obs = [
            np.insert(obs[0], 0, 0),
            np.insert(obs[1], 0, 1)
        ]

        actions, _, _ = expert.act(
            model_obs,
            im
        )

        expert_acs = np.zeros(
            (2, 2),
            dtype=np.float32
        )

        obs, rewards, dones, terminations, info = env.step(
            actions,
            expert_acs
        )

        if env.robots[0].dist_to_wp < 1:
            titan_success = True

        if env.robots[1].dist_to_wp < 1:
            spot_success = True

        trajectory.append(
            record_step(
                step=step + 1,
                obs=obs,
                actions=actions,
                rewards=rewards,
                dones=dones,
                terminations=terminations,
                env=env
            )
        )

        # Your evaluator stopping logic
        if all(dones) or all(terminations):
            break

    summary = {
        "steps": len(trajectory),
        "titan_success": titan_success,
        "spot_success": spot_success,
        "team_success": (
            titan_success and spot_success
        ),
    }

    env._p.disconnect()

    return trajectory, summary


# ============================================================
# COMPARISON
# ============================================================

def arrays_match(a, b):

    return np.allclose(
        np.asarray(a),
        np.asarray(b),
        atol=TOLERANCE,
        rtol=0
    )


def compare_trajectories(
    direct,
    wrapper
):

    print("\nComparing trajectories")
    print("=" * 70)

    number_steps = min(
        len(direct),
        len(wrapper)
    )

    fields = [
        "titan_obs",
        "spot_obs",

        "titan_action",
        "spot_action",

        "rewards",

        "titan_pos",
        "spot_pos",

        "titan_goal_distance",
        "spot_goal_distance",
    ]

    for i in range(number_steps):

        direct_step = direct[i]
        wrapper_step = wrapper[i]

        for field in fields:

            if not arrays_match(
                direct_step[field],
                wrapper_step[field]
            ):

                print(
                    f"\nDIVERGENCE FOUND"
                )

                print(
                    f"Step: {i + 1}"
                )

                print(
                    f"Field: {field}"
                )

                print(
                    "\nDirect:"
                )

                print(
                    direct_step[field]
                )

                print(
                    "\nWrapper:"
                )

                print(
                    wrapper_step[field]
                )

                print(
                    "\nAbsolute difference:"
                )

                print(
                    np.abs(
                        np.asarray(
                            direct_step[field]
                        )
                        -
                        np.asarray(
                            wrapper_step[field]
                        )
                    )
                )

                return False

        # Compare booleans separately

        boolean_fields = [
            "dones",
            "terminations",

            "titan_robot_collision",
            "spot_robot_collision",

            "titan_contact",
            "spot_contact",

            "titan_tipped",
            "spot_tipped",
        ]

        for field in boolean_fields:

            if not np.array_equal(
                np.asarray(
                    direct_step[field]
                ),
                np.asarray(
                    wrapper_step[field]
                )
            ):

                print(
                    "\nDIVERGENCE FOUND"
                )

                print(
                    f"Step: {i + 1}"
                )

                print(
                    f"Field: {field}"
                )

                print(
                    "Direct:",
                    direct_step[field]
                )

                print(
                    "Wrapper:",
                    wrapper_step[field]
                )

                return False

    if len(direct) != len(wrapper):

        print(
            "\nTrajectories were identical until one "
            "terminated earlier."
        )

        print(
            "Direct steps:",
            len(direct)
        )

        print(
            "Wrapper steps:",
            len(wrapper)
        )

        return False

    print(
        "\nNO DIVERGENCE FOUND."
    )

    print(
        f"Both methods produced identical trajectories "
        f"for {number_steps} steps."
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        f"\nTesting seed {SEED}"
    )

    print(
        "\nRunning direct PPO..."
    )

    direct_trajectory, direct_summary = run_direct(
        SEED
    )

    print(
        "Direct finished."
    )

    print(
        "\nRunning evaluator PPO..."
    )

    wrapper_trajectory, wrapper_summary = run_wrapper(
        SEED
    )

    print(
        "Evaluator finished."
    )

    identical = compare_trajectories(
        direct_trajectory,
        wrapper_trajectory
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "DIRECT PPO SUMMARY"
    )

    for key, value in direct_summary.items():
        print(
            f"{key}: {value}"
        )

    print(
        "\nEVALUATOR PPO SUMMARY"
    )

    for key, value in wrapper_summary.items():
        print(
            f"{key}: {value}"
        )

    print(
        "\n" + "=" * 70
    )

    if identical:

        print(
            "RESULT: The PPO inference/evaluation paths "
            "produce the same rollout for this seed."
        )

    else:

        print(
            "RESULT: The two rollout paths differ. "
            "Use the first divergence above to identify why."
        )


if __name__ == "__main__":
    main()