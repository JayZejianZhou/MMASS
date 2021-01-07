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
            'agent_test = simulator.agent_tester:main',
            'agent_group_test = simulator.agent_team_tester:main',
            'clock_server = simulator.clock.run_turn_based_clocker:main',
            'clock_client_test = simulator.clock_client_test:main',
            'main = simulator.main:main'
        ],
    },
)
