import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult


class MyParamNode(Node):
    def __init__(self):
        super().__init__('myparamnode')

        # Declare parameters
        self.declare_parameter('robot_name', 'HEBA')
        self.declare_parameter('robot_speed', 1.0)

        # Read initial values
        self.name = self.get_parameter('robot_name').value
        self.speed = self.get_parameter('robot_speed').value

        # Create timer
        self.timer = self.create_timer(self.speed, self.timer_callback)

        # Register parameter callback
        self.add_on_set_parameters_callback(self.parameter_callback)

    def timer_callback(self):
        self.get_logger().info(f'{self.name} speed is {self.speed}')

    def parameter_callback(self, params):
        for param in params:

            if param.name == 'robot_speed':
                if param.value <= 0:
                    self.get_logger().error("robot_speed must be > 0")
                    return SetParametersResult(successful=False)

                # Update speed
                self.speed = param.value

                # Recreate timer with new period
                self.timer.cancel()
                self.timer = self.create_timer(self.speed, self.timer_callback)

                self.get_logger().info(
                    f'Updated robot_speed to {self.speed}'
                )

            elif param.name == 'robot_name':
                self.name = param.value
                self.get_logger().info(
                    f'Updated robot_name to {self.name}'
                )

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = MyParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
