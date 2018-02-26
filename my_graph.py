import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator, NullFormatter
from matplotlib.cm import viridis, copper
import matplotlib as mpl
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep
from graphs.scaling import FONTSIZE, A0_format
from graphs.adjust_plots import *
from graphs.annotations import *

# custom colors
Blue, Orange, Green, Red, Purple, Brown, Pink, Grey,\
    Kaki, Cyan = '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',\
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'


def figure(width_to_height=1.6,
           A0_ratio=0.18,
           wspace=0.4, hspace=0.4,
           left=0.3, right=0.97,
           bottom=0.3, top=0.97,
           axes = (1,1),
           axes_extents=None,
           with_top_left_letter='',
           fontsize=10, fontweight='bold'):
    """
    scales figures with respect to the A0 format !


    Subplots are build with this convention for the geometry:
    (X,Y)
    ------ X -------------->
    |                 |     |
    |      (3,1)      |(1,1)|
    |                 |     |
    |-------------------
    Y     |           |     |
    |(1,1)|   (2,1)   |(1,1)|
    |     |           |     |
    |------------------------     
    v

    TO PRODUCE THIS, RUN:
    figure(axes_extents=[\
                         [[3,1], [1,1] ],
                         [[1,1], [2,1], [1,1] ] ] )
    show()

    """

    if axes_extents is None:
        if (len(axes)==1) and (axes[0]==1):
            axes_extents = [1]
        elif (axes[1]==0):
            axes_extents = np.ones(axes[0])
        elif (axes[0]==0):
            axes_extents = np.ones(axes[1])
        else:
            axes_extents = [[[1,1] for j in range(axes[1])]\
                            for i in range(axes[0])]
    
    x_plots = np.sum([axes_extents[0][j][0] \
                      for j in range(len(axes_extents[0]))])
    y_plots = np.sum([axes_extents[i][0][1] \
                      for i in range(len(axes_extents))])
    
    print(x_plots, y_plots)
    fig = plt.figure(**scale_figure(width_to_height, A0_ratio,
                                            x_plots, y_plots))
    plt.subplots_adjust(**scale_graphs_boudaries(x_plots, y_plots))
    plt.annotate(with_top_left_letter, (0.01,.99),
                 xycoords='figure fraction',
                 fontsize=fontsize, fontweight='bold')

    AX = []
    j0_row = 0
    for j in range(len(axes_extents)):
        AX_line = []
        i0_line = 0
        for i in range(len(axes_extents[j])):
            AX_line.append(plt.subplot2grid(\
                                            (y_plots, x_plots),
                                            (j0_row, i0_line),\
                                            colspan=axes_extents[j][i][0],
                                            rowspan=axes_extents[j][i][1]))
            i0_line += axes_extents[j][i][0]
        j0_row += axes_extents[j][i][1]
        AX.append(AX_line)
        
    return fig, AX

def save_on_desktop(fig, figname='temp.svg'):
    fig.savefig(desktop+figname)
    
def add_errorbar(ax, x, y, sy, width=.25, color='k', facecolor='lightgray', lw=4):
    bar = ax.bar(x, y, width, edgecolor=color, yerr=sy,\
                 error_kw={'ecolor':color,'linewidth':lw}, capsize=10, lw=lw, facecolor=facecolor)
    return bar

def set_subplot_safe_for_labels(fig, FIGSIZE=None, FONTSIZE=16,
                                    hspace=0.1, vspace=0.1):
    if FIGSIZE is None:
        FIGSIZE = [fig.get_figwidth(), fig.get_figheight()]
    x0, y0 = .15*FONTSIZE/FIGSIZE[0], .15*FONTSIZE/FIGSIZE[0]
    fig.subplots_adjust(\
                bottom=x0, left=y0,\
                right=max([1.-0.02*FONTSIZE/FIGSIZE[0],x0*1.1]),
                top=max([1.-0.02*FONTSIZE/FIGSIZE[1],y0*1.1]),
                hspace=hspace)

def replace_axis_by_legend(ax, text, x0=0.1, y0=0.1, on_fig=False):
    ax.axis('off')
    if on_fig:
        ax.annotate(text, (x0, y0), xycoords='figure fraction')
    else:
        ax.annotate(text, (x0, y0), xycoords='axes fraction')

    
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)    


def build_bar_legend(X, ax, mymap, label='$\\nu$ (Hz)',\
                     bounds=None, ticks_labels=None,
                     orientation='vertical', scale='linear',\
                     color_discretization=None):
    """ X -> ticks """
    if color_discretization is None:
        color_discretization = len(X)
        
    # scale : 'linear' / 'log' / 'custom'
    if scale is 'linear':
        if bounds is None:
            bounds = [X[0]+(X[1]-X[0])/2., X[-1]+(X[1]-X[0])/2.]
        bounds = np.linspace(bounds[0], bounds[1], color_discretization)
    elif scale is 'log10':
        if bounds is None:
            bounds = [int(np.log(X[0])/np.log(10))-.1*int(np.log(X[0])/np.log(10)),\
                      int(np.log(X[-1])/np.log(10))+1+.1*int(np.log(X[-1])/np.log(10))]
        else:
            bounds = [np.log(bounds[0])/np.log(10), np.log(bounds[1])/np.log(10)]
        bounds = np.logspace(bounds[0], bounds[1], color_discretization)
    elif scale is 'custom':
        bounds = np.linspace(X[0]+(X[1]-X[0])/2., X[-1]+(X[1]-X[0])/2., color_discretization)
        
    norm = mpl.colors.BoundaryNorm(bounds, mymap.N)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=mymap, norm=norm,\
                                   orientation=orientation)
    cb.set_ticks(X)
    if ticks_labels is not None:
        cb.set_ticklabels(ticks_labels)
    cb.set_label(label)
    return cb

def get_linear_colormap(color1='blue', color2='red'):
    return mpl.colors.LinearSegmentedColormap.from_list(\
                        'mycolors',[color1, color2])

def show(module=None):
    plt.show(block=False)
    input('Hit Enter To Close')
    plt.close()
        

if __name__=='__main__':

    # import matplotlib.pylab as plt
    # plt.subplots()
    # add_errorbar(plt.gca(), [0], [1], [.2])
    # set_plot(plt.gca())
    # figure(axes_extents=[\
    #                      [[3,2], [1,2] ],
    #                      [[1,1], [2,1], [1,1] ] ] )
    fig, _ = figure(axes=(3,3))
    # save_on_desktop(fig, figname='1.svg')
    show()
    fig, _ = figure()
    # save_on_desktop(fig, figname='2.svg')
    show()

