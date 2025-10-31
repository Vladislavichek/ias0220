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

    # declare the argument 'which_bag'
    which_bag_arg = DeclareLaunchArgument(
        'which_bag',

        # You can put in the value "loops" to see an another recording, where
        #  I tried going in the figure 8 loop with the robot.
        # There is also a single recording called "bonus_demo", showcasing
        # the robot speed controlled by the distance from the sensor
        default_value='ros_bag_to_light',
        description='Which bag to use for recording'
    )

    # use LaunchConfiguration to get the value of the argument
    which_bag = LaunchConfiguration('which_bag')

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
            'ros2', 'bag', 'play',
            bag_path,
            '--topics', '/tf', '/tf_static', '/imu', "/distance"
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
