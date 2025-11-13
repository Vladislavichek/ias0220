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
    machine_vision_pkg = get_package_share_directory('machine_vision_part2')

    machine_vision_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(machine_vision_pkg, 'launch', 'mvt_main.launch.py')
        )
    )

    package_path = os.path.join(get_package_share_directory(package_name))

    # Parse the urdf with xacro
    xacro_file = os.path.join(package_path, "urdf",
                              "differential_robot_simu_task4_part2.urdf")
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}

    # Publish robot_description to /robot_description
    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace="detector_robot",
        parameters=[robot_description],
        output='screen'
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        # name='urdf_spawner_bot',
        # namespace='detector_robot',
        output='screen',
        arguments=["-entity", "detector_robot",
                   "-topic", "/detector_robot/robot_description",
                   "-x", "0.6", "-y", "-7.5", "-z", "0.0", "-Y", "1.6"]
    )

    return LaunchDescription(
        [
            robot_state_pub_node,
            spawn_robot,
            machine_vision_launch
        ]
    )
