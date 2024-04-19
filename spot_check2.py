import pybullet as p
import pybullet_data

# Initialize PyBullet simulation environment
p.connect(p.GUI)  # or p.DIRECT for non-graphical simulation
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # Add path to additional resources

# Load Spot URDF model
# spot_urdf_file = "/home/kom018/spot_mini_mini/spot_best/spot_2/src/spotmicro/util/pybullet_data/assets/urdf/spot.urdf"
spot_urdf_file = "/home/kom018/spot_ros/spot_description/urdf/spot.urdf.xacro"
robot_id = p.loadURDF(spot_urdf_file, [0, 0, 0], useFixedBase=True)

# Get information about the robot's joints and links
num_joints = p.getNumJoints(robot_id)
joint_info = [p.getJointInfo(robot_id, i) for i in range(num_joints)]
link_names = [p.getBodyInfo(robot_id)[0].decode("utf-8") for i in range(p.getNumBodies())]

print("Number of joints:", num_joints)
print("Joint information:")
for info in joint_info:
    print(info)

print("Link names:")
print(link_names)

# Control the robot (if needed)
# Add your control logic here

# Disconnect from the PyBullet simulation environment
p.disconnect()
