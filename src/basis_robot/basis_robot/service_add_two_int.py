import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class myserviceadd(Node):
    def __init__(self):
        super().__init__('service_add')

        self.service = self.create_service(
            AddTwoInts,
            'add_two_int',
            self.add_callback
        )
    
    def add_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'The sum of {request.a} and {request.b} is {response.sum}')

        return response
    

def main(args = None):
    rclpy.init(args = args)
    node = myserviceadd()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()