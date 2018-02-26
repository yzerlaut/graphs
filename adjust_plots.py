import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator, NullFormatter
from graphs.scaling import FONTSIZE, A0_format

def set_plot(ax, spines=['left', 'bottom'],\
                num_xticks=4, num_yticks=4,\
                xlabel='', ylabel='', tck_outward=5,\
                xticks=None, yticks=None,\
                xticks_labels=None, yticks_labels=None,\
                xticks_rotation=0, yticks_rotation=0,\
                xlim_enhancment=2, ylim_enhancment=2,\
                xlim=None, ylim=None, fontsize=FONTSIZE):
    
    # drawing spines
    adjust_spines(ax, spines, tck_outward=tck_outward)
    
    # Boundaries
    if xlim is None:
        xmin, xmax = ax.get_xaxis().get_view_interval()
        dx = xmax-xmin
        ax.set_xlim([xmin-xlim_enhancment*dx/100.,xmax+xlim_enhancment*dx/100.])
    else:
        ax.set_xlim(xlim)
    if ylim is None:
        ymin, ymax = ax.get_yaxis().get_view_interval()
        dy = ymax-ymin
        ax.set_ylim([ymin-ylim_enhancment*dy/100.,ymax+ylim_enhancment*dy/100.])
    else:
        ax.set_ylim(ylim)

    if (xticks is None) and ('bottom' or 'top' in spines):
        ax.xaxis.set_major_locator( MaxNLocator(nbins = num_xticks) )
    else:
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_xticks(xticks)
        
    if xticks_labels is not None:
        ax.set_xticklabels(xticks_labels, rotation=xticks_rotation)

    if (yticks is None) and ('left' or 'right' in spines):
        ax.yaxis.set_major_locator( MaxNLocator(nbins = num_yticks) )
    else:
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_yticks(yticks)
        
    if yticks_labels is not None:
        ax.set_yticklabels(yticks_labels, rotation=yticks_rotation)

    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)

        
def ticks_number(ax, xticks=3, yticks=3):
    if xticks>1:
        ax.xaxis.set_major_locator( MaxNLocator(nbins = xticks) )
    if yticks>1:
        ax.yaxis.set_major_locator( MaxNLocator(nbins = yticks) )


def adjust_spines(ax, spines, tck_outward=3):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', tck_outward)) # outward by 10 points by default
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])


def scale_graphs_boudaries(x_plots, y_plots,
                           wspace=0.2, hspace=0.2,
                           left=0.3, right=0.9,
                           bottom=0.3, top=0.9):
    
    return {'left':left/x_plots,
            'right':1.-(1.-right)/x_plots,
            'top':1.-(1.-top)/y_plots,
            'bottom':bottom/y_plots,
            'hspace':hspace*y_plots,
            'wspace':wspace*x_plots}

def scale_figure(width_to_height, A0_ratio, x_plots, y_plots,
                 wspace=0.5, hspace=0.5,
                 left=0.3, right=0.9,
                 bottom=0.3, top=0.9):

    print(x_plots, y_plots)
    SCALE = scale_graphs_boudaries(x_plots, y_plots,
                                   wspace=wspace, hspace=hspace,
                                   left=left, right=right,
                                   bottom=bottom, top=top)
    SCALE0 = scale_graphs_boudaries(1, 1,
                                   wspace=wspace, hspace=hspace,
                                   left=left, right=right,
                                   bottom=bottom, top=top)
    
    print(SCALE)
    print(SCALE0)
    a = (1-SCALE['left']-SCALE['right'])/x_plots-SCALE['wspace']
    a0 = (1-SCALE0['left']-SCALE0['right'])/x_plots-SCALE0['wspace']
    b = (1-SCALE['top']-SCALE['bottom'])/y_plots-SCALE['hspace']
    b0 = (1-SCALE0['top']-SCALE0['bottom'])/y_plots-SCALE0['hspace']
    print('x', a/a0)
    print('y', b/b0)
    return {
        'figsize':(\
            A0_format['width']*A0_ratio*width_to_height*x_plots,
                   A0_format['height']*A0_ratio*y_plots)}



        
