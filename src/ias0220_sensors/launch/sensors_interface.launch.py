from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    imu_static_transform = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["--frame-id", "map", "--child-frame-id", "imu_link"]
    )

    sensors_interface = Node(
        package='ias0220_sensors',
        executable='serial_interface',
        name='sensors',
        output='screen',
        parameters=[
            {'serial_port': '/dev/ttyUSB0'}
        ]
    )


    return LaunchDescription([
        sensors_interface,
        imu_static_transform
        ]
    )