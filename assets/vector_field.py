import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------- Utility Functions -----------

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

def compute_action_no_repulsion(pos, goal):
    direction = goal - pos
    return normalize(direction), np.linalg.norm(direction)

def compute_vector_field_arrows(grid_x, grid_y, goal, other_pos, dt, repel=True):
    """Compute vector field arrows for visualization"""
    arrows = []
    annotations = []
    
    for x in grid_x:
        for y in grid_y:
            pos = np.array([x, y])
            if repel:
                action, magnitude = compute_action(pos, goal, other_pos)
            else:
                action, magnitude = compute_action_no_repulsion(pos, goal)
            arrows.append((x, y, action[0], action[1]))
            annotations.append((x, y, f"{dt:.1f}s\n|v|={magnitude:.2f}"))
    
    return np.array(arrows), annotations

def simulate_simultaneous_trajectories(start_A, goal_A, start_B, goal_B, total_time, dt):
    """Simulate both robots moving simultaneously with repulsion"""
    steps = int(total_time / dt)
    traj_A = [start_A.copy()]
    traj_B = [start_B.copy()]
    times = [0]
    
    for step in range(steps):
        current_time = (step + 1) * dt
        
        # Calculate next position for Robot A considering B's position
        direction_A, _ = compute_action(traj_A[-1], goal_A, traj_B[-1])
        dist_A = np.linalg.norm(goal_A - traj_A[-1])
        step_size_A = min(dt, dist_A)
        next_pos_A = traj_A[-1] + step_size_A * direction_A
        
        # Calculate next position for Robot B considering A's position
        direction_B, _ = compute_action(traj_B[-1], goal_B, traj_A[-1])
        dist_B = np.linalg.norm(goal_B - traj_B[-1])
        step_size_B = min(dt, dist_B)
        next_pos_B = traj_B[-1] + step_size_B * direction_B
        
        # Check if both robots reached their goals
        if dist_A < 0.1 and dist_B < 0.1:
            break
            
        traj_A.append(next_pos_A)
        traj_B.append(next_pos_B)
        times.append(current_time)
        
    return np.array(traj_A), np.array(traj_B), np.array(times)

# ----------- Setup -----------
dt = 0.5
total_time = 30.0  # Total simulation time
grid_x = np.linspace(1, 9, 9)
grid_y = np.linspace(1, 11, 9)

start_A = np.array([3, 1])
goal_A = np.array([6, 9])  # Robot A's goal on the right side
start_B = np.array([6, 1])
goal_B = np.array([3, 9])  # Robot B's goal on the left side

# Simulate the trajectories of both robots simultaneously
traj_A, traj_B, times = simulate_simultaneous_trajectories(
    start_A, goal_A, start_B, goal_B, total_time, dt
)

# Choose time points for visualization
time_points = [0, 5, 10, 15]  # Time points to visualize (in seconds)

# ----------- Plot 1: Both Robots' Trajectories and Vector Fields -----------
fig1, axes1 = plt.subplots(2, 2, figsize=(16, 16))
axes1 = axes1.flatten()

for i, time_point in enumerate(time_points):
    ax = axes1[i]
    
    # Find the closest time index
    t_idx = min(int(time_point/dt), len(times)-1)
    current_time = times[t_idx]
    
    # Get current positions at this time
    pos_A = traj_A[t_idx]
    pos_B = traj_B[t_idx]
    
    # Compute vector field arrows at this time
    field_A, ann_A = compute_vector_field_arrows(grid_x, grid_y, goal_A, pos_B, dt, repel=True)
    field_B, ann_B = compute_vector_field_arrows(grid_x, grid_y, goal_B, pos_A, dt, repel=True)
    
    # Plot vector field arrows for Robot A (red)
    for x, y, u, v in field_A:
        ax.arrow(x, y, u*0.5, v*0.5, head_width=0.1, color='red', alpha=0.5)
    
    # Plot vector field arrows for Robot B (blue)
    for x, y, u, v in field_B:
        ax.arrow(x, y, u*0.5, v*0.5, head_width=0.1, color='blue', alpha=0.5)
    
    # Add selected annotations (not all to avoid clutter)
    for idx, (x, y, label) in enumerate(ann_A):
        if idx % 10 == 0:  # Only show some annotations to avoid clutter
            ax.text(x + 0.1, y + 0.1, label, fontsize=8, color='red')
    
    for idx, (x, y, label) in enumerate(ann_B):
        if idx % 10 == 0 and idx % 11 != 0:  # Offset to avoid overlap
            ax.text(x + 0.1, y - 0.2, label, fontsize=8, color='blue')
    
    # Plot trajectories up to this time
    ax.plot(traj_A[:t_idx+1, 0], traj_A[:t_idx+1, 1], 'r-', label='Trajectory A')
    ax.plot(traj_B[:t_idx+1, 0], traj_B[:t_idx+1, 1], 'b-', label='Trajectory B')
    
    # Mark current positions
    ax.plot(*pos_A, 'ro', markersize=8)
    ax.plot(*pos_B, 'bo', markersize=8)
    
    # Add time annotations along trajectories
    for j in range(0, t_idx+1, 5):
        if j < len(times):
            ax.text(traj_A[j][0] + 0.1, traj_A[j][1], f"{times[j]:.1f}s", color='red', fontsize=8)
            ax.text(traj_B[j][0] + 0.1, traj_B[j][1], f"{times[j]:.1f}s", color='blue', fontsize=8)
    
    # Add obstacles
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # Plot start and goal positions
    ax.plot(*start_A, 'ro', label='Start A')
    ax.plot(*start_B, 'bo', label='Start B')
    ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    
    ax.set_title(f"Both Robots' Trajectories and Vector Fields at Time: {current_time:.1f}s")
    ax.axis("equal")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)

# Add legend to the last subplot
axes1[-1].legend(loc='upper right')

plt.tight_layout()
plt.savefig("both_robots_trajectories_and_fields.png")

# ----------- Plot 2: Robot A Trajectory with Robot B Vector Field -----------
fig2, axes2 = plt.subplots(2, 2, figsize=(16, 16))
axes2 = axes2.flatten()

for i, time_point in enumerate(time_points):
    ax = axes2[i]
    
    # Find the closest time index
    t_idx = min(int(time_point/dt), len(times)-1)
    current_time = times[t_idx]
    
    # Get current positions at this time
    pos_A = traj_A[t_idx]
    pos_B = traj_B[t_idx]
    
    # Compute vector field arrows for Robot B only
    field_B, ann_B = compute_vector_field_arrows(grid_x, grid_y, goal_B, pos_A, dt, repel=True)
    
    # Plot vector field arrows for Robot B (blue)
    for x, y, u, v in field_B:
        ax.arrow(x, y, u*0.5, v*0.5, head_width=0.1, color='blue', alpha=0.5)
    
    # Add selected annotations (not all to avoid clutter)
    for idx, (x, y, label) in enumerate(ann_B):
        if idx % 9 == 0:  # Only show some annotations to avoid clutter
            ax.text(x + 0.1, y, label, fontsize=8, color='blue')
    
    # Plot Robot A's trajectory only
    ax.plot(traj_A[:t_idx+1, 0], traj_A[:t_idx+1, 1], 'r-', label='Trajectory A')
    
    # Mark current positions
    ax.plot(*pos_A, 'ro', markersize=8)
    
    # Add time annotations along trajectory A
    for j in range(0, t_idx+1, 5):
        if j < len(times):
            ax.text(traj_A[j][0] + 0.1, traj_A[j][1], f"{times[j]:.1f}s", color='red', fontsize=8)
    
    # Add obstacles
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # Plot start and goal positions
    ax.plot(*start_A, 'ro', label='Start A')
    ax.plot(*start_B, 'bo', label='Start B')
    ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    
    ax.set_title(f"Robot A Trajectory with Robot B Vector Field at Time: {current_time:.1f}s")
    ax.axis("equal")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)

# Add legend to the last subplot
axes2[-1].legend(loc='upper right')

plt.tight_layout()
plt.savefig("robot_A_traj_with_robot_B_field.png")

# ----------- Plot 3: Robot B Trajectory with Robot A Vector Field -----------
fig3, axes3 = plt.subplots(2, 2, figsize=(16, 16))
axes3 = axes3.flatten()

for i, time_point in enumerate(time_points):
    ax = axes3[i]
    
    # Find the closest time index
    t_idx = min(int(time_point/dt), len(times)-1)
    current_time = times[t_idx]
    
    # Get current positions at this time
    pos_A = traj_A[t_idx]
    pos_B = traj_B[t_idx]
    
    # Compute vector field arrows for Robot A only
    field_A, ann_A = compute_vector_field_arrows(grid_x, grid_y, goal_A, pos_B, dt, repel=True)
    
    # Plot vector field arrows for Robot A (red)
    for x, y, u, v in field_A:
        ax.arrow(x, y, u*0.5, v*0.5, head_width=0.1, color='red', alpha=0.5)
    
    # Add selected annotations (not all to avoid clutter)
    for idx, (x, y, label) in enumerate(ann_A):
        if idx % 10 == 0:  # Only show some annotations to avoid clutter
            ax.text(x + 0.1, y, label, fontsize=8, color='red')
    
    # Plot Robot B's trajectory only
    ax.plot(traj_B[:t_idx+1, 0], traj_B[:t_idx+1, 1], 'b-', label='Trajectory B')
    
    # Mark current position of Robot B
    ax.plot(*pos_B, 'bo', markersize=8)
    
    # Add time annotations along trajectory B
    for j in range(0, t_idx+1, 5):
        if j < len(times):
            ax.text(traj_B[j][0] + 0.1, traj_B[j][1], f"{times[j]:.1f}s", color='blue', fontsize=8)
    
    # Add obstacles
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # Plot start and goal positions
    ax.plot(*start_A, 'ro', label='Start A')
    ax.plot(*start_B, 'bo', label='Start B')
    ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    
    ax.set_title(f"Robot B Trajectory with Robot A Vector Field at Time: {current_time:.1f}s")
    ax.axis("equal")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)

# Add legend to the last subplot
axes3[-1].legend(loc='upper right')

plt.tight_layout()
plt.savefig("robot_B_traj_with_robot_A_field.png")

# Create an animation showing the vector fields with arrows
def create_arrow_animation():
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Set up the initial plot with obstacles and goals
    ax.plot(*start_A, 'ro', label='Start A')
    ax.plot(*start_B, 'bo', label='Start B')
    ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # Initialize trajectories
    line_A, = ax.plot([], [], 'r-', label='Trajectory A')
    line_B, = ax.plot([], [], 'b-', label='Trajectory B')
    
    # Current position markers
    point_A = ax.plot([], [], 'ro', markersize=8)[0]
    point_B = ax.plot([], [], 'bo', markersize=8)[0]
    
    # Initialize arrow collections (we'll update these)
    arrow_artists_A = []
    arrow_artists_B = []
    
    # Create initial arrows (we'll update their positions later)
    for x in grid_x:
        for y in grid_y:
            arrow_A = ax.arrow(x, y, 0, 0, head_width=0.1, color='red', alpha=0.5)
            arrow_B = ax.arrow(x, y, 0, 0, head_width=0.1, color='blue', alpha=0.5)
            arrow_artists_A.append(arrow_A)
            arrow_artists_B.append(arrow_B)
    
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)
    ax.set_title("Robot Vector Fields Evolution Over Time")
    ax.legend(loc='upper right')
    
    def init():
        line_A.set_data([], [])
        line_B.set_data([], [])
        point_A.set_data([], [])
        point_B.set_data([], [])
        time_text.set_text('')
        return [line_A, line_B, point_A, point_B, time_text] + arrow_artists_A + arrow_artists_B
    
    def update(frame):
        # Skip frames to make animation faster
        t_idx = min(frame * 2, len(times)-1)  # Multiply by 2 to speed up animation
        current_time = times[t_idx]
        
        # Get positions at this time
        pos_A = traj_A[t_idx]
        pos_B = traj_B[t_idx]
        
        # Update trajectories
        line_A.set_data(traj_A[:t_idx+1, 0], traj_A[:t_idx+1, 1])
        line_B.set_data(traj_B[:t_idx+1, 0], traj_B[:t_idx+1, 1])
        
        # Update current positions
        point_A.set_data([pos_A[0]], [pos_A[1]])
        point_B.set_data([pos_B[0]], [pos_B[1]])
        
        # Update vector field arrows
        field_A, _ = compute_vector_field_arrows(grid_x, grid_y, goal_A, pos_B, dt, repel=True)
        field_B, _ = compute_vector_field_arrows(grid_x, grid_y, goal_B, pos_A, dt, repel=True)
        
        # Remove old arrows and create new ones
        for a in arrow_artists_A:
            a.remove()
        for b in arrow_artists_B:
            b.remove()
        
        arrow_artists_A.clear()
        arrow_artists_B.clear()
        
        for x, y, u, v in field_A:
            arrow_A = ax.arrow(x, y, u*0.5, v*0.5, head_width=0.1, color='red', alpha=0.5)
            arrow_artists_A.append(arrow_A)
        
        for x, y, u, v in field_B:
            arrow_B = ax.arrow(x, y, u*0.5, v*0.5, head_width=0.1, color='blue', alpha=0.5)
            arrow_artists_B.append(arrow_B)
        
        # Update time text
        time_text.set_text(f'Time: {current_time:.1f}s')
        
        return [line_A, line_B, point_A, point_B, time_text] + arrow_artists_A + arrow_artists_B
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=range(len(times)//2), 
                         init_func=init, interval=200, blit=False)
    
    return anim, fig

# Show all plots
plt.show()

print("Generated all three plot sets:")
print("1. Both robots' trajectories and vector fields")
print("2. Robot A's trajectory with Robot B's vector field")
print("3. Robot B's trajectory with Robot A's vector field")
print("Each plot shows the evolution at time points: 0s, 5s, 10s, and 15s")