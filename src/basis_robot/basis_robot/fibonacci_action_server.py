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
    #Function to run when a goal is received
    #execute_callback() must:
    # Read goal
    # Send feedback (optional)
    # Call goal_handle.succeed()
    # Return result
    def execute_callback(self, goal_handle):
        order = goal_handle.request.order
        self.get_logger().info(

            f'Received goal: order={order}'#This comes from: int32 order
    )

        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()

        a, b = 0, 1
        sequence = []
        timeout_sec = 0.5
        for i in range(order):
            sequence.append(a)

        
            feedback.partial_sequence = sequence.copy()
            #.copy():To avoid: Reference issues Data being modified unexpectedly
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(f'Feedback: {sequence}')

            rclpy.spin_once(self, timeout_sec=timeout_sec)
            #This allows:ROS communication to process  Feedback to actually be sent
            #Without spinning:F eedback may never reach clientThink of it as:
            # Give ROS time to breathe.
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