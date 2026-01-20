from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        Node(
            package='sensor_pipeline',
            executable='udp_bridge',
            name='udp_bridge',
            output='screen'
        ),

        Node(
            package='sensor_pipeline',
            executable='sensor_parser',
            name='sensor_parser',
            output='screen'
        ),

        Node(
            package='sensor_pipeline',
            executable='state_estimator',
            name='state_estimator',
            output='screen'
        ),

        Node(
            package='sensor_pipeline',
            executable='robot_controller',
            name='robot_controller',
            output='screen'
        ),
    ])
