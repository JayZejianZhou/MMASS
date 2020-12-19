from setuptools import setup

package_name = 'simulator'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, 'vanilla_agent'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zejian',
    maintainer_email='zhouzejian1994@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'service = vanilla_agent.main_tester:main'
            'ros_tester = simulator.simulator_tester:main'
        ],
    },
)
