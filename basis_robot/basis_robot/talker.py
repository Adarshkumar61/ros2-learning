import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class talker(Node):
    def __init__(self):
        super().__init__('talker node')
        self.get_logger().info('talker starting..')

        #creating publisgher
        self.publiser_ = self.create_publisher(String, 'chatter', 10)
        timer_sec = 0.5

        # creating timer
        self.timer = self.create_timer(timer_sec, self.publish_msg)
        self.count = 0
    
    #fn for publishing msg
    def publish_msg(self):
        msg = String()
        msg.data = 'hello adarsh {self.count}'
        self.publisher_.publish(msg)
        
        #print log
        self.get_logger().info('Publishing: {msg.data}')
        self.count += 1


def main(args = None):
    rclpy.init(args=args)
    node = talker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()