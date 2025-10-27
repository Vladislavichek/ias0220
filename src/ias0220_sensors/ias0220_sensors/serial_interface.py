#!/usr/bin/python3

"""
Serial interface node between Arduino Nano and ROS 2.
Made for Robotics course IAS0220 "Robotite juhtimine ja tarkvara"

Receives Serial messages from Arduino and publishes them as ROS messages.
The code receives distance and IMU Euler angles from Arduino and publishes 
them as Range and IMU messages.


@author: Roza Gkliva
@author: Kilian Ochs (ROS Melodic version?)
@contact: roza.gkliva@taltech.ee
@date: September 2023
"""

import rclpy
from rclpy.node import Node

import serial
import numpy as np
import math

import tf2_ros

from scipy.spatial.transform import Rotation

from sensor_msgs.msg import Imu, Range
from geometry_msgs.msg import TransformStamped

class SerialInterface(Node):
    """ Interfaces an arduino mcu over serial port. Handles data transfer and publishing of relevant info.
    - Arduino --> ROS:
        - Reads and decodes the incoming packets.
        - Populates and publishes range and imu data.
    """

    def __init__(self):
        super().__init__('serial_interface')

        # serial communication settings:
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        self.baud_rate = 115200

        # Open the serial port
        self.openSerialPort()

        # incoming packet info:
        self.packet_header = '##'
        self.packet_footer = '\n'

        # set up messages and publishers
        self.pub_imu = self.create_publisher(Imu, 'imu', 10)
        self.pub_distance = self.create_publisher(Range, 'distance', 10)

        # distance sensor (hc-sr04) characteristics
        self.hc_sr04_min_range = 0.02           # m
        self.hc_sr04_max_range = 4.0            # m
        self.hc_sr04_field_of_view = 0.523599   # rad
        self.hc_sr04_radiation_type = 0         # 0: ultrasound, 1: infrared

        # set up timer to collect data:
        self.sampling_time = 0.1
        self.receiving_timer = self.create_timer(
            self.sampling_time,
            self.readBuffer
        )

        # set up TF broadcaster
        self.br = tf2_ros.TransformBroadcaster(self)

    def openSerialPort(self):
        """
        Open the serial port for communication.
        """
        try:

            self.ser = serial.Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=0,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS)

            self.get_logger().info(f'Serial port opened: {self.serial_port}')

        except (IndexError, serial.SerialException) as e:
            self.get_logger().error(f'Error: {e}. Check if device connected.')

    def readBuffer(self):
        """
        Reads data from serial buffer. Isolates the packet payload. Calls to publish.
        @input: self
        @returns: /
        """

        self.msg_start = -1
        self.msg_end = -1

        if self.ser.in_waiting > 3:
            packet = self.ser.read(50)

            # if data is in the buffer, read
            if len(packet) > 13:
                self.msg_start = packet.index(
                    self.packet_header.encode('UTF-8')) if self.packet_header.\
                        encode('UTF-8') in packet else None
                self.msg_end = packet.index(
                    self.packet_footer.encode('UTF-8')) if self.packet_footer.\
                        encode('UTF-8') in packet else None
                
                if None not in (self.msg_start, self.msg_end):
                    # isolate data array (payload)
                    payload = packet[ self.msg_start + len(self.packet_header) : self.msg_end ]

                    if self.msg_start < self.msg_end:
                        self.publish(payload)

    def publish(self, payload):

        data = payload.decode('utf-8').split(';')
        distance = data[0]
        roll = float(data[1])
        pitch = float(data[2])
        yaw = float(data[3])

        ## populate and publish Range message
        dist_msg = Range()
        dist_msg.header.frame_id = "ultrasound_distance_sensor"
        dist_msg.header.stamp = self.get_clock().now().to_msg()
        dist_msg.min_range = self.hc_sr04_min_range
        dist_msg.max_range = self.hc_sr04_max_range
        dist_msg.field_of_view = self.hc_sr04_field_of_view
        dist_msg.radiation_type = self.hc_sr04_radiation_type
        dist_msg.range = float(distance)/100.0

        self.pub_distance.publish(dist_msg)

        ## populate and publish imu message
        imu_msg = Imu()
        imu_msg.header.frame_id = "imu_link"
        imu_msg.header.stamp = self.get_clock().now().to_msg()

        # convert euler angles to quaternions
        rot = Rotation.from_euler('xyz', [math.radians(roll), math.radians(pitch), math.radians(yaw)])
        imu_msg.orientation.x = rot.as_quat()[0]
        imu_msg.orientation.y = rot.as_quat()[1]
        imu_msg.orientation.z = rot.as_quat()[2]
        imu_msg.orientation.w = rot.as_quat()[3]

        self.pub_imu.publish(imu_msg)

        # broadcast imu TF for visualizing range sensor on the same frame with rviz 
        range_q = [imu_msg.orientation.w, imu_msg.orientation.x, imu_msg.orientation.y, imu_msg.orientation.z]
        range_t = [0.0, 0.0, 0.0]
        self.broadcastSensorsTF(range_q, range_t)


    def broadcastSensorsTF(self, q, tvec):
        tf = TransformStamped()
        tf.header.stamp = self.get_clock().now().to_msg()
        tf.header.frame_id = "imu_link"

        tf.child_frame_id = "ultrasound_distance_sensor"
        tf.transform.translation.x = tvec[0]
        tf.transform.translation.y = tvec[1]
        tf.transform.translation.z = tvec[2]
        tf.transform.rotation.w = q[0]
        tf.transform.rotation.x = q[1]
        tf.transform.rotation.y = q[2]
        tf.transform.rotation.z = q[3]
        self.br.sendTransform(tf)


def main(args=None):
    rclpy.init(args=args)
    serial_interface = SerialInterface()
    rclpy.spin(serial_interface)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    serial_interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()