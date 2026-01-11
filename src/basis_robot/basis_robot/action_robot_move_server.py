import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci

class RobotMoveAS(Node):
    def __init__(self):
        super().__init__('robot_move')
        self.get_logger().info('Action server started')

        self.action_server = ActionServer(
            self,
            Fibonacci,
            'robot_move',
            # self.execute_callback
        )

    def execute_callback(self, goal_handle):
        target = goal_handle.request.order
        distance = 0

        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()

        while distance < target:

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result.sequence = [distance]
                return result

            distance += 1
            feedback.sequence = [distance]
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(f'Robot moved to: {distance}m')
            time.sleep(1)

        
        goal_handle.succeed()
        self.get_logger().info('Target completed')

        result.sequence = [distance]
        return result

def main(args=None):
    rclpy.init(args=args)
    node = RobotMoveAS()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
