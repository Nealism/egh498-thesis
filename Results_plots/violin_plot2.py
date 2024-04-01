import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the data from the CSV files for two experiments
data1 = pd.read_csv("/home/kom018/Downloads/8r21MGE103_2024_03_07_03_03_11.csv")["Value"]
data2 = pd.read_csv("/home/kom018/Downloads/16r21MGE103_2024_03_07_03_03_23.csv")["Value"]

# Organize data into a dictionary with experiment names as keys
# and a list of values as the values
experiments = {
    "Experiment 1": sorted(data1),
    "Experiment 2": sorted(data2)
}

# Create a list of experiment names and corresponding data
experiment_names = list(experiments.keys())
experiment_data = list(experiments.values())

# Create the violin plot
plt.figure(figsize=(10, 6))
parts = plt.violinplot(experiment_data, showmeans=False, showmedians=False, showextrema=False)

for pc in parts['bodies']:
    pc.set_facecolor('#D43F3A')
    pc.set_edgecolor('black')
    pc.set_alpha(1)

quartile1, medians, quartile3 = np.percentile(experiment_data, [25, 50, 75], axis=1)
whiskers_min, whiskers_max = np.min(experiment_data, axis=1), np.max(experiment_data, axis=1)

inds = np.arange(1, len(medians) + 1)
plt.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)
plt.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
plt.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)

plt.title('Customized Violin Plot for Two Experiments')
plt.xlabel('Experiments')
plt.ylabel('Observed values')

plt.xticks(np.arange(1, len(experiment_names) + 1), experiment_names, rotation=45, ha='right')
plt.tight_layout()

# Save the figure
plt.savefig('Individual_experiment_violin_plot.png')


plt.show()
