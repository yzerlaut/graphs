import sys, os, platform
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep
# module that construct the plot settings
import graphs.draw_figure as df
import graphs.adjust_plots as ap

import numpy as np
from graphs.annotations import *
import graphs.line_plots as line_plots
import graphs.scatter_plots as scatter_plots
from graphs.hist_plots import hist
from graphs.inset import add_inset
from graphs.legend import *

# custom colors
from matplotlib.cm import viridis, viridis_r, copper, copper_r, cool, jet, PiYG
Blue, Orange, Green, Red, Purple, Brown, Pink, Grey,\
    Kaki, Cyan = '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',\
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
Color_List = [Blue, Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan]

def save_on_desktop(fig, figname='temp.svg'):
    fig.savefig(desktop+figname)

def update_rcParams(FONTSIZE):
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
    
class graphs:
    
    
    def __init__(self, output_display='manuscript', color='k'):
        """
        accepts styles such as : manuscript, dark_notebook, ggplot_notebook, ...
        """
        if output_display=='manuscript':
            self.FONTSIZE = 8
            self.size_factor = 1.
            self.default_color = 'k'
        else:
            self.FONTSIZE = 12
            self.size_factor = 2.
            
        self.default_color = color

        self.override_style=True
        if len(output_display.split('dark'))>1:
            self.set_style('dark_background')
            self.default_color = 'lightgray'
        elif len(output_display.split('ggplot'))>1:
            self.default_color = 'dimgrey'
            self.set_style('ggplot')
            self.override_style = False
        elif len(output_display.split('seaborn'))>1:
            self.set_style('seaborn')
            self.override_style = False
        
        update_rcParams(self.FONTSIZE)
        self.colors = [Blue, Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan]
        self.b, self.o, self.g, self.r, self.purple, self.brown,\
            self.pink, self.grey, self.kaki, self.cyan = Blue,\
                            Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan
        self.viridis, self.viridis_r, self.copper, self.copper_r, self.cool, self.jet,\
            self.PiYG = viridis, viridis_r, copper, copper_r, cool, jet, PiYG
        self.cmaps = [viridis, viridis_r, copper, copper_r, cool, jet, PiYG]
        self.blue_to_red = get_linear_colormap(Blue, Red)
        self.red_to_blue = get_linear_colormap(Red, Blue)
        self.blue_to_orange = get_linear_colormap(Blue, Orange)
        self.green_to_red = get_linear_colormap(Green, Red)
        self.red_to_green = get_linear_colormap(Red, Green)
        self.green_to_orange = get_linear_colormap(Green, Orange)
        self.orange_to_green = get_linear_colormap(Orange, Green)
        
        
    def set_style(self, style='default'):
        plt.style.use(style)
        if style=='dark_background':
            self.default_color = 'w'

    def figure(self,
               axes = (1,1),
               axes_extents=None,
               figsize=(1.,1.),
               left=1., right=1.,
               bottom=1., top=1.,
               wspace=1., hspace=1.,
               with_space_for_bar_legend=False,
               shift_up=0., shrink=1.):
        
        if with_space_for_bar_legend:
            fig, ax = df.figure(axes, axes_extents,
                                figsize=self.size_factor*np.array((1.5,1.)),
                                right=5.5,
                                fontsize=self.FONTSIZE)
            acb = df.add_inset(ax, [1.17, -.08+shift_up, .08, shrink*1.])
            return fig, ax, acb
        else:
            fig, AX = df.figure(axes, axes_extents,
                                self.size_factor*np.array(figsize),
                                left, right, bottom, top, wspace, hspace)
            return fig, AX

    def figure_with_bar_legend(self, shift_up=0., shrink=1.):
        fig, ax = self.figure(figsize=(1.5,1.), right=5.5)
        acb = add_inset(ax, [1.17, -.08+shift_up, .08, shrink*1.])
        return fig, ax, acb
        

    def plot(self,
             x=None, y=None, sy=None, color=None,
             X=None, Y=None, sY=None,
             COLORS=None, colormap=viridis,
             ax=None,
             lw=1, alpha_std=0.3, ms=0, m='', ls='-',
             xlabel='', ylabel='', bar_label='',
             label=None,
             LABELS=None,
             fig_args={},
             axes_args={},
             bar_legend_args=None,
             legend_args=None):
        
        """    
        return fig, ax
        """
        # getting or creating the axis
        if ax is None:
            fig, ax = self.figure(**fig_args)
        if color is None:
            color = self.default_color
            
        if (y is None) and (Y is None):
            y = x
            x = np.arange(len(y))

        if (Y is not None):
            if (X is None) and (x is not None):
                X = [x for i in range(len(Y))]
            elif (X is None):
                X = [np.arange(len(y)) for y in Y]

            line_plots.multiple_curves(ax, X, Y, sY, COLORS, LABELS,
                                       alpha_std=alpha_std,
                                       colormap=colormap,
                                       lw=lw, ls=ls, m=m, ms=ms)
        else:
            line_plots.single_curve(ax, x, y, sy,
                                    color=color,
                                    alpha_std=alpha_std,
                                    lw=lw, label=label, ls=ls, m=m, ms=ms)

        if bar_legend_args is not None:
            cb = add_inset(ax, **bar_legend_args)
            build_bar_legend(np.arange(len(LABELS)+1),
                             cb,
                             colormap,
                             label=bar_label,
                             ticks_labels=LABELS)

        if legend_args is not None:
            ax.legend(**legend_args)

        if 'xlabel' not in axes_args:
            axes_args['xlabel'] = xlabel
        if 'ylabel' not in axes_args:
            axes_args['ylabel'] = ylabel
        self.set_plot(ax, **axes_args)

        return ax
        
    ################################################
    ###### Annotate function #######################
    ################################################
    def annotate(self, stuff, s,
                 xy, xycoords='axes fraction', bold=False, italic=False, rotation=0,
                 fontsize=None, size=None, color=None, ha='left', va='bottom', weight='normal', style='normal'):
        """
        """
        if fontsize is None:
            fontsize=self.FONTSIZE
        if size=='small':
            fontsize=self.FONTSIZE-1
        elif size=='x-small':
            fontsize=self.FONTSIZE-2
        if color is None:
            color=self.default_color
        if bold and (weight=='normal'):
            weight = 'bold'
        if italic and (style=='normal'):
            style = 'italic'

        if type(stuff)==mpl.figure.Figure: # if figure, no choice, if figure relative coordinates
            plt.annotate(s, xy, xycoords='figure fraction',
                         weight=weight, fontsize=fontsize, style=style,
                         color=color, rotation=rotation, ha=ha, va=va)
        else:
            stuff.annotate(s, xy, xycoords=xycoords,
                           weight=weight, fontsize=fontsize, style=style,
                           color=color, rotation=rotation, ha=ha, va=va)

    def top_left_letter(self, ax, s, xy=(-0.3,1.02), bold=True, fontsize=None):
        if fontsize is None:
            fontsize=self.FONTSIZE+1
        self.annotate(ax, s, xy, bold=bold, fontsize=fontsize)
        
    def adjust_spines(ax, spines, tck_outward=3, tck_length=4.,
                      xcolor='w', ycolor='w'):
        if xcolor is None:
            xcolor = self.default_color
        if ycolor is None:
            ycolor = self.default_color
        ap.adjust_spines(ax, spines, tck_outward=3, tck_length=4.,
                             xcolor=xcolor, ycolor=ycolor)
        
    def set_plot(self, ax,
                 spines=['left', 'bottom'],
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
                 xcolor=None, ycolor=None, fontsize=None):
        if fontsize is None:
            fontsize=self.FONTSIZE
        if xcolor is None:
            xcolor = self.default_color
        if ycolor is None:
            ycolor = self.default_color

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
        
    def show(self):
        if platform.system()=='Windows':
            plt.show()
        else:
            plt.show(block=False)
            input('Hit Enter To Close')
            plt.close()

###########################################################
###### Now a set of predefined functions
###########################################################
    
    
###########################################################
###### a versatile line plot function
###########################################################

def plot_function(x=None, y=None, sy=None,
                  color='k',
                  X=None, Y=None, sY=None,
                  COLORS=None, colormap=viridis,
                  ax=None,
                  lw=1, alpha_std=0.3, ms=0, m='', ls='-',
                  xlabel='', ylabel='', bar_label='',
                  label=None,
                  LABELS=None,
                  fig_args={},
                  axes_args={},
                  bar_legend_args=None,
                  legend_args=None):

    """    
    return fig, ax
    """
    # getting or creating the axis
    if ax is None:
        fig, ax = figure(**fig_args)
    else:
        fig = plt.gcf()

    if (y is None) and (Y is None):
        y = x
        x = np.arange(len(y))

    if (Y is not None):
        if (X is None) and (x is not None):
            X = [x for i in range(len(Y))]
        elif (X is None):
            X = [np.arange(len(y)) for y in Y]
        
        line_plots.multiple_curves(ax, X, Y, sY, COLORS, LABELS,
                                   alpha_std=alpha_std,
                                   colormap=colormap,
                                   lw=lw, ls=ls, m=m, ms=ms)
    else:
        line_plots.single_curve(ax, x, y, sy,
                                color=color,
                                alpha_std=alpha_std,
                                lw=lw, label=label, ls=ls, m=m, ms=ms)

    if bar_legend_args is not None:
        cb = add_inset(ax, **bar_legend_args)
        build_bar_legend(np.arange(len(LABELS)+1),
                         cb,
                         colormap,
                         label=bar_label,
                         ticks_labels=LABELS)
        
    if legend_args is not None:
        ax.legend(**legend_args)
        
    if 'xlabel' not in axes_args:
        axes_args['xlabel'] = xlabel
    if 'ylabel' not in axes_args:
        axes_args['ylabel'] = ylabel
    set_plot(ax, **axes_args)

    return fig, ax

###########################################################
###### a versatile scatter plot function
###########################################################

def scatter(x=None, y=None, sx=None, sy=None,
            color='k',
            X=None, Y=None, sX=None, sY=None,
            COLORS=None, colormap=viridis,
            ax=None,
            lw=0, elw=1, ms=3, marker='o',
            xlabel='', ylabel='occurence',bar_label='',
            LABELS=None,
            fig_args={},
            axes_args={},
            bar_legend_args=None,
            legend_args=None):

    # getting or creating the axis
    if ax is None:
        fig, ax = figure(**fig_args)
    else:
        fig = plt.gcf()

    if (y is None) and (Y is None):
        y = x
        x = np.arange(len(y))

    if (Y is not None):
        if (X is None) and (x is not None):
            X = [x for i in range(len(Y))]
        elif (X is None):
            X = [np.arange(len(y)) for y in Y]
        scatter_plots.multiple_curves(ax, X, Y, sX, sY, COLORS, LABELS,\
                                      marker=marker, lw=lw, ms=ms,
                                      elw=elw)
    else:
        scatter_plots.single_curve(ax, x, y, sx, sy,
                                   color=color,
                                   marker=marker, lw=lw, ms=ms,
                                   elw=elw)

    if bar_legend_args is not None:
        cb = add_inset(ax, **bar_legend_args)
        build_bar_legend(np.arange(len(Y)+1),
                         cb,
                         colormap,
                         label=bar_label,
                         ticks_labels=LABELS)
        
    # if legend_args is not
    if legend_args is not None:
        ax.legend(**legend_args)
    
    set_plot(ax, **axes_args)
    
    return fig, ax


def set_subplot_safe_for_labels(fig, FIGSIZE=None, FONTSIZE=16,
                                    hspace=0.1, vspace=0.1):
    if FIGSIZE is None:
        FIGSIZE = [fig.get_figwidth(), fig.get_figheight()]
    x0, y0 = .15*FONTSIZE/FIGSIZE[0], .15*FONTSIZE/FIGSIZE[0]
    fig.subplots_adjust(\
                bottom=x0, left=y0,\
                right=max([1.-0.02*FONTSIZE/FIGSIZE[0],x0*1.1]),
                top=max([1.-0.02*FONTSIZE/FIGSIZE[1],y0*1.1]),
                hspace=hspace)

    
def replace_axis_by_legend(ax, text, x0=0.1, y0=0.1, on_fig=False):
    ax.axis('off')
    if on_fig:
        ax.annotate(text, (x0, y0), xycoords='figure fraction')
    else:
        ax.annotate(text, (x0, y0), xycoords='axes fraction')


def show(module=None):
    if platform.system()=='Windows':
        plt.show()
    else:
        plt.show(block=False)
        input('Hit Enter To Close')
        plt.close()


def annotate(s, stuff, x=0.5, y=0.8,
             fontsize=FONTSIZE,
             fontweight='normal',
             rotation=0,
             color='k'):
    if type(stuff)==mpl.figure.Figure:
        plt.annotate(s, (x,y), xycoords='figure fraction',
                     fontweight=fontweight, fontsize=fontsize,
                     color=color, rotation=rotation)
    else:
        stuff.annotate(s, (x,y), xycoords='axes fraction',
                       fontweight=fontweight, fontsize=fontsize,
                       color=color, rotation=rotation)

  
if __name__=='__main__':

    # fig, AX = figure(axes_extents=[\
    #                               [[3,2], [1,2] ],
    #                                [[1,1], [1,1], [2,1] ] ],
    #                  left=.3, bottom=.4, hspace=1.4, wspace=1.2,
    #                  figsize=[.8, .35])
    
    # plot(Y=[
    #     np.random.randn(20),
    #     np.random.randn(20),
    #     np.random.randn(20),
    #     np.random.randn(20)],
    #      sY=[
    #          np.ones(20),
    #          np.ones(20),
    #          np.random.randn(20),
    #          np.random.randn(20)],
    #      ax=AX[0][0],
    #      COLORS=[Red, Purple, Blue, Green],
    #      legend_args={'frameon':False},
    #      axes_args={'spines':['left']})
    
    # scatter(X=np.random.randn(4,5), Y=np.random.randn(4,5),
    #         sX=np.random.randn(4,5),sY=np.random.randn(4,5),
    #         ax=AX[1][0],
    #         bar_legend_args={},
    #         bar_label='condition')
    
    # plot(np.random.randn(20), sy=np.random.randn(20),
    #      ax=AX[1][2])
    # scatter(np.random.randn(20), sy=np.random.randn(20),
    #         ax=AX[1][2])
    # plot(np.random.randn(20), sy=np.random.randn(20),
    #         ax=AX[1][2], color=Red)
    # scatter(np.random.randn(20), sy=np.random.randn(20),
    #         ax=AX[1][2], color=Red)
    # plot(np.sin(np.linspace(0,1,30)*3*np.pi)*2,
    #      ax=AX[1][2], color=Purple)
    # plot(np.cos(np.linspace(0,1,30)*3*np.pi)*2,
    #      ax=AX[1][2], color=Green)
    
    # hist(np.random.randn(200), ax=AX[0][1],\
    #      orientation='vertical',
    #      axes_args={'ylim':AX[0][0].get_ylim(), 'spines':['left']})
    
    # AX[1][1].axis('off')
    # fig.savefig('fig.png', dpi=200)
    # save_on_desktop(fig, figname='fig.png')

    # fig2, AX = figure(axes=(2,1),
    #                   left=.4, bottom=.4, hspace=1.4, wspace=1.2,
    #                   figsize=[.45, .3])
    # import itertools
    # for i in range(2):
    #     plot(np.random.randn(20), sy=np.random.randn(20),
    #          ax=AX[i])
    # # fig2.savefig('fig2.png', dpi=200)
    # fig1, AX = figure(axes_extents=[\
    #                                [[3,1], [1,1] ],
    #                                [[1,1], [2,1], [1,1] ] ] )
    # fig2, AX = figure(axes=(2,1))
    # for ax in AX:
    #     scatter(np.abs(np.exp(np.random.randn(100))), np.abs(np.exp(np.random.randn(100))), ax=ax)
    #     set_plot(ax, yscale='log', xscale='log')
    # show()
    # print('should be 1, 1')
    # fig2, AX = figure(axes=(1,1))
    # print('should be 2, 1')
    # fig2, AX = figure(axes=(2,1))
    # print('should be 1, 2')
    # fig2, AX = figure(axes=(1,2))
    # print('should be 3, 2')
    # fig2, AX = figure(axes=(3,2))
    # # show()

    # fig, _ = figure()
    # fig, _ = plot(Y=np.random.randn(4, 10), sY=np.random.randn(4, 10),
    #               axes_args={'spines':['left', 'bottom'], 'xlabel':'my-x value', 'ylabel':'my-y value'})
    # save_on_desktop(fig, figname='2.svg')
    # show()

    # mg = graphs('ggplot_notebook')
    mg = graphs()
    fig_lf, AX = mg.figure(axes_extents=[[[3,1]],[[1,2],[1,2],[1,2]]], figsize=(1.,.5), wspace=3., hspace=2.)
    for ax in [item for sublist in AX for item in sublist]:
        mg.top_left_letter(ax, 'a')
    # _, ax, _ = mg.figure(with_space_for_bar_legend=True)
    AX[1][0].hist(np.random.randn(100))
    fig, ax = mg.figure()
    ax.hist(np.random.randn(100))
    mg.top_left_letter(ax, 'a')
    mg.annotate(ax, 'blabla', (0.7, 0.8), italic=True)
    mg.set_plot(ax)
    mg.show()
