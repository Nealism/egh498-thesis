import os
import random
import numpy as np
import torch


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class DAggerCollector:

    def __init__(
        self,
        env,
        expert,
        titan_tree,
        spot_tree,
        max_ep_len=200
    ):

        self.env = env
        self.expert = expert

        self.titan_tree = titan_tree
        self.spot_tree = spot_tree

        self.max_ep_len = max_ep_len


    def collect(
        self,
        n_episodes,
        seeds=None,
        beta=0.0
    ):

        titan_obs = []
        titan_actions = []

        spot_obs = []
        spot_actions = []

        episode_ids = []
        episode_rewards = []

        controller_used = []

        if seeds is not None and len(seeds) != n_episodes:
            raise ValueError(
                f"Expected {n_episodes} seeds, "
                f"received {len(seeds)}"
            )


        for episode in range(n_episodes):

            if seeds is not None:
                seed = int(seeds[episode])
                set_seed(seed)

            obs = self.env.reset()
            im = self.env.get_image()

            ep_reward = 0.0


            for step in range(self.max_ep_len):

                model_obs = [
                    np.insert(obs[0], 0, 0),  # Titan
                    np.insert(obs[1], 0, 1)   # Spot
                ]

                # PPO / EXPERT ACTION

                expert_actions, _, _ = self.expert.act(
                    model_obs,
                    im
                )

                # TREE ACTION

                titan_tree_action = self.titan_tree.predict(
                    np.asarray(
                        obs[0],
                        dtype=np.float32
                    )
                )[0]

                spot_tree_action = self.spot_tree.predict(
                    np.asarray(
                        obs[1],
                        dtype=np.float32
                    )
                )[0]


                tree_actions = [
                    np.asarray(
                        titan_tree_action,
                        dtype=np.float32
                    ),
                    np.asarray(
                        spot_tree_action,
                        dtype=np.float32
                    )
                ]


                titan_obs.append(
                    np.asarray(
                        obs[0],
                        dtype=np.float32
                    )
                )

                titan_actions.append(
                    np.asarray(
                        expert_actions[0],
                        dtype=np.float32
                    )
                )

                spot_obs.append(
                    np.asarray(
                        obs[1],
                        dtype=np.float32
                    )
                )

                spot_actions.append(
                    np.asarray(
                        expert_actions[1],
                        dtype=np.float32
                    )
                )

                episode_ids.append(episode)


                if random.random() < beta:

                    actions = expert_actions
                    controller_used.append(1)

                else:

                    actions = tree_actions
                    controller_used.append(0)


                expert_acs = np.zeros(
                    (2, 2),
                    dtype=np.float32
                )


                obs, rewards, dones, terminations, info = (
                    self.env.step(
                        actions,
                        expert_acs
                    )
                )


                ep_reward += float(
                    np.sum(rewards)
                )


                if all(dones) or all(terminations):
                    break


                im = self.env.get_image()


            episode_rewards.append(
                ep_reward
            )

            print(
                f"Episode {episode + 1}/{n_episodes} "
                f"- steps={step + 1} "
                f"- reward={ep_reward:.3f}"
            )


        return {

            "titan_obs":
                np.asarray(titan_obs),

            "titan_actions":
                np.asarray(titan_actions),

            "spot_obs":
                np.asarray(spot_obs),

            "spot_actions":
                np.asarray(spot_actions),

            "episode_ids":
                np.asarray(episode_ids),

            "episode_rewards":
                np.asarray(episode_rewards),

            "controller_used":
                np.asarray(controller_used)
        }


def save_dataset(dataset, output_path):

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True
    )

    np.savez_compressed(
        output_path,
        **dataset
    )

    print(
        f"DAgger dataset saved to {output_path}"
    )