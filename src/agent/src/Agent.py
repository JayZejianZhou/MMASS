# 2020-12-14 Agent.py package main file, created and maintained by Zejian Zhou

class Agent(object):
    """ constructor
     init_state -- the initial states
     init_action -- the initial action"""

    def __init__(self, init_state, init_action):
        self.state = init_state
        self.action = init_action

    """ the system dynamics of the agent, must be a discrete function handler
     action -- the control input"""

    # TODO: set the input as the function handler
    # TODO: can input the continuous dynamics
    def __dynamics(self, action):
        self.state = self.state + action  # system dynamic function

    """ call this function to let the agent run for one step
     action -- the control input list
     steps -- the step number """

    def move_steps(self, action, steps):
        for i in range(steps):
            self.__dynamics(action[i])
