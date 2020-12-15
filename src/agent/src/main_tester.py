# 2020-12-14 main tester of the Agent.py package. Created and maintained by Zejian Zhou
from Agent import Agent
import numpy as np
from scipy import linalg

def linear_dynamics (state, action):
    a,b=np.array([[-3,2],[1,1]]), [[0],[1]]
    return (a*state + b*action)

def linear_actions (state):
    R = 3
    q = np.array([[1,  0], [0, 1]])
    a = np.array([[-3, 2], [1, 1]])
    b= np.array([[0], [1]])
    P = linalg.solve_continuous_are (a, b, q, R)
    k= 1/R * np.transpose(b)* P
    return -k*state


dt=0.01;
# generate a new agent
i_agent = Agent(init_state = 100, init_action = 0, dt=dt, dynam = linear_dynamics)

#generate test action list
steps = 200;
for i in range(steps):
    action = linear_actions(i_agent.state)
    i_agent.move_steps(action= np.asarray(action), steps=1)
print(i_agent.state)