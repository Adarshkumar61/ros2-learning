import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
class ParamNode(Node):
    def __init__(self):
       super().__init__('param_example')
    
       #decleare param values:
       self.declare_parameter('robot_speed', 1.2)
       #creating param:
       self.time = self.create_timer(1.0, self.callback)
      #This tells ROS 2: Every 1 second → call self.callback()
      #Read initial value of parameter
       self.speed =  self.get_parameter('robot_speed').value

      #Register parameter callback
       self.add_on_set_parameters_callback(self.param_callback)
       #whenever someone tries to change any parameter of this node,
       #  call my function param_callback() BEFORE applying the change.”
    def callback(self):
        #Every 1 second ROS 2 executes:
         self.get_logger().info(f'Robot speed is: {self.speed}')

     #does: checks and updates parameter values    
    def param_callback(self, params):
        for param in params:
            if param.name == 'robot_speed':
                if param.value <= 0:
                    self.get_logger().info(f'Robot min speed cant go less than : {self.speed}')
                    return   SetParametersResult(successful = False)
                
                self.speed = param.value
                self.get_logger().info(f'Robot speed updated to : {self.speed}')
        return SetParametersResult(successful = True)
    
def main(args = None):
    rclpy.init(args = args)
    node = ParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


# to change parameter live :
# ros2 param set /param_example robot_speed 2.5

