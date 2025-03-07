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
    # to the second robot to ensure they spawn in the same gazebo instance
    # run the px4_1.launch.py script twice
    lf_1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('push_stl'), '/px4.launch.py']),

        launch_arguments={'id': '0', 'pose': '-0.5,-0.75,0', 'name': 'crackle', 'delay': '0'}.items()
    )
    lf_2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('push_stl'), '/px4.launch.py']),

        launch_arguments={'id': '1', 'pose': '-0.5,0.75,0', 'name': 'snap', 'delay': '5'}.items()
    )
    ld.add_action(lf_1)
    ld.add_action(lf_2)

    return ld


