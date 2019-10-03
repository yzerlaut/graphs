import sys, os, platform
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep
from graphs.dependencies import *
# module that construct the plot settings
import graphs.draw_figure as df
import graphs.adjust_plots as ap

import graphs.annotations as annotations
import graphs.line_plots as line_plots
import graphs.scatter_plots as scatter_plots
from graphs.hist_plots import hist
from graphs.inset import add_inset
from graphs.legend import *
from graphs.features_plot import features_plot
from graphs.cross_correl_plot import cross_correl_plot
from graphs.surface_plots import twoD_plot
from graphs.bar_plots import bar
from graphs.pie_plots import pie

# CUSTOM colors
from matplotlib.cm import viridis, viridis_r, copper, copper_r, cool, jet, PiYG, binary, bone, Pastel1, Pastel2, Paired, Accent, Dark2, Set1, Set2, Set3, tab10, tab20, tab20b, tab20c

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
    
    def __init__(self,
                 output_display='manuscript',
                 color='k'):
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
        elif len(output_display.split('ggplot'))>1:
            self.default_color = 'dimgrey'
            self.set_style('ggplot')
            self.override_style = False
        elif len(output_display.split('seaborn'))>1:
            self.set_style('seaborn')
            self.override_style = False
        
        update_rcParams(self.FONTSIZE)
        self.colors = [Blue, Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan]
        self.blue, self.orange, self.green, self.red, self.purple, self.brown,\
            self.pink, self.grey, self.kaki, self.cyan = Blue,\
                Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan
        self.viridis, self.viridis_r, self.copper, self.copper_r, self.cool, self.jet,\
         self.PiYG, self.binary, self.bone = viridis, viridis_r, copper, copper_r,\
                                             cool, jet, PiYG, binary, bone
        self.Pastel1, self.Pastel2, self.Paired, self.Accent, self.Dark2,\
            self.Set1, self.Set2, self.Set3, self.tab10, self.tab20,\
            self.tab20b, self.tab20c = Pastel1, Pastel2, Paired,\
            Accent, Dark2, Set1, Set2, Set3, tab10, tab20, tab20b, tab20c
        
        
        self.cmaps = [viridis, viridis_r, copper, copper_r, cool, jet, PiYG]
        self.blue_to_red = get_linear_colormap(Blue, Red)
        self.red_to_blue = get_linear_colormap(Red, Blue)
        self.blue_to_orange = get_linear_colormap(Blue, Orange)
        self.green_to_red = get_linear_colormap(Green, Red)
        self.red_to_green = get_linear_colormap(Red, Green)
        self.green_to_orange = get_linear_colormap(Green, Orange)
        self.orange_to_green = get_linear_colormap(Orange, Green)
        self.b, self.o, self.g, self.r = self.blue, self.orange, self.green, self.red
        
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
               with_legend_space=False,
               with_space_for_bar_legend=False,
               shift_up=0., shrink=1.):
        
        if with_legend_space:
            fig, ax = df.figure(axes, axes_extents,
                                figsize=self.size_factor*np.array((1.5,1.)),
                                right=self.size_factor*5.5,
                                fontsize=self.FONTSIZE)
            return fig, ax
        if with_space_for_bar_legend:
            fig, ax = df.figure(axes, axes_extents,
                                figsize=self.size_factor*np.array((1.5,1.)),
                                right=self.size_factor*5.5,
                                fontsize=self.FONTSIZE)
            acb = df.add_inset(ax, [1.17, -.08+shift_up, .08, shrink*1.])
            return fig, ax, acb
        else:
            fig, AX = df.figure(axes, axes_extents,
                                self.size_factor*np.array(figsize),
                                left, right, bottom, top, wspace, hspace)
            return fig, AX

    def plot(self,
             x=None, y=None, sy=None, color='k',
             X=None, Y=None, sY=None,
             COLORS=None, colormap=viridis,
             ax=None,
             lw=1, alpha_std=0.3, ms=0, m='', ls='-',
             xlabel='', ylabel='', bar_label='', title='',
             label=None,
             LABELS=None,
             fig_args={},
             axes_args={},
             bar_legend_args=None,
             legend_args=None, no_set=False):
        
        """    
        return fig, ax
        """
        # getting or creating the axis
        if ax is None:
            fig, ax = self.figure(**fig_args)

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
            
        if not no_set:
            self.set_plot(ax, **axes_args)

        if title!='':
            self.title(ax, title)
            
        return ax

    def scatter(self,
                x=None, y=None, sx=None, sy=None, color='k',
                X=None, Y=None, sX=None, sY=None,
                COLORS=None, colormap=viridis,
                ax=None,
                lw=0, alpha_std=0.3, ms=3, m='', ls='-',
                xlabel='', ylabel='', bar_label='', title='',
                label=None,
                LABELS=None,
                fig_args={},
                axes_args={},
                bar_legend_args=None,
                legend_args=None,
                no_set=False):
        
        """    
        return fig, ax
        """
        # getting or creating the axis
        if ax is None:
            fig, ax = self.figure(**fig_args)

        if (y is None) and (Y is None):
            y = x
            x = np.arange(len(y))

        if (Y is not None):
            if (X is None) and (x is not None):
                X = [x for i in range(len(Y))]
            elif (X is None):
                X = [np.arange(len(y)) for y in Y]

            scatter_plots.multiple_curves(ax, X, Y, sX, sY, COLORS, LABELS,
                                          colormap=colormap,
                                          lw=lw, ms=ms)
        else:
            scatter_plots.single_curve(ax, x, y, sx, sy,
                                       color=color, label=label,
                                       lw=lw,
                                       ms=ms)

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

        if not no_set:
            self.set_plot(ax, **axes_args)
        if title!='':
            self.title(ax, title)

        return ax

    ################################################
    ###### Classical plot functions ################
    ################################################

    # histogram 
    def hist(self, x, **args):
        return hist(self, x, **args)

    # bar plot
    def bar(self, x, **args):
        return bar(self, x, **args)

    # pie plot
    def pie(self, x, **args):
        return pie(self, x, **args)
    
    # features plot
    def features_plot(self, data, **args):
        return features_plot(self, data, **args)

    # features plot
    def cross_correl_plot(self, data, **args):
        return cross_correl_plot(self, data, **args)

    # twoD-plot with x-y axis from bottom left
    def twoD_plot(self, x, y, z, **args):
        return twoD_plot(self, x, y, z, **args)

    def image(self, X, cmap=binary, alpha=1., ax=None, title=''):
        if ax is None:
            fig, ax = self.figure()
        else:
            fig = plt.gcf()
        ax.imshow(X, cmap=cmap, alpha=alpha,
                  interpolation=None,
                  aspect='equal')
        ax.axis('off')
        if title!='':
            self.title(ax, title)
        return fig, ax

        
    ################################################
    ###### Annotate function #######################
    ################################################
    def title(self, ax, title, **args):
        annotations.title(self, ax, title, **args)
        
    def annotate(self, stuff, s, xy, **args):
        annotations.annotate(self, stuff, s, xy, **args)

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
        
    def show(self, block=False):
        if platform.system()=='Windows':
            plt.show()
        else:
            plt.show(block=block)
            input('Hit Enter To Close')
            plt.close()

    def gcf(self):
        return plt.gcf()



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

    # mg = graphs('ggplot_npotebook')
    # mg = graphs()
    # mg.hist(np.random.randn(100), xlabel='ksjdfh')
    
    # fig_lf, AX = mg.figure(axes_extents=[[[3,1]],[[1,2],[1,2],[1,2]]], figsize=(1.,.5), wspace=3., hspace=2.)
    # for ax in [item for sublist in AX for item in sublist]:
    #     mg.top_left_letter(ax, 'a')
    # # _, ax, _ = mg.figure(with_space_for_bar_legend=True)
    # AX[1][0].hist(np.random.randn(100))
    # fig, ax = mg.figure()
    # ax.hist(np.random.randn(100))
    # mg.top_left_letter(ax, 'a')
    # mg.annotate(ax, 'blabla', (0.7, 0.8), italic=True)
    # mg.set_plot(ax)
    # mg.show()
    
    from sklearn.datasets import load_digits
    mg = graphs('screen')
    digits = load_digits()
    fig, ax = mg.image(digits['data'][100].reshape(8,8), alpha=0.2)
    mg.scatter(np.random.randint(8, size=30), np.random.randint(8, size=30), ax=ax)
    mg.title(ax, 'title', size='large')
    # mg.show()
