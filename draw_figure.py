import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE, A0_format, Single_Plot_Size
import matplotlib.pylab as plt
import numpy as np
from graphs.inset import add_inset


def figure(axes = (1,1),
           axes_extents=None,
           grid=None,
           figsize=(1.,1.),
           left=1., right=1.,
           bottom=1., top=1.,
           wspace=1., hspace=1.,
           with_top_left_letter='',
           fontsize=FONTSIZE,
           fontweight='bold'):
    
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
    |-----------------------|
    Y     |           |     |
    |(1,1)|   (2,1)   |(1,1)|
    |     |           |     |
    |------------------------
    |
    v

    TO PRODUCE THIS, RUN:
    figure(axes_extents=[\
                         [[3,1], [1,1] ],
                         [[1,1], [2,1], [1,1] ] ] )
    show()


    OTHERWISE, you can use the "grid" arguments that corresponds to "subplot2grid"
    TO PRODUCE THIS, RUN:
    figure(grid=[(0,0,1,4),
                 (x,y,dx,dy)])

    """

    AX = []
    
    if grid is not None:
        x_plots = np.max([g[0]+g[2] for g in grid])
        y_plots = np.max([g[1]+g[3] for g in grid])
        fig = plt.figure(figsize=(A0_format['width']*Single_Plot_Size[0]*x_plots*figsize[0], A0_format['height']*Single_Plot_Size[1]*y_plots*figsize[1]))
        for g in grid:
            ax = plt.subplot2grid((y_plots, x_plots),
                                  (g[1], g[0]),
                                  colspan=g[2],
                                  rowspan=g[3])
            AX.append(ax)
    else:
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
        fig = plt.figure(figsize=(A0_format['width']*Single_Plot_Size[0]*x_plots*figsize[0], A0_format['height']*Single_Plot_Size[1]*y_plots*figsize[1]))
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

    if left*0.55/figsize[0]>=1.-right*0.1/figsize[1]:
        print('left=%.2f and right=%.2f leads to a too large space' % (left, right),
              'set to 0.01, & 0.99 respectively')
        left, right = 0.01, 0.99
    if bottom*0.5/figsize[1]>=1.-top*0.1/figsize[0]:
        print('bottom=%.2f and top=%.2f leads to a too large space' % (bottom, top),
              'set to 0.01, & 0.99 respectively')
        bottom, top = 0.01, 0.99
        
    # # Subplots placements adjustements
    plt.subplots_adjust(left=left*0.55/figsize[0], # 0.5cm by default
                        bottom=bottom*0.5/figsize[1],# 0.5cm by default
                        top=1.-top*0.1/figsize[0], # 0.1cm by default
                        right=1.-right*0.1/figsize[1],# 0.1cm by default
                        wspace=wspace*0.5/figsize[0]*x_plots, # 0.5cm by default
                        hspace=hspace*0.5/figsize[1]*y_plots) # 0.5cm by default

    plt.annotate(with_top_left_letter, (0.01,.99),
                 xycoords='figure fraction',
                 fontsize=fontsize+1, fontweight='bold')

    if grid is not None:
        return fig, AX
    elif len(AX)==1 and (len(AX[0])==1):
        return fig, AX[0][0]
    elif (len(AX[0])==1) and (len(AX[-1])==1):
        return fig, [AX[i][0] for i in range(len(AX))]
    elif len(AX)==1:
        return fig, AX[0]
    else:
        return fig, AX

def figure_with_legend_space():
    fig, ax = figure(figsize=(1.5,1.), right=5.5)
    
def figure_with_bar_legend(shift_up=0., shrink=1.):

    fig, ax = figure_with_legend_space()
    acb = add_inset(ax, [1.17, -.08+shift_up, .08, shrink*1.])

    return fig, ax, acb
    
if __name__=='__main__':
    
    from graphs.my_graph import graphs
    mg = graphs()
    # mg.figure()
    fig, _ = mg.figure(axes_extents=[\
                                  [[3,1], [1,1] ],
                                  [[1,1], [2,1], [1,1] ] ] )
    # figure(axes_extents=[\
    #                      [[3,2], [1,2] ],
    #                      [[1,1], [2,1], [1,1] ] ] )
    # fig, ax, acb = figure_with_bar_legend()
    fig.savefig('fig.png')
    mg.show()

