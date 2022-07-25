cmake_minimum_required(VERSION 2.8.3)
project(titan_gazebo)

find_package(catkin REQUIRED COMPONENTS
  gazebo_dev
  gazebo_ros
  geometry_msgs
  roscpp
)

###################################
## catkin specific configuration ##
###################################

catkin_package()

###########
## Build ##
###########

include_directories(
  ${catkin_INCLUDE_DIRS}
)

# ROS Gazebo Dynamic track suspension interface
add_library(
  ${PROJECT_NAME}_suspension_ros
  src/titan_gazebo_suspension_ros.cpp
)
target_link_libraries(
  ${PROJECT_NAME}_suspension_ros
  ${catkin_LIBRARIES}
)

# ROS Gazebo Dynamic track velocity interface
add_library(
  dynamic_${PROJECT_NAME}_ros
  src/dynamic_titan_gazebo_ros.cpp
)
target_link_libraries(
  dynamic_${PROJECT_NAME}_ros
  ${catkin_LIBRARIES}
)

# ROS Gazebo SimpleTrackedVehiclePlugin interface
add_library(
  ${PROJECT_NAME}_ros
  src/titan_gazebo_ros.cpp
)
target_link_libraries(
  ${PROJECT_NAME}_ros
  ${catkin_LIBRARIES}
)

# Fork of TrackedVehiclePlugin and SimpleTrackedVehiclePlugin
add_library(
  ${PROJECT_NAME}_tracks
  src/titan_gazebo_tracks/SimpleTrackedVehiclePlugin.cc
  src/titan_gazebo_tracks/SimpleTrackedVehiclePlugin.hh
  src/titan_gazebo_tracks/TrackedVehiclePlugin.cc
  src/titan_gazebo_tracks/TrackedVehiclePlugin.hh
)
target_link_libraries(
  ${PROJECT_NAME}_tracks
  ${catkin_LIBRARIES}
)

#############
## Install ##
#############

install(TARGETS
  ${PROJECT_NAME}_suspension_ros
  dynamic_${PROJECT_NAME}_ros
  ${PROJECT_NAME}_ros
  ${PROJECT_NAME}_tracks
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)

install(DIRECTORY
  config
  launch
  models
  worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
