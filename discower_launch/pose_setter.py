import sys
import ast

import numpy as np
from std_msgs.msg import Bool
from geometry_msgs.msg import Point
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Pose
import rclpy
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from rosidl_runtime_py import set_message_fields
from rclpy.node import Node

from px4_msgs.msg import VehicleStatus
from mpc_msgs.srv import SetPose


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(SetPose, 'set_pose')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = SetPose.Request()

    def send_request(self, pose):
        self.req.pose.position.x = pose.position.x
        self.req.pose.position.y = pose.position.y
        self.req.pose.position.z = pose.position.z
        self.req.pose.orientation.w = pose.orientation.w
        self.req.pose.orientation.x = pose.orientation.x
        self.req.pose.orientation.y = pose.orientation.y
        self.req.pose.orientation.z = pose.orientation.z
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

        
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

        self.minimal_client = MinimalClientAsync()
        # self.cli = self.create_client(SetPose, 'set_pose')
        # while not self.cli.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        # self.req = SetPose.Request()

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
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX

        self.start_time = None
        self.sequence_started = False
        self.pose_idx = 0

        # timer for publishing the current pose
        self.start_time_offset = 0

    def sync_callback(self, msg):
        """Receive the start signal"""
        if msg.data and not self.sequence_started:
            self.sequence_started = True
            self.start_time = self.get_clock().now()
            self.get_logger().info('Sequence started')

    def vehicle_status_callback(self, msg):
        """Receive the vehicle status"""
        self.nav_state = msg.nav_state

    def timer_callback(self):
        print("timer_callback")
        print("self.sequence_started: ", self.sequence_started)
        print("self.start_time: ", self.start_time)
        """Publish the poses from the pose array"""
        if self.sequence_started and self.start_time:
            elapsed_time = self.get_clock().now() - self.start_time
            elapsed_time = elapsed_time.nanoseconds / 1e9

            # find the index of the time_array that is closest
            idx = np.argmin(np.abs(self.time_array - elapsed_time))
            if idx > self.pose_idx:
                self.pose_idx = idx
                print(f"elapsed_time: {elapsed_time}")
                print(f"idx: {idx}")
                pose = self.pose_array[idx]
                print(f"pose: {pose}")
                # pack it into a proper Pose message
                pose_msg = Pose()
                pose_msg.position.x = pose[0]
                pose_msg.position.y = pose[1]
                pose_msg.orientation.z = pose[2]
                self.minimal_client.send_request(pose_msg)

    # def send_request(self, pose):
    #     self.req.pose.position.x = pose.position.x
    #     self.req.pose.position.y = pose.position.y
    #     self.req.pose.position.z = pose.position.z
    #     self.req.pose.orientation.w = pose.orientation.w
    #     self.req.pose.orientation.x = pose.orientation.x
    #     self.req.pose.orientation.y = pose.orientation.y
    #     self.req.pose.orientation.z = pose.orientation.z
    #     self.future = self.cli.call_async(self.req)
    #     rclpy.spin_until_future_complete(self, self.future)
    #     return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    node = PoseSetter()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()