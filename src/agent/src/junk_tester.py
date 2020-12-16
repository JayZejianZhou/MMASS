# load matlab engine
# import matlab.engine
# eng = matlab.engine.start_matlab()

#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from fplanck import fokker_planck, boundary, gaussian_pdf, harmonic_potential
from mpl_toolkits.mplot3d import Axes3D

from scipy.io import loadmat

# load the parameters from the matlab file
# annots = loadmat('params/sim_param.mat')
# nm = annots['nm'][0][0]
# viscosity = annots['viscosity'][0][0]
# radius = annots['radius'][0][0]
# drag = annots['drag'][0][0] #drag force
# init_pos = annots['init_pos'][0] #the mean of the initial distribution
# var = annots['var'][0][0] # the variance of the initial distribution

nm = 1e-9
viscosity = 8e-4
radius = 50*nm
drag = 1*np.pi*viscosity*radius

#define the force function
def F(x, y):
    # rad = np.sqrt(x**2 + y**2)
    # phi = np.arctan2(y, x)
    # L = 200*nm
    #
    # Fphi = 1e-12*rad/L*np.exp(-rad/L)
    # Frad = 1e-12*(1 - rad/L)*np.exp(-rad/L)
    #
    # Fx = -np.sin(phi)*Fphi + np.cos(phi)*Frad
    # Fy = np.cos(phi)*Fphi + np.sin(phi)*Frad

    A=np.array([[-3,2],[1,1]])
    B=np.array([0,1]).reshape((-1,1)).reshape((-1,1))
    P=np.array([[0.5895,1.8216],[1.8216,8.8188]])
    K=np.array([0.607191574962028,2.939613268974371]).reshape((1,-1)) #横向量

    Fx = np.zeros((80, 80))
    Fy = np.zeros((80, 80))

    grid_len=x[:,0].size
    com = np.array([x,y])
    for i in range(grid_len):
        for j in range(grid_len):
            u_t=-K@com[:,i,j].reshape((-1,1))
            u=u_t[0][0]
            this_f=A@com[:,i,j].reshape((-1,1))+B*u
            Fx[i,j]=this_f[0][0]
            Fy[i,j]=this_f[1][0]
            pass

    # 不要太大，这个放在1e-13是比较好的选择
    Fx_r = 1e-8*Fx
    Fy_r = 1e-8*Fy

    # Fx_r=-1e-13*np.ones((80,80))
    # Fy_r = -1e-13 * np.ones((80, 80))
    return np.array([Fx_r, Fy_r])

# generate the FPK equation
sim = fokker_planck(temperature=10, drag=drag, extent=[800 * nm, 800 * nm],
                    resolution=10 * nm, boundary=boundary.reflecting, force=F)

### time-evolved solution
# pdf = gaussian_pdf(center=(init_pos[0] * nm, init_pos[1] * nm), width=var * nm)
pdf = gaussian_pdf(center=(200 * nm, 200 * nm), width=30 * nm)

p0 = pdf(*sim.grid)

Nsteps = 500
time, Pt = sim.propagate_interval(pdf, 20e-3, Nsteps=Nsteps)

### animation
fig = plt.figure(figsize=plt.figaspect(1/2))
ax1 = fig.add_subplot(1,2,1, projection='3d')

surf = ax1.plot_surface(*sim.grid/nm, p0, cmap='viridis')

ax1.set_zlim([0,np.max(Pt)/5])
ax1.autoscale(False)

ax1.set(xlabel='x (nm)', ylabel='y (nm)', zlabel='normalized PDF')

ax2 = fig.add_subplot(1,2,2)

skip = 5
idx = np.s_[::skip, ::skip]
im = ax2.pcolormesh(*sim.grid/nm, p0, vmax=np.max(Pt)/5)
current = sim.probability_current(p0)
arrows = ax2.quiver(sim.grid[0][idx]/nm, sim.grid[1][idx]/nm,
        current[0][idx], current[1][idx], pivot='mid')

xmax = 400
ax2.set_xlim([-xmax, xmax])
ax2.set_ylim([-xmax, xmax])

def update(i):
    global surf
    surf.remove()
    surf = ax1.plot_surface(*sim.grid/nm, Pt[i], cmap='viridis')

    data = Pt[i, :-1,:-1]
    im.set_array(np.ravel(data))
    im.set_clim(vmax=np.max(data))

    current = sim.probability_current(Pt[i])
    arrows.set_UVC(current[0][idx], current[1][idx])
    return [surf, im, arrows]

anim = FuncAnimation(fig, update, frames=range(Nsteps), interval=30)
plt.tight_layout()
# anim.save('im2.gif')

plt.show()
