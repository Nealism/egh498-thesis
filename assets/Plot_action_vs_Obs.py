import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
file1 = '/home/kom018/behaviour_rl/Results_plots/Action_plots/action_1_0/actions_data.csv'
file2 = '/home/kom018/behaviour_rl/Results_plots/Action_plots/action_-0.5_0/actions_data.csv'
file3 = '/home/kom018/behaviour_rl/Results_plots/Action_plots/action_0_1.5/actions_data.csv'
file4 = '/home/kom018/behaviour_rl/Results_plots/Action_plots/action_0_-1.5/actions_data.csv'

df1 = pd.read_csv(file1).round(2)
df2 = pd.read_csv(file2).round(2)
df3 = pd.read_csv(file3).round(2)
df4 = pd.read_csv(file4).round(2)

# Define the colors for different experiments
colors = ['red', 'blue', 'green', 'purple']

# Plot Command Linear Velocity vs Time
plt.figure(figsize=(12, 8))
plt.plot(df1['Time'], df1['Command Linear Velocity'], color=colors[0], label='Experiment 1')
plt.plot(df2['Time'], df2['Command Linear Velocity'], color=colors[1], label='Experiment 2')
plt.plot(df3['Time'], df3['Command Linear Velocity'], color=colors[2], label='Experiment 3')
plt.plot(df4['Time'], df4['Command Linear Velocity'], color=colors[3], label='Experiment 4')
plt.xlabel('Time')
plt.ylabel('Command Linear Velocity')
plt.legend()
plt.title('Command Linear Velocity vs Time')
plt.xticks(range(0, 11), [f'{i:.0f}' for i in range(0, 11)])  # Set x-axis from 0 to 10 with interval 1
plt.yticks([i/10.0 for i in range(-6, 12)], [f'{i/10:.1f}' for i in range(-6, 12)])  # Set y-axis from -0.6 to 1.1 with interval 0.1
plt.ylim(-0.6, 1.1)
plt.xlim(0, 10)
plt.grid(True)
plt.savefig('/home/kom018/behaviour_rl/Results_plots/Action_plots/command_linear_velocity_vs_time.png')
plt.close()

# Plot Robot Linear Velocity vs Time
plt.figure(figsize=(12, 8))
plt.plot(df1['Time'], df1['Robot\'s Linear Velocity'], color=colors[0], label='Experiment 1')
plt.plot(df2['Time'], df2['Robot\'s Linear Velocity'], color=colors[1], label='Experiment 2')
plt.plot(df3['Time'], df3['Robot\'s Linear Velocity'], color=colors[2], label='Experiment 3')
plt.plot(df4['Time'], df4['Robot\'s Linear Velocity'], color=colors[3], label='Experiment 4')
plt.xlabel('Time')
plt.ylabel('Robot\'s Linear Velocity')
plt.legend()
plt.title('Robot\'s Linear Velocity vs Time')
plt.xticks(range(0, 11), [f'{i:.0f}' for i in range(0, 11)])  # Set x-axis from 0 to 10 with interval 1
plt.yticks([i/10.0 for i in range(-6, 12)], [f'{i/10:.1f}' for i in range(-6, 12)])  # Set y-axis from -0.6 to 1.1 with interval 0.1
plt.ylim(-0.6, 1.1)
plt.xlim(0, 10)
plt.grid(True)
plt.savefig('/home/kom018/behaviour_rl/Results_plots/Action_plots/robot_linear_velocity_vs_time.png')
plt.close()

# Plot Command Angular Velocity vs Time
plt.figure(figsize=(12, 8))
plt.plot(df1['Time'], df1['Command Angular Velocity'], color=colors[0], label='Experiment 1')
plt.plot(df2['Time'], df2['Command Angular Velocity'], color=colors[1], label='Experiment 2')
plt.plot(df3['Time'], df3['Command Angular Velocity'], color=colors[2], label='Experiment 3')
plt.plot(df4['Time'], df4['Command Angular Velocity'], color=colors[3], label='Experiment 4')
plt.xlabel('Time')
plt.ylabel('Command Angular Velocity')
plt.legend()
plt.title('Command Angular Velocity vs Time')
plt.xticks(range(0, 11), [f'{i:.0f}' for i in range(0, 11)])  # Set x-axis from 0 to 10 with interval 1
plt.yticks([i/10.0 for i in range(-16, 17)], [f'{i/10:.1f}' for i in range(-16, 17)])  # Set y-axis from -1.6 to 1.6 with interval 0.1
plt.ylim(-1.6, 1.6)
plt.xlim(0, 10)
plt.grid(True)
plt.savefig('/home/kom018/behaviour_rl/Results_plots/Action_plots/command_angular_velocity_vs_time.png')
plt.close()

# Plot Robot Angular Velocity vs Time
plt.figure(figsize=(12, 8))
plt.plot(df1['Time'], df1['Robot\'s Angular Velocity'], color=colors[0], label='Experiment 1')
plt.plot(df2['Time'], df2['Robot\'s Angular Velocity'], color=colors[1], label='Experiment 2')
plt.plot(df3['Time'], df3['Robot\'s Angular Velocity'], color=colors[2], label='Experiment 3')
plt.plot(df4['Time'], df4['Robot\'s Angular Velocity'], color=colors[3], label='Experiment 4')
plt.xlabel('Time')
plt.ylabel('Robot\'s Angular Velocity')
plt.legend()
plt.title('Robot\'s Angular Velocity vs Time')
plt.xticks(range(0, 11), [f'{i:.0f}' for i in range(0, 11)])  # Set x-axis from 0 to 10 with interval 1
plt.yticks([i/10.0 for i in range(-16, 17)], [f'{i/10:.1f}' for i in range(-16, 17)])  # Set y-axis from -1.6 to 1.6 with interval 0.1
plt.ylim(-1.6, 1.6)
plt.xlim(0, 10)
plt.grid(True)
plt.savefig('/home/kom018/behaviour_rl/Results_plots/Action_plots/robot_angular_velocity_vs_time.png')
plt.close()
