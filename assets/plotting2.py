import pandas as pd
import matplotlib.pyplot as plt

# Read the .ods file for the second set of data
df2 = pd.read_excel("/home/kom018/behaviour_rl/action_velocity_time_constant51.ods", engine="odf")


# Plot the second set of data
plt.plot(df2['T'], df2['A1'], label='action[1]')
plt.plot(df2['T'], df2['AV'], label='Angular Velocity (rad/s)')

# Add labels and title
plt.xlabel('Time (s)')
plt.ylabel('velocity (rad/s)')
plt.title('action[1] and Angular_velocity(rad/s) vs Time(s)')

# Add legend
plt.legend()

# Save the second plot as an image file
plt.savefig('Constant_angular.png')

# Show second plot
plt.show()
