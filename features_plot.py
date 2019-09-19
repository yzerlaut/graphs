import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.dependencies import *
from scipy.stats.stats import pearsonr
from graphs.legend import get_linear_colormap, build_bar_legend
from graphs.hist_plots import hist

def features_plot(graph, data,
                  features=None,
                  nrow_fig=5,
                  shrink_fig=0.3,
                  wspace=.5, hspace=.5, right=0.8, left=0.1,\
                  ms=3, many_data=False):
    """
    'data' should be an array of dictionaries with keys 'vec' and labels 'label'
    """

    if features is None:
        features = list(data.keys())
        
    fig, AX = graph.figure(axes=(int(np.ceil(len(features)/nrow_fig)), nrow_fig), hspace=2.)

    LIMS = [[np.inf, -np.inf] for f in features]
    for i, key_i in enumerate(features):
        hist(graph, data[key_i], ax=np.ravel(AX)[i],
             ylabel='', xlabel=key_i, axes_args={'spines':'bottom'})

    for i in range(len(features), len(np.ravel(AX))):
        np.ravel(AX)[i].axis('off')
        
    return fig

if __name__=='__main__':

    from graphs.my_graph import graphs
    mg = graphs()

    # breast cancer dataset from sklearn
    from sklearn.datasets import load_breast_cancer
    raw = load_breast_cancer()
    data = {}
    for feature, values in zip(raw['feature_names'], raw['data']):
        data[feature+'\n(log)'] = np.log(values)
    features_plot(mg, data, ms=3)
    mg.show()

