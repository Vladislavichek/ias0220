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
        self.threshold = 0.2
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
        self.can_move = 0

    def move_callback(self, msg):
        if msg.range < self.threshold:
            self.can_move = 1
        else:
            self.can_move = 0

    def velocity_callback(self, msg):
        qw = msg.orientation.w
        qx = msg.orientation.x
        qy = msg.orientation.y
        qz = msg.orientation.z
        roll, pitch, yaw = euler.quat2euler((qw, qx, qy, qz))

        self.twist.linear.x = pitch * self.can_move
        self.twist.angular.z = roll

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
