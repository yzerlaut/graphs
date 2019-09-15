import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.dependencies import *
from scipy.stats.stats import pearsonr
from graphs.legend import get_linear_colormap, build_bar_legend
from graphs.hist_plots import hist

def cross_correl_plot(graph,
                      data, FIGSIZE=(7,7), wspace=.5, hspace=.5, right=0.98, left=0.1,\
                      many_data=False):
    """
    'data' should be a dictionary with "features" keys whose values are the instances
    """

    fig, AX = plt.subplots(len(data)-1, len(data)-1, figsize=FIGSIZE)
    plt.subplots_adjust(wspace=wspace, hspace=hspace, right=right, left=left)

    mymap = get_linear_colormap(color1='white', color2='gray')

    significance = np.array([1e-3, 2e-2, 1e-1, 1])
    
    for i, key_i in enumerate(data.keys()):
        for j, key_j in enumerate(list(data.keys())[i+1:]):
            AX[j-1,i].plot(data[key_i], data[key_j], 'ko')
            if not many_data:
                graph.set_plot(AX[j-1,i], xlabel=key_i, ylabel=key_j,
                                    num_xticks=4, num_yticks=3)
            else:
                if ((i==0) and (j==len(data)-1)):
                    graph.set_plot(AX[j-1,i], xlabel=key_i, ylabel=key_j,
                                    num_xticks=4, num_yticks=3)

                elif (j==len(data)-1):
                    graph.set_plot(AX[j-1,i], xlabel=key_i, yticks_labels=[],
                                    num_xticks=4, num_yticks=3)
                elif (i==0):
                    graph.set_plot(AX[j-1,i], ylabel=key_j, xticks_labels=[],
                                    num_xticks=4, num_yticks=3)
                else:
                    graph.set_plot(AX[j-1,i], xticks_labels=[], yticks_labels=[],
                                    num_xticks=4, num_yticks=3)

            cc, pp = pearsonr(data[key_i], data[key_j])
            
            x = np.linspace(data[key_i].min(), data[key_i].max())
            AX[j-1, i].plot(x,\
                np.polyval(np.polyfit(np.array(data[key_i], dtype='f8'),\
                                      np.array(data[key_j], dtype='f8'), 1), x),\
                                      'k--', lw=.5)

            ii = np.arange(len(significance))[significance-pp>=0][0]
            color = -1.*(ii-len(significance)+1)/(len(significance)-1)
            xmin, xmax = AX[j-1, i].get_xaxis().get_view_interval()
            ymin, ymax = AX[j-1, i].get_yaxis().get_view_interval()
            AX[j-1, i].add_patch(plt.Rectangle((xmin, ymin),\
                                               xmax-xmin, ymax-ymin, color=mymap(1.*color,1)))

    ax = plt.axes([.7,.7,.02,.2])
    build_bar_legend(np.arange(len(significance)+1),\
                     ax, mymap,\
                     ticks_labels=['n.s.', '$<$0.1', '$<$0.02', '$<$0.001'],
                     label='Significance \n \n (p, Pearson correl.)')
                 
    for ax in AX.flatten():
        if ax.get_xaxis().get_view_interval()[1]==1.:
            ax.axis('off')

    return fig

def features_plot(graph, data, features=None,
                  FIGSIZE=(9,7), wspace=.5, hspace=.5, right=0.8, left=0.1,\
                  ms=3, many_data=False):
    """
    'data' should be an array of dictionaries with keys 'vec' and labels 'label'
    """

    if features is None:
        features = list(data.keys())
        
    fig, AX = plt.subplots(len(data), len(data), figsize=FIGSIZE)
    plt.subplots_adjust(wspace=wspace, hspace=hspace, right=right, left=left)

    mymap = get_linear_colormap(color1='white', color2='gray')

    significance = np.array([1e-3, 2e-2, 1e-1, 1])

    LIMS = [[np.inf, -np.inf] for f in features]
    for i, key_i in enumerate(features):
        for j, key_j in enumerate(features):
            if i==j:
                hist(graph, data[key_i], ax=AX[i,i])
            else:
                AX[j,i].plot(data[key_i], data[key_j], 'ko', ms=ms)
                cc, pp = pearsonr(data[key_i], data[key_j])
                x = np.linspace(data[key_i].min(), data[key_i].max())
                AX[j,i].plot(x,\
                    np.polyval(np.polyfit(np.array(data[key_i], dtype='f8'),\
                                          np.array(data[key_j], dtype='f8'), 1), x),\
                                          'k--', lw=.5)

                ii = np.arange(len(significance))[significance-pp>=0][0]
                color = -1.*(ii-len(significance)+1)/(len(significance)-1)
                xmin, xmax = AX[j,i].get_xaxis().get_view_interval()
                ymin, ymax = AX[j,i].get_yaxis().get_view_interval()
                AX[j,i].add_patch(plt.Rectangle((xmin, ymin),\
                                                   xmax-xmin, ymax-ymin, color=mymap(1.*color,1)))

                graph.set_plot(AX[j,i], num_xticks=3, num_yticks=3)
                LIMS[i] = [xmin, xmax]
                
    for i, key_i in enumerate(features):
        for j, key_j in enumerate(features):
            
            if (i==0) and (j==0):
                graph.set_plot(AX[j,i], ['bottom', 'left'],
                               xlim=LIMS[i], num_xticks=3, num_yticks=1,
                               yticks_labels=[], xticks_labels=[], ylabel=key_i)
            elif (i==j) and (j==len(data)-1):
                graph.set_plot(AX[j,i], ['bottom'],
                               xlim=LIMS[i], num_xticks=3, xlabel=key_i)
            elif (i==j):
                graph.set_plot(AX[j,i], ['bottom'],
                               xlim=LIMS[i], num_xticks=3, xticks_labels=[])
            elif ((i==0) and (j==len(data)-1)):
                graph.set_plot(AX[j,i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               xlabel=key_i, ylabel=key_j,
                               num_xticks=3, num_yticks=3, yticks_labels=[])
            elif (j==len(data)-1):
                graph.set_plot(AX[j,i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               xlabel=key_i,
                               num_xticks=3, num_yticks=3, yticks_labels=[])
            elif (i==0):
                graph.set_plot(AX[j,i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               ylabel=key_j,
                               num_xticks=3, num_yticks=3, xticks_labels=[], yticks_labels=[])
            else:
                graph.set_plot(AX[j,i],
                               xlim=LIMS[i], ylim=LIMS[j],
                               num_xticks=3, num_yticks=3, yticks_labels=[], xticks_labels=[])

    ax = plt.axes([.85,.3,.02,.3])
    build_bar_legend(np.arange(len(significance)+1),\
                     ax, mymap,\
                     ticks_labels=['n.s.', '$<$0.1', '$<$0.02', '$<$0.001'],
                     label='Significance \n \n (p, Pearson correl.)')
                 

    return fig

if __name__=='__main__':

    data = {}
    for i in range(7):
        data['feature_%s'%(i+1)] = np.random.randn(30)

    from graphs.my_graph import graphs
    mg = graphs()
    # cross_correl_plot(mg, data, many_data=True)
    features_plot(mg, data, ms=3)
    mg.show()
