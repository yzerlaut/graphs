import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE

def from_pval_to_star(p,
                      threshold1=1e-3,
                      threshold2=1e-2,
                      threshold3=5e-2):
    if p<threshold1:
        return '***'
    elif p<threshold2:
        return '**'
    elif p<threshold3:
        return '*'
    else:
        return 'n.s.'
    
def sci_str(x, rounding=0, remove_0_in_exp=True):
    y = ('{:.' + str(int(rounding))+'e}').format(x)
    if remove_0_in_exp: y = y.replace('-0', '-')
    return y

def bar_scales(ax,
               xlim=None, ylim=None,
               xbar=0, ybar=0,
               xbar_label='', ybar_label='',
               location = 'top right',
               remove_axis=True,
               factor=0.98):

    if remove_axis:
        ax.axis('off')
    
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
        
    if location=='top right':
        x0 = xlim[1]-(1.-factor)*(xlim[1]-xlim[0])
        y0 = ylim[1]-(1.-factor)*(ylim[1]-ylim[0])
        ax.plot([x0, x0-xbar], [y0, y0], 'k-', lw=1)
        ax.plot([x0, x0], [y0, y0-ybar], 'k-', lw=1)
        ax.annotate(ybar_label, (x0, y0-ybar/2.), fontsize=FONTSIZE, rotation=90)
        ax.annotate(xbar_label, (x0-xbar, y0), fontsize=FONTSIZE)
    elif location=='top left':
        x0 = xlim[0]+(1.-factor)*(xlim[1]-xlim[0])
        y0 = ylim[1]-(1.-factor)*(ylim[1]-ylim[0])
        ax.plot([x0, x0+xbar], [y0, y0], 'k-', lw=1)
        ax.plot([x0, x0], [y0, y0-ybar], 'k-', lw=1)
        ax.annotate(xbar_label, (x0, y0), fontsize=FONTSIZE)
        ax.annotate(ybar_label, (x0, y0-ybar/2.), fontsize=FONTSIZE, rotation=90)
    elif location=='bottom right':
        x0 = xlim[1]-(1.-factor)*(xlim[1]-xlim[0])
        y0 = ylim[0]+(1.-factor)*(ylim[1]-ylim[0])
        ax.plot([x0, x0-xbar], [y0, y0], 'k-', lw=1)
        ax.plot([x0, x0], [y0, y0+ybar], 'k-', lw=1)
        ax.annotate(xbar_label, (x0-xbar, y0), fontsize=FONTSIZE)
        ax.annotate(ybar_label, (x0, y0+ybar/2.), fontsize=FONTSIZE, rotation=90)
    elif location=='bottom left':
        x0 = xlim[0]+(1.-factor)*(xlim[1]-xlim[0])
        y0 = ylim[0]+(1.-factor)*(ylim[1]-ylim[0])
        ax.plot([x0, x0+xbar], [y0, y0], 'k-', lw=1)
        ax.plot([x0, x0], [y0, y0+ybar], 'k-', lw=1)
        ax.annotate(xbar_label, (x0, y0), fontsize=FONTSIZE)
        ax.annotate(ybar_label, (x0, y0+ybar/2.), fontsize=FONTSIZE, rotation=90)
    else:
        x0, y0 = location
        
    # we reintroduce the data limits
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    

if __name__=='__main__':
    x = 32.23545345e-5
    print(sci_str(x, rounding=2))
    print(from_pval_to_star(x))

    from my_graph import *

    fig, ax = figure()

    ax.plot(np.random.randn(30), np.random.randn(30), 'o')
    bar_scales(ax, xbar=2, ybar=2, location='bottom left',
               ybar_label=r'10$\mu$V', xbar_label='200ms')
    show()
