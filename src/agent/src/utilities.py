# 2020-12-14 the utility functions for Agent package. Created and maintained by Zejian Zhou

import matplotlib.pyplot as plt
import numpy as np

""" simply plot the states
    states -- list of ndarray, list length is the step number
"""
def simple_plot_states(states):
    this_state = np.stack(states).squeeze(2) #squeeze to eliminate the extra dimension
    legend_list = []
    for i in range(this_state.shape[1]):
        temp, =plt.plot(this_state[:, i], label = "state"+str(i))
        legend_list.append(temp)

    plt.legend(handles=legend_list, loc='upper right')
    plt.title("All states plot")
    plt.show()