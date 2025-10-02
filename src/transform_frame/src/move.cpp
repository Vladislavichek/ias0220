#include <chrono>
#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2/LinearMath/Quaternion.h>

double vx = 0.0;
double vy = 0.0;
double vth = 0.0;

void receiveCmd(const geometry_msgs::msg::Twist::SharedPtr input_velocity)
{
  vx = input_velocity->linear.x;
  vy = 0;
  vth = input_velocity->angular.z;
}

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("move");

  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr vel_sub =
      node->create_subscription<geometry_msgs::msg::Twist>("move/cmd_vel", 1, receiveCmd);
  
  auto tf_broadcaster = std::make_shared<tf2_ros::TransformBroadcaster>(node);

  double x = 0.0;
  double y = 0.0;
  double th = 0.0;
  rclcpp::Time current_time, last_time;
  current_time = node->now();
  last_time = node->now();

  rclcpp::Rate r(100);
  while (rclcpp::ok()) {

    rclcpp::spin_some(node);  // Check for incoming messages

    current_time = node->now();
    // Compute odometry in a typical way given the velocities of the robot
    double dt = (current_time - last_time).seconds();
    double delta_x = (vx * cos(th) - vy * sin(th)) * dt;
    double delta_y = (vx * sin(th) + vy * cos(th)) * dt;
    double delta_th = vth * dt;

    x += delta_x;
    y += delta_y;
    th += delta_th;

    // Since all odometry is 6DOF, we'll need a quaternion created from yaw
    tf2::Quaternion odom_quat;
    odom_quat.setRPY(0, 0, th);

    // First, we'll publish the transform over tf
    geometry_msgs::msg::TransformStamped odom_trans;
    odom_trans.header.stamp = current_time;
    odom_trans.header.frame_id = "map";
    odom_trans.child_frame_id = "base_footprint";

    odom_trans.transform.translation.x = x;
    odom_trans.transform.translation.y = y;
    odom_trans.transform.translation.z = 0.0;
    odom_trans.transform.rotation.x = odom_quat.x();
    odom_trans.transform.rotation.y = odom_quat.y();
    odom_trans.transform.rotation.z = odom_quat.z();
    odom_trans.transform.rotation.w = odom_quat.w();

    // Send the transform
    tf_broadcaster->sendTransform(odom_trans);

    vx = 0.0;
    vy = 0.0;
    vth = 0.0;

    last_time = current_time;
    r.sleep();
  }

  rclcpp::shutdown();
  return 0;
}
