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

