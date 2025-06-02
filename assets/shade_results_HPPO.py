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
        mean = np.mean(accuracies) * 100  # Scale by 100 to convert to percentage
        std = np.std(accuracies) * 100    # Scale by 100 to convert to percentage
        
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

    # plt.title('Training Performance Comparison', fontsize=30)
    plt.xlabel('Epoch', fontsize=30)
    plt.ylabel('Goal Reaching Success Rate (%)', fontsize=30)
    plt.ylim(0, 100)  # Set y-axis limit to 100 for percentages
    # Explicitly setting the axes limits
    plt.xlim(left=0)  # Start x-axis at 0
    plt.ylim(bottom=0)  # Start y-axis at 0
    plt.xticks(range(0, max(epochs_list[-1]) + 1, 100),fontsize=30)
    plt.yticks(fontsize=30)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left', fontsize=25)

    plt.tight_layout()
    plt.savefig('comparison_performance_plot2.png')  # Save the plot as a PNG file
    plt.show()

def main():
    # Directories containing CSV files for each method
    directories = ['/home/kom018/titan_results_data_tensorboard/accuracy/boot_Gap/', '/home/kom018/titan_results_data_tensorboard/accuracy/Gap_only/', '/home/kom018/titan_results_data_tensorboard/accuracy/End_to_End/']
    labels = ['THPPO', 'HPPO', 'TMAPPO', 'MAPPO']
    colors = ['green', 'blue', 'orange', 'violet']  # darkorange for dark yellow
    
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
