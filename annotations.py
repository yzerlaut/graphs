import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE

def annotate(s, stuff, x=0.5, y=0.8,
             fontsize=FONTSIZE,
             fontweight='normal'):
    if type(stuff)==mpl.figure.Figure:
        plt.annotate(s, (x,y), xycoords='figure fraction',
                     fontweight=fontweight, fontsize=fontsize)
    else:
        stuff.annotate(s, (x,y), xycoords='axes fraction',
                     fontweight=fontweight, fontsize=fontsize)


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

def bar_scales(ax,
               Xbar=None, Ybar=None,
               Xbar_label=None, Ybar_label=None,
               location = 'top right',
               factor=0.95):

    x1, x2 = ax.get_xlim()
    y1, y2 = ax.get_ylim()

    if location=='top right':
        x0 = x2-(1-factor)*(x2-x1)
        y0 = y2-(1-factor)*(y2-y1)
        
    if Xbar is not None:
        ax.plot([x0, x0-Xbar], [y0, y0], 'k-', lw=1)
        ax.annotate(Xbar_label, (x0-Xbar, y0), fontsize=FONTSIZE)
    if Ybar is not None:
        ax.plot([x0, x0], [y0, y0-Ybar], 'k-', lw=1)
        ax.annotate(Ybar_label, (x0, y0-Ybar), fontsize=FONTSIZE, rotation=90)

    

if __name__=='__main__':
    x = 32.23545345e-5
    print(sci_str(x, rounding=2))
    print(from_pval_to_star(x))
