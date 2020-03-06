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
                 label='',
                 lw=0, ms=3, elw=1):
    if (sy is None) and (sx is None):
        ax.errorbar(x, y, fmt='o-',
                  marker=marker, color=color,
                  lw=lw, ms=ms, label=label)
    elif (sy is None):
        ax.errorbar(x, y, xerr=sx, fmt='o-',
                    marker=marker, color=color,
                    lw=lw, ms=ms, elinewidth=elw, label=label)
    elif (sx is None):
        ax.errorbar(x, y, yerr=sy, fmt='o-',
                    marker=marker, color=color,
                    lw=lw, ms=ms, elinewidth=elw, label=label)
    else:
        ax.errorbar(x, y, xerr=sx, yerr=sy, fmt='o-',
                    marker=marker, color=color,
                    lw=lw, ms=ms, elinewidth=elw, label=label)

def multiple_curves(ax, X, Y, sX, sY, COLORS, LABELS,
                    marker='o', lw=0,
                    colormap=viridis, ms=3, elw=1):
    
    # meaning we have to plot several curves
    if COLORS is None:
        COLORS = [colormap(i/(len(Y)-1)) for i in range(len(Y))]
    if (LABELS is None):
        LABELS = ['Y'+str(i+1) for i in range(len(Y))]

    if (sY is None) and (sX is None):
        for x, y, c, label in zip(X, Y, COLORS, LABELS):
            ax.errorbar(x, y,
                       color=c, marker=marker,
                       lw=lw, ms=ms, label=label)
    elif (sY is None):
        for x, y, sx, c, label in zip(X, Y, sX, COLORS, LABELS):
            ax.errorbar(x, y, xerr=sx,
                        color=c, marker=marker,
                        lw=lw, ms=ms, elinewidth=elw, label=label)
    elif (sX is None):
        for x, y, sy, c, label in zip(X, Y, sY, COLORS, LABELS):
            ax.errorbar(x, y, yerr=sy,
                        color=c, marker=marker,
                        lw=lw, ms=ms, elinewidth=elw, label=label)
    else:
        for x, y, sx, sy, c, label in zip(X, Y, sX, sY, COLORS, LABELS):
            ax.errorbar(x, y, xerr=sx, yerr=sy,
                        color=c, marker=marker,
                        lw=lw, ms=ms, elinewidth=elw, label=label)


if __name__=='__main__':
    
    import datavyz
    ge = datavyz.graph_env('manuscript')
    
    # two_variable_analysis(np.random.randn(10), np.random.randn(10),
    #                       colormap=viridis)
    fig, ax = ge.plot(Y=np.random.randn(4, 10),
                      sY=np.random.randn(4, 10),
                      xlabel='xlabel (xunit)',
                      ylabel='ylabel (yunit)',
                      title='datavyz demo plot')
    fig.savefig('fig.svg')
    ge.show()
        
