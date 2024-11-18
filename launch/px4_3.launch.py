#!/usr/bin/env python3
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():
    """Launch Gazebo with two freeflyers running PX4 communicating over ROS 2."""
    ld = LaunchDescription()

    # run the px4_1.launch.py script twice
    lf_1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('discower_launch'), '/launch/px4_1.launch.py']),

        launch_arguments={'id': '0', 'pose': '0,0,0', 'name': 'snap', 'delay': '0'}.items()
    )

    lf_2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('discower_launch'), '/launch/px4_1.launch.py']),

        launch_arguments={'id': '1', 'pose': '0,1,0', 'name': 'crackle', 'delay': '5'}.items()
    )

    lf_3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('discower_launch'), '/launch/px4_1.launch.py']),

        launch_arguments={'id': '2', 'pose': '0,-1,0', 'name': 'pop', 'delay': '5'}.items()
    )
    ld.add_action(lf_1)
    ld.add_action(lf_2)
    ld.add_action(lf_3)
    return ld


