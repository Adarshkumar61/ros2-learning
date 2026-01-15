import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from custom_action_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

        self.get_logger().info('Fibonacci Action Server started')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing Fibonacci goal')

        order = goal_handle.request.order

        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()

        sequence = [0, 1]
        feedback.partial_sequence = sequence.copy()
        goal_handle.publish_feedback(feedback)

        for i in range(2, order):
            sequence.append(sequence[i-1] + sequence[i-2])
            feedback.partial_sequence = sequence.copy()
            goal_handle.publish_feedback(feedback)
            time.sleep(1)

        goal_handle.succeed()
        result.sequence = sequence

        self.get_logger().info('Fibonacci goal succeeded')
        return result



def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
