import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci

class RobotMoveAC(Node):
    def __init__(self):
        super().__init__('robot_move_client')
        
        self.action_client = ActionClient(
            self,
            Fibonacci,
            'robot_move'
        )

        self.get_logger().info('Action Client Node has been started')
        self.action_client.wait_for_server()
        
        goal = Fibonacci.Goal()
        goal.order = 3

        self.action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        ).add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        current = feedback_msg.feedback.sequence[-1]
        self.get_logger().info(
            f'Current Distance: {current} m'
        )

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        goal_handle.get_result_async().add_done_callback(
            self.result_callback
        )

    def result_callback(self, future):
        result = future.result().result
        final_distance = result.sequence[-1]

        self.get_logger().info(
            f'Finished at distance: {final_distance} m'
        )
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = RobotMoveAC()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
