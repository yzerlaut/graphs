import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator, NullFormatter
from matplotlib.cm import viridis, copper
import matplotlib as mpl
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

# custom colors
Blue, Orange, Green, Red, Purple, Brown, Pink, Grey,\
    Kaki, Cyan = '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',\
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'


def figure(A0_ratio=[0.25, 0.14],
           wspace=1., hspace=1.,
           left=1., right=1.,
           bottom=1., top=1.,
           wspace0=0.4, hspace0=0.4,
           left0=0.32, right0=0.97,
           bottom0=0.32, top0=0.97,
           axes = (1,1),
           axes_extents=None,
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
    
    fig = plt.figure(figsize=(A0_format['width']*A0_ratio[0],
                              A0_format['height']*A0_ratio[1]))

    plt.subplots_adjust(wspace=wspace0*wspace,
                        hspace=hspace0*hspace,
                        left=left0*left,
                        right=right0*right,
                        bottom=bottom0*bottom,
                        top=top0*top)
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


###########################################################
###### a versatile line plot function
###########################################################

def plot(x=None, y=None, sy=None, color='k',
         X=None, Y=None, sY=None, COLORS=None, colormap=viridis,
         ax=None,
         lw=2, alpha_std=0.3, ms=3,
         xlabel='', ylabel='occurence',
         LABELS=None,
         figure_args={},
         axes_args={},
         legend_args=None):

    # getting or creating the axis
    if ax is None:
        fig, AX = figure(**figure_args)
        ax = AX[0][0]
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
                                   alpha_std=alpha_std, lw=lw)
    else:
        line_plots.single_curve(ax, x, y, sy, color,
                                alpha_std=alpha_std, lw=lw)

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
            xlabel='', ylabel='occurence',
            LABELS=None,
            figure_args={},
            axes_args={},
            legend_args=None):

    # getting or creating the axis
    if ax is None:
        fig, AX = figure(**figure_args)
        ax = AX[0][0]
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

    # if legend_args is not
    if legend_args is not None:
        ax.legend(**legend_args)
    
    set_plot(ax, **axes_args)
    
    return fig, ax


###########################################################
######  Histogram
###########################################################

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
    fig, AX = figure(axes_extents=[\
                                  [[3,2], [1,2] ],
                                   [[1,1], [2,1], [1,1] ] ],
                     left=.3, bottom=.4, hspace=1.4, wspace=1.2,
                     with_top_left_letter='A',\
                     A0_ratio=[.8, .35])

    
    plot(Y=[
        np.random.randn(20),
        np.random.randn(20),
        np.random.randn(20),
        np.random.randn(20)],
         sY=[
             np.ones(20),
             np.ones(20),
             np.random.randn(20),
             np.random.randn(20)],
         ax=AX[0][0],
         COLORS=[Red, Purple, Blue, Green],
         legend_args={'frameon':False,
                      'prop':{'size':'small'}})
    
    scatter(X=np.random.randn(4,5), Y=np.random.randn(4,5),
            sX=np.random.randn(4,5),sY=np.random.randn(4,5),
            ax=AX[1][0], color='r')
    
    plot(np.random.randn(20), sy=np.random.randn(20),
         ax=AX[1][1])
    scatter(np.random.randn(20), sy=np.random.randn(20),
            ax=AX[1][1])

    plot(np.sin(np.linspace(0,1)*6*np.pi), np.linspace(0,1),
         ax=AX[0][1], color=Purple)
    plot(np.cos(np.linspace(0,1)*6*np.pi), np.linspace(0,1),
         ax=AX[0][1], color=Green)
    
    hist(np.random.randn(200), ax=AX[1][2])
    
    save_on_desktop(fig, figname='fig.svg')
    show()
    # fig, _ = figure()
    # fig, _ = hist(np.random.randn(200),
    #               xlabel='some value')
    # save_on_desktop(fig, figname='2.svg')
    # show()

