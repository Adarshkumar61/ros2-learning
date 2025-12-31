import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class listener(Node):
    def __init__(self):
        super().__init__('listener_node')
        self.get_logger().info('listener started..')

        self.listener = self.create_subscription(
            String,
            'chatter',
            self.call_back,
            10
        )
        
    def call_back(self, msg):
        self.get_logger().info(f'i recieved: {msg.data}')


def main(args = None):
    rclpy.init(args=args)
    node = listener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()