import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Vector3


class PosCalc(Node):
    def __init__(self):
        super().__init__('pos_calc')
        self.sub_move = self.create_subscription(
            Vector3, 'velocity', self.sub_move, 10)

        self.sub_time = self.create_subscription(
            String, "name_and_time", self.pub_info, 10)
        self.sub_time

        self.pose = Pose()

        self.pose.position.x = 0.0
        self.pose.position.y = 0.0
        self.pose.position.z = 0.0

        # A constant time difference between vectors
        self.dt = 0.5

    def pub_info(self, msg):
        parts = msg.data.split(",")
        if len(parts) == 2:
            student_id = parts[0].strip()
            timestamp = float(parts[1].strip())
            self.get_logger().info(
                f'Student {student_id} contacted me, '
                f'and told me that current time is {timestamp}')

    def sub_move(self, msg):
        pos = self.pose.position

        pos.x += msg.x * self.dt
        pos.y += msg.y * self.dt
        pos.z += msg.z * self.dt

        self.get_logger().info(
            f'The new position of the walker is :'
            f'\nx: {pos.x}\ny: {pos.y}\nz: {pos.z}')

        # msg = Vector3()
        # msg.x = float(random.randint(-1, 2))
        # msg.y = float(random.randint(-1, 2))
        # msg.z = float(random.randint(-1, 2))
        # self.pub_move.publish(msg)
        # to_log = (f'The random velocity: \n{msg.x}\n{msg.y}\n{msg.z}')
        # self.get_logger().info(f'{to_log}')

    # def publish_name_time(self):
    #     now = self.get_clock().now()  # rclpy.time.Time object
    #     # timestamp = now.nanoseconds() * 1e-9
    #     sec, nsec = now.seconds_nanoseconds()
    #     timestamp = sec + nsec * 1e-9
    #     msg = String()
    #     msg.data = "250620," + str(timestamp)

    #     self.pub_time.publish(msg)
    #     self.get_logger().info(f'My ID and current time: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    sub_node = PosCalc()
    rclpy.spin(sub_node)

    sub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
