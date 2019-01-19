import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.inset import add_inset
from graphs.scaling import FONTSIZE, A0_format
from graphs.adjust_plots import find_good_log_ticks, set_ticks_to_log10_axis
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt

def get_linear_colormap(color1='blue', color2='red'):
    return mpl.colors.LinearSegmentedColormap.from_list(\
                        'mycolors',[color1, color2])

def build_bar_legend(X, ax, mymap,
                     label='$\\nu$ (Hz)',\
                     bounds=None,
                     ticks_labels=None,
                     no_ticks=False,
                     orientation='vertical',
                     labelpad=1.,
                     alpha=1.,
                     scale='linear',\
                     color_discretization=None):
    
    """ X -> ticks """
    if color_discretization is None:
        color_discretization = len(X)

    # scale : 'linear' / 'log' / 'custom'
    if scale is 'linear':
        if bounds is None:
            try:
                bounds = [X[0]+(X[1]-X[0])/2., X[-1]+(X[1]-X[0])/2.]
            except IndexError:
                bounds = [X[0], X[0]+1]
                
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
                                   orientation=orientation, alpha=alpha)
    if no_ticks:
        cb.set_ticks([])
    else:
        cb.set_ticks(X)
        if ticks_labels is not None:
            cb.set_ticklabels(ticks_labels)
        
    cb.set_label(label, labelpad=labelpad)
    return cb

def build_bar_legend_continuous(ax, mymap,
                                label='$\\nu$ (Hz)',\
                                bounds=None,
                                ticks=None,
                                ticks_labels=None,
                                orientation='vertical',
                                labelpad=1.,
                                alpha=1.,
                                scale='linear'):

    cb = mpl.colorbar.ColorbarBase(ax, cmap=mymap, orientation=orientation, alpha=alpha)
    
    if (bounds is None):
        cb.set_ticks([])
    else:
        if scale=='log':
            if bounds[0]<=0.:
                print('need to set a positive lower bound for the data')
                print('set to 0.01')
                bounds[0] = 0.01
            if orientation=='vertical':
                set_ticks_to_log10_axis(cb.ax.yaxis, bounds, normed_to_unit=True)
                if ticks_labels is not None:
                    cb.ax.yaxis.set_ticklabels(ticks_labels)
            elif orientation=='horizontal':
                set_ticks_to_log10_axis(cb.ax.xaxis, bounds, normed_to_unit=True)
                if ticks_labels is not None:
                    cb.ax.xaxis.set_ticklabels(ticks_labels)
        else:
            if ticks is None:
                ticks = np.linspace(bounds[0]+.1*(bounds[1]-bounds[0]), bounds[1]-.1*(bounds[1]-bounds[0]), 3)
            if ticks_labels is None:
                ticks_labels = ['%.1f' % t for t in ticks]
            cb.set_ticks((np.array(ticks)-bounds[0])/(bounds[1]-bounds[0]))
            cb.set_ticklabels(ticks_labels)
        
    cb.set_label(label, labelpad=labelpad)
    return cb

def bar_legend(X, ax,
               inset_rect=[.8,.5,.07,.46],
               colormap=mpl.cm.copper,
               facecolor='w',
               label='$\\nu$ (Hz)',\
               bounds=None,
               ticks_labels=None,
               no_ticks=False,
               orientation='vertical',
               scale='linear',\
               labelpad=2.,
               color_discretization=None):

    cb = add_inset(ax,
                   rect=inset_rect,
                   facecolor=facecolor)

    build_bar_legend(X,
                     cb,
                     colormap,
                     label=label,
                     scale=scale, bounds=bounds,
                     orientation=orientation,
                     labelpad=labelpad,
                     color_discretization=color_discretization,
                     no_ticks=no_ticks, ticks_labels=ticks_labels)
    
    return cb


def legend(list_of_lines,
           list_of_labels,
           fig=None,
           frameon=False,
           handletextpad=0.3,
           handlelength=1.,
           ncol=1,
           title='',
           fontsize=FONTSIZE-1,
           columnspacing=1.,
           loc='upper center'):

    if fig is None:
        fig = plt.gcf()

    fig.legend(list_of_lines,
               list_of_labels,
               loc=loc,
               frameon=frameon,
               ncol=ncol,
               # numpoints=1,
               # scatterpoints=1,
               columnspacing=columnspacing,
               handletextpad=handletextpad,
               handlelength=handlelength,
               title=title,
               fontsize=fontsize)

    

if __name__=='__main__':

    from my_graph import *
    
    Y = [np.exp(np.random.randn(100)) for i in range(4)]
    fig, ax, acb = figure_with_bar_legend()
    plot(Y=Y,
         xlabel='time', ylabel='y-value',
         colormap=copper,
         lw=1., ax=ax)
    LINES, LABELS = [], []
    for i in range(2):
        line, = ax.plot(np.arange(10)*10, np.exp(np.random.randn(10)), 'o', ms=2)
        LINES.append(line)
        LABELS.append('line'+str(i+1))
    for i in range(2):
        line, = ax.plot(np.arange(10)*10, np.exp(np.random.randn(10)), '-')
        LINES.append(line)
        LABELS.append('line'+str(i+1))

    legend(LINES, LABELS, ncol=2, loc=(.2,.6))
    
    bar_legend(np.arange(5), ax,
               colormap=copper,
               # orientation='horizontal',
               label='Trial ID', no_ticks=True)
    build_bar_legend_continuous(acb, copper)
    # set_plot(acb, [])
    
    show()
