import numpy as np
from matplotlib.pylab import Circle, setp

def pie(graph, data,
        ax=None,
        ext_labels= None,
        pie_labels = None,
        explodes=None,
        COLORS=None,
        ext_labels_distance = 1.1,
        pie_labels_distance = 0.6,
        ext_text_settings=dict(weight='normal'),
        pie_text_settings=dict(weight='bold', color='k'),
        center_circle=0.3,
        title='',
        fig_args=dict(bottom=0.3, left=0.3, top=3.),
        axes_args={},
        legend=None):

    """    
    return fig, ax
    """
    
    # getting or creating the axis
    if ax is None:
        if legend is not None:
            fig, ax = graph.figure(with_legend_space=True)
        else:
            fig, ax = graph.figure(**fig_args)
    else:
        fig = graph.gcf()
        
    if COLORS is None:
        COLORS = graph.colors[:len(data)]
    if (explodes is None):
        explodes = np.zeros(len(data))
    if (ext_labels is None):
        ext_labels = np.zeros(len(data), dtype=str)

    if pie_labels is not None:
        pie_labels_map = {}
        for pl, val in zip(pie_labels, data):
            pie_labels_map[str(np.round(100.*val/data.sum(),2))] = pl
        def func(pct):
            return pie_labels_map[str(np.round(pct,2))]
        print(pie_labels_map)
    else:
        def func(pct):
            return ''
        
    
    wedges, ext_texts, pie_texts = ax.pie(data,
                                      labels=ext_labels,
                                      autopct=func,
                                      explode=explodes,
                                      pctdistance=pie_labels_distance,
                                      labeldistance=ext_labels_distance,
                                      colors=COLORS)
    setp(pie_texts, **pie_text_settings)
    setp(ext_texts, **ext_text_settings)
    
    Centre_Circle = Circle((0,0), center_circle, fc='white')
    ax.add_artist(Centre_Circle)
                                  
    if legend is not None:
        if 'loc' not in legend:
            legend['loc']=(1.21,.2)
        ax.legend(**legend)

    if title!='':
        graph.title(ax, title)
        
    ax.axis('equal')
    return fig, ax

if __name__=='__main__':
    
    from my_graph import graphs
    import matplotlib.pylab as plt
    mg = graphs()
    data = .5+np.random.randn(3)*.4
    fig, ax = mg.pie(data,
                     ext_labels = ['Data1', 'Data2', 'Data3'],
                     pie_labels = ['%.1f%%' % (100*d) for d in data],
                     ext_labels_distance=1.2,
                     explodes=[.05,.05,.05],
                     center_circle=0.2,
                     COLORS = [mg.tab20(x) for x in np.linspace(0,1,len(data))],
                     legend={})
    mg.show()
