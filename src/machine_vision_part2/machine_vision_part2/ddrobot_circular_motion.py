# This creates a ros2 node that publishes /cmd_vel vel message of type Twist
# It makes the robot move with velocity 1 in x direction and 0.3 in angular z
# This makes the robot move in a circle 

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node # Handles the creation of nodes
from ament_index_python.packages import get_package_share_directory


class RobotCircularMotion(Node):

    def __init__(self):
        super().__init__('ddrobot_circular_motion')
        
        # create Twist msg
        self.msg = Twist()
        
        self.msg.linear.x = 0.0
        self.msg.linear.y = 0.0
        self.msg.linear.z = 0.0

        self.msg.angular.x = 0.0
        self.msg.angular.y = 0.0
        self.msg.angular.z = 0.0
        
        # create timer, publishes 0.01s 
        rate = 0.01  # seconds 2Hz
        self.pub = self.create_timer(rate, self.run)
        
        # creates /cmd_vel publisher
        self.robot_velocities = self.create_publisher(Twist, '/cmd_vel', 10)

    def robot_path(self):

        # assigns the velocity 
        self.msg.linear.x = 1.0
        self.msg.angular.z = 0.3
        self.robot_velocities.publish(self.msg)


    def run(self):
        while rclpy.ok():
            self.robot_path()
        
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.0
        self.robot_velocities.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)

    circular_motion_node = RobotCircularMotion()

    rclpy.spin(circular_motion_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    circular_motion_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
