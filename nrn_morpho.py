import brian2
import sys, pathlib, os, json
# specific modules
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from graphs.my_graph import *
from matplotlib.cm import viridis, copper, plasma, gray, binary

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
    ax.plot(0, 0, 'o', ms=ms, color=dend_color)
    for c in COMP_LIST[1:]:
        x = np.cos(polar_angle)*(1e6*c.x-x0)+np.sin(polar_angle)*(1e6*c.y-y0)
        y = np.sin(polar_angle)*(1e6*c.x-x0)+np.cos(polar_angle)*(1e6*c.y-y0)

        if (len(c.type.split('dend'))>1) or (len(c.type.split('apic'))>1):
            ax.plot(x, y, '-', lw=lw, color=dend_color)
        if (len(c.type.split('axon'))>1) and (axon_color is not 'None'):
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
        if (c.type=='axon') and (axon_color is not 'None'):
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

    from my_graph import *
    import argparse
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
                                   """ 
                                   Plots a 2D representation of the morphological reconstruction of a single cell
                                   """
                                   ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-ac", "--axon_color",help="", default='r')
    parser.add_argument("-pa", "--polar_angle",help="", type=float, default=0.)
    parser.add_argument("-aa", "--azimuth_angle",help="", type=float, default=0.)
    # parser.add_argument("--std",help="std of the random values", type=float, default=10.)
    # parser.add_argument("--n",help="number of random events",\
    #                     type=int, default=2000)
    # parser.add_argument("-v", "--verbose", help="increase output verbosity",
    #                     action="store_true")
    # parser.add_argument("-s", "--save", help="save the figures",
    #                     action="store_true")
    # parser.add_argument("-u", "--update_plot", help="plot the figures", action="store_true")
    parser.add_argument("--filename", '-f', help="filename", type=str,
                 default=home+'work/neural_network_dynamics/single_cell_integration/morphologies/Jiang_et_al_2015/L5pyr-j140408b.CNG.swc')
    # filename = home+'work/neural_network_dynamics/single_cell_integration/morphologies/Jiang_et_al_2015/L23pyr-j150123a.CNG.swc'
    args = parser.parse_args()
    
    print('[...] loading morphology')
    morpho = brian2.Morphology.from_swc_file(args.filename)
    print('[...] creating list of compartments')
    COMP_LIST = get_compartment_list(morpho)
    plot_nrn_shape(COMP_LIST, lw=0.5, ms=0.1,
                   polar_angle=args.polar_angle, azimuth_angle=args.azimuth_angle, 
                   axon_color=args.axon_color)
    
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
