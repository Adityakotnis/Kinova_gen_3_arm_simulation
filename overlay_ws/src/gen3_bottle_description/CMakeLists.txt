cmake_minimum_required(VERSION 3.5)
project(gen3_bottle_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    urdf
    launch
  DESTINATION share/${PROJECT_NAME}
)

# Install robots directory (needed for kortex_bringup compatibility)
install(
  DIRECTORY
    robots
  DESTINATION share/${PROJECT_NAME}
  OPTIONAL
)

# Install arms directory (needed for controllers - copy controllers from kortex_description first)
install(
  DIRECTORY
    arms
  DESTINATION share/${PROJECT_NAME}
  OPTIONAL
)

ament_package()
