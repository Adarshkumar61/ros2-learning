import rclpy
from rclpy.node import Node

class FirstNode(Node):
    def __init__(self):
        super().__init__('first_Node')
        self.get_logger().info('First Node has been started')

def main(args = None):
    rclpy.init(args= args)
    node = FirstNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()