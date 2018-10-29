import numpy as np
from matplotlib import cm
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import *
from graphs.my_graph import figure
    
def twoD_plot(x, y, z,
              ax=None,
              acb=None,
              bar_legend={},
              alpha=1.,
              fig_args={},
              cmap=cm.viridis,
              diverging=False,
              vmin=None,
              vmax=None,
              interpolation='none'):
    """
    surface plots for x, y and z 1 dimensional data

    switch to bar_legend=None to remove the bar legend
    """
    
    if ax is None:
        if ('figsize' not in fig_args) and (bar_legend is not None):
            fig_args['figsize'] = (1.4, 1.)
            fig_args['right'] = 5.5
        fig, ax = figure(**fig_args)
    if (bar_legend is not None) and (acb is None):
        if 'position' not in bar_legend:
            bar_legend['position'] = [.7,.35,.03,.55]
        acb = plt.axes(bar_legend['position'], facecolor='b')
    else:
        fig = plt.gcf()
        
    if diverging and (cmap==cm.viridis):
        cmap = cm.PiYG # we switch to a diverging colormap
        
    x, y = np.array(x), np.array(y)
    Z = np.ones((len(np.unique(y)), len(np.unique(x))))*np.nan
    for i, yy in enumerate(np.unique(y)):
        cond1 = y==yy
        for j, xx in enumerate(np.unique(x[cond1])):
            Z[i,j] = z[cond1][x[cond1]==xx]
    z1 = np.array(Z).reshape(len(np.unique(y)), len(np.unique(x)))
    z1 = Z
    
    if vmin is None:
        if diverging:
            vmin = -np.max(np.abs(z))
        else:
            vmin = np.min(z)
    if vmax is None:
        if diverging:
            vmax = np.max(np.abs(z))
        else:
            vmax = np.max(z)
            
    ac = ax.imshow(z1,
                   interpolation=interpolation,
                   extent = (x.min(), x.max(), y.min(), y.max()),
                   vmin = vmin,
                   vmax = vmax,
                   alpha=alpha,
                   cmap=cmap,
                   origin='lower',
                   aspect='auto')

    """
    Need to polish the integration of "build_bar_legend" within this function
    """
    if bar_legend is not None:
        if not 'ticks' in bar_legend:
            bar_legend['ticks'] = np.unique(np.round(np.linspace(vmin, vmax, 5), 1))
        if not 'label' in bar_legend:
            bar_legend['label'] = ''
        if not 'color_discretization' in bar_legend:
            bar_legend['color_discretization'] = None
        build_bar_legend(bar_legend['ticks'], acb, cmap,
                         label=bar_legend['label'],
                         color_discretization=bar_legend['color_discretization'])
    return ax, acb
    

if __name__=='__main__':
    from my_graph import *
    
    x, y = np.meshgrid(np.arange(1, 11), np.arange(1, 11))
    z = np.sqrt(x*y)
    x, y, z = np.array(x).flatten(),\
              np.array(y).flatten(),\
              np.array(z).flatten()*np.random.randn(len(z.flatten()))
    index = np.arange(len(x))
    np.random.shuffle(index)
    x, y, z = x[index], y[index], z[index]

    # ax, acb = twoD_plot(x[x<y], y[x<y], z[x<y],
    ax, acb = twoD_plot(x, y, z,
                        vmin=-7, vmax=7,
                        bar_legend={'label':'color',
                                    'color_discretization':20})
    set_plot(ax, xlabel='x-label (X)', ylabel='y-label (Y)')
    show()
