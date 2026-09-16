import numpy as np
from sklearn.tree import DecisionTreeRegressor, export_text

class RegressionDTPolicy:
    def __init__(self, max_depth=None, random_state=42):
        self.max_depth = max_depth
        self.tree = DecisionTreeRegressor(max_depth=max_depth, random_state=random_state)

    def train(self, observations, actions):
        observations = np.asarray(observations)
        actions = np.asarray(actions)
        self.tree.fit(observations, actions)

    def predict(self, observations):
        observations = np.asarray(observations)
        if observations.ndim == 1:
            observations = observations.reshape(1, -1)
        return self.tree.predict(observations)

    def get_depth(self):
        return self.tree.get_depth()

    def get_node_count(self):
        return self.tree.tree_.node_count

    def export_rules(self, feature_names=None):
        return export_text(self.tree, feature_names=feature_names)