import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
# from std_msgs.msg import String
from encoders_interfaces.msg import Counter
# from builtin_interfaces.msg import Time
import transforms3d.euler as euler


class PubOdom(Node):
    def __init__(self):
        super().__init__('odometry')
        self.sub_encod = self.create_subscription(
            Counter, '/encoders_ticks', self.encoder_callback, 10)

        self.odom_pub = self.create_publisher(Odometry, "/my_odom", 10)
        # self.timer_visual = self.create_timer(1, self.timer_callback)

        self.pose = Pose()
        self.odometry_msg = Odometry()

        # self.fake_msg = Counter()
        # self.fake_msg.count_left = 508
        # self.fake_msg.count_right = 0

        self.pose.position.x = 0.0
        self.pose.position.y = 0.0
        self.pose.position.z = 0.0

        self.old_left_cnt = 508
        self.old_right_cnt = 0

        self.x_linear = 0.0
        self.z_angular = 0.0
        self.delta_rot_angle = 0
        self.yaw = 0

        self.pose.position.x = 0.0
        self.pose.position.y = 0.0
        self.pose.position.z = 0.0

        # Constant values used later in the programme
        self.dt = 1

        self.max_rotation = 508   # The max wheel encoder counter value
        self.wheel_r = 0.036        # Wheel radius in meters
        self.wheel_distance = 0.35  # The distance between the wheels

        self.counter = 0

    # # A function used to debug the encoderCallback
    # # Generates a fake, easily changable message that is then pushed to the
    # # callback
    # def timer_callback(self):
    #     F = self.fake_msg
    #     # Simulate both wheels moving forward 10 ticks per tick
    #     F.count_left = self.old_left_cnt + 10
    #     F.count_right = self.old_right_cnt - 10

    #     if (F.count_left > 508.8):
    #         F.count_left -= 508
    #     elif (F.count_left < 0):
    #         F.count_left += 508

    #     if (F.count_right > 508.8):
    #         F.count_right -= 508
    #     elif (F.count_right < 0):
    #         F.count_right += 508

    #     self.get_logger().info(f'\tMsg published: count_left -{F.count_left}'
    #                            f' count_right - {F.count_right}')

    #     self.encoder_callback(self.fake_msg)

    def MakeLinear(self, delta_counter):
        if (math.fabs(delta_counter) > self.max_rotation/2):
            self.get_logger().info(
                f"Comparing {delta_counter} to {self.max_rotation/2}")
            if (delta_counter > 0):
                delta_counter -= self.max_rotation
            elif (delta_counter < 0):
                delta_counter += self.max_rotation

        left_rad = (delta_counter * 2 * math.pi) / self.max_rotation
        return (left_rad / self.dt) * self.wheel_r

    def encoder_callback(self, msg):
        delta_left_cnt = msg.count_left - self.old_left_cnt
        delta_right_cnt = -(msg.count_right - self.old_right_cnt)

        if delta_left_cnt == 0 and delta_right_cnt == 0:
            return

        left_lin_speed = float(self.MakeLinear(delta_left_cnt))
        right_lin_speed = float(self.MakeLinear(delta_right_cnt))

        self.x_linear = (left_lin_speed + right_lin_speed) / 2
        self.z_angular = (right_lin_speed - left_lin_speed)/self.wheel_distance
        self.delta_rot_angle = self.z_angular * self.dt

        self.pose.position.x += self.x_linear * math.cos(self.yaw)
        self.pose.position.y += self.x_linear * math.sin(self.yaw)

        # Set the current count as the old one
        self.old_left_cnt = msg.count_left
        self.old_right_cnt = msg.count_right

        self.pub_odometry()

    def pub_odometry(self):
        ODO = self.odometry_msg
        self.yaw += self.delta_rot_angle

        # Transforming Euler to quaternions
        qw, qx, qy, qz = euler.euler2quat(0.0, 0.0, self.yaw)

        # self.get_logger().info(
        #     f'The new z_angular: {self.z_angular:.4f}, '
        #     f'x_linear - {self.x_linear:.4f}\n')

        ODO.header.frame_id = "odom"
        ODO.header.stamp = self.get_clock().now().to_msg()
        ODO.child_frame_id = "base_link"
        ODO.pose.pose.position.x = self.pose.position.x
        ODO.pose.pose.position.y = self.pose.position.y
        ODO.pose.pose.position.z = 0.0
        ODO.pose.pose.orientation.w = qw
        ODO.pose.pose.orientation.x = qx
        ODO.pose.pose.orientation.y = qy
        ODO.pose.pose.orientation.z = qz
        ODO.twist.twist.angular.x = 0.0
        ODO.twist.twist.angular.y = 0.0
        ODO.twist.twist.angular.z = self.z_angular
        ODO.twist.twist.linear.x = self.x_linear
        ODO.twist.twist.linear.y = 0.0
        ODO.twist.twist.linear.z = 0.0

        self.odom_pub.publish(ODO)


def main(args=None):
    rclpy.init(args=args)
    pub_node = PubOdom()
    rclpy.spin(pub_node)

    pub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
