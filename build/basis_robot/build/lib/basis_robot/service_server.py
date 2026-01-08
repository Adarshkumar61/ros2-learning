import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class erviceserver(Node):
    def __init__(self):
        super().__init__('serviceserver')

        self.service = self.create_service(
            SetBool,
            'set_robot_state',
            self.service_callback
        )

        self.robot_enabled = False
        self.get_logger().info('Service server ready')
    
    def service_callback(self, request, response):
        if request.data:
            self.robot_enabled  = True
            response.success = True
            response.message = 'robot enabled'

        else:
            self.robot_enabled = False
            response.success = False
            response.message = 'robot disabled'
        
        self.get_logger().info(response.message)
        return response

def main(args = None):
    rclpy.init(args = args)
    node = erviceserver() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()