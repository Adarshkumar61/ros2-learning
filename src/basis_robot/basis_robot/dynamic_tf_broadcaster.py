import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math


class SimpleTFBroadcaster(Node):

    def __init__(self):
        super().__init__('simple_tf_broadcaster')

        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_transform)

        self.angle = 0.0
        self.get_logger().info("TF Broadcaster Started")

    def broadcast_transform(self):
        t = TransformStamped()

        # Time
        t.header.stamp = self.get_clock().now().to_msg()

        # Parent and Child
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'

        # Simulate circular motion
        self.angle += 0.1
        t.transform.translation.x = math.cos(self.angle)
        t.transform.translation.y = math.sin(self.angle)
        t.transform.translation.z = 0.0

        # No rotation (identity quaternion)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = SimpleTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()