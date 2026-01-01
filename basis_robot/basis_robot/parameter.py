import rclpy
from rclpy.node import Node

def __init__(self: Node) -> None:
    super().__init__('basis_robot_parameter_node')
    self.declare_parameter('robot_name', 'BasisRobot')
    self.declare_parameter('max_speed', 1.0)
    self.declare_parameter('sensor_enabled', True)

    robot_name = self.get_parameter('robot_name').get_parameter_value().string_value
    max_speed = self.get_parameter('max_speed').get_parameter_value().double_value
    sensor_enabled = self.get_parameter('sensor_enabled').get_parameter_value().bool_value

    self.get_logger().info(f'Robot Name: {robot_name}')
    self.get_logger().info(f'Max Speed: {max_speed}')
    self.get_logger().info(f'Sensor Enabled: {sensor_enabled}')