# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import String

# class listener(Node):
#     def __init__(self):
#         super().__init__('listener_node')
#         self.get_logger().info('listener started..')

#         self.listener = self.create_subscription( #create_subscription(...)
#                                         #Subscribes to topic 'chatter'
#                                         #Whenever a message arrives → callback() runs

#             String,
#             'chatter',
#             self.call_back,
#             10
#             # """That 10 is the QoS depth (queue size).
#             # Meaning:If subscriber is slow,
#             # ROS2 can store up to 10 messages in queue.
#             # After that:Old messages get dropped.
#             # Think like:
#             # Publisher is fast.
#             # Subscriber is slow.
#             # Queue prevents immediate data loss.
#             # This is part of QoS (Quality of Service).=
#             # And QoS is VERY important in robotics."""
#         )
        
#     def call_back(self, msg):
#         self.get_logger().info(f'i recieved: {msg.data}')


# def main(args = None):
#     rclpy.init(args=args)
#     node = listener()
#     rclpy.spin(node)
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()












 
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocitySubscriber(Node):

    def __init__(self):
        super().__init__('velocity_subscriber')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.velocity_callback,
            10 # QoS depth (queue size)
        )

        self.get_logger().info("Velocity Subscriber Started")

    def velocity_callback(self, msg):
        self.get_logger().info(
            f"Received -> Linear.x: {msg.linear.x}, Angular.z: {msg.angular.z}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = VelocitySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()






