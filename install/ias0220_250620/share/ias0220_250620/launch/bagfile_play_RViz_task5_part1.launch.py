import os
import launch
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_packages_with_prefixes
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

package_name = "ias0220_250620"


def generate_launch_description():
    # declare the argument 'which_bag'
    which_bag_arg = DeclareLaunchArgument(
        'which_bag',
        default_value='bag1',
        description='Which bag to use for recording'
    )

    rvizconfig = LaunchConfiguration(
        "rvizconfig",
        default=os.path.join(
            get_package_share_directory(package_name),
            "config",
            "task_5-1_config.rviz",
        ),
    )

    # Define nodes
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz",
        arguments=["--display-config", rvizconfig],
    )



    # use LaunchConfiguration to get the value of the argument
    which_bag = LaunchConfiguration('which_bag')

    ## find the location of the ros2 workspace

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
            which_bag_arg,
            rviz_node,
            bag_replay
        ]
    )
