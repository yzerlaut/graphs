import matplotlib.pylab as plt
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE, A0_format, Single_Plot_Size
from matplotlib.ticker import MaxNLocator, NullFormatter

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
             xcolor='k', ycolor='k',
             fontsize=FONTSIZE):

    # no ticks if no axis bar
    if not (('top' in spines) or ('bottom' in spines)):
        xticks=[]
    if not (('left' in spines) or ('right' in spines)):
        yticks=[]
        
    # drawing spines
    adjust_spines(ax, spines,
                  tck_outward=tck_outward,
                  ycolor=ycolor, xcolor=xcolor)
    
    if yscale=='log':
        ax.set_yscale('log')
    if xscale=='log':
        ax.set_xscale('log')
    
    # Boundaries
    if xlim is None:
        xmin, xmax = ax.get_xlim()
        dx = xmax-xmin
        if xscale=='log':
            if xmin<=0:
                xmin = np.concatenate([line.get_xdata() for line in ax.get_lines()[:2]]).min() # what are the additional line objects ??
            xlim = [xmin/1.1,1.1*xmax]
        else:
            xlim = [xmin-xlim_enhancment*dx/100.,xmax+xlim_enhancment*dx/100.]

    if xscale=='log': # we calculate the tick positions
        xlim, xmajor_ticks, xminor_ticks2 = find_good_log_ticks(lim=xlim)
        if xminor_ticks is None:
            xminor_ticks = xminor_ticks2
        if xticks is None:
            xticks = xmajor_ticks
        
    if ylim is None:
        ymin, ymax = ax.get_ylim()
        dy = ymax-ymin
        if yscale=='log':
            if ymin<=0:
                ymin = np.concatenate([line.get_ydata() for line in ax.get_lines()[::-2]]).min() # what are the additional lines ??
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
    ax.plot(np.ones(2)*np.mean(xlim), ylim, 'w.', ms=0.001, alpha=0.001)
    ax.plot(xlim, np.ones(2)*np.mean(ylim), 'w.', ms=0.001, alpha=0.001)
    ax.set_xlim(xlim)
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

    ax.set_xlabel(xlabel, fontsize=fontsize, color=xcolor)
    ax.set_ylabel(ylabel, fontsize=fontsize, color=ycolor)

    if grid:
        ax.grid()

        
        
def ticks_number(ax, xticks=3, yticks=3):
    if xticks>1:
        ax.xaxis.set_major_locator( MaxNLocator(nbins = xticks) )
    if yticks>1:
        ax.yaxis.set_major_locator( MaxNLocator(nbins = yticks) )

def adjust_spines(ax, spines, tck_outward=3, xcolor='k', ycolor='k'):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', tck_outward)) # outward by 10 points by default
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_color(ycolor)
        ax.tick_params('y', colors=ycolor, which='both')
    elif 'right' in spines:
        ax.yaxis.set_ticks_position('right')
        ax.spines['right'].set_color(ycolor)
        ax.tick_params('y', colors=ycolor, which='both')
        ax.yaxis.set_label_position('right')
    else:
        ax.yaxis.set_ticks([]) # no yaxis ticks

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_color(xcolor)
        ax.tick_params('x', colors=xcolor, which='both')
    elif 'top' in spines:
        ax.xaxis.set_ticks_position('top')
        ax.spines['top'].set_color(xcolor)
        ax.tick_params('x', colors=xcolor, which='both')
        ax.xaxis.set_label_position('top')
    else:
        ax.xaxis.set_ticks([]) # no xaxis ticks
        

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
    from my_graph import *
    fig, ax = figure(axes_extents=[[[2,1]]], left=2., right=3.)
    ax2 = ax.twinx()
    ax.plot(np.exp(np.random.randn(100)), 'o', ms=2, color=Blue)
    ax2.plot(np.exp(np.random.randn(100)), 'o', ms=1, color=Red)
    set_plot(ax2, ['right'], yscale='log', ylabel='blabal',
             tck_outward=2, ycolor=Red)
    set_plot(ax, ycolor=Blue, xcolor='k',
             yscale='log', ylabel='blabal',
             tck_outward=2, xlabel='trying')
    show()
