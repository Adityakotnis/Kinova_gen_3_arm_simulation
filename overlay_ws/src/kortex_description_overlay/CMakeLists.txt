cmake_minimum_required(VERSION 3.5)
project(kortex_description_overlay)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY robots/
  DESTINATION share/${PROJECT_NAME}/robots
)

ament_package()
