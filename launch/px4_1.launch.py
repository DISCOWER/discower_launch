#!/usr/bin/env python3
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os
# from utilities.utilities import *


def generate_launch_description():
    """Launch Gazebo with a freeflyer running PX4 communicating over ROS 2."""

    px4_dir = os.getenv("PX4_SPACE_SYSTEMS_DIR")
    if not px4_dir:
        raise RunTimeError("PX4_SPACE_SYSTEMS_DIR is not set. Did you add it to your .bashrc file?")

    id_to_name = {"0": "snap",
                  "1": "crackle",
                  "2": "pop"}

    return LaunchDescription(
        [
            # We have the first robot always start with id 0
            DeclareLaunchArgument("id", default_value="0"),
            DeclareLaunchArgument("pose", default_value="0,0,0"),
            ExecuteProcess(
                cmd=[
                    "xterm",        # or "gnome-terminal", "konsole", "xterm"
                    "-hold",      # Keep terminal open for debugging
                    "-e",
                    px4_dir + "/build/px4_sitl_default/bin/px4",
                    "-i",
                    LaunchConfiguration("id"),
                    "",

                ],
                cwd=px4_dir,
                env={**os.environ,
                    "PX4_SIM_AUTOSTART": "4001",
                    "PX4_SIM_SPEED_FACTOR": "1",
                    "PX4_GZ_MODEL_POSE": LaunchConfiguration("pose"),
                    "PX4_SIM_MODEL": "gz_spacecraft_2d"},
                output="screen",
            ),
        ]
    )
