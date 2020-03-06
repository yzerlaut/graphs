import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))


from scipy.stats.stats import pearsonr

from graphs.dependencies import *

from graphs.legend import get_linear_colormap, build_bar_legend
from graphs.hist_plots import hist

def cross_correl_plot(graph, data, features=None,
                      figsize=(.8,.7),
                      fig_args=dict(left=0.1, bottom=0.1, right=1.4, top=0.1, wspace=0.1, hspace=0.1),
                      ms=3, many_data=False):
    """
    'data' should be an array of dictionaries with keys 'vec' and labels 'label'
    """

    if features is None:
        features = list(data.keys())
        
    fig, AX = graph.figure(axes=(len(features), len(features)), figsize=figsize, **fig_args)

    mymap = graph.get_linear_colormap(color1='white', color2='gray')

    significance = np.array([1e-3, 2e-2, 1e-1, 1])

    LIMS = [[np.inf, -np.inf] for f in features]
    for i, key_i in enumerate(features):
        for j, key_j in enumerate(features):
            if i==j:
                graph.hist(data[key_i], ax=AX[i][i])
            else:
                AX[j][i].plot(data[key_i], data[key_j], 'ko', ms=ms)
                cc, pp = pearsonr(data[key_i], data[key_j])
                x = np.linspace(data[key_i].min(), data[key_i].max())
                AX[j][i].plot(x,\
                    np.polyval(np.polyfit(np.array(data[key_i], dtype='f8'),\
                                          np.array(data[key_j], dtype='f8'), 1), x),\
                                          'k--', lw=.5)

                ii = np.arange(len(significance))[significance-pp>=0][0]
                color = -1.*(ii-len(significance)+1)/(len(significance)-1)
                xmin, xmax = AX[j][i].get_xaxis().get_view_interval()
                ymin, ymax = AX[j][i].get_yaxis().get_view_interval()
                AX[j][i].add_patch(plt.Rectangle((xmin, ymin),\
                                                 xmax-xmin, ymax-ymin, color=mymap(1.*color,1)))

                graph.set_plot(AX[j][i], num_xticks=3, num_yticks=3)
                LIMS[i] = [xmin, xmax]
                
    for i, key_i in enumerate(features):
        for j, key_j in enumerate(features):
            
            if (i==0) and (j==0):
                graph.set_plot(AX[j][i], ['bottom', 'left'],
                               xlim=LIMS[i], num_xticks=3, num_yticks=1,
                               yticks_labels=[], xticks_labels=[], ylabel=key_i)
            elif (i==j) and (j==len(features)-1):
                graph.set_plot(AX[j][i], ['bottom'],
                               xlim=LIMS[i], num_xticks=3, xlabel=key_i)
            elif (i==j):
                graph.set_plot(AX[j][i], ['bottom'],
                               xlim=LIMS[i], num_xticks=3, xticks_labels=[])
            elif ((i==0) and (j==len(features)-1)):
                graph.set_plot(AX[j][i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               xlabel=key_i, ylabel=key_j,
                               num_xticks=3, num_yticks=3, yticks_labels=[])
            elif (j==len(features)-1):
                graph.set_plot(AX[j][i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               xlabel=key_i,
                               num_xticks=3, num_yticks=3, yticks_labels=[])
            elif (i==0):
                graph.set_plot(AX[j][i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               ylabel=key_j,
                               num_xticks=3, num_yticks=3, xticks_labels=[], yticks_labels=[])
            else:
                graph.set_plot(AX[j][i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               num_xticks=3, num_yticks=3, yticks_labels=[], xticks_labels=[])

    ax = plt.axes([.85,.3,.02,.3])
    graph.build_bar_legend(np.arange(len(significance)+1),\
                           ax, mymap,\
                           ticks_labels=['n.s.', '$<$0.1', '$<$0.02', '$<$0.001'],
                           label='Significance \n \n (p, Pearson correl.)')
                 

    return fig

if __name__=='__main__':

    import os
    
    import datavyz
    ge = datavyz.graph_env('manuscript')


    # building random data
    data = {}
    for i in range(7):
        data['feature_%s'%(i+1)] = np.random.randn(30)

    fig = mg.cross_correl_plot(data,
                               features=list(data.keys())[:7])
    
    fig_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),'docs/cross-correl.png')
    fig.savefig(fig_location, dpi=200)
    print('Figure saved as: ', fig_location)
    mg.show()

