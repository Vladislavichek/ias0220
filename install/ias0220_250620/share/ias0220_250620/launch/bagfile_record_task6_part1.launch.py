import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

package_name = "ias0220_250620"


def generate_launch_description():
    # the static_transform_publisher (relating RViz' fixed frame to the IMU reference frame), 

        # the "serial_interface.py" node and 
        # a ros2 bag node which records all published data into a bag file named "recorded" inside a "bags" folder of your package.


        # 1. Static transform publisher from "world" to "imu_link"
    static_transform_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub',
        arguments=['0', '0', '0', '0', '0', '0', 'world', 'imu_link'],
        output='screen'
    )

    # 2. Launch the serial_interface.py node
    serial_interface = Node(
        package='ias0220_sensors',  # Replace with your actual package name
        executable='serial_interface',  # Must match the name of the installed executable
        name='serial_interface_node',
        output='screen'
    )
    

    return LaunchDescription(
        [
        static_transform_publisher,
        serial_interface,
        ]
    )
