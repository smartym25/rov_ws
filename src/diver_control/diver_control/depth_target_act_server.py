import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from interfaces.action import Immersion

#build the package and update the CMake if the library interfaces isn't recognised
class ImmersionActionServer(Node):
    def __init__(self, name):
        super().__init__(name)

        self.declare_parameter('immersion_velocity', 0.5)
        self.declare_parameter('starting_point', 3.0)

        self.action_server = ActionServer(self, Immersion, 'immersion', self.execute_callback)

    def execute_callback(self, goal_handle):
        feedback = Immersion.Feedback()

        #devo sempre mettere .value per estrarre il valore dal parameter
        velocity = self.get_parameter('immersion_velocity').value

        feedback.current_depth = self.get_parameter('starting_point').value
        time_past = 0.0

        while feedback.current_depth < goal_handle.request.target_depth:
            feedback.current_depth += velocity

            goal_handle.publish_feedback(feedback)

            time_past += 1

            time.sleep(0.5)

        goal_handle.succeed()

        if feedback.current_depth == goal_handle.request.target_depth:

            result = Immersion.Result()

            result.operation_time = time_past 
            result.final_depth = feedback.current_depth 
            result.success = True 

            self.get_logger().info('Operation time: {} s'.format(result.operation_time))
            self.get_logger().info('Reached depth: {} m'.format(result.final_depth))
            self.get_logger().info('Goal reached: {}'.format(result.success))

            return result 
        else:
            self.get_logger().error('Current depth exceed the target')
            return 

#printed result on server
def main(args=None):
    rclpy.init(args=args)

    depth_target_action_server = ImmersionActionServer('depth_target_action_server_node')

    rclpy.spin(depth_target_action_server)

    rclpy.shutdown()

if __name__=='__main__':
    main()