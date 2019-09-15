from .dependencies import *

def annotate(graph, stuff, s,
             xy,
             xycoords='axes fraction',
             bold=False, italic=False,
             rotation=0,
             fontsize=None, size=None, color=None, ha='left', va='bottom', weight='normal', style='normal'):
    """
    stuff can be either a figure or a subplot
    """
    if fontsize is None:
        fontsize=graph.FONTSIZE
    if size=='small':
        fontsize=graph.FONTSIZE-1
    elif size=='x-small':
        fontsize=graph.FONTSIZE-2
    elif size=='large':
        fontsize=graph.FONTSIZE+1
    elif size=='x-large':
        fontsize=graph.FONTSIZE+2
    if color is None:
        color=graph.default_color
    if bold and (weight=='normal'):
        weight = 'bold'
    if italic and (style=='normal'):
        style = 'italic'

    if type(stuff)==mpl.figure.Figure: # if figure, no choice, if figure relative coordinates
        plt.annotate(s, xy, xycoords='figure fraction',
                     weight=weight, fontsize=fontsize, style=style,
                     color=color, rotation=rotation, ha=ha, va=va)
    else: # means subplot
        stuff.annotate(s, xy, xycoords=xycoords,
                       weight=weight, fontsize=fontsize, style=style,
                       color=color, rotation=rotation, ha=ha, va=va)
    
def from_pval_to_star(p,
                      threshold1=1e-3,
                      threshold2=1e-2,
                      threshold3=5e-2):
    if p<threshold1:
        return '***'
    elif p<threshold2:
        return '**'
    elif p<threshold3:
        return '*'
    else:
        return 'n.s.'
    
def sci_str(x, rounding=0, remove_0_in_exp=True):
    y = ('{:.' + str(int(rounding))+'e}').format(x)
    if remove_0_in_exp: y = y.replace('-0', '-')
    return y

def int_to_roman(input, capitals=False):
   """
   #########################################################
   TAKEN FROM:
   http://code.activestate.com/recipes/81611-roman-numerals/
   #########################################################
   
   Convert an integer to Roman numerals.
   """
   ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
   if capitals:
       nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
   else:
       nums = ('m',  'cm', 'd', 'cd','c', 'xc','l','xl','x','ix','v','iv','i')
   result = ""
   for i in range(len(ints)):
      count = int(input / ints[i])
      result += nums[i] * count
      input -= ints[i] * count
   return result


def draw_bar_scales(ax, xyLoc, Xbar, Xbar_label, Ybar, Ybar_label,
                    orientation='left-bottom',
                    Xbar_label2='',Ybar_label2='',
                    xcolor='k', ycolor='k', ycolor2='k',
                    fontsize=10,
                    shift_factor=20., color='k', lw=1):
    """
    USE:

    fig, ax = figure()
    ax.plot(np.random.randn(10), np.random.randn(10), 'o')
    draw_bar_scales(ax, (0,0), 1, '1s', 2, '2s', orientation='right-bottom', Ybar_label2='12s')
    set_plot(ax)    
    """

    if orientation=='left-bottom':
        
        ax.plot(xyLoc[0]-np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]-np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=xcolor, va='bottom', ha='right',fontsize=fontsize)
        ax.annotate(Ybar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=ycolor, va='top', ha='left',fontsize=fontsize)
        if Ybar_label2!='':
            ax.annotate('\n'+Ybar_label2, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor),
                        color=ycolor2, va='top', ha='left',fontsize=fontsize)
            
    elif orientation=='right-bottom':
        
        ax.plot(xyLoc[0]+np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]-np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=xcolor, va='bottom', ha='left',fontsize=fontsize)
        ax.annotate(Ybar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=ycolor, va='top', ha='right',fontsize=fontsize)
        if Ybar_label2!='':
            ax.annotate('\n'+Ybar_label2, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor),
                        color=ycolor2, va='top', ha='right',fontsize=fontsize)

    elif orientation=='left-top':
        
        ax.plot(xyLoc[0]-np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]+np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=xcolor, va='top', ha='right',fontsize=fontsize)
        ax.annotate(Ybar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=ycolor, va='bottom', ha='left',fontsize=fontsize)
        if Ybar_label2!='':
            ax.annotate(Ybar_label2+'\n',
                        (xyLoc[0]+Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor),
                        color=ycolor2, va='bottom', ha='left',fontsize=fontsize)

    elif orientation=='right-top':
        
        ax.plot(xyLoc[0]+np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]+np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=xcolor, va='top', ha='left',fontsize=fontsize)
        ax.annotate(Ybar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=ycolor, va='bottom', ha='right',fontsize=fontsize)
        if Ybar_label2!='':
            ax.annotate(Ybar_label2+'\n', (xyLoc[0]-Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor),
                        color=ycolor2, va='bottom', ha='right',fontsize=fontsize)
    else:
        print("""
        orientation not recognized, it should be one of
        - right-top
        - left-top
        - right-bottom
        - left-bottom
        """)
        

def bar_scales(ax,
               xlim=None, ylim=None,
               xbar=0, ybar=0,
               xbar_label='', ybar_label='',
               location = 'top right',
               remove_axis=True,
               factor=0.98):
    """
    deprecated !
    TO BE REPLACED BY the above function
    """

    print("""
    deprecated !
    TO BE REPLACED BY the function "draw_bar_scale"
    """)

    # if remove_axis:
    #     ax.axis('off')
    
    # if xlim is None:
    #     xlim = ax.get_xlim()
    # if ylim is None:
    #     ylim = ax.get_ylim()
        
    # if location=='top right':
    #     x0 = xlim[1]-(1.-factor)*(xlim[1]-xlim[0])
    #     y0 = ylim[1]-(1.-factor)*(ylim[1]-ylim[0])
    #     ax.plot([x0, x0-xbar], [y0, y0], 'k-', lw=1)
    #     ax.plot([x0, x0], [y0, y0-ybar], 'k-', lw=1)
    #     ax.annotate(ybar_label, (x0, y0-ybar/2.), fontsize=FONTSIZE, rotation=90)
    #     ax.annotate(xbar_label, (x0-xbar, y0), fontsize=FONTSIZE)
    # elif location=='top left':
    #     x0 = xlim[0]+(1.-factor)*(xlim[1]-xlim[0])
    #     y0 = ylim[1]-(1.-factor)*(ylim[1]-ylim[0])
    #     ax.plot([x0, x0+xbar], [y0, y0], 'k-', lw=1)
    #     ax.plot([x0, x0], [y0, y0-ybar], 'k-', lw=1)
    #     ax.annotate(xbar_label, (x0, y0), fontsize=FONTSIZE)
    #     ax.annotate(ybar_label, (x0, y0-ybar/2.), fontsize=FONTSIZE, rotation=90)
    # elif location=='bottom right':
    #     x0 = xlim[1]-(1.-factor)*(xlim[1]-xlim[0])
    #     y0 = ylim[0]+(1.-factor)*(ylim[1]-ylim[0])
    #     ax.plot([x0, x0-xbar], [y0, y0], 'k-', lw=1)
    #     ax.plot([x0, x0], [y0, y0+ybar], 'k-', lw=1)
    #     ax.annotate(xbar_label, (x0-xbar, y0), fontsize=FONTSIZE)
    #     ax.annotate(ybar_label, (x0, y0+ybar/2.), fontsize=FONTSIZE, rotation=90)
    # elif location=='bottom left':
    #     x0 = xlim[0]+(1.-factor)*(xlim[1]-xlim[0])
    #     y0 = ylim[0]+(1.-factor)*(ylim[1]-ylim[0])
    #     ax.plot([x0, x0+xbar], [y0, y0], 'k-', lw=1)
    #     ax.plot([x0, x0], [y0, y0+ybar], 'k-', lw=1)
    #     ax.annotate(xbar_label, (x0, y0), fontsize=FONTSIZE)
    #     ax.annotate(ybar_label, (x0, y0+ybar/2.), fontsize=FONTSIZE, rotation=90)
    # else:
    #     x0, y0 = location
        
    # # we reintroduce the data limits
    # ax.set_ylim(ylim)
    # ax.set_xlim(xlim)
    

if __name__=='__main__':
    x = 32.23545345e-5
    print(sci_str(x, rounding=2))
    print(from_pval_to_star(x))
    for i in range(20):
        print(int_to_roman(i))
    # from my_graph import *
    # fig, ax = figure()
    # ax.plot(np.random.randn(30), np.random.randn(30), 'o')
    # bar_scales(ax, xbar=2, ybar=2, location='bottom left',
    #            ybar_label=r'10$\mu$V', xbar_label='200ms')
    # show()
