# Titan in Gazebo

This package provides:

* A URDF representation of Titan (see ./models/titan/) tested in Gazebo and Rviz
* A ROS launch file to use in Gazebo simulations
* A standalone ROS launch file to start Gazebo and spawn a Titan
* A fork of the SimpleTrackedVehiclePlugin that exists in Gazebo with bugfixes

## Launch files

### Include (sim.launch)

Include this from another launch file that starts Gazebo and requires a Titan.
For example, in SubT the following is used:

```
<include ns="$(arg robot_name)" file="$(find titan_gazebo)/launch/sim.launch">
  <arg name="extra_urdf" value="$(find subt_launch)/config/kitten/kitten_nav_backpack.urdf.xacro"/>
  <arg name="extra_urdf_args" value="nav_namespace:=/$(arg robot_name)"/>
  <arg name="init_pose" value="-x 0.0 -y $(arg init_y_position) -z 0.0 -R 0.0 -P 0.0 -Y 0.0"/>
  <arg name="namespace" value="/$(arg robot_name)"/>
  <arg name="output" value="$(arg output)"/>
  <arg name="ros_cmd_vel_topic" value="/kitten/cmd_vel_stamped"/>
</include>
```

### Standalone (gazebo.launch)

Checkout this repo into the src directory of a catkin workspace; build and
source the workspace; run `roslaunch titan_gazebo gazebo.launch`. To move the
Titan you will need to run something like this:

```
rostopic pub /titan/cmd_vel geometry_msgs/TwistStamped "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
twist:
  linear:
    x: 1.0
    y: 0.0
    z: 0.0
  angular:
    x: 0.0
    y: 0.0
    z: 0.0"
```
