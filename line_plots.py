from matplotlib.cm import viridis
# import sys, os
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

def single_curve(ax, x, y, sy,
                 color='k-',
                 lw=1, ms=0, ls='-', m='',
                 label=None,
                 alpha_std=0.3):
    # we print a single curve
    ax.plot(x, y, color=color, lw=lw, label=label, linestyle=ls, marker=m, ms=ms)
    # then errorbars if needed:
    if (sy is not None):
        ax.fill_between(x, y-sy, y+sy,
                        color=color, lw=0, alpha=alpha_std)


def multiple_curves(ax, X, Y, sY, COLORS, LABELS,
                    lw=1, ms=0, ls='-', m='',
                    alpha_std=0.3, colormap=viridis):
    # meaning we have to plot several curves
    if COLORS is None:
        COLORS = [colormap(i/(len(Y)-1)) for i in range(len(Y))]
    if (LABELS is None):
        LABELS = ['Y'+str(i+1) for i in range(len(Y))]
    for x, y, l, c in zip(X, Y, LABELS, COLORS):
        ax.plot(x, y,
                color=c, linestyle=ls,
                marker=m, ms=ms, label=l)

    # then errorbars if needed:
    if (sY is not None):
        for x, y, sy, c in zip(X, Y, sY, COLORS):
            ax.fill_between(x, y-sy, y+sy,
                            color=c, lw=0, alpha=alpha_std)

if __name__=='__main__':
    from my_graph import *
    plot(Y=np.random.randn(4,10), ls=':', m='o', ms=2, lw=0.4)
    show()
