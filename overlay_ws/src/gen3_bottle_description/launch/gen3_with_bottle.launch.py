from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    return LaunchDescription([

        DeclareLaunchArgument(
            'robot_ip',
            default_value='127.0.0.1'
        ),

        DeclareLaunchArgument(
            'use_fake_hardware',
            default_value='true'
        ),

        DeclareLaunchArgument(
            'launch_rviz',
            default_value='true'
        ),

        DeclareLaunchArgument(
            'description_package',
            default_value='gen3_bottle_description'
        ),

        DeclareLaunchArgument(
            'description_file',
            default_value='gen3_with_bottle.xacro'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('kortex_bringup'),
                    'launch',
                    'kortex_control.launch.py'
                ])
            ),
            launch_arguments={
                'robot_type': 'gen3',
                'robot_ip': LaunchConfiguration('robot_ip'),
                'dof': '7',
                'username': 'admin',
                'password': 'admin',
                'port': '10000',
                'port_realtime': '10001',
                'session_inactivity_timeout_ms': '60000',
                'connection_inactivity_timeout_ms': '2000',
                'use_fake_hardware': LaunchConfiguration('use_fake_hardware'),
                'fake_sensor_commands': 'false',
                'robot_controller': 'joint_trajectory_controller',
                'gripper': 'robotiq_2f_85',
                'gripper_joint_name': 'robotiq_85_left_knuckle_joint',
                'use_internal_bus_gripper_comm': 'false',
                'gripper_max_velocity': '100.0',
                'gripper_max_force': '100.0',
                'launch_rviz': LaunchConfiguration('launch_rviz'),
                'controllers_file': 'ros2_controllers.yaml',
                'description_package': LaunchConfiguration('description_package'),
                'description_file': LaunchConfiguration('description_file'),
                'robot_name': 'gen3',
                'prefix': '""',
            }.items()
        )
    ])
