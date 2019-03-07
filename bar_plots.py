from scipy.stats import ttest_rel, ttest_ind
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.draw_figure import figure
from graphs.adjust_plots import set_plot

def related_samples_two_conditions_comparison(first_observations,
                                              second_observations,
                                              with_annotation=True,
                                              xticks_rotation=0,
                                              lw=.5,
                                              color1='#1f77b4', color2='#ff7f0e',
                                              ylabel='value',
                                              xticks=[0, 1],
                                              xticks_labels=['cond1', 'cond2'],
                                              colormap=None):

    if len(first_observations)!=len(second_observations):
        print('Pb with sample size !! Test is not applicable !!')

    pval = ttest_rel(first_observations, second_observations)[1]

    if colormap is None:
        def colormap(x):return 'k'
        
    fig, ax = figure(figsize=(.6,1.))
    
    for i in range(len(first_observations)):
        ax.plot([0, 1], [first_observations[i], second_observations[i]], '-', lw=lw, color=colormap(i/(len(first_observations)-1)))
        
    ax.bar([0], [np.mean(first_observations)], yerr=np.std(first_observations), color=color1, lw=lw)
    ax.bar([1], [np.mean(second_observations)], yerr=np.std(second_observations), color=color2, lw=lw)
    
    if with_annotation:
        ax.annotate('paired t-test:\n p=%.2f' % pval, (.99,.4), xycoords='axes fraction')
        
    set_plot(ax, ylabel=ylabel,
             xticks=xticks,
             xticks_labels=xticks_labels,
             xticks_rotation=xticks_rotation)
    
    return fig, ax, pval

def unrelated_samples_two_conditions_comparison(first_observations,
                                              second_observations,
                                              with_annotation=True,
                                              xticks_rotation=0,
                                              lw=.5,
                                              color1='#1f77b4', color2='#ff7f0e',
                                              ylabel='value',
                                              xticks=[0, 1],
                                              xticks_labels=['cond1', 'cond2']):

    pval = ttest_ind(first_observations, second_observations)[1]

    fig, ax = figure(figsize=(.6,1.))
    
    for i in range(len(first_observations)):
        ax.plot([0+np.random.randn()*.1], [first_observations[i]], 'o', ms=2, color=color1)
        ax.plot([1+np.random.randn()*.1], [second_observations[i]], 'o', ms=2, color=color2)
        
    ax.bar([0], [np.mean(first_observations)], yerr=np.std(first_observations), color=color1, lw=lw, alpha=.7)
    ax.bar([1], [np.mean(second_observations)], yerr=np.std(second_observations), color=color2, lw=lw, alpha=.7)
    
    if with_annotation:
        ax.annotate('unpaired t-test:\n p=%.2f' % pval, (.99,.4), xycoords='axes fraction')
        
    set_plot(ax, ylabel=ylabel,
             xticks=xticks,
             xticks_labels=xticks_labels,
             xticks_rotation=xticks_rotation)
    
    return fig, ax, pval

if __name__=='__main__':

    from graphs.my_graph import *
    
    unrelated_samples_two_conditions_comparison(np.random.randn(10)+1.4, np.random.randn(12)+1.4,
                                              xticks_labels=['$\||$cc($V_m$,$V_{ext}$)$\||$', '$cc(V_m,pLFP)$'],
                                              xticks_rotation=90)
    
    show()
