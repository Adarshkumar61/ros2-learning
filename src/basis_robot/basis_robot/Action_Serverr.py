import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci

class ActionServerNode(Node):
    def __init__(self):
        super().__init__('action_server_node')

        self.action_server = ActionServer(
            self,
            Fibonacci,          # action type (MUST be here)
            'count_until',      # action name
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Goal received')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = []

        for i in range(1, goal_handle.request.order + 1):
            feedback_msg.sequence.append(i)
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')
            goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    node = ActionServerNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()