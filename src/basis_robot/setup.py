from setuptools import find_packages, setup

package_name = 'basis_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='adarsh61',
    maintainer_email='adarshb2k61@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'first_node = basis_robot.first_node:main',
            'talker = basis_robot.talker:main',
            'listener = basis_robot.listener:main',
            'parameter = basis_robot.parameter:main',
            'myparamnode = basis_robot.parameter2:main',
            'robotspeed = basis_robot.parameter3:main',
            'myparamnodee = basis_robot.parameter4:main',
            'service_server = basis_robot.service_server:main',
            'service_client = basis_robot.service_client:main',
            'service_add = basis_robot.service_add_two_int:main',
            'client_add = basis_robot.client_add_two_int:main',

            'ActionServerNode = basis_robot.Action_Serverr:main',
            'ActionClientNode = basis_robot.action_client:main',
        ],
    },
)
