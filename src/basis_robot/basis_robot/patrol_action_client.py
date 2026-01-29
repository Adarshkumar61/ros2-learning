import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from patrol_robot.action import Patrol


class PatrolActionClient(Node):

    def __init__(self):
        super().__init__('patrol_action_client')

        # Create Action Client
        self._action_client = ActionClient(
            self,
            Patrol,
            'patrol'
        )

    def send_goal(self):
        # Create goal message
        goal_msg = Patrol.Goal()
        goal_msg.num_waypoints = 5   # ✅ PROPER GOAL VALUE

        # Wait for server to be available
        self._action_client.wait_for_server()

        # Send goal asynchronously
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        # Register callback for goal response
        self._send_goal_future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Patrol goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Patrol goal accepted')

        # Request result from server
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(
            self.get_result_callback
        )

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Robot reached waypoint {feedback.current_waypoint}'
        )

    def get_result_callback(self, future):
        result = future.result().result

        self.get_logger().info(
            f'Patrol finished successfully = {result.success}'
        )

        # Shut down client after completion
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    patrol_client = PatrolActionClient()
    patrol_client.send_goal()

    rclpy.spin(patrol_client)


if __name__ == '__main__':
    main()
