cmake_minimum_required(VERSION 3.5)
project(qt_gui_ros2)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rviz_common REQUIRED)
find_package(rviz_default_plugins REQUIRED)
find_package(rviz_ogre_vendor REQUIRED)
find_package(rviz_rendering REQUIRED)
find_package(Qt5 REQUIRED COMPONENTS Widgets Core)
find_package(nav_msgs REQUIRED)

set(THIS_PACKAGE_INCLUDE_DEPENDS
  rclcpp
  rclcpp_components
  rviz_common
  rviz_default_plugins
  rviz_ogre_vendor
  rviz_rendering
  nav_msgs
)

include_directories(
  include
  ${rclcpp_INCLUDE_DIRS}
  ${rviz_common_INCLUDE_DIRS}
  ${Qt5Core_INCLUDE_DIRS}
  ${Qt5Widgets_INCLUDE_DIRS}
)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(headers_to_moc
  include/qt_gui_ros2/mainWindow.hpp
)

foreach(header "${headers_to_moc}")
  qt5_wrap_cpp(moc_files "${header}")
endforeach()

# Add the executable and link the libraries
add_executable(main
  src/main.cpp
  src/mainWindow.cpp
  ${moc_files}
)

ament_target_dependencies(main ${THIS_PACKAGE_INCLUDE_DEPENDS})

target_link_libraries(main
  Qt5::Widgets
  Qt5::Core
  ${rclcpp_LIBRARIES}
  ${rviz_common_LIBRARIES}
  ${rviz_rendering_LIBRARIES}
)

install(TARGETS main
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

