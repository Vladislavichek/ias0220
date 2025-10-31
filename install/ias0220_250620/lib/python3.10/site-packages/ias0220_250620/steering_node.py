import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
import transforms3d.euler as euler


class Steer(Node):
    def __init__(self):
        super().__init__('steering_node')

        # A constant threshold for distance above which the sensor has to see
        # for the robot to move
        self.high_speed_threshold = 0.04
        self.low_speed_threshold = 0.08
        # A consant value (Hz) showing the frequency of published movement
        # messages
        self.pub_freq = 30

        self.sub_imu = self.create_subscription(
            Imu, 'imu', self.velocity_callback, 10)
        self.sub_distance = self.create_subscription(
            Range, "distance", self.move_callback, 10)

        self.pub_move = self.create_publisher(
            Twist, "/cmd_vel", 10)

        self.move_timer = self.create_timer(1/self.pub_freq, self.pub_velocity)

        self.twist = Twist()
        # A variable to show whether the robot is allowed to move or not
        self.move_multiplier = 0

    def move_callback(self, msg):
        if msg.range < self.low_speed_threshold and msg.range > 0:
            if msg.range < self.high_speed_threshold:
                self.move_multiplier = 2
            else:
                self.move_multiplier = 1
        else:
            self.move_multiplier = 0

    def velocity_callback(self, msg):
        qw = msg.orientation.w
        qx = msg.orientation.x
        qy = msg.orientation.y
        qz = msg.orientation.z
        roll, pitch, yaw = euler.quat2euler((qw, qx, qy, qz))

        self.twist.linear.x = pitch * self.move_multiplier
        self.twist.angular.z = roll * 0.5 * self.move_multiplier

    def pub_velocity(self):
        self.pub_move.publish(self.twist)


def main(args=None):
    rclpy.init(args=args)
    sub_node = Steer()
    rclpy.spin(sub_node)

    sub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
