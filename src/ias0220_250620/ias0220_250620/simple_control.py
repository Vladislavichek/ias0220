#!/usr/bin/env python3

"""
Solution to home assignment 7 (Robot Control). Node to take a set of
waypoints and to drive a differential drive robot through those waypoints
using a simple PD controller and provided odometry data.

@author: Yuya Hamamatsu
@date: 04.11.23
@input: Odometry as nav_msgs Odometry message
@output: body velocity commands as geometry_msgs Twist message.
"""

import math
import rclpy
import time
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
import numpy as np
from geometry_msgs.msg import Twist, PoseStamped, Point
from visualization_msgs.msg import Marker
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion


class PDController(Node):
    def __init__(self):
        # Your code here
        super().__init__('controller')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Wait for run other nodes
        time.sleep(5)

        # variables for error change rate calculation
        self.start_time = self.get_clock().now()
        self.last_odom_time = self.get_clock().now()

        self.sub_odom = self.create_subscription(
            Odometry, '/detector_robot/diff_cont/odom', self.onOdom, 10)
        self.sub_goal = self.create_subscription(
            PoseStamped, '/goal_pose', self.onGoal, 10)

        self.vel_cmd_pub = self.create_publisher(
            Twist, '/detector_robot/cmd_vel', 10)
        self.pub_viz = self.create_publisher(Marker, "waypoints", 10)

        # self.create_timer(1, self.debugPrint)

        self.marker_frame = "map"

        self.dt = 0.01

        self.vel_cmd_msg = Twist()

        # [linear_velocity, angular_velocity]
        self.vel_cmd = np.array([0.0, 0.0])

        self.pos = np.array([0.0, 0.0])     # Current position [x, y]
        self.pos_diff = 0.0                 # Distance to the current waypoint
        self.theta = 0.0                    # Current orientation (yaw)
        self.prev_theta = 0.0
        self.th_diff = 0.0                  # Angle error to current waypoint
        self.prev_th_diff = 0.0

        self.error = np.array([0.0, 0.0])   # [dx, dy] to current waypoint

        # Norm of error change for derivative term
        self.error_change_rate_norm = 0.0

        self.prev_error = np.array([0.0, 0.0])
        # self.prev_pos_diff = 0.0

        # Load params from parameter server
        self.waypoints = []
        # self.waypoints_x = []
        # self.waypoints_y = []
        read_waypoints_x = self.declare_parameter('waypoints_x', [0.0]).value
        read_waypoints_y = self.declare_parameter('waypoints_y', [0.0]).value
        self.Kp = np.array(self.declare_parameter('Kp', [0.0, 0.0]).value)
        self.Kd = np.array(self.declare_parameter('Kd', [0.0, 0.0]).value)

        # Identify the waypoints parameter is correcly load or not
        if (read_waypoints_x == [0.0]) and (read_waypoints_y == [0.0]):
            self.get_logger().error("!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!")
            self.get_logger().error("Parameters not loaded correctly")
            self.get_logger().error(
                "Please check your launch file to load yaml file correctly")
            self.get_logger().error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if (read_waypoints_x) and (read_waypoints_y):
            for i in range(len(read_waypoints_x)):
                self.waypoints.append(
                    [read_waypoints_x[i], read_waypoints_y[i]])
        self.waypoints = np.array(self.waypoints)

        self.distance_margin = self.declare_parameter(
            'distance_margin', 0.05).value
        self.target_angle = self.wrapAngle(self.declare_parameter(
            'target_angle', 0.0).value)

        # Check Params
        self.get_logger().info(f'Waypoints: \n {self.waypoints}')
        self.get_logger().info(f'Kp: {self.Kp}')
        self.get_logger().info(f'Kd: {self.Kd}')
        self.get_logger().info(f'Start Time: {self.start_time}')


    # def debugPrint(self):
    #     self.get_logger().info(f'Angular: th_diff - {self.th_diff}  ')
    #     self.get_logger().info(f'theta_change_rat - {self.theta_change_rate}')
    #     self.get_logger().info(f'Linear: pos_diff - {self.pos_diff}   ')
    #     self.get_logger().info(f'error_change_rate - {self.error_change_rate_norm}')

    def onGoal(self, msg):
        new_wp = np.array([[msg.pose.position.x, msg.pose.position.y]])
        self.waypoints = np.vstack([self.waypoints, new_wp])


    def update_pose_from_tf(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                'map',        # target frame
                'base_link',  # source frame
                rclpy.time.Time()
            )

            # Position
            self.pos[0] = transform.transform.translation.x
            self.pos[1] = transform.transform.translation.y

            # Orientation
            q = transform.transform.rotation
            (roll, pitch, yaw) = euler_from_quaternion([q.x, q.y, q.z, q.w])
            self.theta = yaw

            return True

        except Exception as e:
            self.get_logger().warn(f"TF lookup failed: {e}")
            return False


    def wrapAngle(self, angle):
        """
        Helper function that returns angle wrapped between +- Pi.
        Hint: Pass your error in heading [rad] into this function, and it
        returns the shorter angle. This prevents your robot from turning
        along the wider angle and makes it turn along the smaller angle (but
        in opposite direction) instead.
        @param: self
        @param: angle - angle to be wrapped in [rad]
        @result: returns wrapped angle -Pi <= angle <= Pi
        """
        return (angle + math.pi) % (2 * math.pi) - math.pi

    def control(self):
        """
        Takes the errors and calculates velocities from it, according to
        PD control algorithm.
        @param: self (errors got using "calculateError" function)
        @result: sets the values in self.vel_cmd
        """

        ang_vel = self.Kp[0]*self.th_diff + self.Kd[0]*self.theta_change_rate
        lin_vel = self.Kp[1]*self.pos_diff + self.Kd[1]*self.error_change_rate_norm


        # self.get_logger().info(f'')

        if abs(self.th_diff) > 0.25:  # large angle?
            ang_vel *= 3
            lin_vel = 0.01

        self.vel_cmd = (lin_vel, ang_vel)


    def publishWaypoints(self):
        """
        Publishes the list of waypoints, so RViz can see them.
        @param: self
        @result: publish message
        """
        marker = Marker()
        marker.header.frame_id = self.marker_frame

        marker.type = marker.SPHERE_LIST
        marker.action = marker.ADD

        marker.scale.x = self.distance_margin
        marker.scale.y = self.distance_margin
        marker.scale.z = self.distance_margin
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0

        marker.pose.orientation.w = 1.0

        marker.points = [Point(x=waypoint[0], y=waypoint[1], z=0.0)
                         for waypoint in self.waypoints]

        self.pub_viz.publish(marker)

    def calculateError(self):
        """
        calculate the lateral error to the first waypoint and the angle error.
        The angle error - the difference between where the robot was originally
        headed to and where it should be headed
        @param: self
        @result: updates self.error, self.error_change_rate, self.th_diff and
                 self.pos_diff
        """
        # Your code here
        if self.waypoints.size == 0:
            return

        delta_x = self.waypoints[0, 0] - self.pos[0]
        delta_y = self.waypoints[0, 1] - self.pos[1]

        self.error[0] = delta_x
        self.error[1] = delta_y

        theta_goal = math.atan2(delta_y, delta_x)

        self.th_diff = self.wrapAngle(theta_goal - self.theta)

        ang_diff = self.wrapAngle(self.th_diff - self.prev_th_diff)
        self.theta_change_rate = ang_diff / max(self.dt, 0.01)

        self.pos_diff = math.sqrt(delta_x ** 2 + delta_y ** 2)

        error_change_rate = (self.error - self.prev_error) / max(self.dt, 0.01)
        self.error_change_rate_norm = math.sqrt(error_change_rate[0]**2
                                                + error_change_rate[1]**2)

        self.prev_error = self.error.copy()


    def isWaypointReached(self):
        """
        check if a waypoint is reached. The user defines the threshold during 
        the runtime
        @param: self
        @result: if a waypoint is reached, that waypoint is popped from the
                 waypoint list and a value "True" is returned,
                 otherwise a value "False" is returned.
        """

        if self.waypoints.size != 0:
            if (self.pos_diff < self.distance_margin):
                self.waypoints = np.delete(self.waypoints, 0, axis=0)
                return True

        return False

    def onOdom(self, odom_msg):
        """
        Handles incoming odometry updates (callback function).
        @param: self
        @param odom_msg - odometry geometry message
        @result: update of relevant vehicle state variables
        """

        if not self.update_pose_from_tf():
            return

        now_odom_time = rclpy.time.Time.from_msg(odom_msg.header.stamp)

        dt_tmp = (now_odom_time - self.last_odom_time).to_msg()
        self.dt = float(dt_tmp.sec + dt_tmp.nanosec/1e9)
        self.last_odom_time = now_odom_time

        # Calculate error between current pose and next waypoint position
        self.calculateError()

        # Check reaching waypoint or not
        if self.isWaypointReached():
            self.get_logger().info(
                "Reached waypoint!\nFuture waypoint list: "
                + str(self.waypoints))
            self.calculateError()  # Update error with new target waypoint

        # Calculate velocity command using PID control
        self.control()

        self.prev_theta = self.theta
        self.prev_th_diff = self.th_diff

        # publish velocity commands
        self.vel_cmd_msg.linear.x = self.vel_cmd[0]
        self.vel_cmd_msg.angular.z = self.vel_cmd[1]
        self.vel_cmd_pub.publish(self.vel_cmd_msg)

        # Publish waypoints visualization
        self.publishWaypoints()



def main(args=None):
    rclpy.init(args=args)
    controller = PDController()
    rclpy.spin(controller)


if __name__ == "__main__":
    main()
