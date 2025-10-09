#!/usr/bin/env python3
"""
Publishes encoder output data based on a fake encoder for the two wheels of a differentially steered robot

@author: Simon Godon
@contact: simon.godon@taltech.ee
@creation_date: 25-08-2020
@updated_on: 14-09-2023
"""

import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from encoders_interfaces.msg import Counter
import sys
import math
import transforms3d
import random


class EncodersNode(Node):
    """
    uses /tf to publish the count of the encoder
    publishes topic "encoders_ticks"
    """

    def __init__(self):
        super().__init__("encoders_node")
        self.declare_parameters(
        namespace='',
        parameters=[
            ('noisy', False),
        ])
        self.cpr = 508.8  # ticks per wheel revolution
        self.rate = 100.0
        timer_period = 1.0/self.rate  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.count_publisher = self.create_publisher(
            Counter, '/encoders_ticks', 1000)
        self.msg = Counter()
        self.noisy = self.get_parameter("noisy").value

    def corrector(self, y):
        """ Corrects the instability of the transformation from quaternion to Euler angles."""
        if y > 0:
            return y
        else:
            return y+2*math.pi
        
    def get_count(self, rot):
        """ Takes a quaternion as an input and outputs the absolute encoder count of the rotation between the two frames. """
        quaternion = [rot.w , rot.x, rot.y, rot.z]
        euler = transforms3d.euler.quat2euler(quaternion, axes='sxyz')
        roll = euler[0]
        pitch = euler[1]
        yaw = euler[2]
        interval = 2*math.pi/self.cpr
        count = self.corrector(yaw)/interval
        if self.noisy:
            # Add a random gaussian noise
           count = random.normalvariate(count, 0.5)
        return int(math.modf(self.cpr - count)[1])

    def timer_callback(self):
        """
        Performs one iteration of class loop.
        Publishes click count for each wheel based on the transformations between base_link and the wheels.
        """
        self.msg.count_left = 0
        self.msg.count_right = 0
        try:
            rot_left = self.tf_buffer.lookup_transform(
                        'left_wheel',
                        'base_link',
                        rclpy.time.Time()).transform.rotation
            rot_right = self.tf_buffer.lookup_transform(
                        'right_wheel',
                        'base_link',
                        rclpy.time.Time())._transform.rotation
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform wheel to body: {ex}')
            return
        self.msg.count_left = self.get_count(rot_left)
        self.msg.count_right = self.get_count(rot_right)
        self.count_publisher.publish(self.msg)

def main():
    rclpy.init()
    encoders = EncodersNode()
    encoders.get_logger().warn(f'Started encoder node with noisy set to =  {encoders.get_parameter("noisy").value}')
    rclpy.spin(encoders)
    encoders.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
