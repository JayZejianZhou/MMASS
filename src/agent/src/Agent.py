# 2020-12-14 Agent.py package main file, created and maintained by Zejian Zhou
import utilities

class Agent(object):
    """ constructor
     init_state -- the initial states
     init_action -- the initial action
     dynam -- the system dynamics as a function handler
     dt -- the simulation segment duration"""

    def __init__(self, init_state, init_action, dt=0.01, dynam = None):
        self.state = init_state
        self.action = init_action
        self.dt = dt
        if dynam == None:
            self.dynam = self.__basic_dynam
        else:
            self.dynam = dynam


    """ basic linear dynamics
         action -- action"""
    def __basic_dynam(self, state, action):
        return state+action

    # TODO: set the input as the function handler
    # TODO: can input the continuous dynamics
    def __dynamics(self, action):
        self.state = self.dt * self.dynam(state=self.state, action=action) #update the state

    """ call this function to let the agent run for one step
     action -- the control input list
     steps -- the step number """

    def move_steps(self, action, steps):
        for i in range(steps):
            self.__dynamics(action[i])
