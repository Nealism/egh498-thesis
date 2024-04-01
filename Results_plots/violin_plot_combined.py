import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the data from the CSV files for two experiments
data1 = pd.read_csv("/home/kom018/Downloads/8r21MGE103_2024_03_07_03_03_11.csv")["Value"]
data2 = pd.read_csv("/home/kom018/Downloads/16r21MGE103_2024_03_07_03_03_23.csv")["Value"]

# Combine the data from both experiments into a single list
combined_data = sorted(list(data1) + list(data2))

# Create the violin plot
plt.figure(figsize=(10, 6))
parts = plt.violinplot(combined_data, showmeans=False, showmedians=False, showextrema=False)

for pc in parts['bodies']:
    pc.set_facecolor('#D43F3A')
    pc.set_edgecolor('black')
    pc.set_alpha(1)

quartile1, medians, quartile3 = np.percentile(combined_data, [25, 50, 75])
whiskers_min, whiskers_max = np.min(combined_data), np.max(combined_data)

inds = [1]
plt.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)
plt.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
plt.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)

plt.title('Customized Violin Plot for Combined Experiments')
plt.xlabel('Combined Experiments')
plt.ylabel('Observed values')

plt.xticks([1], ['Combined Data'])
plt.tight_layout()

# Save the figure
plt.savefig('combined_experiment_violin_plot.png')


plt.show()


