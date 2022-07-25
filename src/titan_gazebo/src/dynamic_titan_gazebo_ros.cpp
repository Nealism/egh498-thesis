#include <gazebo/common/Plugin.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/transport/TransportTypes.hh>
#include <gazebo/transport/transport.hh>

#include <ignition/math/Quaternion.hh>

#include <geometry_msgs/Twist.h>
#include <geometry_msgs/TwistStamped.h>
#include <sensor_msgs/JointState.h>
#include <std_msgs/Float64.h>

#include <ros/ros.h>

#include <algorithm>
#include <unordered_map>

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

    LoadParam(_sdf, "max_track_velocity", max_track_velocity_, 1.0d);
    LoadParam(_sdf, "track_acceleration", track_acceleration_, 1.0d);
    LoadParam(_sdf, "track_separation", track_separation_, 1.0d);
    LoadParam(_sdf, "steering_efficiency", steering_efficiency_, 1.0d);

    LoadParam(_sdf, "sim_rate", sim_rate_, 500.0d);

    LoadParam(_sdf, "wheel_radius", wheel_radius_, 0.05d);
  }

  /// Set up the subscribers and publishers
  void Init()
  {
    // Set up ROS subscriber
    if (!ros::isInitialized())
    {
      ROS_ERROR_STREAM("TitanPlugin::Init(): ROS not initialised");
    }

    if (is_ros_cmd_vel_stamped_)
    {
      ros_cmd_vel_subscriber_ = nh_.subscribe<const geometry_msgs::TwistStamped::ConstPtr &>(
        ros_cmd_vel_topic_, 1, &TitanPlugin::rosCmdVelCallbackStamped, this);
    }
    else
    {
      ros_cmd_vel_subscriber_ = nh_.subscribe<const geometry_msgs::Twist::ConstPtr &>(
        ros_cmd_vel_topic_, 1, &TitanPlugin::rosCmdVelCallbackUnstamped, this);
    }

    joint_state_sub_ = nh_.subscribe<const sensor_msgs::JointState::ConstPtr &>(
      robot_namespace_ + "/joint_states", 1, &TitanPlugin::rosJointStateCallback, this);

    left_track_vel_actual_pub_ = nh_.advertise<std_msgs::Float64>(robot_namespace_ + "/left_track/actual", 1);
    left_track_vel_desired_pub_ = nh_.advertise<std_msgs::Float64>(robot_namespace_ + "/left_track/desired", 1);
    right_track_vel_actual_pub_ = nh_.advertise<std_msgs::Float64>(robot_namespace_ + "/right_track/actual", 1);
    right_track_vel_desired_pub_ = nh_.advertise<std_msgs::Float64>(robot_namespace_ + "/right_track/desired", 1);
  }

private:
  /// ROS node_handle in public namespace
  ros::NodeHandle nh_;

  /// Namespace for Gazebo
  std::string robot_namespace_;

  /// Topic for ROS
  std::string ros_cmd_vel_topic_;

  /// Is the velocity command from ROS timestamped?
  bool is_ros_cmd_vel_stamped_;

  /// ros pub and sub for joint control
  ros::Subscriber joint_state_sub_;
  ros::Publisher left_track_vel_actual_pub_;
  ros::Publisher left_track_vel_desired_pub_;
  ros::Publisher right_track_vel_actual_pub_;
  ros::Publisher right_track_vel_desired_pub_;

  /// Joint pub map for gazebo control
  std::unordered_map<std::string, ros::Publisher> joint_pub_map_;

  double sim_rate_ = 1000;

  /// Track drive parameters
  double max_track_velocity_ = 0.0;
  double track_acceleration_ = 0.0;
  double track_separation_ = 0.0;
  double steering_efficiency_ = 0.0;

  /// Wheel drive parameters
  double wheel_radius_ = 0.0;

  /// If the most recent command is more than this many seconds old, stop moving
  double timeout_;

  /// Gazebo publisher
  gazebo::transport::PublisherPtr gazebo_cmd_vel_publisher_;

  /// ROS subscriber
  ros::Subscriber ros_cmd_vel_subscriber_;

  /// Velocity terms from callback
  double linear_vel_ = 0.0;
  double angular_vel_ = 0.0;

  double track_left_desired_ = 0.0;
  double track_right_desired_ = 0.0;

  double track_left_commanded_ = 0.0;
  double track_right_commanded_ = 0.0;

  /// Callback on new stamped command from ROS (TODO(TH): handle timeout)
  void rosCmdVelCallbackStamped(const geometry_msgs::TwistStamped::ConstPtr &msg)
  {
    // Check validity of command
    geometry_msgs::TwistStamped msg_valid;
    msg_valid.header = msg->header;
    msg_valid.twist = msg->twist;
    if (!std::isfinite(msg->twist.angular.x) || !std::isfinite(msg->twist.angular.y) ||
        !std::isfinite(msg->twist.angular.z) || !std::isfinite(msg->twist.linear.x) ||
        !std::isfinite(msg->twist.linear.y) || !std::isfinite(msg->twist.linear.z))
    {
      ROS_ERROR("TitanPlugin::rosCmdVelCallbackStamped msg contains non-finite values");
    }
    else
    {
      linear_vel_ = msg->twist.linear.x;
      angular_vel_ = msg->twist.angular.z;
    }

    // Compute track velocities using the tracked vehicle kinematics model.
    track_left_desired_ = linear_vel_ - (angular_vel_ * (track_separation_ / 2.0)) / steering_efficiency_;

    track_right_desired_ = linear_vel_ + (angular_vel_ * (track_separation_ / 2.0)) / steering_efficiency_;

    // Velocity scaling
    // If right track vel magnitude greater, and above limit, scale down
    if ((std::abs(track_right_desired_) >= std::abs(track_left_desired_)) &&
        (std::abs(track_right_desired_) > max_track_velocity_))
    {
      auto scale_factor = std::abs(max_track_velocity_ / track_right_desired_);
      track_right_desired_ = track_right_desired_ * scale_factor;
      track_left_desired_ = track_left_desired_ * scale_factor;
    }
    // Else if left track vel magnitude greater, and above limit, scale down
    else if ((std::abs(track_left_desired_) >= std::abs(track_right_desired_)) &&
             (std::abs(track_left_desired_) > max_track_velocity_))
    {
      auto scale_factor = std::abs(max_track_velocity_ / track_left_desired_);
      track_right_desired_ = track_right_desired_ * scale_factor;
      track_left_desired_ = track_left_desired_ * scale_factor;
    }
    // final clamp check to catch errors
    track_left_desired_ = std::max(-max_track_velocity_, std::min(track_left_desired_, max_track_velocity_));
    track_right_desired_ = std::max(-max_track_velocity_, std::min(track_right_desired_, max_track_velocity_));
  }

  /// Callback on new unstamped command from ROS
  void rosCmdVelCallbackUnstamped(const geometry_msgs::Twist::ConstPtr &msg)
  {
    const geometry_msgs::TwistStamped::Ptr msg_stamped = boost::make_shared<geometry_msgs::TwistStamped>();
    msg_stamped->twist = *msg;
    msg_stamped->header.stamp = ros::Time::now();
    rosCmdVelCallbackStamped(msg_stamped);
  }

  /// Callback on new joint states command from ROS
  void rosJointStateCallback(const sensor_msgs::JointState::ConstPtr &msg)
  {
    // We require name and velocity.
    // sensor_msgs::JointState fields are optional, so make sure that name and
    // velocity have been provided.
    // Might as well check they are the same length too.
    if (msg->name.empty() || msg->velocity.empty() || (msg->name.size() != msg->velocity.size()))
    {
      return;
    }

    // The max magnitude of velocity change to apply this loop
    const double accel_this_loop = track_acceleration_ / sim_rate_;

    // Handle track accelleration
    // If desired can be reached this loop, just do it
    // Otherwise, step toward it

    if (std::abs(track_left_desired_ - track_left_commanded_) <= accel_this_loop)
    {
      track_left_commanded_ = track_left_desired_;
    }
    else if (track_left_commanded_ > track_left_desired_)
    {
      track_left_commanded_ = track_left_commanded_ - accel_this_loop;
    }
    else if (track_left_commanded_ < track_left_desired_)
    {
      track_left_commanded_ = track_left_commanded_ + accel_this_loop;
    }

    if (std::abs(track_right_desired_ - track_right_commanded_) <= accel_this_loop)
    {
      track_right_commanded_ = track_right_desired_;
    }
    else if (track_right_commanded_ > track_right_desired_)
    {
      track_right_commanded_ = track_right_commanded_ - accel_this_loop;
    }
    else if (track_right_commanded_ < track_right_desired_)
    {
      track_right_commanded_ = track_right_commanded_ + accel_this_loop;
    }

    // Publish internal state for debug
    std_msgs::Float64 float64_msg;
    float64_msg.data = track_left_commanded_;
    left_track_vel_desired_pub_.publish(float64_msg);
    float64_msg.data = track_right_commanded_;
    right_track_vel_desired_pub_.publish(float64_msg);

    // Compute wheel joint commands
    const double left_wheels_joint_command = track_left_commanded_ / wheel_radius_;
    const double right_wheels_joint_command = track_right_commanded_ / wheel_radius_;

    // Publish joint commands
    double left_wheels_velocity_sum = 0.0;
    size_t left_wheels_count = 0;
    double right_wheels_velocity_sum = 0.0;
    size_t right_wheels_count = 0;

    for (size_t joint_index = 0; joint_index < msg->name.size(); ++joint_index)
    {
      const std::string &joint_name = msg->name[joint_index];
      const double joint_velocity = msg->velocity[joint_index];

      const bool is_wheel = (joint_name.find("wheel") != std::string::npos);
      const bool is_left_wheel = is_wheel && (joint_name.find("left") != std::string::npos);
      const bool is_right_wheel = is_wheel && (joint_name.find("right") != std::string::npos);

      if (is_left_wheel)
      {
        left_wheels_velocity_sum += joint_velocity;
        ++left_wheels_count;
      }

      if (is_right_wheel)
      {
        right_wheels_velocity_sum += joint_velocity;
        ++right_wheels_count;
      }

      if (is_left_wheel || is_right_wheel)
      {
        // Create command publisher if haven't already
        if (joint_pub_map_.find(joint_name) == joint_pub_map_.end())
        {
          joint_pub_map_[joint_name] =
            nh_.advertise<std_msgs::Float64>(robot_namespace_ + "/" + joint_name + "/command", 1);
        }

        // Select command
        if (is_left_wheel)
        {
          float64_msg.data = left_wheels_joint_command;
        }
        if (is_right_wheel)
        {
          float64_msg.data = right_wheels_joint_command;
        }

        // Publish command
        joint_pub_map_[joint_name].publish(float64_msg);
      }
    }

    const double left_wheels_velocity_average =
      (left_wheels_count == 0) ? 0.0 :
                                 ((left_wheels_velocity_sum * wheel_radius_) / static_cast<double>(left_wheels_count));
    float64_msg.data = left_wheels_velocity_average;
    left_track_vel_actual_pub_.publish(float64_msg);

    const double right_wheels_velocity_average =
      (right_wheels_count == 0) ?
        0.0 :
        ((right_wheels_velocity_sum * wheel_radius_) / static_cast<double>(right_wheels_count));
    float64_msg.data = right_wheels_velocity_average;
    right_track_vel_actual_pub_.publish(float64_msg);
  }
};

GZ_REGISTER_MODEL_PLUGIN(TitanPlugin)

}  // namespace gazebo
