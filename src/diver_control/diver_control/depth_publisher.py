import rclpy
import math
from rclpy.node import Node 
from interfaces.msg import DepthSensor

class DepthPublisher(Node):
    def __init__(self, name):
        super().__init__(name)

        self.publisher = self.create_publisher(DepthSensor, f'{name}/depth_data', 10)

        #create timer for the sine function
        self.t0 = self.get_clock().now()

        self.timer = self.create_timer(0.2, callback=self.tick)

    def tick(self):
        t = (self.get_clock().now() - self.t0).nanoseconds / 1e9

        msg = DepthSensor()

        msg.depth_value = 5.0 + 2.0 * math.sin(t / 4.0)

        self.publisher.publish(msg)

        self.get_logger().info(f'depth : {msg.depth_value:.2f} m')

def main(args=None):

    rclpy.init(args=args)

    depth_publisher = DepthPublisher('pub_depth_node')

    rclpy.spin(depth_publisher)
    rclpy.shutdown()

if __name__ == "__main__":
    main()