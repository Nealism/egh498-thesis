import pybullet as p
import time
import pybullet_data

# Initialize PyBullet simulation environment
p.connect(p.GUI)  # or p.DIRECT for non-graphical simulation
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # Add path to additional resources

# Load Spot URDF model
spot_urdf_file = "/home/kom018/spot_mini_mini/spot_best/spot_2/src/spotmicro/util/pybullet_data/assets/urdf/spot.urdf"
robot_id = p.loadURDF(spot_urdf_file, [0, 0, 0], useFixedBase=True)

# Simulate and render the robot for 50 seconds
for _ in range(5000):
    p.stepSimulation()
    time.sleep(0.01)  # control simulation speed (optional)

# Keep the simulation window open for a while after simulation ends
time.sleep(5)

# Disconnect from the PyBullet simulation environment
p.disconnect()
