import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# from matplotlib.patches import Rectangle
# from matplotlib.offsetbox import AnnotationBbox, TextArea
# from matplotlib.patches import FancyArrow

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
        # Priority: Robot A has higher priority
        direction_A, _ = compute_action(traj_A[-1], goal_A, traj_B[-1])
        dist_A = np.linalg.norm(goal_A - traj_A[-1])
        step_size_A = min(dt, dist_A)
        next_pos_A = traj_A[-1] + step_size_A * direction_A

        # Robot B decides whether to wait
        distance_to_A = np.linalg.norm(traj_B[-1] - traj_A[-1])
        direction_to_A = traj_A[-1] - traj_B[-1]
        same_heading = np.dot(normalize(goal_B - traj_B[-1]), normalize(direction_to_A)) > 0.7

        if distance_to_A < 1.5 and same_heading:
            # Robot B waits (give-way)
            next_pos_B = traj_B[-1]
        else:
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

# ----------- Plot 1: Both Robots' Vector Fields -----------
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
            # for idx, (x, y, label) in enumerate(ann_A):
            #     if idx % 10 == 0:  # Only show some annotations to avoid clutter
            #         text_box = TextArea(label, textprops=dict(color='red', size=8, multialignment='center'))
            #         ab = AnnotationBbox(text_box, (x, y),
            #                         xybox=(x + 0.3, y + 0.3),
            #                         xycoords='data',
            #                         boxcoords="data",
            #                         box_alignment=(0, 0),
            #                         bboxprops=dict(facecolor='white', alpha=0.8, edgecolor='red'),
            #                         arrowprops=dict(arrowstyle="->", color='red'))
            #         ax.add_artist(ab)
    
    for idx, (x, y, label) in enumerate(ann_B):
        if idx % 10 == 0 and idx % 11 != 0:  # Offset to avoid overlap
            ax.text(x + 0.1, y - 0.2, label, fontsize=8, color='blue')
    
    # # Mark current positions (no trajectories)
    # ax.plot(*pos_A, 'ro', markersize=8)
    # ax.plot(*pos_B, 'bo', markersize=8)
    # With:
    robot_size = 20  # Control size of robots - adjust as needed
    ax.plot(*pos_A, marker='s', color='red', markersize=robot_size)  # 's' for square
    ax.plot(*pos_B, marker='s', color='blue', markersize=robot_size)
    
    # Add time annotations at current positions
    ax.text(pos_A[0] + 0.1, pos_A[1], f"{current_time:.1f}s", color='red', fontsize=10)
    ax.text(pos_B[0] + 0.1, pos_B[1], f"{current_time:.1f}s", color='blue', fontsize=10)
    
    # Add obstacles
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # # Plot start and goal positions
    # ax.plot(*start_A, 'ro', label='Start A')
    # ax.plot(*start_B, 'bo', label='Start B')
    # With:
    start_size = 14  # Control size of starting positions - adjust as needed
    ax.plot(*start_A, marker='^', color='red', markersize=start_size, label='Start A')  # '^' for triangle
    ax.plot(*start_B, marker='^', color='blue', markersize=start_size, label='Start B')
    # ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    # ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    # With:
    goal_size = 16  # Control size of goals - adjust as needed
    ax.plot(*goal_A, marker='o', color='red', markersize=goal_size, label='Goal A')  # 'o' for circle
    ax.plot(*goal_B, marker='o', color='blue', markersize=goal_size, label='Goal B')
    
    ax.set_title(f"Both Robots' Positions and Vector Fields at Time: {current_time:.1f}s")
    ax.axis("equal")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)

# # Add legend to the last subplot
# axes1[-1].legend(loc='upper right')
# Collect handles/labels manually for clarity
# Define custom legend handles
from matplotlib.lines import Line2D

# Define custom legend handles
handles = [
    Line2D([], [], marker='^', color='red', linestyle='None', markersize=6, label='Start A'),
    Line2D([], [], marker='^', color='blue', linestyle='None', markersize=6, label='Start B'),
    Line2D([], [], marker='o', color='red', linestyle='None', markersize=6, label='Goal A'),
    Line2D([], [], marker='o', color='blue', linestyle='None', markersize=6, label='Goal B'),
    Line2D([], [], marker='s', color='red', linestyle='None', markersize=6, label='Robot A'),
    Line2D([], [], marker='s', color='blue', linestyle='None', markersize=6, label='Robot B'),
    Line2D([], [], color='black', linewidth=8, label='Obstacle'),
    Line2D([], [], color='red', linewidth=2, marker='>', markersize=6, label='Vector Field A'),
    Line2D([], [], color='blue', linewidth=2, marker='>', markersize=6, label='Vector Field B'),
]

# Add the legend
axes1[-1].legend(handles=handles, loc='upper right', fontsize=12)


plt.tight_layout()
plt.savefig("both_robots_positions_and_fields.png")

# ----------- Plot 2: Robot A Position with Robot B Vector Field -----------
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
    
    # # Mark current position of Robot A (no trajectory)
    # ax.plot(*pos_A, 'ro', markersize=8)
    robot_size = 20  # Control size of robots - adjust as needed
    ax.plot(*pos_A, marker='s', color='red', markersize=robot_size)  # 's' for square
    
    # Add time annotation at current position
    ax.text(pos_A[0] + 0.1, pos_A[1], f"{current_time:.1f}s", color='red', fontsize=10)
    
    # Add obstacles
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # # Plot start and goal positions
    # ax.plot(*start_A, 'ro', label='Start A')
    # ax.plot(*start_B, 'bo', label='Start B')
    # # With:
    start_size = 14  # Control size of starting positions - adjust as needed
    ax.plot(*start_A, marker='^', color='red', markersize=start_size, label='Start A')  # '^' for triangle
    ax.plot(*start_B, marker='^', color='blue', markersize=start_size, label='Start B')
    # ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    # ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    # With:
    goal_size = 16  # Control size of goals - adjust as needed
    ax.plot(*goal_A, marker='o', color='red', markersize=goal_size, label='Goal A')  # 'o' for circle
    ax.plot(*goal_B, marker='o', color='blue', markersize=goal_size, label='Goal B')
    
    ax.set_title(f"Robot A Position with Robot B Vector Field at Time: {current_time:.1f}s")
    ax.axis("equal")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)

# Add legend to the last subplot
# axes2[-1].legend(loc='upper right')

# Define custom legend handles
handles = [
    Line2D([], [], marker='^', color='red', linestyle='None', markersize=10, label='Start A'),
    Line2D([], [], marker='^', color='blue', linestyle='None', markersize=10, label='Start B'),
    Line2D([], [], marker='o', color='red', linestyle='None', markersize=10, label='Goal A'),
    Line2D([], [], marker='o', color='blue', linestyle='None', markersize=10, label='Goal B'),
    Line2D([], [], marker='s', color='red', linestyle='None', markersize=10, label='Robot A'),
    # Line2D([], [], marker='s', color='blue', linestyle='None', markersize=10, label='Robot B'),
    Line2D([], [], color='black', linewidth=8, label='Obstacle'),
    # Line2D([], [], color='red', linewidth=2, marker='>', markersize=10, label='Vector Field A'),
    Line2D([], [], color='blue', linewidth=2, marker='>', markersize=10, label='Vector Field B'),
]

# Add the legend
axes2[-1].legend(handles=handles, loc='upper right', fontsize=15)

plt.tight_layout()
plt.savefig("robot_A_pos_with_robot_B_field.png")

# ----------- Plot 3: Robot B Position with Robot A Vector Field -----------
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
    
    # # Mark current position of Robot B (no trajectory)
    # ax.plot(*pos_B, 'bo', markersize=8)
    robot_size = 20  # Control size of robots - adjust as needed
    # ax.plot(*pos_A, marker='s', color='red', markersize=robot_size)  # 's' for square
    ax.plot(*pos_B, marker='s', color='blue', markersize=robot_size)
    
    # Add time annotation at current position
    ax.text(pos_B[0] + 0.1, pos_B[1], f"{current_time:.1f}s", color='blue', fontsize=10)
    
    # Add obstacles
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # # Plot start and goal positions
    # ax.plot(*start_A, 'ro', label='Start A')
    # ax.plot(*start_B, 'bo', label='Start B')
    # With:
    start_size = 14  # Control size of starting positions - adjust as needed
    ax.plot(*start_A, marker='^', color='red', markersize=start_size, label='Start A')  # '^' for triangle
    ax.plot(*start_B, marker='^', color='blue', markersize=start_size, label='Start B')
    # ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    # ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    # With:
    goal_size = 16  # Control size of goals - adjust as needed
    ax.plot(*goal_A, marker='o', color='red', markersize=goal_size, label='Goal A')  # 'o' for circle
    ax.plot(*goal_B, marker='o', color='blue', markersize=goal_size, label='Goal B')
    
    ax.set_title(f"Robot B Position with Robot A Vector Field at Time: {current_time:.1f}s")
    ax.axis("equal")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 11.5)
    ax.grid(True)

# # Add legend to the last subplot
# axes3[-1].legend(loc='upper right')


# Define custom legend handles
handles = [
    Line2D([], [], marker='^', color='red', linestyle='None', markersize=10, label='Start A'),
    Line2D([], [], marker='^', color='blue', linestyle='None', markersize=10, label='Start B'),
    Line2D([], [], marker='o', color='red', linestyle='None', markersize=10, label='Goal A'),
    Line2D([], [], marker='o', color='blue', linestyle='None', markersize=10, label='Goal B'),
    # Line2D([], [], marker='s', color='red', linestyle='None', markersize=10, label='Robot A'),
    Line2D([], [], marker='s', color='blue', linestyle='None', markersize=10, label='Robot B'),
    Line2D([], [], color='black', linewidth=8, label='Obstacle'),
    Line2D([], [], color='red', linewidth=2, marker='>', markersize=10, label='Vector Field A'),
    # Line2D([], [], color='blue', linewidth=2, marker='>', markersize=10, label='Vector Field B'),
]

# Add the legend
axes3[-1].legend(handles=handles, loc='upper right', fontsize=15)

plt.tight_layout()
plt.savefig("robot_B_pos_with_robot_A_field.png")

# Create an animation showing the vector fields with arrows
def create_arrow_animation():
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # # Set up the initial plot with obstacles and goals
    # ax.plot(*start_A, 'ro', label='Start A')
    # ax.plot(*start_B, 'bo', label='Start B')
    # With:
    start_size = 14  # Control size of starting positions - adjust as needed
    ax.plot(*start_A, marker='^', color='red', markersize=start_size, label='Start A')  # '^' for triangle
    ax.plot(*start_B, marker='^', color='blue', markersize=start_size, label='Start B')
    # ax.plot(*goal_A, 'r*', markersize=12, label='Goal A')
    # ax.plot(*goal_B, 'b*', markersize=12, label='Goal B')
    # With:
    goal_size = 16  # Control size of goals - adjust as needed
    ax.plot(*goal_A, marker='o', color='red', markersize=goal_size, label='Goal A')  # 'o' for circle
    ax.plot(*goal_B, marker='o', color='blue', markersize=goal_size, label='Goal B')
    ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
    ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)
    
    # Current position markers (no trajectories)
    point_A = ax.plot([], [], 'ro', markersize=8)[0]
    point_B = ax.plot([], [], 'bo', markersize=8)[0]
    
    # Time text for positions
    time_text_A = ax.text(0, 0, '', color='red')
    time_text_B = ax.text(0, 0, '', color='blue')
    
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
    ax.set_title("Robot Positions and Vector Fields Evolution Over Time")
    ax.legend(loc='upper right')
    
    def init():
        point_A.set_data([], [])
        point_B.set_data([], [])
        time_text.set_text('')
        time_text_A.set_text('')
        time_text_B.set_text('')
        return [point_A, point_B, time_text, time_text_A, time_text_B] + arrow_artists_A + arrow_artists_B
    
    def update(frame):
        # Skip frames to make animation faster
        t_idx = min(frame * 2, len(times)-1)  # Multiply by 2 to speed up animation
        current_time = times[t_idx]
        
        # Get positions at this time
        pos_A = traj_A[t_idx]
        pos_B = traj_B[t_idx]
        
        # Update current positions (no trajectories)
        point_A.set_data([pos_A[0]], [pos_A[1]])
        point_B.set_data([pos_B[0]], [pos_B[1]])
        
        # Update time texts for positions
        time_text_A.set_position((pos_A[0] + 0.1, pos_A[1]))
        time_text_A.set_text(f"{current_time:.1f}s")
        time_text_B.set_position((pos_B[0] + 0.1, pos_B[1]))
        time_text_B.set_text(f"{current_time:.1f}s")
        
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
        
        # Update main time text
        time_text.set_text(f'Time: {current_time:.1f}s')
        
        return [point_A, point_B, time_text, time_text_A, time_text_B] + arrow_artists_A + arrow_artists_B
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=range(len(times)//2), 
                         init_func=init, interval=200, blit=False)
    
    return anim, fig

# Show all plots
plt.show()

print("Generated all three plot sets:")
print("1. Both robots' positions and vector fields")
print("2. Robot A's position with Robot B's vector field")
print("3. Robot B's position with Robot A's vector field")
print("Each plot shows the positions at time points: 0s, 5s, 10s, and 15s")