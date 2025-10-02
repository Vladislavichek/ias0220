import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from numpy import random
from geometry_msgs.msg import Vector3

random.seed(None)


class PublishRandom(Node):
    def __init__(self):
        super().__init__('random_walker')
        self.pub_move = self.create_publisher(Vector3, 'velocity', 10)
        self.pub_time = self.create_publisher(String, "name_and_time", 10)
        self.timer_name_time = self.create_timer(0.5, self.publish_name_time)
        self.timer_vector3 = self.create_timer(0.5, self.publish_vector3)

    def publish_vector3(self):
        msg = Vector3()
        msg.x = float(random.randint(-1, 2))
        msg.y = float(random.randint(-1, 2))
        msg.z = float(random.randint(-1, 2))
        self.pub_move.publish(msg)
        to_log = (f'The random velocity: \nx: {msg.x}\ny: {msg.y}\nz: {msg.z}')
        self.get_logger().info(f'{to_log}')

    def publish_name_time(self):
        now = self.get_clock().now()  # rclpy.time.Time object
        # timestamp = now.nanoseconds() * 1e-9
        sec, nsec = now.seconds_nanoseconds()
        timestamp = sec + nsec * 1e-9
        msg = String()
        msg.data = "250620," + str(timestamp)

        self.pub_time.publish(msg)
        self.get_logger().info(f'My ID and current time: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = PublishRandom()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
