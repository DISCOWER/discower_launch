#!/usr/bin/env python
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    """Launch multiple spacecrafts in the kth_space_lab world with PX4 and ROS 2."""
    ld = LaunchDescription()

    # Path to the shared px4 launcher
    px4_launch_path = [get_package_share_directory('discower_launch'), '/px4.launch.py']

    # First agent
    spacecraft_0 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(px4_launch_path),
        launch_arguments={
            'id': '0',
            'pose': '1,0,0.2',
            'name': 'snap',
            'delay': '0',
            'world': 'kth_space_lab'
        }.items()
    )

    # Second agent
    spacecraft_1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(px4_launch_path),
        launch_arguments={
            'id': '1',
            'pose': '2,0,0.2',
            'name': 'crackle',
            'delay': '5',
            'world': 'kth_space_lab'
        }.items()
    )

    # Third agent
    spacecraft_2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(px4_launch_path),
        launch_arguments={
            'id': '2',
            'pose': '3,0,0.2',
            'name': 'pop',
            'delay': '5',
            'world': 'kth_space_lab'
        }.items()
    )

    # Add all to launch description
    ld.add_action(spacecraft_0)
    ld.add_action(spacecraft_1)
    ld.add_action(spacecraft_2)

    return ld