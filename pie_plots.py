import numpy as np

def pie(graph, data,
        COLORS=None,
        LABELS=None,
        EXPLODES=None,
        ax=None,
        autopct='%1.1f%%',
        lw=0, alpha=1.,
        title='',
        fig_args={},
        axes_args={},
        legend_args=None):

    """    
    return fig, ax
    """
    
    # getting or creating the axis
    if ax is None:
        fig, ax = graph.figure(**fig_args, bottom=0.3, left=0.3, top=3.)
        
    if COLORS is None:
        COLORS = graph.colors[:len(data)]
    if (LABELS is None) or (len(LABELS)!=len(data)):
        # print('need to set up labels')
        # LABELS = [str(i+1) for i in range(len(data))]
        LABELS = []
    if (EXPLODES is None):
        EXPLODES = np.zeros(len(data))
        
    ax.pie(data,
           labels=LABELS,
           autopct=autopct,
           explode=EXPLODES,
           colors=COLORS)

    if legend_args is not None:
        ax.legend(**legend_args)

    if title!='':
        graph.title(ax, title)
        
    ax.axis('equal')
    return ax

if __name__=='__main__':
    
    from my_graph import graphs
    mg = graphs()
    mg.pie([0.3, 0.3, 0.4], title='Title', LABELS=['Data1', 'Data2', 'Data3'], EXPLODES=[0,.1,0])
    mg.show()
