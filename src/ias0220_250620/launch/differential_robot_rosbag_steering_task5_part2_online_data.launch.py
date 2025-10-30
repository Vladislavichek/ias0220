import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

package_name = "ias0220_250620"


def generate_launch_description():
    package_path = os.path.join(get_package_share_directory(package_name))

    # Parse the urdf with xacro
    xacro_file = os.path.join(package_path, "urdf",
                              "differential_robot_simu_task4_part1.urdf")
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("setup_gazebo_ias0220"),
                "launch",
                "gazebo.launch.py"
            )
        ),
        launch_arguments={
            "xacro_file": xacro_file
        }.items(),
    )

    serial_interface = Node(
        package='ias0220_sensors',
        executable='serial_interface',
        name='serial_interface_node',
        output='screen'
    )

    steering_node = Node(
        package="ias0220_250620",
        executable="steering_node",
        name="steering_node",
        output="screen"
    )

    return LaunchDescription(
        [
            gazebo_launch,
            serial_interface,
            steering_node
        ]
    )
