import pybullet as p
import numpy as np
import cv2
import time

# Global map initialization
global_map_size_x = 100.0
global_map_size_y = 100.0
global_resolution = 0.1  # 0.1 meters per row and column
global_num_rows = int(global_map_size_y / global_resolution)
global_num_cols = int(global_map_size_x / global_resolution)
global_map = np.zeros((global_num_rows, global_num_cols), dtype=np.float32)

# Local map initialization
local_map_size_x = 80.0
local_map_size_y = 80.0
local_resolution = global_resolution
local_num_rows = int(local_map_size_y / local_resolution)
local_num_cols = int(local_map_size_x / local_resolution)
local_map = np.zeros((local_num_rows, local_num_cols), dtype=np.float32)

# Function to insert an obstacle into the global map
# def insert_obstacle(position_x, position_y, yaw, length, width, height):
#     # Convert obstacle position and dimensions to grid indices
#     grid_x_indices = np.clip(
#         ((position_x - global_map_size_x / 2) / global_resolution).astype(int), 0, global_num_rows - 1
#     )
#     grid_y_indices = np.clip(
#         ((position_y - global_map_size_y / 2) / global_resolution).astype(int), 0, global_num_cols - 1
#     )

#     # Update the global_map at the calculated indices to mark the obstacle
#     global_map[grid_x_indices, grid_y_indices] = 1  # Mark the obstacle as occupied

def insert_obstacle(position_x, position_y, yaw, length, width, height):
    # Convert obstacle position and dimensions to grid indices
    grid_x_center = int((position_x + global_map_size_x / 2) / global_resolution)
    grid_y_center = int((position_y + global_map_size_y / 2) / global_resolution)
    
    # Calculate half-length and half-width in grid cells
    half_length_cells = int(length / (2 * global_resolution))
    half_width_cells = int(width / (2 * global_resolution))
    
    # Set the obstacle region in the global map to occupied (1)
    for i in range(grid_x_center - half_length_cells, grid_x_center + half_length_cells + 1):
        for j in range(grid_y_center - half_width_cells, grid_y_center + half_width_cells + 1):
            if 0 <= i < global_num_rows and 0 <= j < global_num_cols:
                global_map[i, j] = 1.0  # Mark the obstacle as occupied

# Function to get the local heightmap
def get_heightmap(robot_position):
    # Calculate the boundaries of the local map based on robot_position and local_map_size
    local_x_min = robot_position[0] - local_map_size_x / 2
    local_x_max = robot_position[0] + local_map_size_x / 2
    local_y_min = robot_position[1] - local_map_size_y / 2
    local_y_max = robot_position[1] + local_map_size_y / 2

    # Calculate grid indices for the local map within the global map
    # Calculate grid indices for the local map within the global map
    local_x_indices = np.clip(
        np.array(((local_x_min + global_map_size_x / 2) / global_resolution), dtype=int), 0, global_num_rows - 1
    )
    local_y_indices = np.clip(
        np.array(((local_y_min + global_map_size_y / 2) / global_resolution), dtype=int), 0, global_num_cols - 1
    )
    # local_x_indices = np.clip(
    #     ((local_x_min + global_map_size_x / 2) / global_resolution).astype(int), 0, global_num_rows - 1
    # )
    # local_y_indices = np.clip(
    #     ((local_y_min + global_map_size_y / 2) / global_resolution).astype(int), 0, global_num_cols - 1
    # )

    # Extract the local heightmap from the global map
    local_heightmap = global_map[
        local_x_indices:local_x_indices + local_num_rows, local_y_indices:local_y_indices + local_num_cols
    ]

    return local_heightmap

# Function to visualize the heightmap using OpenCV
def visualize_heightmap(heightmap):
    # Scale the heightmap values to the range [0, 255] for visualization
    scaled_heightmap = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap)) * 200

    # Convert to uint8
    scaled_heightmap = scaled_heightmap.astype(np.uint8)

    # Create a grayscale image
    heightmap_image = cv2.cvtColor(scaled_heightmap, cv2.COLOR_GRAY2BGR)

    # Display the image
    cv2.imshow("Heightmap", heightmap_image)
    cv2.waitKey(1)

# PyBullet simulation setup
p.connect(p.GUI)
p.setGravity(0, 0, -9.81)  # Set gravity
p.setTimeStep(1 / 240)  # Set time step

# Create a ground plane
planeId = p.createCollisionShape(p.GEOM_PLANE)
p.createMultiBody(0, planeId)

# Create a turtlebot (you'll need to provide the model URDF file)
turtlebotId = p.loadURDF("/home/kom018/pybullet_robots/data/turtlebot.urdf", [0, 0, 0.1])

# Simulation loop
robot_position = [0, 0]
# for _ in range(1000):
#     # Insert obstacles as needed (for demonstration, inserting a simple box obstacle)
#     if _ == 300:
#         insert_obstacle(2.0, 2.0, 0, 1.0, 1.0, 0.2)

#     # Get the turtlebot's position
#     pos, _ = p.getBasePositionAndOrientation(turtlebotId)
#     robot_position = pos[:2]

#     # Get and visualize the local heightmap
#     local_heightmap = get_heightmap(robot_position)
#     visualize_heightmap(local_heightmap)

#     # Move the turtlebot forward (you'll need to implement your robot's movement logic)
#     p.stepSimulation()
#     p.setJointMotorControl2(turtlebotId, 1, p.VELOCITY_CONTROL, targetVelocity=1.0, force=10)
p.setRealTimeSimulation(1)
for j in range (p.getNumJoints(turtlebotId)):
    print(p.getJointInfo(turtlebotId,j))
forward=0
turn=0
while (1):
    p.setGravity(0,0,-10)
    time.sleep(1./240.)
    keys = p.getKeyboardEvents()
    leftWheelVelocity=0
    rightWheelVelocity=0
    speed=10
    #if _ == 300:
        
    insert_obstacle(2.0, 2.0, 0, 1.0, 1.0, 0.2)

    # Get the turtlebot's position
    pos, _ = p.getBasePositionAndOrientation(turtlebotId)
    robot_position = pos[:2]

    # Get and visualize the local heightmap
    local_heightmap = get_heightmap(robot_position)
    visualize_heightmap(local_heightmap)
    for k,v in keys.items():
                
                if (k == p.B3G_RIGHT_ARROW and (v&p.KEY_WAS_TRIGGERED)):
                        turn = -0.5
                if (k == p.B3G_RIGHT_ARROW and (v&p.KEY_WAS_RELEASED)):
                        turn = 0
                if (k == p.B3G_LEFT_ARROW and (v&p.KEY_WAS_TRIGGERED)):
                        turn = 0.5
                if (k == p.B3G_LEFT_ARROW and (v&p.KEY_WAS_RELEASED)):
                        turn = 0

                if (k == p.B3G_UP_ARROW and (v&p.KEY_WAS_TRIGGERED)):
                        forward=1
                if (k == p.B3G_UP_ARROW and (v&p.KEY_WAS_RELEASED)):
                        forward=0
                if (k == p.B3G_DOWN_ARROW and (v&p.KEY_WAS_TRIGGERED)):
                        forward=-1
                if (k == p.B3G_DOWN_ARROW and (v&p.KEY_WAS_RELEASED)):
                        forward=0

    rightWheelVelocity+= (forward+turn)*speed
    leftWheelVelocity += (forward-turn)*speed
    
    p.setJointMotorControl2(turtlebotId,0,p.VELOCITY_CONTROL,targetVelocity=leftWheelVelocity,force=1000)
    p.setJointMotorControl2(turtlebotId,1,p.VELOCITY_CONTROL,targetVelocity=rightWheelVelocity,force=1000)

# Close the PyBullet simulation
p.disconnect()
