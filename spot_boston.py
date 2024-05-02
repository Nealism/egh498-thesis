import pybullet as p
import time
import numpy as np




# Connect to PyBullet
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.8)



p.setRealTimeSimulation(1)


objects = p.loadMJCF("./assets/xmls/ground.xml")
worldId = objects[0]
# Load Spot URDF
robot_urdf_file = "/home/kom018/spot_ros/spot_description/urdf/spot.urdf.xacro"



# Function to set joint velocities
def set_joint_velocities(robot_id, joint_indices, velocities):
    for i, joint_index in enumerate(joint_indices):
        p.setJointMotorControl2(robot_id, joint_index, p.VELOCITY_CONTROL, targetVelocity=velocities[i])


robot_start_pos = [0, 0, 0.3]  # Adjust starting position as needed
robot_start_orientation = p.getQuaternionFromEuler([0, 0, 0])  # Adjust starting orientation as needed
robot_id = p.loadURDF(robot_urdf_file, robot_start_pos, robot_start_orientation)

# Get joint information
num_joints = p.getNumJoints(robot_id)
joint_indices = []
for i in range(num_joints):
    joint_info = p.getJointInfo(robot_id, i)
    joint_name = joint_info[1].decode("utf-8")
    if "hip" in joint_name and "x" in joint_name:
        joint_indices.append(i)
    elif "hip" in joint_name and "y" in joint_name:
        joint_indices.append(i)
    elif "knee" in joint_name:
        joint_indices.append(i)

# Control loop parameters
t = 0
linear_velocity = 0  # Adjust as needed
angular_velocity = 0  # Adjust as needed
lateral_fraction = 0  # Adjust as needed

# Main control loop
while True:
    t += 1 / 240  # Assuming 240 Hz simulation frequency

    # Calculate joint velocities based on input commands
    joint_velocities = [linear_velocity,  # Front left hip x
                        lateral_fraction * linear_velocity,  # Front left hip y
                        -angular_velocity,  # Front left knee
                        linear_velocity,  # Front right hip x
                        -lateral_fraction * linear_velocity,  # Front right hip y
                        angular_velocity,  # Front right knee
                        -linear_velocity,  # Rear left hip x
                        lateral_fraction * linear_velocity,  # Rear left hip y
                        -angular_velocity,  # Rear left knee
                        -linear_velocity,  # Rear right hip x
                        -lateral_fraction * linear_velocity,  # Rear right hip y
                        angular_velocity]  # Rear right knee

    # Update joint velocities
    set_joint_velocities(robot_id, joint_indices, joint_velocities)

    time.sleep(1 / 240)  # Control loop frequency

# Disconnect from PyBullet
p.disconnect()
