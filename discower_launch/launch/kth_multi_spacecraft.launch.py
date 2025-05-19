#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    launch_dir = get_package_share_directory('discower_launch')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'kth_single_spacecraft.launch.py')),
            launch_arguments={
                'id': '0',
                'pose': '1,0,0.2',
                'name': 'snap',
                'delay': '0'
            }.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'kth_single_spacecraft.launch.py')),
            launch_arguments={
                'id': '1',
                'pose': '2,0,0.2',
                'name': 'crackle',
                'delay': '5'
            }.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'kth_single_spacecraft.launch.py')),
            launch_arguments={
                'id': '2',
                'pose': '3,0,0.2',
                'name': 'pop',
                'delay': '5'
            }.items()
        ),
    ])
