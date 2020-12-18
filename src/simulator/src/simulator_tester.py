#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from Simulator import Simulator
import numpy as np
from scipy import linalg
from vanilla_agent import utilities
from FPK_solver import gaussian_pdf


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


def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        aNum=3
        init_states=[np.array([[1],[1]]),   np.array([[2],[2]]), np.array([[3],[3]])]
        this_simulator=Simulator(aNum=aNum,
                                 init_states=init_states,
                                 init_dynams=linear_dynamics_fpk)



    except rospy.ROSInterruptException:
        pass
