import sys, os, platform
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep
# module that construct the plot settings
from graphs.draw_figure import figure
from graphs.adjust_plots import *

import numpy as np
from graphs.annotations import *
import graphs.line_plots as line_plots
import graphs.scatter_plots as scatter_plots
from graphs.hist_plots import hist
from graphs.inset import add_inset
from graphs.legend import *

# custom colors
from matplotlib.cm import viridis, viridis_r, copper, copper_r, cool, jet
Blue, Orange, Green, Red, Purple, Brown, Pink, Grey,\
    Kaki, Cyan = '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',\
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
Color_List = [Blue, Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan]

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
         lw=1, alpha_std=0.3, ms=0, m='', ls='-',
         xlabel='', ylabel='', bar_label='',
         label=None,
         LABELS=None,
         fig_args={},
         axes_args={},
         bar_legend_args=None,
         legend_args=None):

    """    
    return fig, ax
    """
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
                                   colormap=colormap,
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
        
    if 'xlabel' not in axes_args:
        axes_args['xlabel'] = xlabel
    if 'ylabel' not in axes_args:
        axes_args['ylabel'] = ylabel
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
    if platform.system()=='Windows':
        plt.show()
    else:
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
    for ax in AX:
        scatter(np.abs(np.exp(np.random.randn(100))), np.abs(np.exp(np.random.randn(100))), ax=ax)
        set_plot(ax, yscale='log', xscale='log')
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

