from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    patrol_server = Node(
        package='basis_robot',
        executable='patrol_action_server',
        name='patrol_action_server',
        output='screen'
    )

    patrol_client = Node(
        package='basis_robot',
        executable='patrol_action_client',
        name='patrol_action_client',
        output='screen'
    )

    return LaunchDescription([
        patrol_server,
        patrol_client
    ])
