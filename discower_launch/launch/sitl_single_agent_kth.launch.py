#!/usr/bin/env python
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    """Launch Gazebo with a spacecraft in the kthspacelab world and ROS bridge."""
    px4_launch_path = [get_package_share_directory('discower_launch'), '/px4.launch.py']

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(px4_launch_path),
            launch_arguments={
                'id': '0',
                'pose': '2,0,0',
                'name': 'snap',
                'delay': '0',
                'world': 'kthspacelab',
                'use_odom_bridge': 'true',
            }.items()
        )
    ])