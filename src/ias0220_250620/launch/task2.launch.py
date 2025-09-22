from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
import os

def generate_launch_description():
    # Declare model argument
    model_arg = DeclareLaunchArgument(
        "model",
        default_value=os.path.join(
            os.path.dirname(__file__), "..", "urdf", "differential_robot.urdf"
        ),
        description="Absolute path to URDF/Xacro file"
    )

    # Robot description (defer xacro call until launch time)
    robot_description = Command(["xacro ", LaunchConfiguration("model")])

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        output="screen",
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])