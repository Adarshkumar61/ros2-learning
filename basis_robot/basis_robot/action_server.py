
import rclpy 
from rclpy.node import Node
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci

class actionserver(Node):
    def __init__(self):
        super().__init__('action_server')
        #Node name must be unique
        self.action_server = ActionServer(
            self,
            Fibonacci,
                    'count_until',
                        self.execute_callback# When a goal arrives → run this function”    
                            )
        
    def execute_callback(self, goal_handle):
        # Action callback ALWAYS receives goal_handle
        #Called automatically when client sends goal:
# goal_handle contains:
# Goal data
# Cancel info
# Feedback publisher
        self.get_logger().info('goal started..')

