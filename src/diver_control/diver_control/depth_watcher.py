import rclpy
from rclpy.node import Node 
from interfaces.msg import DepthSensor

class DepthWatcher(Node):
    def __init__(self, name):
        super().__init__(name)

        self.last = None 
        self.create_subscription(DepthSensor, 'pub_depth_node/depth_data', self.depth_mode, 10)

    def depth_mode(self, msg):
        depth = msg.depth_value 
        tolerance = 0.01

        if self.last == None:
            mode = 'starting'
        else:
            difference = self.last - depth 
            if difference > 0:
                mode = 'rising'
            elif difference < 0:
                mode = 'diving'
            elif abs(difference) <= tolerance:
                mode = 'holding'

        self.last = depth
        self.get_logger().info(f'depth : {depth:.2f} m -> state : {mode}')
        

def main(args=None):

    rclpy.init(args=args)

    depth_subscriber = DepthWatcher('sub_depth_node')

    rclpy.spin(depth_subscriber)
    rclpy.shutdown()

if __name__ == "__main__":
    main()