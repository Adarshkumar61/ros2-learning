import rclpy
from rclpy.node import Node

class ParamNode(Node):
    def __init__(self):
       super().__init__('param_example')
    
       #decleare param values:
       self.declare_parameter('robot_speed', 1.2)

       #creating param:
       self.time = self.create_timer(1.0, self.callback)

    def callback(self):
        speed =  self.get_parameter('robot_speed').value
        self.get_logger().info(f'Robot speed is: {speed}')

def main(args = None):
    rclpy.init(args = args)
    node = ParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()