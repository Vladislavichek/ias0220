import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from encoders_interfaces.msg import Counter
from builtin_interfaces.msg import Time
import transforms3d.euler as euler


class PosCalc(Node):
    def __init__(self):
        super().__init__('odometry')
        self.sub_encod = self.create_subscription(
            Counter, 'encoders_ticks', self.encoder_callback, 10)

        self.pub_odom = self.create_publisher(Odometry, "cord_visual", 10)
        self.timer_visual = self.create_timer(0.5, self.pub_visualise)

        self.pose = Pose()
        self.odometry_msg = Odometry()

        self.pose.position.x = 0.0
        self.pose.position.y = 0.0
        self.pose.position.z = 0.0

        self.old_left_cnt = 1
        self.old_right_cnt = 1

        self.x_linear = 0
        self.z_angular = 0
        self.delta_rot_angle = 0
        self.yaw = 0

        self.pose.position.x = 0.0
        self.pose.position.y = 0.0
        self.pose.position.z = 0.0

        # A constant time difference between vector value recipience
        self.dt = 0.5

        self.max_rotation = 518.8   # The max wheel encoder counter value
        self.wheel_r = 0.036        # Wheel radius in meters
        self.wheel_distance = 0.35  # The distance between the wheels

        self.counter = 0

    def encoder_callback(self, msg):
        delta_left_cnt = msg.count_left - self.old_left_cnt
        delta_right_cnt = msg.count_right - self.old_right_cnt

        if (delta_left_cnt < self.max_rotation/2):
            left_rad = (delta_left_cnt * 2 * math.pi) / self.max_rotation
            left_lin_speed = (left_rad / self.dt) * self.wheel_r
        # else if()
        #

        if (delta_right_cnt < self.max_rotation/2):
            right_rad = (delta_right_cnt * 2 * math.pi) / self.max_rotation
            right_lin_speed = (right_rad / self.dt) * self.wheel_r

        self.x_linear = (left_lin_speed + right_lin_speed) / 2
        self.z_angular = (left_lin_speed - right_lin_speed)/self.wheel_distance
        self.delta_rot_angle = self.z_angular * self.dt

        self.pose.position.x += self.x_linear * math.cos(self.yaw)
        self.pose.position.y += self.x_linear * math.sin(self.yaw)

        # Set the current count as the old one
        self.old_left_cnt = msg.count_left
        self.old_right_cnt = msg.count_right

        # self.get_logger().info(
        #     f'The new position of the walker is :'
        #     f'\nx: {pos.x}\ny: {pos.y}\nz: {pos.z}')

    
    


    def pub_odom(self):
        ODO = self.odometry_msg
        self.yaw += self.delta_rot_angle

        # Transforming Euler to quaternions
        qw, qx, qy, qz = euler.euler2quat(0.0, 0.0, self.yaw)

        ODO.header.frame_id = "odom"
        ODO.header.stamp = self.get_clock().now().to_msg()
        ODO.child_frame_id = "base_link"
        ODO.pose.pose.position.x = self.pose.position.x
        ODO.pose.pose.position.y = self.pose.position.y
        ODO.pose.pose.position.z = 0
        ODO.pose.pose.orientation.w = qw
        ODO.pose.pose.orientation.x = qx
        ODO.pose.pose.orientation.y = qy
        ODO.pose.pose.orientation.z = qz
        ODO.twist.twist.angular.x = 0
        ODO.twist.twist.angular.y = 0
        ODO.twist.twist.angular.z += self.z_angular
        ODO.twist.twist.linear.x += self.x_linear
        ODO.twist.twist.linear.y = 0
        ODO.twist.twist.linear.z = 0

        self.pub_odom.publish(ODO)


def main(args=None):
    rclpy.init(args=args)
    sub_node = PosCalc()
    rclpy.spin(sub_node)

    sub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
