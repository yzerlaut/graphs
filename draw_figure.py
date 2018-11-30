import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE, A0_format, Single_Plot_Size
import matplotlib.pylab as plt
import numpy as np

def figure(axes = (1,1),
           axes_extents=None,
           figsize=(1.,1.),
           left=1., right=1.,
           bottom=1., top=1.,
           wspace=1., hspace=1.,
           with_top_left_letter='',
           fontsize=FONTSIZE, fontweight='bold'):
    
    """
    scales figures with respect to the A0 format !

    the wspace, hspace, ... values are factor that modulates the wspace0, hspace0
    -> then use >1 to make bigger, and <1 to make smaller...

    Subplots are build with this convention for the geometry:
    (X,Y)
    ------ X -------------->
    |                 |     |
    |      (3,1)      |(1,1)|
    |                 |     |
    |-------------------
    Y     |           |     |
    |(1,1)|   (2,1)   |(1,1)|
    |     |           |     |
    |------------------------     
    v

    TO PRODUCE THIS, RUN:
    figure(axes_extents=[\
                         [[3,1], [1,1] ],
                         [[1,1], [2,1], [1,1] ] ] )
    show()

    """

    if axes_extents is None:
        if (len(axes)==1) and (axes[0]==1):
            axes_extents = [1]
        elif (axes[1]==0):
            axes_extents = np.ones(axes[0])
        elif (axes[0]==0):
            axes_extents = np.ones(axes[1])
        else:
            axes_extents = [[[1,1] for j in range(axes[1])]\
                            for i in range(axes[0])]

    x_plots = np.sum([axes_extents[0][j][0] \
                      for j in range(len(axes_extents[0]))])
    y_plots = np.sum([axes_extents[i][0][1] \
                      for i in range(len(axes_extents))])

    # FIGURE size
    figsize = (A0_format['width']*Single_Plot_Size[0]*x_plots*figsize[0],
               A0_format['height']*Single_Plot_Size[1]*y_plots*figsize[1])
    fig = plt.figure(figsize=figsize)

    
    # Subplots placements adjustements
    plt.subplots_adjust(left=left*0.55/figsize[0], # 0.5cm by default
                        bottom=bottom*0.5/figsize[1],# 0.5cm by default
                        top=1.-top*0.1/figsize[0], # 0.1cm by default
                        right=1.-right*0.1/figsize[1],# 0.1cm by default
                        wspace=wspace*0.5/figsize[0]*x_plots, # 0.5cm by default
                        hspace=hspace*0.5/figsize[1]*y_plots) # 0.5cm by default

    AX = []
    j0_row = 0
    for j in range(len(axes_extents)):
        AX_line = []
        i0_line = 0
        for i in range(len(axes_extents[j])):
            AX_line.append(plt.subplot2grid(\
                                            (y_plots, x_plots),
                                            (j0_row, i0_line),\
                                            colspan=axes_extents[j][i][0],
                                            rowspan=axes_extents[j][i][1]))
            i0_line += axes_extents[j][i][0]
        j0_row += axes_extents[j][i][1]
        AX.append(AX_line)
        
    plt.annotate(with_top_left_letter, (0.01,.99),
                 xycoords='figure fraction',
                 fontsize=fontsize+1, fontweight='bold')

    if len(AX)==1 and (len(AX[0])==1):
        return fig, AX[0][0]
    elif len(AX[0])==1:
        return fig, [AX[i][0] for i in range(len(AX))]
    elif len(AX)==1:
        return fig, AX[0]
    else:
        return fig, AX
    
if __name__=='__main__':
    from graphs.my_graph import *
    figure()
    figure(axes_extents=[\
                         [[3,1], [1,1] ],
                         [[1,1], [2,1], [1,1] ] ] )
    figure(axes_extents=[\
                         [[3,2], [1,2] ],
                         [[1,1], [2,1], [1,1] ] ] )
    show()

