import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class myclientadd(Node):
    def __init__(self):
        super().__init__('client_add')

        self.client = self.create_client(
            AddTwoInts,
            'add_two_int'
        )

        while not self.client.wait_for_service(timeout_sec= 1.0):
            self.get_logger().info('Waiting for service')

        self.request = AddTwoInts.Request()
        self.request.a = 5
        self.request.b = 6

        self.future = self.client.call_async(self.request)
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        response = future.result()
        self.get_logger().info(f'The sum is : {response.sum}')
        rclpy.shutdown()

def main(args = None):
    rclpy.init(args = args)
    node = myclientadd()
    rclpy.spin(node)

if __name__ == '__main__':
    main()