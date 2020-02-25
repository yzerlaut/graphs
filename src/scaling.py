"""
In this module we rewrite the matplotlib functions
"""
import matplotlib as mpl
import matplotlib.pylab as plt

FONTSIZE= 8
mpl.rcParams.update({'axes.labelsize': FONTSIZE,
                     'axes.titlesize': FONTSIZE,
                     'figure.titlesize': FONTSIZE,
                     'font.size': FONTSIZE,
                     'legend.fontsize': FONTSIZE,
                     'xtick.labelsize': FONTSIZE,
                     'ytick.labelsize': FONTSIZE,
                     'figure.facecolor': 'none',
                     'legend.facecolor': 'none',
                     'axes.facecolor': 'none',
                     'savefig.transparent':True,
                     'savefig.dpi':150,
                     'savefig.facecolor': 'none'})

A0_format = {'width':8.3, 'height':11.7}
Single_Plot_Size = (0.2, 0.12) # DEFAULT SIZE OF PLOT in terms of A0 format ratio

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)    

def inch2cm(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i*inch for i in tupl[0])
    else:
        return tuple(i*inch for i in tupl)    
    

if __name__=='__main__':

    for key in mpl.rcParams.keys():
        if 'facecolor' in key:
            print(key)

    from ..graphs import graphs
    mg = graphs('screen')
    
    import sys

    try:
        FONTSIZE = int(sys.argv[-1])
    except ValueError:
        FONTSIZE = mg.FONTSIZE
        
    # mpl.rcParams.update({'axes.labelsize': FONTSIZE,
    #                      'font.size': FONTSIZE,
    #                      'xtick.labelsize': FONTSIZE,
    #                      'ytick.labelsize': FONTSIZE})
    

    fig, ax = mg.figure()
    mg.top_left_letter(ax, 'a')
    mg.annotate(ax, 'The fontsize is \n now set to '+str(FONTSIZE), (.5,.97),
                va='top', ha='center', fontsize=FONTSIZE)
    mg.set_plot(ax,
                xlabel='my xlabel (Unit)', ylabel='my ylabel (Unit)',
                fontsize=FONTSIZE, num_xticks=3, num_yticks=3)
    # fig.savefig('fig.png')
    mg.show()

