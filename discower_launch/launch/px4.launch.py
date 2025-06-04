#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, ExecuteProcess
from launch.substitutions import LaunchConfiguration
import os

def launch_px4_with_bridge(context, *args, **kwargs):
    px4_dir = os.getenv("PX4_SPACE_SYSTEMS_DIR")
    if not px4_dir:
        raise RuntimeError("PX4_SPACE_SYSTEMS_DIR is not set. Did you add it to your .bashrc file?")

    id_ = LaunchConfiguration("id").perform(context)
    pose = LaunchConfiguration("pose").perform(context)
    name = LaunchConfiguration("name").perform(context)
    delay = LaunchConfiguration("delay").perform(context)
    world = LaunchConfiguration("world").perform(context)

    model_name = f"spacecraft_2d_{id_}"

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
                "PX4_SIM_SPEED_FACTOR": "1",
                "PX4_GZ_MODEL_POSE": pose,
                "PX4_INSTANCE": id_,
                "PX4_DELAY": delay,
                "PX4_SIM_MODEL": "gz_spacecraft_2d",
                "PX4_UXRCE_DDS_NS": name,
                "PX4_GZ_WORLD": world
            },
            output="screen"
        ),

        ExecuteProcess(
            cmd=[
                "ros2", "run", "ros_gz_bridge", "parameter_bridge",
                f"/model/{model_name}/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry",
                "--ros-args", "-r", f"/model/{model_name}/odometry:=/{name}/odom"
            ],
            output="screen"
        )
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("id", default_value="0"),
        DeclareLaunchArgument("pose", default_value="0,0,0"),
        DeclareLaunchArgument("name", default_value="snap"),
        DeclareLaunchArgument("delay", default_value="0"),
        DeclareLaunchArgument("world", default_value=""),

        OpaqueFunction(function=launch_px4_with_bridge)
    ])