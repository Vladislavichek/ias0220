from setuptools import find_packages
from setuptools import setup

setup(
    name='encoders_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('encoders_interfaces', 'encoders_interfaces.*')),
)
