import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from graphs.dependencies import *
from graphs.scaling import mm2inch
from graphs.inset import add_inset

A0_format = {'width':8.3, 'height':11.7}

def dimension_calculus(cls,
                       figsize,
                       left, right,
                       bottom, top,
                       wspace, hspace,
                       x_plots, y_plots):
    """
    calculate the dimension quantities required by *matplotlib* plt.figure object
    """
    dimension = {}
    
    # horizontal 
    dimension['full_width'] = left*cls.left_size+\
        right*cls.right_size+\
        x_plots*figsize[0]*cls.single_plot_size[0]+\
        wspace*(x_plots-1)*cls.wspace_size
    dimension['left'] = left*cls.left_size/dimension['full_width']
    dimension['right'] = right*cls.right_size/dimension['full_width']
    dimension['wspace'] = wspace*cls.wspace_size/figsize[0]/cls.single_plot_size[0]

    # vertical
    dimension['full_height'] = bottom*cls.bottom_size+\
        top*cls.top_size+\
        y_plots*figsize[1]*cls.single_plot_size[1]+\
        hspace*(y_plots-1)*cls.hspace_size
    dimension['bottom'] = bottom*cls.bottom_size/dimension['full_height']
    dimension['top'] = top*cls.top_size/dimension['full_height']
    dimension['hspace'] = hspace*cls.hspace_size/figsize[1]/cls.single_plot_size[1]

    return dimension


def figure(cls,
           axes = (1,1),
           axes_extents=None,
           grid=None,
           figsize=(1.,1.),
           left=1., right=1.,
           bottom=1., top=1.,
           wspace=1., hspace=1.,
           with_top_left_letter='',
           Single_Plot_Size=(0.2,0.12),
           fontsize=9,
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

        dim =  dimension_calculus(cls, figsize,left, right, bottom, top, wspace, hspace, x_plots, y_plots)
        
        fig = plt.figure(figsize=(mm2inch(dim['full_width']),
                                  mm2inch(dim['full_height'])))
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

        dim =  dimension_calculus(cls, figsize,left, right, bottom, top, wspace, hspace, x_plots, y_plots)
        
        fig = plt.figure(figsize=(mm2inch(dim['full_width']),
                                  mm2inch(dim['full_height'])))
        
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


    
    if dim['left']>=(1-dim['right']):
        print('left=%.2f and right=%.2f leads to a too large space' % (dim['left'], dim['right']),
              'set to 0.2, & 0.95 respectively')
        dim['left'], dim['right'] = 0.2, 0.95
    if dim['bottom']>=(1-dim['top']):
        print('left=%.2f and right=%.2f leads to a too large space' % (dim['bottom'], dim['top']),
              'set to 0.2, & 0.95 respectively')
        dim['bottom'], dim['top'] = 0.2, 0.95

        
    # # Subplots placements adjustements
    plt.subplots_adjust(left=dim['left'],
                        bottom=dim['bottom'],
                        top=1.-dim['top'],
                        right=1.-dim['right'],
                        wspace=dim['wspace'],
                        hspace=dim['hspace'])

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
    fig, ax = figure(right=5.5)
    
def figure_with_bar_legend(shift_up=0., shrink=1.):

    fig, ax = figure_with_legend_space()
    acb = add_inset(ax, [1.17, -.08+shift_up, .08, shrink*1.])

    return fig, ax, acb
    
if __name__=='__main__':
    
    import itertools, string
    
    import datavyz
    ge = datavyz.graph_env('manuscript')

    # fig, ax = ge.figure()
    fig1, AX1 = ge.figure(axes=(2,2))
    fig2, AX2 = ge.figure(axes_extents=[\
                                        [[1,1], [1,1], [1,1]],
                                        [[2,2], [1,2]]])
    fig3, AX3 = ge.figure(axes_extents=[\
                                        [[3,1], [1,1]],
                                        [[4,1]],
                                        [[1,1], [2,1], [1,1] ] ],
                          figsize=[.95,.95])
    for i, fig, AX in zip(range(3), [fig1, fig2, fig3], [AX1, AX2, AX3]):
        for l, ax in zip(list(string.ascii_lowercase), itertools.chain(*AX)):
            ge.top_left_letter(ax, l+'     ')
            ge.set_plot(ax, xlabel='xlabel (xunit)', ylabel='ylabel (yunit)', grid=True)

        fig.savefig('fig%i.svg' % int(i+1))
    ge.show()

