import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.patches import Patch

def load_csv_files(directory):
    """
    Load CSV files from the specified directory.
    Expects CSV files with columns: 'wall_time', 'Step', 'Value'
    """
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    # Dictionary to store accuracies for each epoch
    epoch_accuracies = {}
    
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        df = pd.read_csv(file_path)
        
        # Group by Step (epoch) and collect accuracies
        for Step, group in df.groupby('Step'):
            if Step not in epoch_accuracies:
                epoch_accuracies[Step] = []
            epoch_accuracies[Step].append(group['Value'].mean())
    
    return epoch_accuracies

def analyze_epoch_performance(epoch_accuracies):
    """
    Analyze performance across epochs
    """
    # Sort epochs to ensure correct order
    sorted_epochs = sorted(epoch_accuracies.keys())
    
    means = []
    stds = []
    
    for epoch in sorted_epochs:
        accuracies = epoch_accuracies[epoch]
        mean = np.mean(accuracies)
        std = np.std(accuracies)
        
        means.append(mean)
        stds.append(std)
    
    return sorted_epochs, means, stds

def plot_performance(epochs_list, means_list, stds_list, labels, colors):
    """
    Create performance visualization for multiple sets of results
    """
    plt.figure(figsize=(12, 10))

    for epochs, means, stds, label, color in zip(epochs_list, means_list, stds_list, labels, colors):
        # Plot mean accuracy
        plt.plot(epochs, means, marker='o', linestyle='-', linewidth=5, label=label, color=color)

        # Plot variance as shaded area
        plt.fill_between(
            epochs, 
            np.array(means) - np.array(stds), 
            np.array(means) + np.array(stds), 
            alpha=0.2, 
            color=color
        )

    # Adding hatch fills and separator lines
    plt.axvspan(0, 63, facecolor='none', edgecolor='blue', hatch='/', linewidth=2)  # Adjust linewidth to 0 for hatching only
    plt.axvline(x=63, color='blue', linestyle='-', linewidth=5)  # Separator line

    plt.axvspan(63, 107, facecolor='none', edgecolor='magenta', hatch='\\\\', linewidth=2)  # Adjust linewidth to 0 for hatching only
    plt.axvline(x=107, color='magenta', linestyle='-', linewidth=5)  # Separator line

    # Creating legend entries for hatch areas
    hatch_patch1 = Patch(facecolor='none', edgecolor='blue', hatch='//', label='MA_Bootstrap Cur Phase')
    hatch_patch2 = Patch(facecolor='none', edgecolor='magenta', hatch='\\\\\\', label='Gap Cur Phase')

    # plt.title('Training Performance Comparison', fontsize=30)
    plt.xlabel('Epoch', fontsize=30)
    plt.ylabel('Cumulative Reward', fontsize=30)
    plt.ylim(-500, 4000)
    plt.xlim(left=0, right=700)
    plt.xticks(range(0, max(epochs_list[-1]) + 1, 100), fontsize=30)
    plt.yticks(fontsize=30)
    plt.grid(True, linestyle='--', alpha=0.9)
    plt.legend(fontsize=30)

    # Update legend to include all elements
    plt.legend(handles=  [plt.Line2D([0], [0], color=color, lw=4, label=label) for label, color in zip(labels, colors)]+[hatch_patch1, hatch_patch2], fontsize=30)
    plt.tight_layout()
    plt.savefig('curriculum_learning_plot.png')  # Save the plot as a PNG file
    plt.show()

def main():
    # Directories containing CSV files for each method
    directories = ['/home/kom018/titan_results_data_tensorboard/reward/single_Giveway_reward/', '/home/kom018/titan_results_data_tensorboard/reward/single_Endtoend_reward/']
    labels = ['MA_Bootstrap+Gap Cur','End-to-End Learning']
    colors = ['green','red']
    
    epochs_list = []
    means_list = []
    stds_list = []

    # Load and analyze performance from each directory
    for directory in directories:
        epoch_accuracies = load_csv_files(directory)
        epochs, means, stds = analyze_epoch_performance(epoch_accuracies)
        epochs_list.append(epochs)
        means_list.append(means)
        stds_list.append(stds)
    
    # Plot performance comparison
    plot_performance(epochs_list, means_list, stds_list, labels, colors)

if __name__ == '__main__':
    main()
