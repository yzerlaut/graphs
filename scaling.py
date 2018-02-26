"""
In this module we rewrite the matplotlib functions
"""
import matplotlib as mpl
import matplotlib.pylab as plt

FONTSIZE= 9
mpl.rcParams.update({'axes.labelsize': FONTSIZE,
                     'font.size': FONTSIZE,
                     'xtick.labelsize': FONTSIZE,
                     'ytick.labelsize': FONTSIZE})

A0_format = {'width':8.3, 'height':11.7}


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
    
    import sys
    FONTSIZE = int(sys.argv[-1])
    
    mpl.rcParams.update({'axes.labelsize': FONTSIZE,
                         'font.size': FONTSIZE,
                         'xtick.labelsize': FONTSIZE,
                         'ytick.labelsize': FONTSIZE})
    
    fig, [ax] = subplots(width_to_height=1.5, with_top_left_letter='a')
    annotate('The fontsize is \n now set to '+str(FONTSIZE), fig,
             fontsize=FONTSIZE)
    set_plot(ax, xlabel='my xlabel (Unit)', ylabel='my ylabel (Unit)',
             fontsize=FONTSIZE, num_xticks=3, num_yticks=3)
    fig.savefig(desktop+'fig.svg')
    show()

