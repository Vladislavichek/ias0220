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
    package_path = os.path.join(get_package_share_directory(package_name))

    # Parse the urdf with xacro
    xacro_file = os.path.join(package_path, "urdf",
                              "differential_robot_simu_task4_part1.urdf")
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)

    # Define launch arguments
    rvizconfig = LaunchConfiguration(
        "rvizconfig",
        default=os.path.join(
            get_package_share_directory(package_name),
            "config",
            "Task_4-1_config.rviz",
        ),
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

    # Define nodes
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz",
        arguments=["--display-config", rvizconfig],
    )

    launch_encoders = Node(
        package='encoders_pkg',
        executable='encoders_node',
        name='encoders_node',
        output='screen',

    )

    # joint_state_publisher_gui_node = Node(
    #     package="joint_state_publisher_gui",
    #     executable="joint_state_publisher_gui",
    #     name="joint_state_publisher_gui",
    # )

    # move_node = Node(
    #     package="transform_frame",
    #     executable="move",
    #     name="move",
    #     output="screen",
    # )

    teleop_twist_node = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="teleop_twist_keyboard",
        # remappings=[
        #     ("/cmd_vel", "move/cmd_vel")
        # ],
        output="screen",
        prefix="konsole -e"
    )

    rqt_node = Node(
        package="rqt_graph",
        executable="rqt_graph",
        name="rqt_graph",
    )

    return LaunchDescription(
        [
            gazebo_launch,
            rviz_node,
            launch_encoders,
            # joint_state_publisher_gui_node,
            # move_node,
            teleop_twist_node,
            rqt_node,
        ]
    )
