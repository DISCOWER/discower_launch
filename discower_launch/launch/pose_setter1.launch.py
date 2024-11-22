from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    return LaunchDescription([
        # ros2 topic pub /start std_msgs/Bool "data: true"


        # Snap
        Node(
            package='discower_launch',
            namespace='snap',
            executable='pose_setter',
            name='pose_setter_0',
            output='screen',
            emulate_tty=True,
            parameters=[{'time_array': '[0, 5, 10, 15]'},{'pose_array': '[[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]]'}],
        ),
        Node(
            package='rviz2',
            namespace='snap',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', [os.path.join(get_package_share_directory('px4_mpc'), 'config.rviz')]]
        ),
        Node(
            package='px4_mpc',
            namespace='snap',
            executable='mpc_spacecraft',
            name='mpc_spacecraft_0',
            output='screen',
            emulate_tty=True,
            parameters=[{'mode': 'rate'}], # rate/wrench/direct_allocation
        ),
        Node(
            package='px4_offboard',
            namespace='snap',
            executable='visualizer',
            name='visualizer_0',
        ),
    ])