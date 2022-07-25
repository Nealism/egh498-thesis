#include <ros/ros.h>

#include <geometry_msgs/Twist.h>
#include <geometry_msgs/TwistStamped.h>

#include <ignition/math/Quaternion.hh>

#include <gazebo/common/Plugin.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/transport/TransportTypes.hh>
#include <gazebo/transport/transport.hh>

namespace gazebo
{
class TitanPlugin : public ModelPlugin
{
public:
  /// Load the parameters from SDF
  void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf)
  {
    // Get config params
    LoadParam(_sdf, "robot_namespace", robot_namespace_, _model->GetName());
    LoadParam(_sdf, "is_ros_cmd_vel_stamped", is_ros_cmd_vel_stamped_, true);
    LoadParam(_sdf, "ros_cmd_vel_topic", ros_cmd_vel_topic_, robot_namespace_ + "/cmd_vel");
    LoadParam(_sdf, "timeout", timeout_, 10.0d);
  }

  /// Set up the subscribers and publishers
  void Init()
  {
    // Set up Gazebo publisher
    gazebo_node_ = gazebo::transport::NodePtr(new gazebo::transport::Node());
    gazebo_node_->Init(robot_namespace_);
    gazebo_cmd_vel_publisher_ = gazebo_node_->Advertise<gazebo::msgs::Twist>("~/cmd_vel_twist");

    // Set up ROS subscriber
    if (!ros::isInitialized())
    {
      ROS_ERROR("TitanPlugin::Load ROS not initialised");
    }
    ros::NodeHandle node_private("~");
    if (is_ros_cmd_vel_stamped_)
    {
      ros_cmd_vel_subscriber_ = node_private.subscribe(ros_cmd_vel_topic_, 1, &TitanPlugin::rosCmdVelCallbackStamped,
                                                       this);
    }
    else
    {
      ros_cmd_vel_subscriber_ = node_private.subscribe(ros_cmd_vel_topic_, 1, &TitanPlugin::rosCmdVelCallbackUnstamped,
                                                       this);
    }
  }

private:
  /// Namespace for Gazebo
  std::string robot_namespace_;

  /// Topic for ROS
  std::string ros_cmd_vel_topic_;

  /// Is the velocity command from ROS timestamped?
  bool is_ros_cmd_vel_stamped_;

  /// If the most recent command is more than this many seconds old, stop moving
  double timeout_;

  /// Gazebo node
  gazebo::transport::NodePtr gazebo_node_;

  /// Gazebo publisher
  gazebo::transport::PublisherPtr gazebo_cmd_vel_publisher_;

  /// ROS subscriber
  ros::Subscriber ros_cmd_vel_subscriber_;

  /// Callback on new unstamped command from ROS
  void rosCmdVelCallbackUnstamped(geometry_msgs::TwistConstPtr msg)
  {
    geometry_msgs::TwistStampedPtr msg_stamped = boost::make_shared<geometry_msgs::TwistStamped>();
    msg_stamped->twist = *msg;
    msg_stamped->header.stamp = ros::Time::now();
    rosCmdVelCallbackStamped(msg_stamped);
  }

  /// Callback on new stamped command from ROS (TODO(TH): handle timeout)
  void rosCmdVelCallbackStamped(geometry_msgs::TwistStampedConstPtr msg)
  {
    // Check validity of command
    geometry_msgs::TwistStamped msg_valid;
    msg_valid.header = msg->header;
    msg_valid.twist = msg->twist;
    if (!std::isfinite(msg->twist.angular.x) ||
        !std::isfinite(msg->twist.angular.y) ||
        !std::isfinite(msg->twist.angular.z) ||
        !std::isfinite(msg->twist.linear.x) ||
        !std::isfinite(msg->twist.linear.y) ||
        !std::isfinite(msg->twist.linear.z))
    {
      ROS_ERROR("TitanPlugin::rosCmdVelCallbackStamped msg contains non-finite values");
      msg_valid.twist.angular.x = std::isfinite(msg->twist.angular.x) ? msg->twist.angular.x : 0;
      msg_valid.twist.angular.y = std::isfinite(msg->twist.angular.y) ? msg->twist.angular.y : 0;
      msg_valid.twist.angular.z = std::isfinite(msg->twist.angular.z) ? msg->twist.angular.z : 0;
      msg_valid.twist.linear.x = std::isfinite(msg->twist.linear.x) ? msg->twist.linear.x : 0;
      msg_valid.twist.linear.y = std::isfinite(msg->twist.linear.y) ? msg->twist.linear.y : 0;
      msg_valid.twist.linear.z = std::isfinite(msg->twist.linear.z) ? msg->twist.linear.z : 0;
    }

    gazebo::msgs::Twist twist;

    twist.mutable_linear()->set_x(msg_valid.twist.linear.x);
    twist.mutable_linear()->set_y(msg_valid.twist.linear.y);
    twist.mutable_linear()->set_z(msg_valid.twist.linear.z);

    twist.mutable_angular()->set_x(msg_valid.twist.angular.x);
    twist.mutable_angular()->set_y(msg_valid.twist.angular.y);
    twist.mutable_angular()->set_z(-msg_valid.twist.angular.z); //gazebo has opposite direction for pos yaw (NED)

    gazebo_cmd_vel_publisher_->Publish(twist);
  }
};

GZ_REGISTER_MODEL_PLUGIN(TitanPlugin)

}  // namespace gazebo
