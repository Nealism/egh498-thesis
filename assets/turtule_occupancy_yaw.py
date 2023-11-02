import pybullet as p
import numpy as np
import cv2
import time
from pybullet import getEulerFromQuaternion


# Global map initialization
global_map_size_x = 100.0
global_map_size_y = 100.0
global_resolution = 0.1  # 0.1 meters per row and column
global_num_rows = int(global_map_size_y / global_resolution)
global_num_cols = int(global_map_size_x / global_resolution)
global_map = np.zeros((global_num_rows, global_num_cols), dtype=np.float32)

# Local map initialization
local_map_size_x = 8.0
local_map_size_y = 8.0
local_resolution = global_resolution
local_num_rows = int(local_map_size_y / local_resolution)
local_num_cols = int(local_map_size_x / local_resolution)
local_map = np.zeros((local_num_rows, local_num_cols), dtype=np.float32)




# Function to insert an obstacle into the global map
# Function to insert an obstacle into the global map and place a 3D object in PyBullet
def insert_obstacle_with_object(position_x, position_y, yaw, length, width, height):
    # Convert obstacle position and dimensions to grid indices
    grid_x_center = int((position_x + global_map_size_x / 2) / global_resolution)
    grid_y_center = int((position_y + global_map_size_y / 2) / global_resolution)
    
    # Calculate half-length and half-width in grid cells
    half_length_cells = int(length / (2 * global_resolution))
    half_width_cells = int(width / (2 * global_resolution))
    
    # Set the obstacle region in the global map to a higher value for visualization
    for i in range(grid_x_center - half_length_cells, grid_x_center + half_length_cells + 1):
        for j in range(grid_y_center - half_width_cells, grid_y_center + half_width_cells + 1):
            if 0 <= i < global_num_rows and 0 <= j < global_num_cols:
                global_map[i, j] = 2.0  # Mark the obstacle as occupied with a value of 2

    # # Create a PyBullet box object to represent the obstacle
    # p.createMultiBody(
    #     baseMass=1,
    #     baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_BOX, halfExtents=[length/2, width/2, height/2]),
    #     basePosition=[position_x, position_y, height / 2],
    #     baseOrientation=p.getQuaternionFromEuler([0, 0, yaw]),
    # )

# Function to get the local heightmap with robot's yaw
def get_heightmap_with_yaw(robot_position, robot_yaw):
    # Calculate the boundaries of the local map based on robot_position and local_map_size
    local_x_min = robot_position[0] - local_map_size_x / 2
    local_x_max = robot_position[0] + local_map_size_x / 2
    local_y_min = robot_position[1] - local_map_size_y / 2
    local_y_max = robot_position[1] + local_map_size_y / 2

    # Calculate grid indices for the local map within the global map
    local_x_indices = np.clip(
        np.array(((local_x_min + global_map_size_x / 2) / global_resolution), dtype=int), 0, global_num_rows - 1
    )
    local_y_indices = np.clip(
        np.array(((local_y_min + global_map_size_y / 2) / global_resolution), dtype=int), 0, global_num_cols - 1
    )

    # Extract the local heightmap from the global map
    local_heightmap = global_map[
        local_x_indices:local_x_indices + local_num_rows, local_y_indices:local_y_indices + local_num_cols
    ]

    # Calculate the position of the local heightmap within the local map
    local_heightmap_x_min = local_x_min
    local_heightmap_x_max = local_x_max
    local_heightmap_y_min = local_y_min
    local_heightmap_y_max = local_y_max

    # Rotate the local heightmap based on the robot's yaw
    #angle = -robot_yaw  # Negative angle for counterclockwise rotation
    # Convert robot_yaw to degrees
    robot_yaw_degrees = np.degrees(robot_yaw)

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(
        (local_num_cols / 2, local_num_rows / 2),
        -robot_yaw_degrees,  # Negative angle to match PyBullet's coordinate system
        1.0
    )

    # Apply the rotation to the local heightmap
    rotated_local_heightmap = cv2.warpAffine(local_heightmap.astype(np.float32), rotation_matrix, (local_num_cols, local_num_rows), flags=cv2.INTER_NEAREST)

    return rotated_local_heightmap, (local_heightmap_x_min, local_heightmap_x_max, local_heightmap_y_min, local_heightmap_y_max)


# Function to visualize the maps using OpenCV


# Function to visualize the maps using OpenCV
def visualize_maps(global_map, local_heightmap, local_heightmap_position, turtlebot_position, robot_yaw):
    
    print("global_map", global_map)
    np.savetxt('global_map.txt', global_map)
    # Scale the maps for visualization
    scaled_global_map = (global_map - np.min(global_map)) / (np.max(global_map) - np.min(global_map)) * 200
    scaled_heightmap = (local_heightmap - np.min(local_heightmap)) / (np.max(local_heightmap) - np.min(local_heightmap)) * 200

    # Convert to uint8 and create color images
    scaled_global_map = scaled_global_map.astype(np.uint8)
    scaled_heightmap = scaled_heightmap.astype(np.uint8)

    global_map_image = cv2.cvtColor(scaled_global_map, cv2.COLOR_GRAY2BGR)
    heightmap_image = cv2.cvtColor(scaled_heightmap, cv2.COLOR_GRAY2BGR)

    # Set colors: Blue for global map, Green for local heightmap, Red for obstacles
    global_map_image[:, :, 0] = 255  # Blue channel to 255 for global map (blue color)
    heightmap_image[:, :, 1] = 255  # Green channel to 255 for local heightmap (green color)

    # Find obstacle cells and mark them as red
    obstacle_indices = np.where(global_map == 2.0)
    for i, j in zip(obstacle_indices[0], obstacle_indices[1]):
        global_map_image[i, j] = (0, 0, 255)  # Red color

    # Calculate the position of the local heightmap within the global map
    local_map_x_min = local_heightmap_position[0]
    local_map_x_max = local_heightmap_position[1]
    local_map_y_min = local_heightmap_position[2]
    local_map_y_max = local_heightmap_position[3]

    local_map_x_min_index = int((local_map_x_min + global_map_size_x / 2) / global_resolution)
    local_map_x_max_index = int((local_map_x_max + global_map_size_x / 2) / global_resolution)
    local_map_y_min_index = int((local_map_y_min + global_map_size_y / 2) / global_resolution)
    local_map_y_max_index = int((local_map_y_max + global_map_size_y / 2) / global_resolution)

    # Rotate the local heightmap back to its original orientation
    rotated_heightmap_image = cv2.warpAffine(heightmap_image, cv2.getRotationMatrix2D((local_num_cols / 2, local_num_rows / 2), np.degrees(-robot_yaw), 1), (local_num_cols, local_num_rows))
    
    # Overlay the rotated local heightmap on the global map
    global_map_image[
        local_map_x_min_index:local_map_x_max_index,
        local_map_y_min_index:local_map_y_max_index,
    ] = rotated_heightmap_image

    # Draw a blue dot for the turtlebot's position
    turtlebot_x_index = int((turtlebot_position[0] + global_map_size_x / 2) / global_resolution)
    turtlebot_y_index = int((turtlebot_position[1] + global_map_size_y / 2) / global_resolution)
    global_map_image = cv2.circle(global_map_image, (turtlebot_y_index, turtlebot_x_index), 5, (255, 0, 0), -1)

    # Display the combined map with the turtlebot in the center
    cv2.imshow("Global Map with Local Heightmap", global_map_image)
    cv2.waitKey(10)


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



# Create a PyBullet box object to represent the obstacle (as a static object)
obstacle_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1.0 / 2, 1.0 / 2, 0.6 / 2])
obstacle_id = p.createMultiBody(
    baseMass=0,  # Set mass to 0 to make it a static object
    baseCollisionShapeIndex=obstacle_shape,
    basePosition=[2.0, 2.0, 0.2 / 2],  # Initial position
    baseOrientation=p.getQuaternionFromEuler([0, 0, 0]),
)

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

    insert_obstacle_with_object(2.0, 2.0, 0, 1.0, 1.0, 0.2)  # Place the obstacle and a PyBullet object

    # Get the base position and orientation of the TurtleBot
    pos, orn = p.getBasePositionAndOrientation(turtlebotId)
    robot_position = pos[:2]
    #print("pos",pos,"robot_pos",robot_position)
    
    # Get the Euler angles from the orientation quaternion (roll, pitch, yaw)
    roll, pitch, robot_yaw = getEulerFromQuaternion(orn)


    # Get the local heightmap and its position within the local map
    local_heightmap, local_heightmap_position = get_heightmap_with_yaw(robot_position,robot_yaw)

    # Visualize both global map and local heightmap
    visualize_maps(global_map, local_heightmap, local_heightmap_position, robot_position,robot_yaw)

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

    rightWheelVelocity += (forward + turn) * speed
    leftWheelVelocity += (forward - turn) * speed

    p.setJointMotorControl2(turtlebotId, 0, p.VELOCITY_CONTROL, targetVelocity=leftWheelVelocity, force=1000)
    p.setJointMotorControl2(turtlebotId, 1, p.VELOCITY_CONTROL, targetVelocity=rightWheelVelocity, force=1000)

# Close the PyBullet simulation
p.disconnect()
