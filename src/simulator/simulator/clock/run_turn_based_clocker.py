import rclpy
# from .clock.clock import Timer
from clocks.srv import Clock
from rclpy.node import Node


class Timer(Node):
    """constructor"""

    def __init__(self):
        super().__init__('main_timer')
        self.srv = self.create_service(Clock, 'main_clock', self.main_clock_callback)
        self.current_time = 0

    def main_clock_callback(self, request, response):
        self.current_time += 1
        response.current_time = self.current_time
        self.get_logger().info('Incoming time request\nType: %s Time: %d' % (request.name, self.current_time))
        return response

def main():
    rclpy.init()
    minimal_service = Timer()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()