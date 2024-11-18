from setuptools import setup, find_packages
from glob import glob
import os

package_name = 'discower_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
    ],
    zip_safe=True,
    maintainer='Joris',
    maintainer_email='jorisv@kth.se',
    description='TODO: Package description',
    license='TODO: License declaration',
)
