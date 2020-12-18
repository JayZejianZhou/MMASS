""" main simulator class"""
from vanilla_agent.RosAgent import Ros_agent
import rospy_tutorials.msg
import rospy

class Simulator (object):
    """constructor
    aNum -- vanilla_agent number
    init_states -- list of ndarrays
    init_actions -- list of ndarrays
    init_dynams -- list of function handlers
    """
    def __init__(self, aNum, init_states, init_dynams, init_actions=None):
        self.aNum = aNum
        self.agent_list = ['']*aNum
        #initialize ros_agent nodes
        for i in range(aNum):
            node_name='agent_' + str(i)
            self.agent_list[i] = Ros_agent(ros_node_name= node_name,
                                           init_state= init_states[i],
                                           init_action= None,
                                           dynam= init_dynams)
            #init nodes
            rospy.init_node(node_name, anonymous=False)


