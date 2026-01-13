import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from robo_action_pkg.action import MoveRobot


class MoveRobotActionServer(Node):

    def __init__(self):
        super().__init__('move_robot_action_server')

        self._action_server = ActionServer(
            self,
            MoveRobot,
            'move_robot',
            self.execute_callback
        )

        self.get_logger().info('MoveRobot Action Server started')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        distance = goal_handle.request.distance
        speed = goal_handle.request.speed

        feedback = MoveRobot.Feedback()
        result = MoveRobot.Result()

        current_position = 0.0

        while current_position < distance:
            current_position += speed
            feedback.current_position = current_position
            goal_handle.publish_feedback(feedback)
            time.sleep(1.0)

        goal_handle.succeed()
        result.success = True

        self.get_logger().info('Goal completed')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotActionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
