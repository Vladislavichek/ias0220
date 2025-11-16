import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    package_name = 'machine_vision_part2'
    world_file_name = 'mvt_light.world'

    world = os.path.join(get_package_share_directory(
        package_name), 'worlds', world_file_name)

    package_path = os.path.join(
        get_package_share_directory('machine_vision_part2'))

    rviz_path = package_path+'/config/mvt_config.rviz'


    urdf = os.path.join(package_path,
                              'urdf','ddrobot'
                              '/robot.xacro')
    
    doc = xacro.parse(open(urdf))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml(), 'use_sim_time': use_sim_time}


    return LaunchDescription([


        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', world],
            output='screen'),

        
        Node(
            package="machine_vision_part2",
            executable="circ_motion",
            namespace='ddrobot',
        ),


        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace='ddrobot',
            output='screen',
            parameters=[params],
            ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            namespace='ddrobot',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='urdf_spawner_bot',
            namespace='ddrobot',
            output='screen',
            arguments=["-topic", "/ddrobot/robot_description", "-entity", "ddrobot", "-z", "0.2"])
])
