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

        self.get_logger().info('Fibonacci Action Server ready')

    def execute_callback(self, goal_handle):
        self.get_logger().info(

            f'Received goal: order={goal_handle.request.order}'
    )

        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()

        a, b = 0, 1
        sequence = []

        for i in range(goal_handle.request.order):
            sequence.append(a)

        
            feedback.partial_sequence = sequence.copy()
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(f'Feedback: {sequence}')

            rclpy.spin_once(self, timeout_sec=0.5)
            a, b = b, a + b

        goal_handle.succeed()
        result.sequence = sequence
        return result



def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()