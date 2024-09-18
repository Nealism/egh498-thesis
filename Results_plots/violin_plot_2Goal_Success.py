import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

# Read the data from the CSV files for two experiments
# data1 = pd.read_csv("/home/kom018/Downloads/8r21MGE103_2024_03_07_03_03_11.csv")["Value"]
# data2 = pd.read_csv("/home/kom018/Downloads/16r21MGE103_2024_03_07_03_03_23.csv")["Value"]

# data1 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Ray_Reward_Cur_with_other_robot_info.csv")["value"]
# data2 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Without_other_robot_info.csv")["value"]

# data1 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/All_cur_1_robot.csv")["value"]
# data2 = pd.read_csv("/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Gap_Cur_1_robot.csv")["value"]


# Creating data1 with a value of 100 for 100 times
# data1 = np.full(100, 100)
data1 = np.concatenate([np.full(99, 100), np.zeros(1)])

# Creating data2 with a value of 100 for 98 times and 0 for two times
data2 = np.concatenate([np.full(98, 100), np.zeros(2)])

# Organize data into a dictionary with experiment names as keys
# and a list of values as the values
# experiments = {
#     "Using Other Robot Information": sorted(data1),
#     "Without Using Other Robot Information": sorted(data2)
# }

# experiments = {
#     "Ray Mechanism Based Reward": sorted(data1),
#     "Regular Reward": sorted(data2)
# }

# experiments = {
#     "MA_Boostrap + Gap Cur": sorted(data1),
#     "Gap Cur only": sorted(data2),
    
# }

experiments = {
    "": sorted(data1),
    " ": sorted(data2),
    
}



# Create a list of experiment names and corresponding data
experiment_names = list(experiments.keys())

experiment_data = list(experiments.values())


# Create the violin plot
fig, ax = plt.subplots(figsize=(40, 20))
# plt.figure(figsize=(25, 10))
parts = ax.violinplot(experiment_data, showmeans=False, showmedians=False, showextrema=False)

# colors = ['#87CEEB']+ ['#FFFF00']+ ['#87CEEB']+ ['#FFFF00']+['#87CEEB']+ ['#FFFF00']+['#87CEEB']+ ['#FFFF00']# Sky Blue for first 4, Yellow for next 4
colors = ['#FFA500']+ ['#FF007F']+ ['#FFA500']+ ['#008000']+['#FFA500']+ ['#008000']+['#FFA500']+ ['#008000']# Sky Blue for first 4, Yellow for next 4

# Set the colors for each violin
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(colors[i])
    pc.set_edgecolor('black')
    pc.set_alpha(1)

quartile1, medians, quartile3 = np.percentile(experiment_data, [25, 50, 75], axis=1)
whiskers_min, whiskers_max = np.min(experiment_data, axis=1), np.max(experiment_data, axis=1)

inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='o', color='white', s=1000, zorder=3)
ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=50)
ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=2)

# ax.title('Customized Violin Plot for Two Experiments', fontsize=20)
# ax.xlabel('Training Results on Training with Different Inputs', fontsize=20)
ax.set_ylabel('Goal Reaching Success-rate (%)', fontsize=80)

ax.set_xticks(np.arange(1, len(experiment_names) + 1), experiment_names, rotation=0, ha='center', fontsize=80)
plt.yticks(fontsize=80)

# Set custom labels
ax.set_xticks(range(1, len(experiment_names) + 1))
ax.set_xticklabels(experiment_names, rotation=0)  # Keep labels horizontal

# Add custom legend
legend_patches = [
    Patch(color='#FFA500', label='Simultaneuos Navigation'),
    Patch(color='#FF007F', label='Staggered Navigation')
]
ax.legend(handles=legend_patches, loc='lower center',fontsize=60)

plt.tight_layout()

# Save the figure
plt.savefig('/home/kom018/behaviour_rl/Results_plots/pybullet_excels/Pybullet_Goal_Success.png')


plt.show()
