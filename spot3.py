import pybullet as p
import time

# Connect to the PyBullet simulation environment
p.connect(p.GUI)
p.setGravity(0, 0, -9.8)

objects = p.loadMJCF("./assets/xmls/ground.xml")
worldId = objects[0]

# Load the Spot URDF model
spot_urdf_file = "/home/kom018/spot_mini_mini/spot_best/spot_2/src/spotmicro/util/pybullet_data/assets/urdf/spot.urdf"
spot_robot = p.loadURDF(spot_urdf_file, [0, 0, 2])

# Define linear and angular velocities
linear_velocity = 0.0
angular_velocity = 0.0

# Control loop
while True:
    # Get keyboard events
    keys = p.getKeyboardEvents()
    
    # Update linear and angular velocities based on key presses
    for key, state in keys.items():
        if state & p.KEY_IS_DOWN:
            if key == p.B3G_UP_ARROW:
                linear_velocity = 0.1  # Move forward
                angular_velocity = 0.0
            elif key == p.B3G_DOWN_ARROW:
                linear_velocity = -0.1  # Move backward
                angular_velocity = 0.0
            elif key == p.B3G_LEFT_ARROW:
                linear_velocity = 0.0
                angular_velocity = 0.1  # Turn left
            elif key == p.B3G_RIGHT_ARROW:
                linear_velocity = 0.0
                angular_velocity = -0.1  # Turn right

    # Reset joint target velocities
    for joint_index in range(p.getNumJoints(spot_robot)):
        p.setJointMotorControl2(spot_robot, joint_index, p.VELOCITY_CONTROL, targetVelocity=0, force=100)

    # Calculate joint target velocities for walking gait
    for leg_index in range(4):
        shoulder_joint = leg_index * 5 + 2
        hip_joint = leg_index * 5 + 3
        knee_joint = leg_index * 5 + 4

        # Determine leg swing based on linear and angular velocities
        if linear_velocity != 0.0:
            if leg_index % 2 == 0:  # Even legs
                target_swing = linear_velocity
            else:  # Odd legs
                target_swing = -linear_velocity
        else:
            target_swing = 0.0

        # Set joint target velocities
        p.setJointMotorControl2(spot_robot, shoulder_joint, p.VELOCITY_CONTROL, targetVelocity=target_swing, force=100)
        p.setJointMotorControl2(spot_robot, hip_joint, p.VELOCITY_CONTROL, targetVelocity=-target_swing, force=100)

    # Step simulation
    p.stepSimulation()
    time.sleep(1. / 240.)
