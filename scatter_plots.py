from matplotlib.cm import viridis
from scipy.stats import pearsonr
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.draw_figure import figure
from graphs.adjust_plots import *

def two_variable_analysis(first_observations,
                          second_observations,
                          with_correl_annotation=True,
                          ylabel='y-value', xlabel='x-value',
                          colormap=None, ms=4):

    if len(first_observations)!=len(second_observations):
        print('Pb with sample size !! Test is not applicable !!')

    if colormap is None:
        def colormap(x):return 'k'
        
    fig, ax = figure()
    
    for i in range(len(first_observations)):
        ax.plot([first_observations[i]], [second_observations[i]], 'o', color=colormap(i/(len(first_observations)-1)), ms=ms)

    if with_correl_annotation:
        c, pval = pearsonr(first_observations, second_observations)
        lin = np.polyfit(first_observations, second_observations, 1)
        x = np.linspace(np.min(first_observations), np.max(first_observations), 3)
        ax.plot(x, np.polyval(lin, x), 'k:', lw=1)
        ax.annotate('Pearson correlation:\n c=%.2f, p=%.2f' % (c, pval), (.99,.4), xycoords='axes fraction')
    else:
        c, pval = 0., 1.
        
    set_plot(ax, ylabel=ylabel, xlabel=xlabel)
    
    return fig, ax, c, pval


def single_curve(ax, x, y, sx, sy,
                 color='k-', marker='o',
                 lw=0, ms=3, elw=1):
    if (sy is None):
        sy = [0 for s in y]
    if (sx is None):
        sx = [0 for s in x]
        # then errorbars
    ax.errorbar(x, y, xerr=sx, yerr=sy, fmt='o-',
                marker=marker, color=color,
                lw=lw, ms=ms, elinewidth=elw)

def multiple_curves(ax, X, Y, sX, sY, COLORS, LABELS,
                    marker='o', lw=0,
                    colormap=viridis, ms=3, elw=1):
    # meaning we have to plot several curves
    if COLORS is None:
        COLORS = [colormap(i/(len(Y)-1)) for i in range(len(Y))]
    if (LABELS is None):
        LABELS = ['Y'+str(i+1) for i in range(len(Y))]

    if (sY is None):
        sY = []
        for y in Y:
            sY.append([0 for s in y])
    if (sX is None):
        sX = []
        for x in X:
            sX.append([0 for s in x])
        
    for x, y, sx, sy, c in zip(X, Y, sX, sY, COLORS):
        ax.errorbar(x, y, xerr=sx, yerr=sy,
                    color=c, marker=marker,
                    lw=lw, ms=ms, elinewidth=elw)


if __name__=='__main__':
    from my_graph import *
    two_variable_analysis(np.random.randn(10), np.random.randn(10),
                          colormap=viridis)
    # fig, ax = scatter(np.random.randn(10), np.random.randn(10),
    #                   np.random.randn(10), np.random.randn(10))
    # ax.plot([-2,2], [-2,2], 'k:')
    show()
        
