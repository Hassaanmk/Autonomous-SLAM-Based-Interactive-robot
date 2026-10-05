# qt_gui_ros2

This package helps you integrate RViz into a Qt GUI application.

## Credit

This package was written by **saikrishna** ([@bandasaikrishna](https://github.com/bandasaikrishna)).
Original repository: https://github.com/bandasaikrishna/qt_gui_ros2 (copied from commit `0368860`).

All credit for the original code goes to the author. The upstream repository does not declare a licence; contact the author before reusing this code outside this project.

## Changes made for this project

Only `CMakeLists.txt` was changed, to build on ROS 2 Humble:

- The executable is named `main` instead of `qt_gui_ros2`.
- It links rclcpp, rviz_common and rviz_rendering through their `${..._LIBRARIES}` variables instead of the imported targets.

The source files (`src/`, `include/`) and `package.xml` are unchanged.

## Run

```sh
ros2 run qt_gui_ros2 main
```
