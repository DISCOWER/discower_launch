import sys
import ast

import numpy as np
from std_msgs.msg import Bool
from geometry_msgs.msg import Point
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Pose
from px4_msgs.msg import VehicleStatus
import rclpy
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from rosidl_runtime_py import set_message_fields
from rclpy.node import Node


class PoseSetter(Node):
    def __init__(self):
        super().__init__('pose_setter')
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1
        )

        # get a time array, [0,5,10.5,...] from the parameter server
        self.time_array = self.declare_parameter('time_array',"").value
        self.time_array = np.array(ast.literal_eval(self.time_array),dtype=float)
        print(f"time_array: {self.time_array}")
        # get a pose array, [[x1,y1,z1],[x2,y2,z2],...] from the parameter server
        self.pose_array = self.declare_parameter('pose_array',"").value
        self.pose_array = np.array(ast.literal_eval(self.pose_array),dtype=float)
        print(f"pose_array: {self.pose_array}")

        self.status_sub = self.create_subscription(
            VehicleStatus,
            'fmu/out/vehicle_status',
            self.vehicle_status_callback,
            qos_profile)

        self.sync_sub = self.create_subscription(
            Bool,
            '/start',
            self.sync_callback,
            qos_profile
        )
        self.set_pose_pub = self.create_publisher(Pose, 'set_pose', qos_profile)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX

        self.start_time = None
        self.sequence_started = False
        self.pose_idx = 0

        # timer for publishing the current pose
        self.start_time_offset = 0

    def sync_callback(self, msg):
        """Receive the start signal"""
        if msg.data:
            self.sequence_started = True
            self.start_time = self.get_clock().now()
            self.get_logger().info('Sequence started')

    def vehicle_status_callback(self, msg):
        """Receive the vehicle status"""
        self.nav_state = msg.nav_state

    def timer_callback(self):
        """Publish the poses from the pose array"""
        if self.sequence_started and self.start_time:
            elapsed_time = self.get_clock().now() - self.start_time
            elapsed_time = elapsed_time.nanoseconds / 1e9

            # find the index of the time_array that is closest
            idx = np.argmin(np.abs(self.time_array - elapsed_time))
            pose = self.pose_array[idx]
            # pack it into a proper Pose message
            pose_msg = Pose()
            pose_msg.position.x = pose[0]
            pose_msg.position.y = pose[1]
            pose_msg.orientation.z = pose[2]
            self.set_pose_pub.publish(pose_msg)


def main(args=None):
    rclpy.init(args=args)

    node = PoseSetter()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()