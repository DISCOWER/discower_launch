# discower_launch: SITL launch files
This repository contains launch files indicating how a single and multiple ATMOS space platform SITL simulation can be started.
The dependencies for launching the SITL simulation are
- [PX4-Space-Systems](https://github.com/DISCOWER/PX4-Space-Systems)
- [px4_msgs](https://github.com/DISCOWER/px4_msgs)

As this repository contains simple examples to merely run the SITL, you might need to follow additional instructions in the `PX4-Space-Systems` repository to fully get started. In short, you additionally need to
- build the workspace: `colcon build --symlink-install`
- start the microros service: `ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888`
after which you can display the robot's topics with `ros2 topic list`. Then, you can arm/disarm the robot with [QGroundControl](https://github.com/DISCOWER/qgroundcontrol). 

Further details can be found on the [ATMOS website](https://atmos.discower.io/pages/Simulation/)