import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.scaling import FONTSIZE, A0_format, inch2cm, cm2inch

import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import string, datetime

# SPECIAL PYTHON PACKAGES FOR:
import svgutils.compose as sg # SVG
# import fpdf # PDF
from PIL import Image # BITMAP (png, jpg, ...)

def put_list_of_figs_to_svg_fig(FIGS,
                                fig_name="fig.svg",
                                visualize=True,\
                                Props = None,
                                with_top_left_letter=False,
                                transparent=True):
    """ take a list of figures and make a multi panel plot"""
    
    label = list(string.ascii_uppercase)[:len(FIGS)]


    if Props is None:
        LABELS, XCOORD, YCOORD = [], [], []

        SIZE = []
        for fig in FIGS:
            SIZE.append(fig.get_size_inches())
        width = np.max([s[0] for s in SIZE])
        height = np.max([s[1] for s in SIZE])
        
        # saving as svg
        for i in range(len(FIGS)):
            LABELS.append(label[i])
            XCOORD.append((i%3)*width*100)
            YCOORD.append(int(i/3)*height*100)

    else:
        XCOORD, YCOORD = Props['XCOORD'],\
                Props['YCOORD'], 
        if 'LABELS' in Props:
            LABELS = Props['LABELS']
        else:
            LABELS = ['' for x in XCOORD]
            
    for i in range(len(FIGS)):
        ff = 'f.svg'
        FIGS[i].savefig('/tmp/'+str(i)+'.svg', format='svg',
                        transparent=transparent)
        
    PANELS = []
    for i in range(len(FIGS)):
        PANELS.append(sg.Panel(\
            sg.SVG('/tmp/'+str(i)+'.svg').move(XCOORD[i],YCOORD[i]),\
            sg.Text(LABELS[i], 15, 10,
                    size=FONTSIZE, weight='bold').move(\
                                                       XCOORD[i],YCOORD[i]))\
        )
    sg.Figure("21cm", "29.7cm", *PANELS).save(fig_name)

    if visualize:
        os.system('convert '+fig_name+' '+fig_name.replace('.svg', '.png'))
        plt.close('all')
        z = plt.imread(fig_name.replace('.svg', '.png'))
        plt.imshow(z)
        show()
        # os.system('open '+fig_name.replace('.svg', '.png'))
        
def put_list_of_figs_to_multipage_pdf(FIGS,
                                      pdf_name='figures.pdf',
                                      pdf_title=''):
    """
    adapted from:
    http://matplotlib.org/examples/pylab_examples/multipage_pdf.html
    """
    
    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
    with PdfPages(pdf_name) as pdf:
        
        for fig in FIGS:
            pdf.savefig(fig)  # saves the current figure into a pdf page

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = u'Y. Zerlaut'
        # d['Keywords'] = 'PdfPages multipage keywords author title subject'
        d['CreationDate'] = datetime.datetime(2009, 11, 13)
        d['ModDate'] = datetime.datetime.today()


def concatenate_pngs(PNG_LIST, ordering='vertically', figname='fig.png'):
    
    images = map(Image.open, PNG_LIST)
    widths, heights = zip(*(i.size for i in images))

    if ordering=='vertically':
        total_height = sum(heights)
        max_width = max(widths)
        new_im = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for fig in PNG_LIST:
            im = Image.open(fig)
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

    new_im.save(figname)


if __name__=='__main__':

    from my_graph import *

    fig1, ax1 = plot(Y=np.random.randn(10,4),\
                     sY=np.random.randn(10,4),
                     fig_args={'with_top_left_letter':'A'})
    fig2, ax2 = scatter(Y=np.random.randn(10,4),\
                        sY=np.random.randn(10,4),
                        fig_args={'with_top_left_letter':'B'})
    
    # put_list_of_figs_to_multipage_pdf([fig1, fig2])
    put_list_of_figs_to_svg_fig([fig1, fig2, fig1],
                                Props={'XCOORD':[100,250,400], 'YCOORD':[100,100,100]},
                                visualize=True)
        
