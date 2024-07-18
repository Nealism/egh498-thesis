import pybullet as p
import pybullet_data
import time
import numpy as np

# Function to create a box with a hollow middle area
def create_attached_box(box_length, box_width, box_height, hollow_radius):
    # Define the box dimensions
    box_half_extents = [box_length / 2, box_width / 2, box_height / 2]
    
    # Create the external box
    box_visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=box_half_extents, rgbaColor=[1, 0, 0, 0.5])
    box_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=box_half_extents)
    box_position = [0, 0, box_height / 2]  # Position the box at z=0
    box = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=box_collision_shape,
                            baseVisualShapeIndex=box_visual_shape, basePosition=box_position)

    # Create a cylindrical hollow shape
    hollow_visual_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=hollow_radius, length=box_height,
                                              rgbaColor=[0, 1, 0, 0.5], visualFramePosition=[0, 0, 0])
    hollow_collision_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=hollow_radius, height=box_height)

    # Position the hollow shape inside the box
    hollow_position = [0, 0, 0]  # Centered inside the box
    hollow = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=hollow_collision_shape,
                               baseVisualShapeIndex=hollow_visual_shape, basePosition=hollow_position)

    return box, hollow

# Connect to the physics server
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Create the attached box with a hollow middle area
box_length = 1.4
box_width = 0.78
box_height = 0.3
hollow_radius = 0.3  # Radius of the hollow area

box, hollow = create_attached_box(box_length, box_width, box_height, hollow_radius)

# Run the simulation
while True:
    p.stepSimulation()
    time.sleep(1./240.)

# Disconnect from the physics server
p.disconnect()
