import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.inset import add_inset
from graphs.scaling import FONTSIZE, A0_format
import numpy as np
import matplotlib as mpl

def get_linear_colormap(color1='blue', color2='red'):
    return mpl.colors.LinearSegmentedColormap.from_list(\
                        'mycolors',[color1, color2])

def build_bar_legend(X, ax, mymap,
                     label='$\\nu$ (Hz)',\
                     bounds=None,
                     ticks_labels=None,
                     no_ticks=False,
                     orientation='vertical',
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
                                   orientation=orientation)
    if no_ticks:
        cb.set_ticks([])
    else:
        cb.set_ticks(X)
        if ticks_labels is not None:
            cb.set_ticklabels(ticks_labels)
        
    cb.set_label(label)
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
                     color_discretization=color_discretization,
                     no_ticks=no_ticks, ticks_labels=ticks_labels)
    
    return cb



if __name__=='__main__':

    from my_graph import *
    
    Y = [np.exp(np.random.randn(100)) for i in range(4)]
    fig, ax = plot(Y=Y,
                   xlabel='time', ylabel='y-value',
                   colormap=copper,
                   lw=1.)
    bar_legend(np.arange(5), ax,
               colormap=copper,
               label='Trial ID', no_ticks=True)
    
    show()
