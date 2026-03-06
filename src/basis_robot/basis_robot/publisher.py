import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.publisher = self.create_publisher(
            String,
            'chatter',
            10
        )
        timer = 1.0 
        self.timer_ = self.create_timer(timer, self.callback)
        self.count = 0
    def callback(self):
        msg = String()
        msg.data = f'hlo adarsh {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(msg.data)
        self.count += 1

def main(args = None):
    rclpy.init(args= args)
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()