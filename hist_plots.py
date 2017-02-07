import matplotlib.pylab as plt
from my_graph import set_plot

def hist(x, bins=20, ax=None,
         edgecolor='k', facecolor='b'):

    hist, be = np.histogram(x, bins=bins)
    with plt.style.context(('ggplot')):
        if ax is None:
            fig, ax = plt.subplots(figsize=(5,3))
            plt.subplots_adjust(bottom=.2, left=.2)
        plt.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0],lw=2)
        set_plot(ax)

if __name__=='__main__':

    import numpy as np
    hist(np.random.randn(100))
    plt.show()
