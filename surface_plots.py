import numpy as np
from matplotlib import cm

def twoD_plot(ax, x, y, z, alpha=1., cmap=cm.viridis):
    """
    surface plots for x, y and z 1 dimensional data
    """
    x, y = np.array(x), np.array(y)
    z1 = np.array(z).reshape(len(np.unique(y)), len(np.unique(x)))
    return ax.imshow(z1, interpolation='none',
                     extent = (x.min(), x.max(), y.min(), y.max()),
                     alpha=1., cmap=cmap, origin='lower')
    

if __name__=='__main__':
    from my_graph import *
    x, y = np.meshgrid(np.arange(10), np.arange(20))
    z = x*y
    x, y, z = np.array(x).flatten(), np.array(y).flatten(), np.array(z).flatten()
    ax = surface_plot(plt.gca(), x, y, z)
    plt.gca().set_xticks(np.arange(6)*2)
    plt.colorbar(ax)
    show()
