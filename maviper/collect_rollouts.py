import os
import numpy as np
import torch

from heterogeneous_expert import HeterogeneousExpert

class RolloutCollector:
    def __init__(self, env, expert, max_ep_len=200):
        self.env = env
        self.expert = expert
        self.max_ep_len = max_ep_len

    def collect(self, n_episodes=10):


        titan_obs = []
        titan_im = []
        titan_actions = []

        spot_obs = []
        spot_im = []
        spot_actions = []

        episode_rewards = []

        for episode in range(n_episodes):
            obs = self.env.reset()
            im = self.env.get_image()

            # verify collection exists
            if episode == 0:
                print("Initial observation shape:", np.asarray(obs).shape)
                print("Initial image shape:", np.asarray(im).shape)
                print("Titan observation:", obs[0])
                print("Spot observation:", obs[1])
        

            ep_reward = 0.0

            for step in range(self.max_ep_len):
                actions, value, logps = self.expert.act(obs, im)

                titan_obs.append(np.asarray(obs[0], dtype=np.float32))
                titan_im.append(np.asarray(im[0], dtype=np.float32))
                titan_actions.append(np.asarray(actions[0], dtype=np.float32))

                spot_obs.append(np.asarray(obs[1], dtype=np.float32))
                spot_im.append(np.asarray(im[1], dtype=np.float32))
                spot_actions.append(np.asarray(actions[1], dtype=np.float32))

                expert_acs = np.zeros((2, 2), dtype=np.float32)

                result = self.env.step(actions, expert_acs)

                obs, rewards, dones, terminations, info = result

                ep_reward += float(np.sum(rewards))

                if any(dones) or any(terminations):
                    break

                im = self.env.get_image()

            episode_rewards.append(ep_reward)

            print(
                f"Episode {episode + 1}/{n_episodes} "
                f"- steps: {step + 1} "
                f"- reward: {ep_reward:.3f}"
            )

            return {
                "titan_obs": np.asarray(titan_obs),
                "titan_im": np.asarray(titan_im),
                "titan_actions": np.asarray(titan_actions),
                "spot_obs": np.asarray(spot_obs),
                "spot_im": np.asarray(spot_im),
                "spot_actions": np.asarray(spot_actions),
                "episode_rewards": np.asarray(episode_rewards)
            }

    def save_dataset(dataset, output_path):
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        np.savez_compressed(output_path, **dataset)

        print(f"Dataset saved to {output_path}")

        for key, value in dataset.items():
            print(f"{key}: {np.asarray(value).shape}")