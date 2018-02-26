from matplotlib.cm import viridis
# import sys, os
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

def single_curve(ax, x, y, sy, color, lw=1, alpha_std=0.3):
    # we print a single curve
    ax.plot(x, y, color=color, lw=lw)
    # then errorbars if needed:
    if (sy is not None):
        ax.fill_between(x, y-sy, y+sy,
                        color=color, lw=0, alpha=alpha_std)


def multiple_curves(ax, X, Y, sY, COLORS, LABELS, alpha_std=0.3, lw=1, colormap=viridis):
    # meaning we have to plot several curves
    if COLORS is None:
        COLORS = [colormap(i/(len(Y)-1)) for i in range(len(Y))]
    if (LABELS is None):
        LABELS = ['Y'+str(i+1) for i in range(len(Y))]
    for x, y, l, c in zip(X, Y, LABELS, COLORS):
        ax.plot(x, y, color=c, lw=lw, label=l)

    # then errorbars if needed:
    if (sY is not None):
        for x, y, sy, c in zip(X, Y, sY, COLORS):
            ax.fill_between(x, y-sy, y+sy,
                            color=c, lw=0, alpha=alpha_std)
            
# def set_scale_and_annotation(ax,
#                              xunit='s', yunit='mV',
#                              xscale=None, yscale=None):
#     x1, x2 = ax.get_xlim()
#     y1, y2 = ax.get_ylim()
#     if xscale is None:
#         xscale = int((x2-x1)/10)
#     if yscale is None:
#         yscale = int((y2-y1)/10)
#     ax.plot([x1, x1+xscale], [y1, y1],  '-', lw=5, color='gray')
#     ax.annotate(str(xscale)+xunit, (x1+1.1*xscale,y1))
#     ax.plot([x1,x1], [y1,y1+yscale], '-', lw=5, color='gray')
#     ax.annotate(str(yscale)+yunit, (x1,y1+1.1*yscale))
#     set_plot(ax, [], xticks=[], yticks=[])
    
# def bars_only(ax, x, y,
#               xunit='s', yunit='mV',
#               xscale=None, yscale=None, color='k', label=''):
#     ax.plot(x, y, '-', color=color, label=label)

#     set_scale_and_annotation(ax, xunit=xunit, yunit=yunit,
#                              xscale=xscale, yscale=yscale)
#     return ax


# def bars_only_multiple_traces(ax, X, Y,
#                               xunit='s', yunit='mV',
#                               xscale=None, yscale=None,
#                               color='k', LABELS=None, COLORS=None):

#     if LABELS is None:
#         LABELS = ['' for i in range(len(X))]
#     if COLORS is None:
#         COLORS = [color for i in range(len(X))]

#     for i in range(len(X)):
#         ax.plot(X[i], Y[i], '-', label=LABELS[i], color=COLORS[i])

#     set_scale_and_annotation(ax, xunit=xunit, yunit=yunit,
#                              xscale=xscale, yscale=yscale)
#     return ax

# if __name__=='__main__':

#     from graphs.my_graph import *
    
#     fig, _ = figure(axes_extents=[\
#                                        [[3,2]],
#                                        [[3,1]]\
#                                        ],
#                     height_to_width=0.4, hspace=.01)
#     save_on_desktop(fig)
    
#     show()
