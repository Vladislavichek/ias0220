import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
import xacro

package_name = "ias0220_250620"


def generate_launch_description():
    package_path = os.path.join(get_package_share_directory(package_name))

    # Parse the urdf with xacro
    xacro_file = os.path.join(package_path, "urdf",
                              "differential_robot_simu_task4_part2.urdf.xacro")

    doc = xacro.process_file(xacro_file)
    robot_description = doc.toxml()

    config = os.path.join(
        package_path,
        'config',
        'simple_control_v2.yaml'
    )

    control_node = Node(
        package="ias0220_250620",
        executable="control_node",
        name="controller",
        output="screen",
        parameters=[config],
        # remappings=[
        #     ('/cmd_vel', '/detector_robot/cmd_vel'),
        #     # ('/diff_cont/odom', '/detector_robot/diff_cont/odom')
        # ]
    )

    rvizconfig = LaunchConfiguration(
        "rvizconfig",
        default=os.path.join(
            get_package_share_directory(package_name),
            "config",
            "differential_robot_rviz_task8.rviz",
        ),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output="screen",
        parameters=[{"robot_description": robot_description}],
        arguments=["--display-config", rvizconfig],
    )

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

    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',  # or 'sync_slam_toolbox_node'
        name='slam_toolbox',
        output='screen',
        parameters=[{
            'use_sim_time': True,          # important for simulation
            'scan_topic': '/scan',         # your laser topic
            'base_frame': 'base_link',
            'odom_frame': 'odom',
            'map_frame': 'map'
        }]
    )

    # static_transform = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     name="map_to_odom_broadcaster",
    #     output="screen",
    #     arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    # )

    return LaunchDescription(
        [
            control_node,
            gazebo_launch,
            rviz_node,
            slam_node,
            # static_transform
        ]
    )
