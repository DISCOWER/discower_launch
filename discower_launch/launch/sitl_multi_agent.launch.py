#!/usr/bin/env python
__author__ = "Joris Verhagen"
__contact__ = "jorisv@kth.se"

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    """Launch Gazebo with two freeflyers running PX4 communicating over ROS 2."""
    ld = LaunchDescription()

    # Run the Gazebo simulator and the PX4 SITL simulation. We add a delay
    # to the additional robots to ensure they spawn in the same gazebo instance
    # run the px4_1.launch.py script three times
    lf_1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('discower_launch'), '/px4.launch.py']),

        launch_arguments={'id': '0', 'pose': '1,0,0.2', 'name': 'snap', 'delay': '0'}.items()
    )
    lf_2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('discower_launch'), '/px4.launch.py']),

        launch_arguments={'id': '1', 'pose': '2,0,0.2', 'name': 'crackle', 'delay': '5'}.items()
    )
    lf_3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('discower_launch'), '/px4.launch.py']),

        launch_arguments={'id': '2', 'pose': '3,0,0.2', 'name': 'pop', 'delay': '5'}.items()
    )
    ld.add_action(lf_1)
    ld.add_action(lf_2)
    ld.add_action(lf_3)

    return ld


