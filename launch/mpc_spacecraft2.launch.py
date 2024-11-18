#!/usr/bin/env python
############################################################################
#
#   Copyright (C) 2022 PX4 Development Team. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name PX4 nor the names of its contributors may be
#    used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
############################################################################

__author__ = "Pedro Roque, Jaeyoung Lim"
__contact__ = "padr@kth.se, jalim@ethz.ch"

from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    
    return LaunchDescription([
        # Snap
        Node(
            package='px4_mpc',
            namespace='snap',
            executable='rviz_pos_marker',
            name='rviz_pos_marker_0',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='rviz2',
            namespace='snap',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', [os.path.join(get_package_share_directory('px4_mpc'), 'config.rviz')]]
        ),
        Node(
            package='px4_mpc',
            namespace='snap',
            executable='mpc_spacecraft',
            name='mpc_spacecraft_0',
            output='screen',
            emulate_tty=True,
            parameters=[{'mode': 'rate'}], # rate/wrench/direct_allocation
        ),
        Node(
            package='px4_offboard',
            namespace='snap',
            executable='visualizer',
            name='visualizer_0',
        ),



        # Crackle 
        Node(
            package='px4_mpc',
            namespace='crackle',
            executable='rviz_pos_marker',
            name='rviz_pos_marker_1',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='px4_mpc',
            namespace='crackle',
            executable='mpc_spacecraft',
            name='mpc_spacecraft_1',
            output='screen',
            emulate_tty=True,
            parameters=[{'mode': 'rate'}], # rate/wrench/direct_allocation
        ),
        Node(
            package='px4_offboard',
            namespace='crackle',
            executable='visualizer',
            name='visualizer_1',
        ),

    ])
