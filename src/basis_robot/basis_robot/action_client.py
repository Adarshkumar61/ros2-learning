import rclpy 
from rclpy.node import Node 
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci

class actionclient(Node):
    def __init__(self):
        super().__init__('action_client')

        self.action_client = ActionClient(
            self,
            Fibonacci,
            'count_until',
        )

        self.action_client.wait_for_server()

        goal = Fibonacci.Goal()
        goal.order = 10

        self.action_client.send_goal_async(
            goal,
            feedback_callback= self.feedback_callback,

        ).add_done_callback(self.goal_response_callback)
#   Add_done_callbac: Add a callback to be executed when the task is done.
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('goal rejected')
            return
        self.get_logger().info('goal accepted')

        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback.sequence
        self.get_logger().info(f'Received feedback: {feedback}')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

def main(args = None):
    rclpy.init(args=args)
    node = actionclient()
    rclpy.spin(node)

if __name__ == '__main__':
    main() 

# I am a node
# I want an action
# I send a goal
# While running:
#     receive feedback
# When done:
#     receive result
