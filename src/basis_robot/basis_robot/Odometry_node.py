import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class OdometryNode(Node):

    def __init__(self):
        super().__init__('odometry_node')

        # Subscriber to velocity commands
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        # Publisher for odometry
        self.odom_publisher = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        # Robot pose (initial position)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Velocity storage
        self.v = 0.0
        self.omega = 0.0

        # Time tracking
        self.last_time = self.get_clock().now()

        # Timer for 5 Hz update (0.2 sec)
        self.timer = self.create_timer(0.2, self.update_odometry)

        self.get_logger().info("Odometry node started...")


    # Velocity callback
    def cmd_callback(self, msg):
        self.v = msg.linear.x
        self.omega = msg.angular.z


    # Timer function (runs at 50Hz)
    def update_odometry(self):

        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        # Kinematic equations
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        self.theta += self.omega * dt

        # Create Odometry message
        odom_msg = Odometry()

        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = "odom"

        # Position
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        # Orientation (simplified: yaw only)
        # NOTE: Proper version uses quaternion conversion,
        #  but for simplicity we use a 2D approximation here    
        odom_msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        odom_msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)

        # Velocity
        odom_msg.twist.twist.linear.x = self.v
        odom_msg.twist.twist.angular.z = self.omega

        # Publish
        self.odom_publisher.publish(odom_msg)

        # Print current pose
        self.get_logger().info(
            f"x: {self.x:.3f}, y: {self.y:.3f}, theta: {self.theta:.3f}"
        )


# def main(args=None):
#     rclpy.init(args=args)
#     node = OdometryNode()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()


# """
#  now Test it properly
# Terminal 1 → Run node
# ros2 run basis_robot odometry_node
# Terminal 2 → publish velocity
# ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 1.0}, angular: {z: 0.5}}"
# Terminal 3 → check odometry
# ros2 topic echo /odom
# """ 







import rclpy
import math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


class odometrynode(Node):
    def __init__(self):
        super().__init__('odometry_node')

        self.create_subscription(
            Twist,
            "/cmd_vel", 
            self.cmd_callback,
            10
        )

        self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        #initilizing robot state:
        self.x = 0.0
        self.y = 0.0
        self.t = 0.0

        self.v = 0.0
        self.w = 0.0

        self.back_timer = self.get_clock().now()

        self.timer = self.create_timer(
            0.2,
            self.update_odom
        )

    def cmd_callback(self, msg):
        self.v = msg.linear.x
        self.w = msg.angular.z

    def update_odom(self):

        current_timer = self.get_clock().now()
        dt = (self.back_timer - current_timer).nanoseconds / 1e9
        self.back_timer = current_timer

        self.x +=  self.v * math.cos(self.t) * dt
        self.y += self.v * math.sin(self.t) * dt
        self.t += self.w * dt

        odom = Odometry()
        odom.header.stamp = current_timer.to_msg()
        odom.header.frame_id = "odom"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        odom.pose.pose.orientation.z = math.sin(self.t / 2.0)
        odom.pose.pose.orientation.w = math.cos(self.t / 2.0)

        odom.twist.twist.linear.x = self.v
        odom.twist.twist.angular.z = self.w

        self.get_logger().info(
            f"x: {self.x:.3f}, y: {self.y:.3f}, theta: {self.t:.3f}"
        )
        self.odom_publisher.publish(odom)


def main(args=None):
    rclpy.init(args=args)
    node = odometrynode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()   

if __name__ == '__main__':
    main()