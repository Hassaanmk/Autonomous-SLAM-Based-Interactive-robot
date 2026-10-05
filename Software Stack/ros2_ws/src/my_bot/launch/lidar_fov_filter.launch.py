# from launch import LaunchDescription
# from launch_ros.actions import Node

# def generate_launch_description():
#     return LaunchDescription([
#         Node(
#             package='lidar_fov_filter_pkg',
#             executable='lidar_fov_filter',
#             name='lidar_fov_filter',
#             parameters=[
#                 {'min_angle_deg': -90.0},
#                 {'max_angle_deg': 90.0},
#                 {'input_topic': '/scan'},
#                 {'output_topic': '/filtered_scan'}
#             ],
#             output='screen'
#         )
#     ])
#     main()
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='lidar_filter',
            executable='filter_node',
            name='lidar_fov_filter',
            parameters=[
                {'min_angle_deg': -90.0},
                {'max_angle_deg': 90.0},
                {'input_topic': '/scan'},
                {'output_topic': '/filtered_scan'}
            ],
            output='screen'
        )
    ])
