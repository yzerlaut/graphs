import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.adjust_plots import set_plot

def set_scale_and_annotation(ax,
                             xunit='s', yunit='mV',
                             xscale=None, yscale=None):
    x1, x2 = ax.get_xlim()
    y1, y2 = ax.get_ylim()
    if xscale is None:
        xscale = int((x2-x1)/10)
    if yscale is None:
        yscale = int((y2-y1)/10)
    ax.plot([x1, x1+xscale], [y1, y1],  '-', lw=5, color='gray')
    ax.annotate(str(xscale)+xunit, (x1+1.1*xscale,y1))
    ax.plot([x1,x1], [y1,y1+yscale], '-', lw=5, color='gray')
    ax.annotate(str(yscale)+yunit, (x1,y1+1.1*yscale))
    set_plot(ax, [], xticks=[], yticks=[])
    
def bars_only(ax, x, y,
              xunit='s', yunit='mV',
              xscale=None, yscale=None, color='k', label=''):
    ax.plot(x, y, '-', color=color, label=label)

    set_scale_and_annotation(ax, xunit=xunit, yunit=yunit,
                             xscale=xscale, yscale=yscale)
    return ax


def bars_only_multiple_traces(ax, X, Y,
                              xunit='s', yunit='mV',
                              xscale=None, yscale=None,
                              color='k', LABELS=None, COLORS=None):

    if LABELS is None:
        LABELS = ['' for i in range(len(X))]
    if COLORS is None:
        COLORS = [color for i in range(len(X))]

    for i in range(len(X)):
        ax.plot(X[i], Y[i], '-', label=LABELS[i], color=COLORS[i])

    set_scale_and_annotation(ax, xunit=xunit, yunit=yunit,
                             xscale=xscale, yscale=yscale)
    return ax

if __name__=='__main__':

    from graphs.my_graph import *
    
    fig, _ = figure(axes_extents=[\
                                       [[3,2]],
                                       [[3,1]]\
                                       ],
                    height_to_width=0.4, hspace=.01)
    save_on_desktop(fig)
    
    show()
