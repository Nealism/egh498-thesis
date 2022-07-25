#include <unordered_map>
#include <algorithm>

#include <ros/ros.h>

#include <geometry_msgs/Twist.h>
#include <geometry_msgs/TwistStamped.h>

#include <sensor_msgs/JointState.h>

#include <std_msgs/Float64.h>

#include <ignition/math/Quaternion.hh>

#include <gazebo/common/Plugin.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/transport/TransportTypes.hh>
#include <gazebo/transport/transport.hh>

namespace gazebo
{
class TitanSuspensionPlugin : public ModelPlugin
{
public:
  /// Load the parameters from SDF
  void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf)
  {
    // Get config params
    LoadParam(_sdf, "robot_namespace", robot_namespace_, _model->GetName());
    LoadParam(_sdf, "joint_name", joint_name_, "joint_1");
    LoadParam(_sdf, "suspension_stiffness", suspension_stiffness_, 1000.0d);
    LoadParam(_sdf, "suspension_preload", suspension_preload_, 100.0d);
    LoadParam(_sdf, "suspension_damping", suspension_damping_, 100.0d);
    LoadParam(_sdf, "suspension_reference", suspension_reference_, 0.0d);
  }

  /// Set up the subscribers and publishers
  void Init()
  {
    // Set up Gazebo publisher
    gazebo_node_ = gazebo::transport::NodePtr(new gazebo::transport::Node());
    gazebo_node_->Init(robot_namespace_);

    // Set up ROS subscriber
    if (!ros::isInitialized())
    {
      ROS_ERROR("TitanSuspensionPlugin::Load ROS not initialised");
    }

    nh_ = ros::NodeHandle("~");

    joint_state_sub_ = nh_.subscribe(robot_namespace_ + "/joint_states", 1, &TitanSuspensionPlugin::rosJointStateCallback, this);
    joint_effort_pub_ = nh_.advertise<std_msgs::Float64>(robot_namespace_ + "/" + joint_name_ + "/command", 1);
    ROS_INFO("Started suspension plugin for joint %s/%s", robot_namespace_.c_str(), joint_name_.c_str());
  }

private:

  /// ROS node_handle
  ros::NodeHandle nh_;

  /// Namespace for Gazebo
  std::string robot_namespace_;

  /// Joint name for suspension
  std::string joint_name_;

  /// ros pub and sub for joint control
  ros::Subscriber joint_state_sub_;

  /// Joint pub map for gazebo control
  ros::Publisher joint_effort_pub_;

  /// Suspension parameters
  double suspension_stiffness_ = 0.0;
  double suspension_preload_ = 0.0;
  double suspension_damping_ = 0.0;
  double suspension_reference_ = 0.0;

  /// Gazebo node
  gazebo::transport::NodePtr gazebo_node_;

  /// Callback on new joint states command from ROS
  void rosJointStateCallback(sensor_msgs::JointStateConstPtr msg)
  {
    std_msgs::Float64 cmd;

    for (uint i=0; i < msg->name.size(); i++)
    {
      if (msg->name.at(i) == joint_name_)
      {
        // apply spring stiffness and damping to each joint
        cmd.data = suspension_preload_ + suspension_stiffness_ * (suspension_reference_-msg->position[i]) + suspension_damping_ * -msg->velocity[i];
        joint_effort_pub_.publish(cmd);
      }
    }
  }
};

GZ_REGISTER_MODEL_PLUGIN(TitanSuspensionPlugin)

}  // namespace gazebo
