import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator, NullFormatter
from matplotlib.cm import viridis, copper
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep
from graphs.scaling import *
from graphs.adjust_plots import *
from graphs.annotations import *
import graphs.line_plots as line_plots
import graphs.scatter_plots as scatter_plots
from graphs.inset import add_inset
from graphs.legend import *

# custom colors
Blue, Orange, Green, Red, Purple, Brown, Pink, Grey,\
    Kaki, Cyan = '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',\
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'


def figure(axes = (1,1),
           axes_extents=None,
           figsize=(1.,1.),
           left=1., right=1.,
           bottom=1., top=1.,
           wspace=1., hspace=1.,
           with_top_left_letter='',
           fontsize=FONTSIZE, fontweight='bold'):
    
    """
    scales figures with respect to the A0 format !

    the wspace, hspace, ... values are factor that modulates the wspace0, hspace0
    -> then use >1 to make bigger, and <1 to make smaller...

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

    # FIGURE size
    figsize = (A0_format['width']*Single_Plot_Size[0]*x_plots*figsize[0],
               A0_format['height']*Single_Plot_Size[1]*y_plots*figsize[1])
    fig = plt.figure(figsize=figsize)

    
    # Subplots placements adjustements
    plt.subplots_adjust(left=left*0.55/figsize[0], # 0.5cm by default
                        bottom=bottom*0.5/figsize[1],# 0.5cm by default
                        top=1.-top*0.1/figsize[0], # 0.1cm by default
                        right=1.-right*0.1/figsize[1],# 0.1cm by default
                        wspace=wspace*0.5/figsize[0]*x_plots, # 0.5cm by default
                        hspace=hspace*0.5/figsize[1]*y_plots) # 0.5cm by default

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
        
    plt.annotate(with_top_left_letter, (0.01,.99),
                 xycoords='figure fraction',
                 fontsize=fontsize+1, fontweight='bold')

    if (x_plots==1) and (y_plots==1):        
        return fig, AX[0][0]
    elif (x_plots==1):
        return fig, [AX[i][0] for i in range(len(AX))]
    elif (y_plots==1):
        return fig, AX[0]
    else:
        return fig, AX

def save_on_desktop(fig, figname='temp.svg'):
    fig.savefig(desktop+figname)

###########################################################
###### a versatile line plot function
###########################################################

def plot(x=None, y=None, sy=None,
         color='k',
         X=None, Y=None, sY=None,
         COLORS=None, colormap=viridis,
         ax=None,
         lw=2, alpha_std=0.3, ms=0, m='', ls='-',
         xlabel='', ylabel='occurence',bar_label='',
         label=None,
         LABELS=None,
         fig_args={},
         axes_args={},
         bar_legend_args=None,
         legend_args=None):

    # getting or creating the axis
    if ax is None:
        fig, ax = figure(**fig_args)
    else:
        fig = plt.gcf()

    if (y is None) and (Y is None):
        y = x
        x = np.arange(len(y))

    if (Y is not None):
        if (X is None) and (x is not None):
            X = [x for i in range(len(Y))]
        elif (X is None):
            X = [np.arange(len(y)) for y in Y]

        line_plots.multiple_curves(ax, X, Y, sY, COLORS, LABELS,
                                   alpha_std=alpha_std,
                                   lw=lw, ls=ls, m=m, ms=ms)
    else:
        line_plots.single_curve(ax, x, y, sy,
                                color=color,
                                alpha_std=alpha_std,
                                lw=lw, label=label, ls=ls, m=m, ms=ms)

    if bar_legend_args is not None:
        cb = add_inset(ax, **bar_legend_args)
        build_bar_legend(np.arange(len(LABELS)+1),
                         cb,
                         colormap,
                         label=bar_label,
                         ticks_labels=LABELS)
        
    # if legend_args is not
    if legend_args is not None:
        ax.legend(**legend_args)

    set_plot(ax, **axes_args)

    return fig, ax

###########################################################
###### a versatile scatter plot function
###########################################################

def scatter(x=None, y=None, sx=None, sy=None,
            color='k',
            X=None, Y=None, sX=None, sY=None,
            COLORS=None, colormap=viridis,
            ax=None,
            lw=0, elw=1, ms=3, marker='o',
            xlabel='', ylabel='occurence',bar_label='',
            LABELS=None,
            fig_args={},
            axes_args={},
            bar_legend_args=None,
            legend_args=None):

    # getting or creating the axis
    if ax is None:
        fig, ax = figure(**fig_args)
    else:
        fig = plt.gcf()

    if (y is None) and (Y is None):
        y = x
        x = np.arange(len(y))

    if (Y is not None):
        if (X is None) and (x is not None):
            X = [x for i in range(len(Y))]
        elif (X is None):
            X = [np.arange(len(y)) for y in Y]
        scatter_plots.multiple_curves(ax, X, Y, sX, sY, COLORS, LABELS,\
                                      marker=marker, lw=lw, ms=ms,
                                      elw=elw)
    else:
        scatter_plots.single_curve(ax, x, y, sx, sy,
                                   color=color,
                                   marker=marker, lw=lw, ms=ms,
                                   elw=elw)

    if bar_legend_args is not None:
        cb = add_inset(ax, **bar_legend_args)
        build_bar_legend(np.arange(len(Y)+1),
                         cb,
                         colormap,
                         label=bar_label,
                         ticks_labels=LABELS)
        
    # if legend_args is not
    if legend_args is not None:
        ax.legend(**legend_args)
    
    set_plot(ax, **axes_args)
    
    return fig, ax


###########################################################
######  Histogram
###########################################################

def hist(x, bins=20, ax=None,
         orientation='horizontal',
         edgecolor='k', facecolor='lightgray',
         lw=0.3,
         xlabel='', ylabel='occurence',
         normed=True,
         fig_args={}, axes_args={}):
    
    hist, be = np.histogram(x, bins=bins, normed=normed)
    
    if ax is None:
        fig, AX = figure(**fig_args)
        ax = AX[0][0]
    else:
        fig = plt.gcf()

    if orientation=='vertical':
        ax.barh(.5*(be[1:]+be[:-1]), hist, height=be[1]-be[0], 
                edgecolor=edgecolor, facecolor=facecolor, lw=lw)
    elif orientation=='horizontal':
        ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], 
                edgecolor=edgecolor, facecolor=facecolor, lw=lw)
        
    set_plot(ax, **axes_args)
    
    return fig, ax


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


def show(module=None):
    plt.show(block=False)
    input('Hit Enter To Close')
    plt.close()


def annotate(s, stuff, x=0.5, y=0.8,
             fontsize=FONTSIZE,
             fontweight='normal',
             rotation=0,
             color='k'):
    if type(stuff)==mpl.figure.Figure:
        plt.annotate(s, (x,y), xycoords='figure fraction',
                     fontweight=fontweight, fontsize=fontsize,
                     color=color, rotation=rotation)
    else:
        stuff.annotate(s, (x,y), xycoords='axes fraction',
                       fontweight=fontweight, fontsize=fontsize,
                       color=color, rotation=rotation)


if __name__=='__main__':

    # fig, AX = figure(axes_extents=[\
    #                               [[3,2], [1,2] ],
    #                                [[1,1], [1,1], [2,1] ] ],
    #                  left=.3, bottom=.4, hspace=1.4, wspace=1.2,
    #                  figsize=[.8, .35])
    
    # plot(Y=[
    #     np.random.randn(20),
    #     np.random.randn(20),
    #     np.random.randn(20),
    #     np.random.randn(20)],
    #      sY=[
    #          np.ones(20),
    #          np.ones(20),
    #          np.random.randn(20),
    #          np.random.randn(20)],
    #      ax=AX[0][0],
    #      COLORS=[Red, Purple, Blue, Green],
    #      legend_args={'frameon':False},
    #      axes_args={'spines':['left']})
    
    # scatter(X=np.random.randn(4,5), Y=np.random.randn(4,5),
    #         sX=np.random.randn(4,5),sY=np.random.randn(4,5),
    #         ax=AX[1][0],
    #         bar_legend_args={},
    #         bar_label='condition')
    
    # plot(np.random.randn(20), sy=np.random.randn(20),
    #      ax=AX[1][2])
    # scatter(np.random.randn(20), sy=np.random.randn(20),
    #         ax=AX[1][2])
    # plot(np.random.randn(20), sy=np.random.randn(20),
    #         ax=AX[1][2], color=Red)
    # scatter(np.random.randn(20), sy=np.random.randn(20),
    #         ax=AX[1][2], color=Red)
    # plot(np.sin(np.linspace(0,1,30)*3*np.pi)*2,
    #      ax=AX[1][2], color=Purple)
    # plot(np.cos(np.linspace(0,1,30)*3*np.pi)*2,
    #      ax=AX[1][2], color=Green)
    
    # hist(np.random.randn(200), ax=AX[0][1],\
    #      orientation='vertical',
    #      axes_args={'ylim':AX[0][0].get_ylim(), 'spines':['left']})
    
    # AX[1][1].axis('off')
    # fig.savefig('fig.png', dpi=200)
    # save_on_desktop(fig, figname='fig.png')

    # fig2, AX = figure(axes=(2,1),
    #                   left=.4, bottom=.4, hspace=1.4, wspace=1.2,
    #                   figsize=[.45, .3])
    # import itertools
    # for i in range(2):
    #     plot(np.random.randn(20), sy=np.random.randn(20),
    #          ax=AX[i])
    # # fig2.savefig('fig2.png', dpi=200)
    # fig1, AX = figure(axes_extents=[\
    #                                [[3,1], [1,1] ],
    #                                [[1,1], [2,1], [1,1] ] ] )
    fig2, AX = figure(axes=(2,1))
    for ax in AX: set_plot(ax)
    # show()
    # print('should be 1, 1')
    # fig2, AX = figure(axes=(1,1))
    # print('should be 2, 1')
    # fig2, AX = figure(axes=(2,1))
    # print('should be 1, 2')
    # fig2, AX = figure(axes=(1,2))
    # print('should be 3, 2')
    # fig2, AX = figure(axes=(3,2))
    # # show()

    # fig, _ = figure()
    # fig, _ = plot(Y=np.random.randn(4, 10), sY=np.random.randn(4, 10),
    #               axes_args={'spines':['left', 'bottom'], 'xlabel':'my-x value', 'ylabel':'my-y value'})
    # save_on_desktop(fig, figname='2.svg')
    show()

