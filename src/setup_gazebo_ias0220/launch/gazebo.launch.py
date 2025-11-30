import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import xacro


def spawn_and_publish(context, xacro_file: LaunchConfiguration):
    # Parse the xacro file
    doc = xacro.parse(open(xacro_file.perform(context)))
    xacro.process_doc(doc)
    model = {'robot_description_xml': doc.toxml()}

    # Spawn the entity
    spawn_entity_action = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-z', '0.05',
                '-unpause',
                '-topic', 'robot_description',
                '-entity',  'my_robot'],
    )
    spawn_entity_action.execute(context)

    # Publish the robot state
    publish_state_action = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'publish_frequency': 50.0,
                    'robot_description': model['robot_description_xml']
                    }])
    publish_state_action.execute(context)

def generate_launch_description():
    # Define launch arguments
    paused = LaunchConfiguration('paused', default='false')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    gui = LaunchConfiguration('gui', default='true')
    headless = LaunchConfiguration('headless', default='false')
    debug = LaunchConfiguration('debug', default='false')
    world_path = os.path.join(get_package_share_directory('setup_gazebo_ias0220'), 'worlds', "room_with_shapes.world")

    world = LaunchConfiguration('world')
    # Declare launch arguments
    declare_xacro_file_arg = DeclareLaunchArgument('xacro_file', description = 'xacro file for gazebo launch file')
    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load')
    
    return LaunchDescription([
        declare_xacro_file_arg,
        declare_world_cmd,

        # Specify launch files
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([get_package_share_directory('gazebo_ros'), '/launch/gazebo.launch.py']),
            launch_arguments={
                'debug': debug,
                'gui': gui,
                'paused': paused,
                'use_sim_time': use_sim_time,
                'headless': headless,
                'world': world
            }.items()
        ),

        # Define an OpaqueFunction action to spawn and publish
        OpaqueFunction(function=spawn_and_publish, args=[LaunchConfiguration('xacro_file')])
        
    ])
