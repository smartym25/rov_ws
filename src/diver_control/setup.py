from setuptools import find_packages, setup

package_name = 'diver_control'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Martina Megla Ibarra',
    maintainer_email='martina.megla25@gmail.com',
    description='',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'depth_pub_exec = diver_control.depth_publisher:main',
            'depth_sub_exec = diver_control.depth_watcher:main',
            'depth_action_server = diver_control.depth_target_act_server:main',
            'depth_action_client = diver_control.depth_target_act_client:main'
        ],
    },
)
