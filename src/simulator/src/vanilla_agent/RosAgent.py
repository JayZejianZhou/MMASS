#! /usr/bin/env python
""" the vanilla_agent used in ros, heritage of the original Agent class"""
from vanilla_agent.Agent import Agent


class Ros_agent(Agent):

    """constructor
    ros_node_name -- string, the ros node associated with this vanilla_agent

    """
    def __init__(self, ros_node_name, init_state, init_action=None, dynam=None):
        super(Ros_agent,self).__init__(init_state=init_state, init_action=init_action, dynam=dynam)
        self.ros_node = ros_node_name




