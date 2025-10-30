import os
import launch
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_packages_with_prefixes
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
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

    steering_node = Node(
        package="ias0220_250620",
        executable="steering_node",
        name="steering_node",
        output="screen"
    )

<<<<<<< HEAD
    # static_transform = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     name="map_to_odom_broadcaster",
    #     output="screen",
    #     arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    # )

    # launch_encoders = Node(
    #     package='encoders_pkg',
    #     executable='encoders_node',
    #     name='encoders_node',
    #     output='screen',
    # )

    # odometry = Node(
    #     package="ias0220_250620",
    #     executable="odometry",
    #     name="odometry",
    #     output="screen"
    # )

    # declare the argument 'which_bag'
=======
>>>>>>> 0797777 (Almost completed the task 5.2. Only left to create own bag file with robot going to the light source in gazebo)
    which_bag_arg = DeclareLaunchArgument(
        'which_bag',
        default_value='bag2',
        description='Which bag to use for recording'
    )

<<<<<<< HEAD
    # rvizconfig = LaunchConfiguration(
    #     "rvizconfig",
    #     default=os.path.join(
    #         get_package_share_directory(package_name),
    #         "config",
    #         "task_5-1_config.rviz",
    #     ),
    # )

    # # Define nodes
    # rviz_node = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     name="rviz",
    #     arguments=["--display-config", rvizconfig],
    # )

=======
>>>>>>> 0797777 (Almost completed the task 5.2. Only left to create own bag file with robot going to the light source in gazebo)
    # use LaunchConfiguration to get the value of the argument
    which_bag = LaunchConfiguration('which_bag')

    # find the location of the ros2 workspace

    # use the 'ias0220_sensors package as reference
    pkg_in = {get_packages_with_prefixes()["ias0220_250620"]}

    # slice the string and remove the last two parts from the list
    pkg_ = pkg_in.pop().split('/')[:-2]

    # create the bag directory path
    where_bag = "/".join(pkg_) + "/bags/"
    print(f'{where_bag}')

    # create the full path to the bag file
    bag_path = PathJoinSubstitution([where_bag, which_bag])

    bag_replay = launch.actions.ExecuteProcess(
        cmd=[
            'ros2', 'bag', 'play', '-r', '1', '-l',
            bag_path
            ],
        output='screen'
        )

    return LaunchDescription(
        [
            gazebo_launch,
            # rviz_node,
            # odometry,
            # static_transform,
            # launch_encoders,
            # rqt_node,
            which_bag_arg,
            bag_replay,
            steering_node
        ]
    )
