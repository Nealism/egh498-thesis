import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else np.zeros_like(v)

def compute_action(pos, goal, other, repel_weight=2.0, repel_radius=2.0):
    to_goal = goal - pos
    repulsion = np.zeros_like(to_goal)
    dist = np.linalg.norm(pos - other)
    if dist < repel_radius and dist > 0:
        repulsion = repel_weight * (pos - other) / dist
    combined = to_goal + repulsion
    return normalize(combined), np.linalg.norm(combined)

# Main parameters
dt = 0.5
grid_x = np.linspace(1, 9, 9)
grid_y = np.linspace(1, 11, 9)

start_A = np.array([3, 1])
goal_A = np.array([6, 9])
start_B = np.array([6, 1])
goal_B = np.array([3, 9])

# Create output directory
output_dir = "robot_field_plots"
os.makedirs(output_dir, exist_ok=True)

# Initial positions
pos_A = start_A.copy()
pos_B = start_B.copy()

# Time range
time_range = np.arange(0, 21)  # 0 to 20 inclusive

# Dictionary to track positions at each time
positions = {0: (start_A.copy(), start_B.copy())}

# Pre-calculate positions for all time points
for t in range(1, max(time_range) + 1):
    # Simple linear interpolation for this example 
    # (you could use your original movement logic instead)
    alpha = min(t / 20.0, 1.0)  # Normalized time from 0 to 1
    
    # Linear interpolation between start and goal
    pos_A = start_A + alpha * (goal_A - start_A)
    pos_B = start_B + alpha * (goal_B - start_B)
    
    positions[t] = (pos_A, pos_B)

# Create and save plots for each time point
for i, t in enumerate(time_range):
    pos_A, pos_B = positions[t]
    print("pos_A, pos_B",pos_A, pos_B)
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw vector field
    for x in grid_x:
        for y in grid_y:
            pos = np.array([x, y])
            action, _ = compute_action(pos, goal_A, pos_B)
            ax.arrow(x, y, action[0]*0.5, action[1]*0.5, head_width=0.1, color='red', alpha=0.5)
    
    # Draw robots
    ax.plot(*pos_A, marker='s', color='red', markersize=20)
    ax.plot(*pos_B, marker='s', color='blue', markersize=20)
    
    # Add time labels
    ax.text(pos_A[0] + 0.1, pos_A[1], f"Time: {t}s", color='red', fontsize=10)
    ax.text(pos_B[0] + 0.1, pos_B[1], f"Time: {t}s", color='blue', fontsize=10)
    
    # Add obstacles
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # Add start and goal positions
    ax.plot(*start_A, marker='^', color='red', markersize=14)
    ax.plot(*start_B, marker='^', color='blue', markersize=14)
    ax.plot(*goal_A, marker='o', color='red', markersize=16)
    ax.plot(*goal_B, marker='o', color='blue', markersize=16)
    
    # Add legend
    handles = [
        Line2D([], [], marker='^', color='red', linestyle='None', markersize=10, label='Start A'),
        Line2D([], [], marker='^', color='blue', linestyle='None', markersize=10, label='Start B'),
        Line2D([], [], marker='o', color='red', linestyle='None', markersize=10, label='Goal A'),
        Line2D([], [], marker='o', color='blue', linestyle='None', markersize=10, label='Goal B'),
        Line2D([], [], marker='s', color='red', linestyle='None', markersize=10, label='Robot A'),
        Line2D([], [], marker='s', color='blue', linestyle='None', markersize=10, label='Robot B'),
        Line2D([], [], color='black', linewidth=8, label='Obstacle'),
        Line2D([], [], color='red', linewidth=2, marker='>', markersize=10, label='Vector Field A'),
    ]
    
    ax.legend(handles=handles, loc='upper right')
    ax.set_title(f"Robot A Vector Field at Time: {t}s")
    ax.axis("equal")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)
    
    # Save the plot with a simple numbered filename
    plt.tight_layout()
    filename = os.path.join(output_dir, f"robot_field_{i:03d}.png")  # Uses counter i with padding
    plt.savefig(filename)
    plt.close(fig)
    
    print(f"Saved plot {i}: {filename} (time={t}s)")

print(f"Generated {len(time_range)} plots in {output_dir} directory")