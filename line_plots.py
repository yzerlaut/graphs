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
                lw=lw, marker=m, ms=ms, label=l)

    # then errorbars if needed:
    if (sY is not None):
        for x, y, sy, c in zip(X, Y, sY, COLORS):
            ax.fill_between(x, y-sy, y+sy,
                            color=c, lw=0, alpha=alpha_std)

if __name__=='__main__':
    
    from my_graph import graphs
    import numpy as np
    
    mg = graphs('screen')
    # mg.plot(Y=3*np.random.randn(4,10),
    #         sY=np.random.randn(4,10),
    #         ls=':', m='o', ms=0.1, lw=0.4,
    #         xlabel='x-label (X)', ylabel='y-label (Y)')

    tstop, dt = 10, 1e-2
    t = np.arange(int(tstop/dt))*dt
    x = np.random.randn(len(t))*10.-70.
    for tt in np.cumsum(np.random.exponential(tstop/10., 10)):
        x[np.argmin(np.abs(tt-t))] = 10.

    
    fig, ax = mg.plot(t, x, fig_args=dict(figsize=(3,1)))
    mg.draw_bar_scales(ax, 'top-left', 10, '10mV', 1, '1s')
    mg.show()
