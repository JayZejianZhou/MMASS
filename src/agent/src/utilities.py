# 2020-12-14 the utility functions for Agent package. Created and maintained by Zejian Zhou

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

""" simply plot the states
    states -- list of ndarray, list length is the step number
"""


def simple_plot_states(states):
    this_state = np.stack(states).squeeze(2)  # squeeze to eliminate the extra dimension
    legend_list = []
    for i in range(this_state.shape[1]):
        temp, = plt.plot(this_state[:, i], label="state" + str(i))
        legend_list.append(temp)

    plt.legend(handles=legend_list, loc='upper right')
    plt.title("All states plot")
    plt.show()


"""the FPK PDF plotter from the FPK package
    this_agent -- the agent instance
    Pt -- the sequence of time evolution of the PDF
"""


def original_fpk_plotter(this_agent, Pt):
    global surf_fig
    ### animation
    nm = this_agent.nm
    fig = plt.figure(figsize=plt.figaspect(1 / 2))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    p0 = this_agent.pdf(*this_agent.solver.grid)

    surf_fig = ax1.plot_surface(*this_agent.solver.grid / nm, p0, cmap='viridis')

    ax1.set_zlim([0, np.max(Pt) / 5])
    ax1.autoscale(False)

    ax1.set(xlabel='x (nm)', ylabel='y (nm)', zlabel='normalized PDF')

    ax2 = fig.add_subplot(1, 2, 2)

    skip = 5
    idx = np.s_[::skip, ::skip]
    im = ax2.pcolormesh(*this_agent.solver.grid / nm, p0, vmax=np.max(Pt) / 5)
    current = this_agent.solver.probability_current(p0)
    arrows = ax2.quiver(this_agent.solver.grid[0][idx] / nm, this_agent.solver.grid[1][idx] / nm,
                        current[0][idx], current[1][idx], pivot='mid')

    xmax = 400
    ax2.set_xlim([-xmax, xmax])
    ax2.set_ylim([-xmax, xmax])

    anim = FuncAnimation(fig, original_anim_update,
                         frames=range(this_agent.Nsteps),
                         interval=30,
                         fargs=(ax1, this_agent, Pt, nm, idx, im, arrows))

    plt.tight_layout()
    # anim.save('im2.gif')

    plt.show()


def original_anim_update(i, ax1, this_agent, Pt, nm, idx, im, arrows):
    global surf_fig
    surf_fig.remove()
    surf_fig = ax1.plot_surface(*this_agent.solver.grid / nm, Pt[i], cmap='viridis')

    data = Pt[i, :-1, :-1]
    im.set_array(np.ravel(data))
    im.set_clim(vmax=np.max(data))

    current = this_agent.solver.probability_current(Pt[i])
    arrows.set_UVC(current[0][idx], current[1][idx])
    return [surf_fig, im, arrows]
