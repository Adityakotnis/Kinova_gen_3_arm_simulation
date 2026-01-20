from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'sensor_pipeline'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # 👇 THIS installs your launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'udp_bridge = sensor_pipeline.udp_bridge:main',
            'state_estimator = sensor_pipeline.state_estimator:main',
            'sensor_parser = sensor_pipeline.sensor_parser:main',
            'robot_controller = sensor_pipeline.robot_controller:main',
            'fake_imu_publisher = sensor_pipeline.fake_imu_publisher:main',
        ],
    },
)
