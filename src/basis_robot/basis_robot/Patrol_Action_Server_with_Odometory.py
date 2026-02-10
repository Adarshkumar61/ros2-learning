import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from patrol_robot.action import Patrol
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

import math


class PatrolActionServer(Node):

    def __init__(self):
        super().__init__('patrol_action_server')

        # Action server
        self.action_server = ActionServer(
            self,
            Patrol,
            'patrol',
            self.execute_callback
        )

        # Robot state
        self.state = "IDLE"
        self.goal_handle = None
        self.current_waypoint = 0
        self.total_waypoints = 0

        # Internal robot position
        self.current_x = 0.0
        self.current_y = 0.0

        # Fake odom publisher
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)

        # Waypoints
        self.waypoints = [
            (1.0, 1.0),
            (2.0, 0.0),
            (3.0, 1.0),
        ]

        # Timer
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info("Headless Patrol Robot Started")

    # --------------------------------------------------
    # ACTION GOAL
    # --------------------------------------------------
    def execute_callback(self, goal_handle):

        self.goal_handle = goal_handle
        self.total_waypoints = goal_handle.request.num_waypoints
        self.current_waypoint = 0
        self.state = "MOVING"

        while self.state != "DONE":
            rclpy.spin_once(self)

        result = Patrol.Result()
        result.success = True
        goal_handle.succeed()

        return result

    # --------------------------------------------------
    # DISTANCE
    # --------------------------------------------------
    def distance_to_goal(self, gx, gy):
        return math.sqrt(
            (gx - self.current_x) ** 2 +
            (gy - self.current_y) ** 2
        )

    # --------------------------------------------------
    # PUBLISH FAKE ODOM
    # --------------------------------------------------
    def publish_odom(self):
        msg = Odometry()
        msg.pose.pose.position.x = self.current_x
        msg.pose.pose.position.y = self.current_y
        self.odom_pub.publish(msg)

    # --------------------------------------------------
    # TIMER (robot heartbeat)
    # --------------------------------------------------
    def timer_callback(self):

        if self.state == "IDLE":
            return

        goal_x, goal_y = self.waypoints[self.current_waypoint]

        # simulate movement toward goal
        dx = goal_x - self.current_x
        dy = goal_y - self.current_y

        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0.01:
            step = 0.1
            self.current_x += step * (dx / distance)
            self.current_y += step * (dy / distance)

        self.publish_odom()

        self.get_logger().info(
            f"Robot position: ({self.current_x:.2f}, {self.current_y:.2f})"
        )

        # check if waypoint reached
        if distance < 0.3:
            feedback = Patrol.Feedback()
            feedback.current_waypoint = self.current_waypoint + 1
            self.goal_handle.publish_feedback(feedback)

            self.current_waypoint += 1

            if self.current_waypoint >= self.total_waypoints:
                self.state = "DONE"

    # --------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = PatrolActionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
