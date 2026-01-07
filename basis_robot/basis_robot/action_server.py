
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

        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()
        #Feedback & Result must be created manually
        count = 0
        target = goal_handle.request.order

        while count < target:
            count+= 1
            feedback.sequence = [count]
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(f'Counting: {count}')
            rclpy.sleep(1)
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('goal canceled')
                return Fibonacci.Result()
        goal_handle.succeed()
        result.sequence = [count]
        return result
    
def main(args = None):
    rclpy.init(args=args)
    node = ActionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
