import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
import xacro

package_name = "ias0220_250620"


def generate_launch_description():
    package_path = os.path.join(get_package_share_directory(package_name))

    # Parse the urdf with xacro
    xacro_file = os.path.join(package_path, "urdf",
                              "differential_robot_simu_task8.urdf.xacro")

    doc = xacro.process_file(xacro_file)
    robot_description = doc.toxml()

    map_file = os.path.join(package_path, "map", "room.yaml")
    nav2_yaml = os.path.join(package_path, "map", "nav2_params.yaml")

    config = os.path.join(
        package_path,
        'config',
        'simple_control_v2.yaml'
    )

    rvizconfig = LaunchConfiguration(
        "rvizconfig",
        default=os.path.join(
            get_package_share_directory(package_name),
            "config",
            "differential_robot_rviz_task8-2.rviz",
        ),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output="screen",
        parameters=[{"robot_description": robot_description},
                    {'use_sim_time': True}],
        arguments=["--display-config", rvizconfig],
    )

    delayedNodes = TimerAction(
        period=3.0,
        actions=[
            Node(
                package="ias0220_250620",
                executable="task9_control",
                name="controller",
                output="screen",
                parameters=[config],
            ),

            IncludeLaunchDescription(
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
            ),

            Node(
                package="nav2_map_server",
                executable="map_server",
                name="map_server",
                output="screen",
                parameters=[{'use_sim_time': True},
                            {"yaml_filename": map_file}]
            ),

            Node(
                package='nav2_amcl',
                executable='amcl',
                name='amcl',
                output='screen',
                parameters=[nav2_yaml]
            ),

            Node(
                package='nav2_lifecycle_manager',
                executable='lifecycle_manager',
                name='lifecycle_manager_localization',
                output='screen',
                parameters=[{'use_sim_time': True},
                            {'autostart': True},
                            {'node_names': ['map_server', 'amcl']}]
            ),

            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="map_to_odom_broadcaster",
                output="screen",
                arguments=['0', '0', '0', '0', '0', '0', 'odom', 'map']
            ),
        ]
    )

    return LaunchDescription(
        [
            rviz_node,
            delayedNodes
        ]
    )
