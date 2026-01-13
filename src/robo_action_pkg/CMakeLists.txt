cmake_minimum_required(VERSION 3.8)
project(robo_action_pkg)

find_package(ament_cmake REQUIRED)
find_package(ament_python REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(action_msgs REQUIRED)

# Install Python package properly (THIS WAS MISSING)
ament_python_install_package(${PROJECT_NAME})

# Generate action interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/MoveRobot.action"
  DEPENDENCIES action_msgs
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()
