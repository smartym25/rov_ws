import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from interfaces.action import Immersion

#printed feedback on client
class ImmersionActionClient(Node):
    def __init__(self, name):
        super().__init__(name)

        self.action_client = ActionClient(self, Immersion, 'immersion')

    def send_goal(self, target_depth):

        #conditions for goals
        if target_depth < 0.0:
            self.get_logger().error(f"Target {target_depth} not valid. Deleyed action.")
            return

        goal_msg = Immersion.Goal()
        goal_msg.target_depth = target_depth

        self.action_client.wait_for_server()

        future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.get_feedback_callback)

        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return 

        self.get_logger().info('Goal accepted')

        future_ = goal_handle.get_result_async()

        future_.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result

        self.get_logger().info('Result: {} m'.format(result.final_depth))

        rclpy.shutdown()

    def get_feedback_callback(self, feedback):
        self.get_logger().info('Feedback: {} m'.format(feedback.feedback.current_depth))

def main(args=None):
    rclpy.init(args=args)

    depth_target_action_client = ImmersionActionClient('depth_target_action_client_node')

    depth_target_action_client.send_goal(target_depth=5.0)

    rclpy.spin(depth_target_action_client)

if __name__=='__main__':
    main()