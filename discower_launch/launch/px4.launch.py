#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, ExecuteProcess
from launch.substitutions import LaunchConfiguration
import os

# usage:
# ld.add_action(IncludeLaunchDescription(
#     PythonLaunchDescriptionSource(
#         [get_package_share_directory('discower_launch'), '/px4.launch.py']),
#     launch_arguments={'id':'0', 'pose':'1,0,0', 'name':'snap', 'delay':'0', 'model':'uuv'}.items()
# ))

def launch_px4(context, *args, **kwargs):
    px4_dir = os.getenv("PX4_SPACE_SYSTEMS_DIR")
    if not px4_dir:
        raise RuntimeError("PX4_SPACE_SYSTEMS_DIR is not set. Did you add it to your .bashrc file?")

    id_ = LaunchConfiguration("id").perform(context)        # Unique identifier for the PX4 instance (string, e.g. '0')
    pose = LaunchConfiguration("pose").perform(context)     # Initial pose of the PX4 instance (string, e.g. "0,0,0")
    name = LaunchConfiguration("name").perform(context)     # Name/namespace of the PX4 instance (string, e.g. "snap")
    delay = LaunchConfiguration("delay").perform(context)   # Delay before starting the PX4 instance (string, e.g. "0")
    model = LaunchConfiguration("model").perform(context)   # Model to use for the PX4 instance (string, e.g. "atmos" or "bluerov")
    world = LaunchConfiguration("world").perform(context)
    model_name = f"{model}_{id_}"

    target = 'px4_sitl_spacecraft'
    if model:
        target = 'px4_sitl_uuv' if model == "bluerov" else target
    gz_model = 'gz_atmos'
    if model:
        gz_model = 'gz_uuv_bluerov2_heavy' if model == "bluerov" else gz_model

    use_odom_bridge = LaunchConfiguration("use_odom_bridge").perform(context).lower() == "true"

    processes = [
        ExecuteProcess(
            cmd=[
                "bash", "-c",
                # f"sleep {delay} && {px4_dir}/build/px4_sitl_{target}/bin/px4 -i {id_}"
                f"sleep {delay} && {px4_dir}/build/{target}/bin/px4 -i {id_}",
            ],
            cwd=px4_dir,
            env={
                **os.environ,
                "PX4_SIM_AUTOSTART": "71002",
                "PX4_SIM_SPEED_FACTOR": "1",
                "PX4_GZ_MODEL_POSE": pose,
                "PX4_INSTANCE": id_,
                "PX4_DELAY": delay,
                "PX4_SIM_MODEL": f"{gz_model}",
                "PX4_UXRCE_DDS_NS": name,
                "PX4_GZ_WORLD": world
            },
            output="screen"
        )
    ]

    if use_odom_bridge:
        processes.append(
            ExecuteProcess(
                cmd=[
                    "ros2", "run", "ros_gz_bridge", "parameter_bridge",
                    f"/model/{model_name}/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                    "--ros-args", "-r", f"/model/{model_name}/odometry:=/{name}/odom"
                ],
                output="screen"
            )
        )

    return processes

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("id", default_value="0"),
        DeclareLaunchArgument("pose", default_value="0,0,0"),
        DeclareLaunchArgument("name", default_value="snap"),
        DeclareLaunchArgument("delay", default_value="0"),
        DeclareLaunchArgument("world", default_value=""),
        DeclareLaunchArgument("use_odom_bridge", default_value="false"),

        OpaqueFunction(function=launch_px4)
    ])