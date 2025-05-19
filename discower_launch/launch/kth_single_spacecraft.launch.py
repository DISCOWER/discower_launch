#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess
import os

def launch_px4(context, *args, **kwargs):
    px4_dir = os.getenv("PX4_SPACE_SYSTEMS_DIR")
    if not px4_dir:
        raise RuntimeError("PX4_SPACE_SYSTEMS_DIR is not set.")

    id_ = LaunchConfiguration("id").perform(context)
    pose = LaunchConfiguration("pose").perform(context)
    name = LaunchConfiguration("name").perform(context)
    delay = LaunchConfiguration("delay").perform(context)

    return [
        ExecuteProcess(
            cmd=[
                "bash", "-c",
                f"sleep {delay} && {px4_dir}/build/px4_sitl_default/bin/px4 -i {id_}"
            ],
            cwd=px4_dir,
            env={
                **os.environ,
                "PX4_SIM_AUTOSTART": "71002",
                "PX4_SIM_MODEL": "gz_spacecraft_2d",
                "PX4_SIM_SPEED_FACTOR": "1",
                "PX4_GZ_MODEL_POSE": pose,
                "PX4_UXRCE_DDS_NS": name,
                "PX4_GZ_WORLD": "kth_space_lab"
            },
            output="screen"
        )
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("id", default_value="0"),
        DeclareLaunchArgument("pose", default_value="2,0,0"),
        DeclareLaunchArgument("name", default_value="snap"),
        DeclareLaunchArgument("delay", default_value="0"),

        OpaqueFunction(function=launch_px4)
    ])
