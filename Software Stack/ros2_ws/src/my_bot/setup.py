from setuptools import setup

package_name = 'my_bot'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],  # This should match the folder where your Python code is
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='My bot with LiDAR filter',
    license='MIT',
    entry_points={
        'console_scripts': [
            'lidar_fov_filter = my_bot.lidar_fov_filter:main',  # Your node entry point
        ],
    },
)