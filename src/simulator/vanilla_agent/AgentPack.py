""" the class for pack of agents"""

from .Agent import Agent

class AgentTeam (object):
    """constructor
        init_states -- list of ndarrays
        aNum -- the number of agents
        """

    def __init__(self, init_states, dt=0.01, aNum=2, dynam=None):
        self.agents=['']*aNum
        for i in range(aNum):
            self.agents[i] = Agent(init_state=init_states[i],
                                   init_action=None,
                                   dt=0.01,
                                   dynam = dynam)

