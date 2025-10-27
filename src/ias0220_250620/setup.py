from setuptools import find_packages, setup
import os

from glob import glob

package_name = 'ias0220_250620'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Vladislav Mulgatsov',
    maintainer_email='vlmulg@taltech.ee',
    description='A package with a moving robot that is used as a part of '
                'independent work in TalTech university for a subject '
                'IAS0220 "Robot guidance and software"',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'random_walker = ias0220_250620.random_walker:main',
            'odometer = ias0220_250620.odometer:main',
            'odometry = ias0220_250620.odometry:main',
            'serial_interface = ias0220_sensors.serial_interface:main'
        ],
    },
)
