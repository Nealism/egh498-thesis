import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

# Read the data from the CSV files for two experiments
# data1 = pd.read_csv("/home/kom018/Downloads/8r21MGE103_2024_03_07_03_03_11.csv")["Value"]
# data2 = pd.read_csv("/home/kom018/Downloads/16r21MGE103_2024_03_07_03_03_23.csv")["Value"]

# data1 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Ray_Reward_Cur_with_other_robot_info.csv")["value"]
# data2 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Without_other_robot_info.csv")["value"]

data1 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Ray_Reward_Cur_with_other_robot_info.csv")["value"]
data2 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Ray_Reward_Cur_with_other_robot_info_R2.csv")["value"]
data3 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Regular_Reward.csv")["value"]
data4 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Regular_Reward_R2.csv")["value"]
# data5 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Gap_Cur_Only.csv")["value"]
# data6 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Gap_Cur_Only_R2.csv")["value"]
# data7 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/No_Cur.csv")["value"]
# data8 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/No_Cur_R2.csv")["value"]

# Organize data into a dictionary with experiment names as keys
# and a list of values as the values
# experiments = {
#     "Using Other Robot Information": sorted(data1),
#     "Without Using Other Robot Information": sorted(data2)
# }

experiments = {
    "Ray Mechanism Based Reward": sorted(data1),
    " ": sorted(data2),
    "Regular Reward": sorted(data3),
    "": sorted(data4)
}

# experiments = {
#     "MA_Boostrap + Gap Cur R1": sorted(data1),
#     "MA_Boostrap + Gap Cur R2": sorted(data2),
#     "MA_Bootstrap R1": sorted(data3),
#     "MA_Bootstrap R2": sorted(data4)
#     # "Gap Cur R1": sorted(data5),
#     # "Gap Cur R2": sorted(data6),
#     # "No Cur R1": sorted(data7),
#     # "No Cur R2": sorted(data8)
# }



# Create a list of experiment names and corresponding data
experiment_names = list(experiments.keys())

experiment_data = list(experiments.values())


# Create the violin plot
fig, ax = plt.subplots(figsize=(30, 10))
# plt.figure(figsize=(25, 10))
parts = ax.violinplot(experiment_data, showmeans=False, showmedians=False, showextrema=False)

# colors = ['#87CEEB']+ ['#FFFF00']+ ['#87CEEB']+ ['#FFFF00']+['#87CEEB']+ ['#FFFF00']+['#87CEEB']+ ['#FFFF00']# Sky Blue for first 4, Yellow for next 4
colors = ['#87CEEB']+ ['#FFFF00']+ ['#87CEEB']+ ['#FFFF00']+['#87CEEB']+ ['#FFFF00']+['#87CEEB']+ ['#FFFF00']# Sky Blue for first 4, Yellow for next 4

# Set the colors for each violin
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(colors[i])
    pc.set_edgecolor('black')
    pc.set_alpha(1)

quartile1, medians, quartile3 = np.percentile(experiment_data, [25, 50, 75], axis=1)
whiskers_min, whiskers_max = np.min(experiment_data, axis=1), np.max(experiment_data, axis=1)

inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='o', color='white', s=100, zorder=3)
ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=15)
ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=5)

# ax.title('Customized Violin Plot for Two Experiments', fontsize=20)
# ax.xlabel('Training Results on Training with Different Inputs', fontsize=20)
ax.set_ylabel('Goal Reaching Success-rate (%)', fontsize=30)

ax.set_xticks(np.arange(1, len(experiment_names) + 1), experiment_names, rotation=0, ha='center', fontsize=30)
plt.yticks(fontsize=30)

# Set custom labels
ax.set_xticks(range(1, len(experiment_names) + 1))
ax.set_xticklabels(experiment_names, rotation=0)  # Keep labels horizontal

# Add custom legend
legend_patches = [
    Patch(color='#87CEEB', label='Robot 1'),
    Patch(color='#FFFF00', label='Robot 2')
]
ax.legend(handles=legend_patches, loc='lower center',fontsize=30)

plt.tight_layout()

# Save the figure
plt.savefig('/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Training_different_Rewards.png')


plt.show()
