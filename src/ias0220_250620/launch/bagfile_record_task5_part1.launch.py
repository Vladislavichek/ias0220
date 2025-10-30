import launch
from ament_index_python.packages import get_packages_with_prefixes
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument

package_name = "ias0220_250620"


def generate_launch_description():
    # For whatever reason picked "world" as static frame instead of map
    # when created the launch file for the lab

    bag_name_arg = DeclareLaunchArgument(
        'bag_name',
        default_value='recorded',
        description='Name for the output bag file'
    )
    # use LaunchConfiguration to get the value of the argument
    bag_name = LaunchConfiguration('bag_name')

    # find the location of the ros2 workspace

    # use the 'ias0220_sensors package as reference
    pkg_in = {get_packages_with_prefixes()["ias0220_250620"]}

    # slice the string and remove the last two parts from the list
    pkg_ = pkg_in.pop().split('/')[:-2]

    # create the bag directory path
    where_bag = "/".join(pkg_) + "/bags/"
    print(f'{where_bag}')

    # create the full path to the bag file
    bag_path = PathJoinSubstitution([where_bag, bag_name])

    bag_record = launch.actions.ExecuteProcess(
        cmd=[
            'ros2', 'bag', 'record', '-o',
            bag_path
            ],
        output='screen'
        )

    static_transform_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub',
        arguments=['0', '0', '0', '0', '0', '0', 'world', 'imu_link'],
        output='screen'
    )

    # 2. Launch the serial_interface.py node
    serial_interface = Node(
        package='ias0220_sensors',
        executable='serial_interface',
        name='serial_interface_node',
        output='screen'
    )

    return LaunchDescription(
        [
            bag_name_arg,
            bag_record,
            static_transform_publisher,
            serial_interface,
        ]
    )
