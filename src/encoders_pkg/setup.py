from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'encoders_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/'+ package_name + '/config', ['config/encoders_params.yaml']),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='simon',
    maintainer_email='simon.godon@taltech.ee',
    description='A package to simulate encoders',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'encoders_node = encoders_pkg.encoders:main'
        ],
    },
)
