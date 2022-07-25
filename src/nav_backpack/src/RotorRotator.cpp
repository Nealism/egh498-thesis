// Copyright (c) 2020
// Commonwealth Scientific and Industrial Research Organisation (CSIRO)
// ABN 41 687 119 230
//
// Author: Thomas Hines, thomas.hines@data61.csiro.au

#include <std_msgs/Float64.h>

#include <ros/ros.h>

namespace rotor_rotator
{
class RotorRotator
{
public:
  /// Reads params then sets up publisher and timer
  RotorRotator()
  {
    std::string topic;
    double period_in_ms;
    if (!node_private_.getParam("frequency", frequency_) || !node_private_.getParam("topic", topic) ||
        !node_private_.getParam("period_in_ms", period_in_ms))
    {
      ROS_FATAL("frequency, topic and period_in_ms params are required");
      return;
    }

    publisher_ = node_.advertise<std_msgs::Float64>(topic, 1, true);
    timer_ = node_private_.createTimer(ros::Duration(period_in_ms / 1000.0), &RotorRotator::onTimer, this);
  }

private:
  /// ROS NodeHandle in public namespace
  ros::NodeHandle node_;

  /// ROS NodeHandle in private namespace
  ros::NodeHandle node_private_{ "~" };

  /// Rotation frequency
  double frequency_;

  /// ROS timer to publish in
  ros::Timer timer_;

  /// Rotation speed message to publish
  std_msgs::Float64 msg_;

  /// ROS publisher to publish with
  ros::Publisher publisher_;

  /// ROS timer callback
  void onTimer(const ros::TimerEvent & /* timer_event */)
  {
    msg_.data = 2.0 * M_PI * frequency_;
    publisher_.publish(msg_);
  }
};
}  // namespace rotor_rotator

int main(int argc, char **argv)
{
  ros::init(argc, argv, "rotor_rotator");
  rotor_rotator::RotorRotator rotor_rotator;
  ros::spin();
  return 0;
}
