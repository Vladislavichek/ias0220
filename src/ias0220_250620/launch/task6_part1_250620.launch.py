import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

package_name = "ias0220_250620"


def generate_launch_description():
    # Define launch arguments
    rvizconfig = LaunchConfiguration(
        "rvizconfig",
        default=os.path.join(
            get_package_share_directory(package_name),
            "config",
            "task6_part1_250620.rviz",
        ),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output="screen",
        arguments=["--display-config", rvizconfig],
    )

    image_publisher = Node(
        package="ias0220_250620",
        executable="image_publish_node",
        name="image_publisher",
        output="screen"
    )

    camera_calibration = Node(
        package="ias0220_250620",
        executable="camera_calibration",
        name="camera_calibration",
        output="screen"
    )

    container = ComposableNodeContainer(
        name="image_proc_container",
        namespace="",
        package="rclcpp_components",
        executable="component_container",
        composable_node_descriptions=[
            ComposableNode(
                package="image_proc",
                plugin="image_proc::RectifyNode",
                name="image_proc",
                remappings=[
                    ("image", "/image_raw"),
                    # ("camera_info", "/camera_info"),
                    # ("image_rect", "/image_rect")  # optional output
                ]
            ),
        ],
        output="screen"
    )

    return LaunchDescription(
        [
            image_publisher,
            camera_calibration,
            container,
            rviz_node
        ]
    )
