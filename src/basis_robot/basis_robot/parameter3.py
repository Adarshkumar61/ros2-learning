import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class robotspeed(Node):
    def __init__(self):
        super().__init__('robotspeed')

        self.declare_parameter('robot_speed', 1.2)
        self.declare_parameter('robot_name', 'HEBA')
        self.declare_parameter('max_speed', 5.0)


        self.speed = self.get_parameter('robot_speed').value
        self.name = self.get_parameter('robot_name').value
        self.max_speed = self.get_parameter('max_speed').value


        self.timer = self.create_timer(1.0, self.callback)

        self.add_on_set_parameters_callback(self.callback)

    def callback(self):
        self.get_logger().info(f'{self.name} speed is {self.speed}')
        self.get_logger().info(f'{self.name} max speed is {self.max_speed}')

def main(args = None):
    rclpy.init(args = args)
    node = robotspeed()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()