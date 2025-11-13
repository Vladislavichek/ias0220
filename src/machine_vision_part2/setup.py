from setuptools import setup
import os
from glob import glob

package_name = 'machine_vision_part2'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf/ddrobot'), glob('urdf/ddrobot/*.xacro')),
        (os.path.join('share', package_name, 'urdf/ddrobot/xacro'), glob('urdf/ddrobot/xacro/*.xacro')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='laura',
    maintainer_email='laura.piho@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['circ_motion = machine_vision_part2.ddrobot_circular_motion:main',
        ],
    },
)
