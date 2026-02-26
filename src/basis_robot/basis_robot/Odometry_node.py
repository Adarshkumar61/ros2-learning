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
        #Rotation happens because theta changes, not because omega exists.
        #Omega just controls how theta changes.
        # #But if you manually change theta, you’re forcing rotation.

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

        # Think of quaternion like this:
           # It’s just a mathematical container that stores:
                # “Robot is rotated by θ radians around Z-axis.”   
        odom_msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        odom_msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)

        # Velocity
        #Speed comes from this:

        odom_msg.twist.twist.linear.x = self.v
        odom_msg.twist.twist.angular.z = self.omega

        # Publish
        self.odom_publisher.publish(odom_msg)

        # Print current pose
        self.get_logger().info(
            f"x: {self.x:.3f}, y: {self.y:.3f}, theta: {self.theta:.3f}"
        )
        """Position → Where am I
Orientation (theta) → Which way am I facing
Velocity (v, omega) → How am I moving

Movement depends on:  v and omega

Orientation depends on:  theta

omega → changes theta
theta → determines quaternion


"""

def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


# """
#  now Test it properly
# Terminal 1 → Run node
# ros2 run basis_robot odometry_node
# Terminal 2 → publish velocity
# ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 1.0}, angular: {z: 0.5}}"
# Terminal 3 → check odometry
# ros2 topic echo /odom
# """ 


"""

question : If:

v = 2
omega = 0
theta = π/2

Is robot rotating?

Is robot moving?

Will x increase or y increase?

Will quaternion change over time?

now understand the answer:

v = 2 → robot is moving forward at speed 2 m/s
omega = 0 → robot is not rotating (no angular velocity)
theta = π/2 → robot is facing 90 degrees (facing "up" in 2D plane)
 
theta = pi/2
x = 0 + 2 * cos(pi/2) * dt = 0 (cos(pi/2) = 0)
y = 0 + 2 * sin(pi/2) * dt = 2 * dt (sin(pi/2) = 1)
means : x will not increase (stays at 0)
y will increase (moves up)




rule :
Facing right → x increases
Facing left → x decreases
Facing up → y increases
Facing down → y decreases




question : theta = -π/2
v = 4
omega = 0


theta = -π/2
v = 4
omega = 0
Step 1 — Is robot rotating?

omega = 0
So:

✔ Robot is NOT rotating.

Correct.

Step 2 — What does theta = -π/2 mean?

First remember the circle:

0 → facing +X

+π/2 → facing +Y

π → facing -X

-π/2 → facing -Y

So:

theta = -π/2

Means robot is facing negative Y direction (downwards).

The minus sign just means clockwise rotation.

Nothing scary.

Step 3 — Apply Motion Equations
𝑥
+
=
𝑣
⋅
𝑐
𝑜
𝑠
(
𝜃
)
⋅
𝑑
𝑡
x+=v⋅cos(θ)⋅dt
𝑦
+
=
𝑣
⋅
𝑠
𝑖
𝑛
(
𝜃
)
⋅
𝑑
𝑡
y+=v⋅sin(θ)⋅dt

Now plug theta = -π/2:

We know:

cos(-π/2) = 0

sin(-π/2) = -1

So:

✅ Final Answer

✔ Robot not rotating
✔ Robot moving
✔ X does not change
✔ Y decreases

          +Y
           ↑
           |
 -X ← ---- 0 ---- → +X
           |
           ↓
          -Y

"""




