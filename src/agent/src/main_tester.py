# 2020-12-14 main tester of the Agent.py package. Created and maintained by Zejian Zhou
from Agent import Agent
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt


def linear_dynamics(state, action):
    a, b = np.array([[-3, 2], [1, 1]]), [[0], [1]]
    return (np.dot(a, state) + b * action)


def linear_actions(state):
    R = 3
    q = np.array([[1, 0], [0, 1]])
    a = np.array([[-3, 2], [1, 1]])
    b = np.array([[0], [1]])
    P = linalg.solve_continuous_are(a, b, q, R)
    k = 1 / R * np.dot(np.transpose(b), P)
    return np.dot(-k, state)


dt = 0.1
# generate a new agent
i_agent = Agent(init_state=np.array([[1], [1]]),
                init_action=np.array([[2], [2]]),
                dt=dt,
                dynam=linear_dynamics)

# generate test action list
steps = 200
states = []
for i in range(steps):
    action = linear_actions(i_agent.state)
    states.append(i_agent.move_steps(action=np.asarray(action), steps=1)[0])
print(i_agent.state)
this_state = np.stack(states)
plt.plot(this_state[:, 0, 0])
plt.plot(this_state[:, 1, 0])
plt.show()
