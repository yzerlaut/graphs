import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE, A0_format
from matplotlib.ticker import MaxNLocator, NullFormatter
import numpy as np

def set_plot(ax, spines=['left', 'bottom'],\
             num_xticks=4, num_yticks=4,\
             xlabel='', ylabel='', tck_outward=3,\
             xticks=None, yticks=None,\
             xminor_ticks=None, yminor_ticks=None,
             xticks_labels=None, yticks_labels=None,\
             xticks_rotation=0, yticks_rotation=0,\
             xscale='linear', yscale='linear',
             xlim_enhancment=1., ylim_enhancment=1.,\
             xlim=None, ylim=None,
             grid=False,
             fontsize=FONTSIZE):

    # no ticks if no axis bar
    if not (('top' in spines) or ('bottom' in spines)):
        xticks=[]
    if not (('left' in spines) or ('right' in spines)):
        yticks=[]
        
    # drawing spines
    adjust_spines(ax, spines, tck_outward=tck_outward)

    if yscale=='log':
        ax.set_yscale('log')
    if xscale=='log':
        ax.set_xscale('log')
    
    # Boundaries
    if xlim is None:
        xmin, xmax = ax.get_xaxis().get_view_interval()
        dx = xmax-xmin
        if xscale=='log':
            xlim = [xmin/1.1,1.1*xmax]
            xlim, xmajor_ticks, xminor_ticks = find_good_log_ticks(lim=xlim)
        else:
            xlim = [xmin-xlim_enhancment*dx/100.,xmax+xlim_enhancment*dx/100.]

    ax.plot(xlim, np.ones(2)*np.mean(ax.get_ylim()), 'w.', ms=0.001, alpha=0.001)
    ax.set_xlim(xlim)
        
    if xscale=='log': # we calculate the tick positions
        xlim, xmajor_ticks, xminor_ticks2 = find_good_log_ticks(lim=ylim)
        if xminor_ticks is None:
            xminor_ticks = xminor_ticks2
        if xticks is None:
            xticks = xmajor_ticks
        
    if ylim is None:
        ymin, ymax = ax.get_yaxis().get_view_interval()
        dy = ymax-ymin
        if yscale=='log':
            ylim = [ymin/1.2,1.2*ymax]
        else:
            ylim = [ymin-ylim_enhancment*dy/100.,ymax+ylim_enhancment*dy/100.]
    if yscale=='log':
        ylim, ymajor_ticks, yminor_ticks = find_good_log_ticks(lim=ylim)
        if yminor_ticks is None:
            yminor_ticks = yminor_ticks2
        if yticks is None:
            yticks = ymajor_ticks
    # then we set it:
    ax.plot(np.ones(2)*np.mean(ax.get_xlim()), ylim, 'w.', ms=0.001, alpha=0.001)
    ax.set_ylim(ylim)

    # x-Ticks
    if (xticks is None) and ('bottom' or 'top' in spines):
        ax.xaxis.set_major_locator( MaxNLocator(nbins = num_xticks) )
    else:
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_xticks(xticks)
    if xscale=='log':
        ax.set_xticks(xminor_ticks, minor=True)
    
    if xticks_labels is not None:
        ax.set_xticklabels(xticks_labels, rotation=xticks_rotation)

    # y-Ticks
    if (yticks is None) and ('left' or 'right' in spines):
        ax.yaxis.set_major_locator( MaxNLocator(nbins = num_yticks) )
    else:
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_yticks(yticks)
    if yscale=='log':
        if (np.all(ax.get_yticks()<ylim[0]) or np.all(ax.get_yticks()>ylim[1])):
            # then no main ticks is on the plot, we set the minor ticks as the major ticks
            print(ax.get_yticks(), ymajor_ticks, yminor_ticks, ylim)
            print('no main ticks is on the plot, we set the minor ticks as the major ticks')
            ax.set_yticks(yminor_ticks)
        else:
            ax.set_yticks(yminor_ticks, minor=True)
        
    if yticks_labels is not None:
        ax.set_yticklabels(yticks_labels, rotation=yticks_rotation)

    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)

    if grid:
        ax.grid()
        
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

def find_good_log_ticks(lim=[0.009, 0.0099]):
    if lim[0]<=0:
        print('/!\ need positive lower bound of graphs, set to 1e-3')
        lim[0] = 1e-3
    if lim[1]<=0:
        print('/!\ need positive lower bound of graphs, set to 10')
        lim[1] = 10
    i0 =  np.floor(np.log(lim[0])/np.log(10))
    i1 =  np.floor(np.log(lim[1])/np.log(10))
    
    major_ticks = np.power(10., np.arange(i0, i1+1))
    major_ticks = major_ticks[(major_ticks>=lim[0]) & (major_ticks<=lim[1])]

    i0 =  int(np.log(lim[0])/np.log(10))-1
    i1 =  int(np.log(lim[1])/np.log(10))
    xx, ii = int(lim[0]/(10.**(i0))), i0
    while xx>10:
        xx, ii = int(lim[0]/(10.**(ii+1))), ii+1
        
    minor_ticks = []
    while (xx*np.power(10., ii)<lim[1]):
        minor_ticks.append(xx*np.power(10., ii))
        xx +=1
        if xx==10:
            ii+=1
            xx=1
    minor_ticks = np.unique(np.array(minor_ticks))
    minor_ticks = minor_ticks[(minor_ticks>=lim[0]) & (minor_ticks<=lim[1])]
    
    return lim, major_ticks, minor_ticks

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

def scale_figure(height_to_width, A0_ratio, x_plots, y_plots,
                 wspace=0.5, hspace=0.5,
                 left=0.3, right=0.9,
                 bottom=0.3, top=0.9):

    SCALE = scale_graphs_boudaries(x_plots, y_plots,
                                   wspace=wspace, hspace=hspace,
                                   left=left, right=right,
                                   bottom=bottom, top=top)
    SCALE0 = scale_graphs_boudaries(1, 1,
                                   wspace=wspace, hspace=hspace,
                                   left=left, right=right,
                                   bottom=bottom, top=top)
    
    a = (1-SCALE['left']-SCALE['right'])/x_plots-SCALE['wspace']
    a0 = (1-SCALE0['left']-SCALE0['right'])/x_plots-SCALE0['wspace']
    b = (1-SCALE['top']-SCALE['bottom'])/y_plots-SCALE['hspace']
    b0 = (1-SCALE0['top']-SCALE0['bottom'])/y_plots-SCALE0['hspace']
    return {
        'figsize':(\
            A0_format['width']*A0_ratio*x_plots,
                   A0_format['height']*A0_ratio*y_plots*height_to_width)}



if __name__=='__main__':
    from my_graph import figure, show
    import numpy as np
    fig, ax = figure()
    ax.plot(np.exp(np.random.randn(100)))
    # ax.plot([1,2], [3.3, 20.3])
    set_plot(ax,
             yscale='log',
             # ylim=[0.71, 2.01],
             # yticks=[0.8, 0.9, 1., 2.],yticks_labels=['0.8', '0.9', '1', '2'],
             # yticks=[0.01, 1., 100.], yticks_labels=['0.01', '1', '100'],
             tck_outward=2)
    show()
