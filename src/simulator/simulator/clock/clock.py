""" the synchronize clock for all agents
    TODO: the update types can be
        turn-based: agent 1 -- agent 2 -- agent 3 ...
        synchronize: agent 1, agent 2, agent 3, ...
        asynchronoize: they happen withut a synchronized clock"""

from clocks.srv import Clock
from rclpy.node import Node

class Timer(Node):
    
    """constructor"""
    def __init__(self):
        super(Timer, self).__init__('main_timer')
        self.srv = self.create_service(Clock, 'main_clock', self)

    def main_clock_callback(self, request, response):
        kk=request.name
        print('time is seen')
        return 0

