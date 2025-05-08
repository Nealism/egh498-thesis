import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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

dt = 0.5
grid_x = np.linspace(1, 9, 9)
grid_y = np.linspace(1, 11, 9)

start_A = np.array([3, 1])
goal_A = np.array([6, 9])
start_B = np.array([6, 1])
goal_B = np.array([3, 9])

pos_A = np.array([3, 3])
pos_B = np.array([6, 3])

fig, ax = plt.subplots(figsize=(10, 10))

for x in grid_x:
    for y in grid_y:
        pos = np.array([x, y])
        action, _ = compute_action(pos, goal_A, pos_B)
        print("actions",action,pos)
        ax.arrow(x, y, action[0]*0.5, action[1]*0.5, head_width=0.1, color='red', alpha=0.5)

ax.plot(*pos_A, marker='s', color='red', markersize=20)
ax.plot(*pos_B, marker='s', color='blue', markersize=20)

ax.text(pos_A[0] + 0.1, pos_A[1], "Robot A", color='red', fontsize=10)
ax.text(pos_B[0] + 0.1, pos_B[1], "Robot B", color='blue', fontsize=10)

ax.plot([2, 4.5], [5, 5], 'k-', linewidth=8)
ax.plot([5.5, 8], [5, 5], 'k-', linewidth=8)

ax.plot(*start_A, marker='^', color='red', markersize=14, label='Start A')
ax.plot(*start_B, marker='^', color='blue', markersize=14, label='Start B')
ax.plot(*goal_A, marker='o', color='red', markersize=16, label='Goal A')
ax.plot(*goal_B, marker='o', color='blue', markersize=16, label='Goal B')

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
ax.set_title("Robot A Vector Field with Robot B Position")
ax.axis("equal")
ax.set_xlim(0.5, 9.5)
ax.set_ylim(0.5, 11.5)
ax.grid(True)

plt.tight_layout()
plt.savefig("robot_vector_field_simple.png")
plt.show()