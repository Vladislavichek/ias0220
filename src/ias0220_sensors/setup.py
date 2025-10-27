import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ias0220_sensors'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Roza Gkliva ',
    maintainer_email='roza.gkliva@taltech.ee',
    description='Serial interface for the sensor module of the IAS0220 TalTech course.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'serial_interface = ias0220_sensors.serial_interface:main'
        ],
    },
)
