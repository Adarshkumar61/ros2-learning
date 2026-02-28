# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import String



# class talker(Node):
#     def __init__(self):
#         super().__init__('talker_node')
#         self.get_logger().info('talker starting..')

#         #creating publisher
#         self.publisher_ = self.create_publisher(
#             String,
#             'chatter',
#             10)
#         timer_sec = 0.5

#         # creating timer
#         self.timer = self.create_timer(timer_sec, self.publish_msg)
#         self.count = 0
    
#     #fn for publishing msg
#     def publish_msg(self):
#         msg = String()
#         msg.data = f'hello adarsh {self.count}'
#         self.publisher_.publish(msg)
        
#         #print log
#         self.get_logger().info(f'Publishing: {msg.data}')
#         self.count += 1


# def main(args = None):
#     rclpy.init(args=args)
#     node = talker()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()







import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('velocity_publisher')

        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(1.0, self.publish_velocity)

        self.get_logger().info("Velocity Publisher Started")

    def publish_velocity(self):
        msg = Twist()

        msg.linear.x = 0.5
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.2

        self.publisher_.publish(msg)

        self.get_logger().info(
            f"Publishing -> Linear.x: {msg.linear.x}, Angular.z: {msg.angular.z}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()