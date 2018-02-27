from matplotlib.cm import viridis
# import sys, os
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

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

            
