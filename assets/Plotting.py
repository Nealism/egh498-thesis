import pandas as pd
import matplotlib.pyplot as plt

# Read the .ods file
df = pd.read_excel("/home/kom018/behaviour_rl/action_velocity_time_constant51.ods", engine="odf")

# Plot the data
plt.plot(df['T'], df['A0'], label='action [0]')
plt.plot(df['T'], df['LV'], label='Linear Velocity')

# Add labels and title
plt.xlabel('Time (s)')
plt.ylabel('velocity (m/s)')
plt.title('action[0] and Linear Velocity (m/s) vs Time(s)')

# Add legend
plt.legend()
plt.savefig('Constant_Linear.png')
# Show plot
plt.show()