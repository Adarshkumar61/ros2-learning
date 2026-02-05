import rclpy
import math
from rclpy.node import Node
from rclpy.action import ActionServer
from patrol_robot.action import Patrol
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class PatrolActionServer(Node):

    def __init__(self):
        super().__init__('patrol_action_server')

        # -------- Action Server --------
        self.action_server = ActionServer(
            self,
            Patrol,
            'patrol',
            self.execute_callback
        )

        # -------- Robot State --------
        self.state = "IDLE"
        self.goal_handle = None
        self.current_waypoint = 0
        self.total_waypoints = 0

        # -------- Robot Position --------
        self.current_x = 0.0
        self.current_y = 0.0

        self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # -------- Velocity Publisher --------
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # -------- Waypoints (x, y) --------
        self.waypoints = [
            (1.0, 1.0),
            (2.0, 0.0),
            (3.0, 1.0),
        ]

        # -------- Timer (heartbeat) --------
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info("Patrol Server Ready (State + Odom + cmd_vel)")

    # ---------------------------------------------------
    # ODOM CALLBACK
    # ---------------------------------------------------
    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    # ---------------------------------------------------
    # DISTANCE CALCULATION
    # ---------------------------------------------------
    def distance_to_goal(self, gx, gy):
        return math.sqrt(
            (gx - self.current_x) ** 2 +
            (gy - self.current_y) ** 2
        )

    # ---------------------------------------------------
    # MOVE / STOP FUNCTIONS
    # ---------------------------------------------------
    def move_forward(self):
        msg = Twist()
        msg.linear.x = 0.2
        self.cmd_pub.publish(msg)

    def stop_robot(self):
        msg = Twist()
        self.cmd_pub.publish(msg)

    # ---------------------------------------------------
    # ACTION GOAL RECEIVED
    # ---------------------------------------------------
    def execute_callback(self, goal_handle):

        self.get_logger().info(
            f"Received patrol goal: {goal_handle.request.num_waypoints}"
        )

        self.goal_handle = goal_handle
        self.total_waypoints = goal_handle.request.num_waypoints
        self.current_waypoint = 0
        self.state = "MOVING"

        # Keep action alive while robot runs
        while self.state != "DONE":
            rclpy.spin_once(self)

        result = Patrol.Result()
        result.success = True
        goal_handle.succeed()

        self.get_logger().info("Patrol completed successfully")
        return result

    # ---------------------------------------------------
    # TIMER CALLBACK = ROBOT BRAIN
    # ---------------------------------------------------
    def timer_callback(self):

        if self.state == "IDLE":
            return

        self.get_logger().info(f"[STATE] {self.state}")

        if self.state == "MOVING":

            goal_x, goal_y = self.waypoints[self.current_waypoint]
            distance = self.distance_to_goal(goal_x, goal_y)

            self.get_logger().info(
                f"Distance to waypoint: {distance:.2f}"
            )

            if distance < 0.3:
                self.stop_robot()

                feedback = Patrol.Feedback()
                feedback.current_waypoint = self.current_waypoint + 1
                self.goal_handle.publish_feedback(feedback)

                self.get_logger().info(
                    f"Reached waypoint {self.current_waypoint + 1}"
                )

                self.current_waypoint += 1
                self.state = "WAITING"

            else:
                self.move_forward()

        elif self.state == "WAITING":
            self.get_logger().info("Waiting at waypoint...")
            self.state = "CHECK_DONE"

        elif self.state == "CHECK_DONE":

            if self.current_waypoint >= self.total_waypoints:
                self.state = "DONE"
            else:
                self.state = "MOVING"

        elif self.state == "DONE":
            pass


def main(args=None):
    rclpy.init(args=args)
    node = PatrolActionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
