# 2020-12-14 main tester of the Agent.py package. Created and maintained by Zejian Zhou
from vanilla_agent.Agent import Agent
import numpy as np
from scipy import linalg
from vanilla_agent import utilities
from FPK_solver import gaussian_pdf

#TODO: python version ADP
#TODO: connect with the FPK solver


dt = 0.1 #delta t to discretize the dynamics in temporal space
fpk_dt = 1e-8 #delta t for FPK solver
""" single linear dynamics
    state -- single vector 
    action -- single vector
"""
def linear_dynamics(state, action):
    a, b = np.array([[-3, 2], [1, 1]]), [[0], [1]]
    return (np.dot(a, state) + b * action)

"""linear dynamics compatible with FPK solver
    x -- MxN matrix, see notibility note for details
    y -- MxN matrix, see notibility note for details
"""
def linear_dynamics_fpk(x, y):
    grid_len = x[:, 0].size
    com = np.array([x, y]) #make the current state
    #the mesh value of the augmented state vector, see notabilitty
    Fx = np.zeros((80, 80))
    Fy = np.zeros((80, 80))
    for i in range(grid_len):
        for j in range(grid_len):
            u_t = linear_actions(com[:,i,j]) # compute optimal control
            state_diff = linear_dynamics(state=com[:,i,j], action=u_t)
            #adjust by delta t, discretization
            Fx[i, j] = fpk_dt * state_diff[0][0]
            Fy[i, j] = fpk_dt * state_diff[1][0]
            pass
    return np.array([Fx, Fy])

""" use CARE to solve for suboptimal control for linear systems"""
def linear_actions(state):
    R = 3
    q = np.array([[1, 0], [0, 1]])
    a = np.array([[-3, 2], [1, 1]])
    b = np.array([[0], [1]])
    P = linalg.solve_continuous_are(a, b, q, R)
    k = 1 / R * np.dot(np.transpose(b), P)
    return np.dot(-k, state)


# generate a new vanilla_agent
i_agent = Agent(init_state=np.array([[1], [1]]),
                init_action=np.array([[2], [2]]),
                dt=dt,
                dynam=linear_dynamics)
### FPK vanilla_agent
nm = 1e-9
pdf = gaussian_pdf(center=(200 * nm, 200 * nm), width=30 * nm)
Pt=i_agent.solve_fpk(drift_force=linear_dynamics_fpk, pdf=pdf)
utilities.original_fpk_plotter(i_agent, Pt)

### one single vanilla_agent
# generate test action list
# steps = 200
# states = []
# for i in range(steps):
#     action = linear_actions(i_agent.state)
#     states.append(i_agent.move_steps(action=np.asarray(action), steps=1)[0])

#simply plot the states
# utilities.simple_plot_states(states)
pass
