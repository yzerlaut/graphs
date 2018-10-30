import brian2
import matplotlib.pylab as plt
import numpy as np
import sys, pathlib, os, json
# specific modules
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
# from data_analysis.IO.load_data import load_file
# from data_analysis.freq_analysis.fourier_for_real import time_to_freq, FT
# from data_analysis.freq_analysis.wavelet_transform import my_cwt
# from data_analysis.processing.signanalysis import gaussian_smoothing,\
#     autocorrel, butter_highpass_filter
from graphs.my_graph import *
from graphs.plot_export import put_list_of_figs_to_multipage_pdf
from matplotlib.cm import viridis, copper, plasma, gray, binary
from scipy.integrate import cumtrapz
Blue, Orange, Green, Red, Purple, Brown, Pink, Grey,\
        Kaki, Cyan = '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',\
        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'

desktop = os.path.join(os.path.join(os.path.expanduser('~')),
                       'Desktop', os.path.sep)
home = os.path.join(os.path.expanduser('~'), os.path.sep)
curdir=os.path.abspath(__file__).replace(os.path.basename(__file__),'')

def get_compartment_list(morpho):

    COMP_LIST = [morpho]
    TOPOL = str(morpho.topology())
    TT = TOPOL.split('\n')
    for t in TT[1:-1]:
        exec("COMP_LIST.append(morpho."+t.split(' .')[-1]+")")
    return COMP_LIST

def plot_nrn_shape(COMP_LIST,
                   ax=None,
                   spatial_scale=100,
                   polar_angle=0, azimuth_angle=np.pi/2., 
                   density_quantity=None,
                   dend_color='k', axon_color='r',
                   ms=3, lw=1):

    if ax is None:
        fig, ax = plt.subplots(1, figsize=(4,6))
        
    ax.set_aspect('equal')

    [x0, y0, z0] = 1e6*COMP_LIST[0].x, 1e6*COMP_LIST[0].y, 1e6*COMP_LIST[0].z

    # plotting each segment
    ax.plot(0, 0, 'ko', ms=ms)
    for c in COMP_LIST[1:]:
        x = np.cos(polar_angle)*(1e6*c.x-x0)+np.sin(polar_angle)*(1e6*c.y-y0)
        y = np.sin(polar_angle)*(1e6*c.x-x0)+np.cos(polar_angle)*(1e6*c.y-y0)

        if (len(c.type.split('dend'))>1) or (len(c.type.split('apic'))>1):
            ax.plot(x, y, '-', lw=lw, color=dend_color)
        if (len(c.type.split('axon'))>1) and (axon_color is not None):
            ax.plot(x, y, '-', lw=lw, color=axon_color)

    # adding a bar for the spatial scale
    if spatial_scale>0:
        ax.plot(ax.get_xlim()[0]*np.ones(2),
                ax.get_ylim()[0]+np.array([0,spatial_scale]), 'k-')
        ax.annotate(str(spatial_scale)+'$\mu$m', (ax.get_xlim()[0], ax.get_ylim()[0]))

    ax.axis('off')
    return ax

def plot_nrn_shape_with_density(COMP_LIST,
                                ax=None,
                                spatial_scale=100,
                                polar_angle=0, azimuth_angle=np.pi/2., 
                                density_quantity=None,
                                dend_color='k', axon_color='r',
                                ms=3, lw=1):

    if ax is None:
        fig, ax = plt.subplots(1, figsize=(4,6))
        
    ax.set_aspect('equal')

    [x0, y0, z0] = 1e6*COMP_LIST[0].x, 1e6*COMP_LIST[0].y, 1e6*COMP_LIST[0].z

    # plotting each segment
    ax.plot(0, 0, 'ko', ms=ms)
    for c in COMP_LIST[1:]:
        x = np.cos(polar_angle)*(1e6*c.x-x0)+np.sin(polar_angle)*(1e6*c.y-y0)
        y = np.sin(polar_angle)*(1e6*c.x-x0)+np.cos(polar_angle)*(1e6*c.y-y0)

        if (c.type=='dend') or (c.type=='apic'):
            ax.plot(x, y, '-', lw=lw, color=dend_color)
        if (c.type=='axon') and (axon_color is not None):
            ax.plot(x, y, '-', lw=lw, color=axon_color)

    # adding a bar for the spatial scale
    if spatial_scale>0:
        ax.plot(ax.get_xlim()[0]*np.ones(2),
                ax.get_ylim()[0]+np.array([0,spatial_scale]), 'k-')
        ax.annotate(str(spatial_scale)+'$\mu$m', (ax.get_xlim()[0], ax.get_ylim()[0]))

    ax.axis('off')
    return ax


def dist_to_soma(comp, soma):
    return np.sqrt((comp.x-soma.x)**2+\
                   (comp.y-soma.y)**2+\
                   (comp.z-soma.z)**2)[0]/brian2.um
    
if __name__=='__main__':

    print('[...] loading morphology')
    morpho = brian2.Morphology.from_file('/Users/yzerlaut/Downloads/tolias/CNG version/L5pyr-j140408b.CNG.swc')
    print('[...] creating list of compartments')
    COMP_LIST = get_compartment_list(morpho)

    from my_graph import *
    plot_nrn_shape(COMP_LIST, lw=0.5, ms=0.1)
    
    # fig, AX = plt.subplots(1, 4, figsize=(7,4))

    # plot(COMP_LIST, ax=AX[0])
    # for ax in AX[1:]:
    #     plot(COMP_LIST, ax=ax, lw=0.1, ms=0.1, spatial_scale=0)

    # x0, y0, z0 = 1e6*COMP_LIST[0][0].x, 1e6*COMP_LIST[0][0].y, 1e6*COMP_LIST[0][0].z

    # # adding density of excitatory synapses
    # Density= 30./(100.*brian2.um2)
    # scale_per_ms = 0.03
    # for comp in COMP_LIST:
    #     for c in comp:
    #         if dist_to_soma(c, COMP_LIST[0][0])>30.:
    #             x = (1e6*c.x-x0)
    #             y = (1e6*c.y-y0)
    #             AX[1].plot([x], [y], 'o',
    #                        ms=c.area*scale_per_ms*Density,
    #                        color = Green)
    # AX[1].plot([AX[1].get_xlim()[0]], [AX[1].get_ylim()[0]], 'o',
    #            ms=10.*scale_per_ms, color=Green, label='10 synapses')
    # AX[1].plot([AX[1].get_xlim()[0]], [AX[1].get_ylim()[0]], 'o',
    #            ms=100.*scale_per_ms, color=Green, label='100 synapses')
    # AX[1].legend(frameon=False, prop={'size':'xx-small'})

    # # adding density of PV synapses
    # scale_per_ms = 0.01
    # # -- Proximal
    # Density= 20./(100.*brian2.um2)
    # for comp in COMP_LIST:
    #     for c in comp:
    #         if dist_to_soma(c, COMP_LIST[0][0])<20.:
    #             x = (1e6*c.x-x0)
    #             y = (1e6*c.y-y0)
    #             AX[2].plot([x], [y], 'o',
    #                        ms=c.area*scale_per_ms*Density,
    #                        color = Red)
    # # -- Distal
    # Density= 2./(100.*brian2.um2)
    # for comp in COMP_LIST:
    #     for c in comp:
    #         if dist_to_soma(c, COMP_LIST[0][0])>30.:
    #             x = (1e6*c.x-x0)
    #             y = (1e6*c.y-y0)
    #             AX[2].plot([x], [y], 'o',
    #                        ms=c.area*scale_per_ms*Density,
    #                        color = Red)
    # AX[2].plot([AX[2].get_xlim()[0]], [AX[2].get_ylim()[0]], 'o',
    #            ms=50.*scale_per_ms, color=Red, label='50 synapses')
    # AX[2].plot([AX[2].get_xlim()[0]], [AX[2].get_ylim()[0]], 'o',
    #            ms=500.*scale_per_ms, color=Red, label='500 synapses')
    # AX[2].legend(frameon=False, prop={'size':'xx-small'})

    # # adding density of SST synapses
    # scale_per_ms = 0.04
    # # -- Distal
    # Density= 4./(100.*brian2.um2)
    # for comp in COMP_LIST:
    #     for c in comp:
    #         if dist_to_soma(c, COMP_LIST[0][0])>30.:
    #             x = (1e6*c.x-x0)
    #             y = (1e6*c.y-y0)
    #             AX[3].plot([x], [y], 'o',
    #                        ms=c.area*scale_per_ms*Density,
    #                        color = Orange)
    # AX[3].plot([AX[3].get_xlim()[0]], [AX[3].get_ylim()[0]], 'o',
    #            ms=10.*scale_per_ms, color=Orange, label='10 synapses')
    # AX[3].plot([AX[3].get_xlim()[0]], [AX[3].get_ylim()[0]], 'o',
    #            ms=100.*scale_per_ms, color=Orange, label='100 synapses')
    # AX[3].legend(frameon=False, prop={'size':'xx-small'})

    # # fig.savefig('temp.svg')

    show()
