import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.my_graph import *
import matplotlib.pylab as plt
import numpy as np


def hist(x, bins=20, ax=None,
         edgecolor='k', facecolor='lightgray',
         lw=0.3,
         xlabel='', ylabel='occurence',
         normed=True,
         figure_args={}):
    
    hist, be = np.histogram(x, bins=bins, normed=normed)
    
    if ax is None:
        fig, AX = figure(**figure_args)
    fig, ax = plt.gcf(), plt.gca()
        
    ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], 
           edgecolor=edgecolor, facecolor=facecolor, lw=lw)

    set_plot(ax, xlabel=xlabel, ylabel=ylabel)
    
    return fig, ax


# def gghist(x, bins=20, ax=None, label=''):

#     hist, be = np.histogram(x, bins=bins)
    
#     with plt.style.context(('ggplot')):
#         if ax is None:
#             fig, ax = plt.subplots(figsize=(4,3))
#             plt.subplots_adjust(bottom=.2, left=.2)
#         ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], label=label)
        
#     return ax

def multiple_gghists(X, bins=20, ax=None, LABELS=None):

    if LABELS is None:
        LABELS = ['' for i in range(len(X))]
        
    ax = gghist(X[0], bins=bins, ax=ax, label=LABELS[0])
    for x, label in zip(X[1:], LABELS[1:]):
        hist, be = np.histogram(x, bins=bins)
        ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], label=label)
    return ax

if __name__=='__main__':

    # import numpy as np
    # ax = multiple_gghists([np.random.randn(100), np.random.randn(100)],\
    #                  LABELS=['Data 1', 'Data 2'])
    # ax.legend()
    # ax = multiple_hists([np.random.randn(100), np.random.randn(100)],\
    #                     LABELS=['Data 1', 'Data 2'])
    fig, ax = hist([np.random.randn(100)], xlabel='some value')
    save_on_desktop(fig)
    show()

