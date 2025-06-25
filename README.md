# discower_launch: SITL launch files for Single and Multi-agent experiments

This repository contains launch files for running Single and Multi-agent ATMOS platform SITL simulations.

## Dependencies

- [PX4-Space-Systems](https://github.com/DISCOWER/PX4-Space-Systems)
- [px4_msgs](https://github.com/DISCOWER/px4_msgs)

As this repository contains simple examples to merely run the SITL, you might need to follow additional instructions in the `PX4-Space-Systems` repository to fully get started. In short, you additionally need to

- build the workspace: `colcon build --symlink-install`
- start the microros service: `micro-xrce-dds-agent udp4 -p 8888`

After that, you can display the robot's topics with `ros2 topic list`. Then, you can arm/disarm the robot with [QGroundControl](https://github.com/DISCOWER/qgroundcontrol). 

Further details can be found on the [ATMOS website](https://atmos.discower.io/pages/Simulation/)

## Launch files overview

This package provides four main launch files:

- `sitl_single_agent.launch.py`: Launches a single agent on the default PX4 world.
- `sitl_multi_agent.launch.py`: Launches multiple agents on the default PX4 world.
- `sitl_single_agent_kth.launch.py`: Launches a single agent in the KTH Space Lab world **with** Gazebo-ROS odometry bridging enabled.
- `sitl_multi_agent_kth.launch.py`: Launches multiple agents in the KTH Space Lab world **with** Gazebo-ROS odometry bridging enabled.

> **Note:** Gazebo-ROS odometry bridging requires an additional ROS package depending on your ROS2 distribution:
>
> - **ROS2 Humble:**
>
>   ```bash
>   sudo apt install ros-humble-ros-gzharmonic-bridge
>   ```
>
> - **ROS2 Jazzy:**
>
>   ```bash
>   sudo apt install ros-jazzy-ros-gz-bridge
>   ```

The bridged odometry simulates the motion capture system used in the real KTH Space Lab and publishes ground-truth data from Gazebo to ROS.

## Testing a Multi-Agent setup

First make sure that your environment variable for `PX4_SPACE_SYSTEMS_DIR` is set. This can be checked with:

```bash
echo $PX4_SPACE_SYSTEMS_DIR
```

If this is not set, you can set it at the end of your `.bashrc` (or `.zshrc`) file with:

```bash
export PX4_SPACE_SYSTEMS_DIR=/path/to/your/PX4-Space-Systems
```

Then, test the multi-agent setup by running the following command:

```bash
ros2 launch discower_launch sitl_multi_agent.launch.py
```

> Alternatively, if you want to simulate in the `kthspacelab` world and use the Gazebo-ROS bridge, you can run:

```bash
ros2 launch discower_launch sitl_multi_agent_kth.launch.py
```

## Adding extra ATMOS platforms

In the launch file, for each vehicle, you can set the namespaces and pose for each vehicle. To add an extra vehicle, add another instance of the `px4.launch.py` with a different `id` and with five extra seconds of delay. Make sure to also change the `pose` variable to avoid agents being deployed in the same position. An example can be found below:

```python
lf_3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('discower_launch'), '/px4.launch.py']),

        launch_arguments={'id': '3', 'pose': '-1.0, 1.75, 0', 'name': 'snap', 'delay': '10', 'world': 'kthspacelab'}.items()
    )

ld.add_action(lf_3)
```
