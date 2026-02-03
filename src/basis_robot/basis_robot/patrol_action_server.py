# import time

# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionServer

# from patrol_robot.action import Patrol


# class PatrolActionServer(Node):

#     def __init__(self):
#         super().__init__('patrol_action_server')

#         self.action_server = ActionServer(
#             self,
#             Patrol,
#             'patrol',
#             self.execute_callback
#         )

#         for i in range(3):
#             self.get_logger().info('Patrol Action Server is up and running...')
#             time.sleep(1)


#     def execute_callback(self, goal_handle):
#         self.get_logger().info(f'Received patrol request with {goal_handle.request.num_waypoints} waypoints')

#         feedback = Patrol.Feedback()
#         result = Patrol.Result()

#         # Loop through each waypoint
#         for i in range(1, goal_handle.request.num_waypoints + 1):

#             # Check for cancel request
#             if goal_handle.is_cancel_requested:
#                 goal_handle.canceled()
#                 result.success = False
#                 self.get_logger().info('Patrol action canceled')
#                 return result

#             # Simulate movement to waypoint
#             time.sleep(1)

#             # Send feedback
#             feedback.current_waypoint = i
#             goal_handle.publish_feedback(feedback)

#             self.get_logger().info(
#                 f'Patrolling waypoint {i}'
#             )

#         # If all waypoints completed
#         goal_handle.succeed()
#         result.success = True
#         self.get_logger().info('Patrol completed successfully')
#         return result


# def main(args=None):
#     rclpy.init(args=args)

#     node = PatrolActionServer()
#     rclpy.spin(node)

#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()




import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from patrol_robot.action import Patrol

class PatrolActionServer(Node):
    def __init__(self):
        super().__init__('patrol_action_server')

        self._action_server = ActionServer(
            self,
            Patrol,
            'patrol',
            self.execute_callback
        )

        self.state = 'IDLE🤖'
        self.current_waypoint = 0
        self.total_waypoints = 0
        goal_handle = None

        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('Patrol Action Server is up and running...')

    def execute_callback(self, goal_handle):
        goal = goal_handle.request.num_waypoints
        self.get_logger().info(f'Received patrol request with {goal} waypoints')

        # self.state = 'PATROLLING🚶‍♂️'
        self.goal_handle = goal_handle
        self.total_waypoints = goal
        self.current_waypoint = 0

        self.state = 'PATROLLING🚶‍♂️'

        while self.state != 'DONE':
            rclpy.spin_once(self)

        
        #result 
