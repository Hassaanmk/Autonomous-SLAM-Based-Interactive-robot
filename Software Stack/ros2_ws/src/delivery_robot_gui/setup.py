from setuptools import find_packages, setup

package_name = 'delivery_robot_gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'rclpy', 'geometry_msgs', 'PyQt5'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='narmeenistic123@gmail.com',
    description='GUI for Autonomous Delivery Robot',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
           'delivery_robot_gui = delivery_robot_gui.delivery_robot_gui:main',  # Entry point to your script
        ],
    },
)
