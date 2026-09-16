## Heterogeneous Expert System for Multi-Robot Collision Avoidance
## Exports Hetereogeneous Multi-Agent policies to export into Interpretable/Explainable AI (xAI) in the form of Decision Trees and Decision Rules

import numpy as np
import torch

# load model
#accept obs and im

class HeterogeneousExpert:
    def __init__(self, model_path, device='cpu'):
        self.device = torch.device(device)

        self.policy = torch.load(
            model_path,
            map_location=self.device,
            weights_only=False
        )

        # debugging code, pls remember to comment out
        print("POLICY TYPE:", type(self.policy))
        print("PI TYPE:", type(self.policy.pi))
        print("PI ATTRIBUTES:")
        print([x for x in dir(self.policy.pi) if "mu" in x or "spot" in x or "titan" in x])

        self.policy.eval()


# call pol.step()

# return Spot/Titan continuous actions

    def act(self, obs, im):
        obs_tensor = torch.as_tensor(
            np.asarray(obs),
            dtype=torch.float32,
            device=self.device
        )

        im_tensor = torch.as_tensor(
            np.asarray(im),
            dtype=torch.float32,
            device=self.device
        )

        with torch.no_grad():
            (
                a_spot,
                a_titan,
                value,
                logp_spot,
                logp_titan
            ) = self.policy.step(
                obs_tensor,
                im_tensor,
                stochastic=False
            )

            actions = [
                self._to_numpy(a_titan[0]),
                self._to_numpy(a_spot[1])
            ]

            logps = [
                self._to_numpy(logp_titan[0]),
                self._to_numpy(logp_spot[1])
            ]

            return actions, self._to_numpy(value), logps

    @staticmethod
    def _to_numpy(value):
        if isinstance(value, torch.Tensor):
            return value.detach().cpu().numpy()
        return np.asarray(value)

#replace/extend DecisionTreeClassifier from MAVIPER

#use DecisionTreeRegressor

# collect training rollouts
# collect state, preception input im, expert Spot/Titan actions

# im Handler
# extract compact meaningful features from occupancy map or from policy's perception encoder

# train/evaluate decision trees
# comparison of RL vs tree on success, reward, collision rate
#export tree to IF/ELSE conditions

# visualise tree

