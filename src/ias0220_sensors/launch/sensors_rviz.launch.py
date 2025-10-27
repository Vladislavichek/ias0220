"""
Launches a ros2 bag play node. The 'which_bag' argument should be given in command line.

launch with:
ros2 launch ias0220_sensors sensors_rviz.launch.py which_bag:=<bag_name>

@author: Roza Gkliva
@contact: roza.gkliva@taltech.ee
@date: October 2023
"""

import launch

from ament_index_python.packages import get_packages_with_prefixes

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

def generate_launch_description():

    # declare the argument 'which_bag'
    DeclareLaunchArgument(
        'which_bag',
        default_value='bag0',
        description='Which bag to use for recording'
    )

    # use LaunchConfiguration to get the value of the argument
    which_bag = LaunchConfiguration('which_bag')

    ## find the location of the ros2 workspace

    # use the 'ias0220_sensors package as reference
    pkg_in = {get_packages_with_prefixes()["ias0220_sensors"]}  

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
    
    return launch.LaunchDescription([
        bag_replay,
    ])
