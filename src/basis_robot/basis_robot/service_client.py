import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')

        self.client = self.create_client(
            SetBool,
            'set_robot_state'
        )

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

    def send_request(self, state):
        request = SetBool.Request()
        request.data = state
        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)
    node = ServiceClient()

    future = node.send_request(True)
    rclpy.spin_until_future_complete(node, future)

    response = future.result()
    node.get_logger().info(
        f'Response: success={response.success}, message="{response.message}"'
    )

    rclpy.shutdown()


if __name__ == '__main__':
    main()
