"""
In this module we rewrite the function for compatibility with
a dark-theme emacs notebook
"""
import sys, os, platform
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep
# module that construct the plot settings

import matplotlib as mpl
import matplotlib.pylab as plt
import numpy as np

plt.style.use('dark_background')

FONTSIZE = 12
def update_rcParams():
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
update_rcParams()

# ##############################
# ######### draw figure ########
# ##############################
import graphs.draw_figure as df
def figure(axes = (1,1),
           axes_extents=None,
           figsize=(1.,1.),
           left=1., right=1.,
           bottom=1., top=1.,
           wspace=1., hspace=1.,
           with_top_left_letter='',
           fontsize=FONTSIZE, fontweight='bold'):
    update_rcParams()
    return df.figure(axes, axes_extents,
           2.*np.array(figsize), # factor here
           left, right, bottom, top, wspace, hspace,
           with_top_left_letter, fontsize, fontweight)
def figure_with_bar_legend(shift_up=0., shrink=1.):
    fig, ax = figure(figsize=(3.,2.), right=5.5, fontsize=FONTSIZE)
    acb = add_inset(ax, [1.17, -.08+shift_up, .08, shrink*1.])
    return fig, ax, acb

# ##############################
# ######### adjust plot ########
# ##############################
import graphs.adjust_plots as ap
def adjust_spines(ax, spines, tck_outward=3, tck_length=4.,
                  xcolor='w', ycolor='w'):
    ap.adjust_spines(ax, spines, tck_outward=3, tck_length=4.,
                         xcolor=xcolor, ycolor=ycolor)
def set_plot(ax, spines=['left', 'bottom'],
             num_xticks=3, num_yticks=3,
             xlabel='', ylabel='',
             tck_outward=3, tck_length=4,
             xticks=None, yticks=None,
             xminor_ticks=None, yminor_ticks=None,
             xticks_labels=None, yticks_labels=None,
             xlabelpad=1.5, ylabelpad=1.5,
             xticks_rotation=0, yticks_rotation=0,
             xscale='linear', yscale='linear',
             xlim_enhancment=1., ylim_enhancment=1.,
             xlim=None, ylim=None,
             grid=False,
             xcolor='w', ycolor='w',
             fontsize=FONTSIZE):
    ap.set_plot(ax, spines,
                       num_xticks, num_yticks,
                       xlabel, ylabel, tck_outward, tck_length,
                       xticks, yticks, xminor_ticks, yminor_ticks,
                       xticks_labels, yticks_labels,
                       xlabelpad, ylabelpad,
                       xticks_rotation, yticks_rotation,
                       xscale, yscale,
                       xlim_enhancment, ylim_enhancment,
                       xlim, ylim, grid, xcolor, ycolor, fontsize)
    

##############################
######### adjust plot ########
##############################
# custom colors
from matplotlib.cm import viridis, viridis_r, copper, copper_r, cool, jet, PiYG
from graphs.my_graph import Blue, Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan, Color_List, save_on_desktop
from graphs.my_graph import plot, hist, scatter, annotate, show
from graphs.annotations import from_pval_to_star, sci_str, int_to_roman
import graphs.annotations as annot
def draw_bar_scales(ax, xyLoc, Xbar, Xbar_label, Ybar, Ybar_label,
                    orientation='left-bottom',
                    Xbar_label2='',Ybar_label2='',
                    xcolor='w', ycolor='w', ycolor2='w',
                    fontsize=FONTSIZE-1,
                    shift_factor=20., color='w', lw=1):
    annot.draw_bar_scales(ax, xyLoc,
                                 Xbar, Xbar_label, Ybar, Ybar_label,
                                 orientation,
                                 Xbar_label2,Ybar_label2,
                                 xcolor, ycolor, ycolor2,
                                 fontsize, shift_factor, color, lw)
import graphs.line_plots as line_plots
import graphs.scatter_plots as scatter_plots
from graphs.inset import add_inset
from graphs.legend import get_linear_colormap, build_bar_legend, build_bar_legend_continuous, bar_legend, legend

    
if __name__=='__main__':

    fig2, AX = figure(axes=(2,1))
    for ax in AX:
        scatter(np.abs(np.exp(np.random.randn(100))), np.abs(np.exp(np.random.randn(100))), ax=ax)
        set_plot(ax, yscale='log', xscale='log')
    show()

