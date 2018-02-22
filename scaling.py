"""
In this module we rewrite the matplotlib functions
"""
import matplotlib as mpl
import matplotlib.pylab as plt

FONTSIZE= 9
# mpl.rcParams.update({'axes.labelsize': 10, 'xtick.labelsize': 10, 'ytick.labelsize': 10})
# mpl.rcParams.update({'axes.labelsize': FONTSIZE,
#                      'font.size': FONTSIZE,
#                      'xtick.labelsize': FONTSIZE,
#                      'ytick.labelsize': FONTSIZE})

A0_format = {'width':8.3, 'height':11.7}


def figure(width_to_height=1.2,
           A0_ratio=0.2,
           wspace=0.2, hspace=0.1,
           left=0.3, right=0.9,
           bottom=0.3, top=0.9,
           with_top_left_letter='',
           fontsize=10, fontweight='bold'):
    """
    scales figures with respect to the A0 format !
    """

    fig = plt.figure(\
                     figsize=(A0_format['width']*A0_ratio*width_to_height,
                              A0_format['height']*A0_ratio))
    plt.subplots_adjust(wspace=wspace, hspace=hspace,
                        left=left, right=right,
                        bottom=bottom, top=top)
    plt.annotate(with_top_left_letter, (0.01,.99), xycoords='figure fraction',
                 fontsize=fontsize, fontweight='bold')
    return fig


def subplots(width_to_height=1.2,
             AX_dim = [1,0],
             A0_ratio=0.2,
             wspace=0.2, hspace=0.1,
             left=0.3, right=0.9,
             bottom=0.3, top=0.9,
             with_top_left_letter='',
             fontsize=10, fontweight='bold'):
    """
    analog to plt.subplots
    """

    fig = figure(
        width_to_height=width_to_height,
        A0_ratio=A0_ratio,
        wspace=wspace, hspace=hspace,
        left=left, right=right,
        bottom=bottom, top=top,
        with_top_left_letter=with_top_left_letter,
        fontsize=fontsize, fontweight=fontweight)

    ax = fig.add_subplot(111)
    
    return fig, [ax]

def annotate(s, stuff, x=0.5, y=0.8, fontsize=FONTSIZE, fontweight='normal'):
    print(type(stuff))
    if type(stuff)==mpl.figure.Figure:
        plt.annotate(s, (x,y), xycoords='figure fraction',
                     fontweight=fontweight, fontsize=fontsize)
    else:
        stuff.annotate(s, (x,y), xycoords='axes fraction',
                     fontweight=fontweight, fontsize=fontsize)


if __name__=='__main__':

    from my_graph import *
    fig, [ax] = subplots(with_top_left_letter='a')
    annotate('The fontsize is now set to '+str(FONTSIZE), fig)
    set_plot(ax, xlabel='my xlabel (Unit)', ylabel='my ylabel (Unit)')
    fig.savefig(desktop+'fig.svg')
    show()

