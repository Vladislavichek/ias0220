import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Vector3
from visualization_msgs.msg import Marker


class PosCalc(Node):
    def __init__(self):
        super().__init__('position_calculator')
        self.sub_move = self.create_subscription(
            Vector3, 'velocity', self.velocity_callback, 10)
        self.sub_time = self.create_subscription(
            String, "name_and_time", self.pub_info, 10)

        self.pub_visual = self.create_publisher(Marker, "cord_visual", 10)
        self.timer_visual = self.create_timer(0.5, self.pub_visualise)

        self.pose = Pose()
        self.marker_msg = Marker()

        self.pose.position.x = 0.0
        self.pose.position.y = 0.0
        self.pose.position.z = 0.0

        # A constant time difference between vector value recipience
        self.dt = 0.5

        self.counter = 0

    def pub_info(self, msg):
        parts = msg.data.split(",")
        if len(parts) == 2:
            student_id = parts[0].strip()
            timestamp = float(parts[1].strip())
            self.get_logger().info(
                f'Student {student_id} contacted me, '
                f'and told me that current time is {timestamp}')

    def velocity_callback(self, msg):
        pos = self.pose.position

        pos.x += msg.x * self.dt
        pos.y += msg.y * self.dt
        pos.z += msg.z * self.dt

        self.get_logger().info(
            f'The new position of the walker is :'
            f'\nx: {pos.x}\ny: {pos.y}\nz: {pos.z}')

    def pub_visualise(self):
        MRK = self.marker_msg

        MRK.header.frame_id = "map"
        MRK.type = MRK.SPHERE
        MRK.action = MRK.ADD
        MRK.scale.x = 0.5
        MRK.scale.y = 0.5
        MRK.scale.z = 0.5
        MRK.color.a = 0.2
        MRK.color.r = 1.0
        MRK.color.g = 0.0
        MRK.color.b = 0.0
        MRK.lifetime = rclpy.duration.Duration(seconds=1000).to_msg()
        MRK.pose = self.pose
        MRK.pose.orientation.x = 0.0
        MRK.pose.orientation.y = 0.0
        MRK.pose.orientation.z = 0.0
        MRK.pose.orientation.w = 1.0
        MRK.id = self.counter
        self.counter += 1

        self.pub_visual.publish(MRK)


def main(args=None):
    rclpy.init(args=args)
    sub_node = PosCalc()
    rclpy.spin(sub_node)

    sub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
