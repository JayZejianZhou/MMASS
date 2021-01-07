import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

# control publisher class, the topic_name parameter is the name of the topic
class ControllerPublisher(Node):
    def __init__(self, left_topic_name='default_topic', right_topic_name='default right'):
        super(ControllerPublisher, self).__init__('control_publisher')
        self.publisher_left_ = self.create_publisher(Float32, left_topic_name, 10) #10: queue size, QOS pofile
        self.publisher_right_ = self.create_publisher(Float32, right_topic_name, 10)  # 10: queue size, QOS pofile
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i=0

    def timer_callback(self):
        msg = Float32()
        msg.data = 40.0
        self.publisher_left_.publish(msg)
        self.publisher_right_.publish(msg)
        self.get_logger().info('Publishing: "%f"' % msg.data)
        self.i+=1

def main(args=None):
    rclpy.init(args=args)
    left_wheel_topic_name = '/LeftMotorHandle'
    right_wheel_topic_name = '/RightMotorHandle'
    control_publisher = ControllerPublisher(left_topic_name=left_wheel_topic_name,
                                               right_topic_name=right_wheel_topic_name)

    rclpy.spin(control_publisher)
    control_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
