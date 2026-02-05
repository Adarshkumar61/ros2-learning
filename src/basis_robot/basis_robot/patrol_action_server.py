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




# import rclpy
# import time
# from rclpy.node import Node
# from rclpy.action import ActionServer
# from patrol_robot.action import Patrol

# class PatrolActionServer(Node):
#     def __init__(self):
#         super().__init__('patrol_action_server')

#         self._action_server = ActionServer(
#             self,
#             Patrol,
#             'patrol',
#             self.execute_callback
#         )

#         self.state = 'IDLE🤖'
#         self.current_waypoint = 0
#         self.total_waypoints = 0
#         goal_handle = None

#         self.timer = self.create_timer(1.0, self.timer_callback)

#         self.get_logger().info('Patrol Action Server is up and running...')
# # execute_callback → accepts the goal and prepares the mission
#     def execute_callback(self, goal_handle):
#         goal = goal_handle.request.num_waypoints
#         self.get_logger().info(f'Received patrol request with {goal} waypoints')

#         self.state = 'PATROLLING 🚶‍♂️'
#         self.goal_handle = goal_handle
#         self.total_waypoints = goal
#         self.current_waypoint = 0

#         # self.state = 'PATROLLING 🚶‍♂️'

#         while self.state != 'DONE':
#             rclpy.spin_once(self)
# #  I will wait here… until my timer finishes the job
        
#         #result 
#         result = Patrol.Result()
#         result.success = True
#         goal_handle.succeed()
#         self.get_logger().info('Patrol completed successfully')
#         return result
#     # Timer (or loop) → actually performs the mission step-by-step
#     def timer_callback(self):

#         if self.state == "IDLE":
#             return

#         self.get_logger().info(f"[STATE] → {self.state}")

#         if self.state == "MOVING":

#             if self.goal_handle.is_cancel_requested:
#                 self.goal_handle.canceled()
#                 self.state = "IDLE"
#                 return

#             self.current_waypoint += 1

#             feedback = Patrol.Feedback()
#             feedback.current_waypoint = self.current_waypoint
#             self.goal_handle.publish_feedback(feedback)

#             self.get_logger().info(
#                 f"Reached waypoint {self.current_waypoint}"
#             )

#             self.state = "WAITING"

#         elif self.state == "WAITING":
#             self.get_logger().info("Pausing at waypoint...")
#             self.state = "CHECK_DONE"

#         elif self.state == "CHECK_DONE":

#             if self.current_waypoint >= self.total_waypoints:
#                 self.state = "DONE"
#             else:
#                 self.state = "MOVING"

#         elif self.state == "DONE":
#             pass

# def main(args = None):
#     rclpy.init(args= args)
#     node = PatrolActionServer()
#     rclpy.spin(node)
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()

# """
#              +--------+
#              |  IDLE  |
#              +--------+
#                  |
#                  v
#              +---------+
#              | MOVING  |
#              +---------+
#                  |
#                  v
#              +----------+
#              | WAITING  |
#              +----------+
#                  |
#                  v
#            +--------------+
#            | CHECK_DONE   |
#            +--------------+
#             |          |
#             |          |
#             v          v
#          DONE       MOVING

# """


import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from patrol_robot.action import Patrol


class PatrolActionServer(Node):
    def __init__(self):
        super().__init__('action_server_node')

        self.action_server = ActionServer(
            self,
            Patrol,
            'patrol',
            self.execute_callback
        )

        self.state = 'IDLE'
        self.current_waypoint = 0
        self.total_waypoints = 0
        self.goal_handle = None

    
        self.timer = self.create_timer(1.0, self.timer_callback)

    def execute_callback(self, goal_handle):
        goal = goal_handle.request.num_waypoints
        self.get_logger().info(f'Received goal with: {goal}')

        # Initialize mission
        self.state = 'MOVING'
        self.current_waypoint = 0
        self.total_waypoints = goal
        self.goal_handle = goal_handle

        # Wait until timer finishes the job
        while self.state != 'DONE':
            rclpy.spin_once(self)

        # Send result
        result = Patrol.Result()
        result.success = True
        goal_handle.succeed()
        self.get_logger().info('Goal completed successfully')

        self.state = 'IDLE'
        return result

    def timer_callback(self):
        if self.state == 'IDLE':
            return

        elif self.state == 'MOVING':
            # Check cancel
            if self.goal_handle.is_cancel_requested:
                self.goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                self.state = 'IDLE'
                return

            self.current_waypoint += 1

            feedback = Patrol.Feedback()
            feedback.current_waypoint = self.current_waypoint
            self.goal_handle.publish_feedback(feedback)

            self.get_logger().info(f'Reached waypoint {self.current_waypoint}')
            self.state = 'WAITING'

        elif self.state == 'WAITING':
            self.get_logger().info('Pausing at waypoint...')
            self.state = 'CHECK_DONE'

        elif self.state == 'CHECK_DONE':
            if self.current_waypoint >= self.total_waypoints:
                self.state = 'DONE'
            else:
                self.state = 'MOVING'

        elif self.state == 'DONE':
            pass


def main(args=None):
    rclpy.init(args=args)
    node = PatrolActionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

    
    
    