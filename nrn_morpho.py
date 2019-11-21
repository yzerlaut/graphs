import brian2
import sys, pathlib, os, json
# specific modules
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np

from matplotlib.cm import viridis, viridis_r, copper, plasma, gray, binary
import matplotlib.animation as animation

def get_compartment_list(morpho, without_axon=False):

    COMP_LIST = [morpho]
    TOPOL = str(morpho.topology())
    TT = TOPOL.split('\n')
    for t in TT[1:-1]:
        if without_axon and (len(t.split('axon'))>1):
            pass
        else:
            exec("COMP_LIST.append(morpho."+t.split(' .')[-1]+")")
    return COMP_LIST

def coordinate_projection(c, x0 ,y0, z0, polar_angle, azimuth_angle):
    """
    /!\
    need to do this propertly, not working yet !!
    """
    x = np.cos(polar_angle)*(c.x-x0)+np.sin(polar_angle)*(c.y-y0)
    y = np.sin(polar_angle)*(c.x-x0)+np.cos(polar_angle)*(c.y-y0)
    z = c.z
    return x, y, z

def get_segment_list(morpho,
                     polar_angle=0, azimuth_angle=np.pi/2., 
                     without_axon=False):

    COMP_LIST = get_compartment_list(morpho, without_axon=without_axon)

    # the first one should be the 
    [x0, y0, z0] = COMP_LIST[0].x, COMP_LIST[0].y, COMP_LIST[0].z
    xcoords = np.concatenate([coordinate_projection(c, x0 ,y0, z0, polar_angle, azimuth_angle)[0] for c in COMP_LIST])
    ycoords = np.concatenate([coordinate_projection(c, x0 ,y0, z0, polar_angle, azimuth_angle)[1] for c in COMP_LIST])
    zcoords = np.concatenate([coordinate_projection(c, x0 ,y0, z0, polar_angle, azimuth_angle)[2] for c in COMP_LIST])
    area = np.concatenate([c.area for c in COMP_LIST])
    comp_type = np.concatenate([[c.type for i in range(len(c.x))] for c in COMP_LIST])

    SEGMENT_LIST = {'xcoords':xcoords, 'ycoords':ycoords, 'zcoords':zcoords,
                    'area':area, 'comp_type':comp_type, 'N':len(area)}
    
    return SEGMENT_LIST

def plot_nrn_shape(graph, COMP_LIST,
                   ax=None,
                   spatial_scale=100,
                   polar_angle=0, azimuth_angle=np.pi/2., 
                   density_quantity=None,
                   dend_color='k',
                   apic_color='k',
                   axon_color='r',
                   ms=2, lw=1):

    if ax is None:
        fig, ax = graph.figure(left=0., top=1., bottom=0., right=1.)
    else:
        fig = None
        
    ax.set_aspect('equal')

    [x0, y0, z0] = COMP_LIST[0].x, COMP_LIST[0].y, COMP_LIST[0].z
    # plotting each segment
    ax.plot(0, 0, 'o', ms=ms, color=dend_color)
    for c in COMP_LIST[1:]:
        x, y, _ = coordinate_projection(c, x0 ,y0, z0, polar_angle, azimuth_angle)
        if (len(c.type.split('dend'))>1):
            ax.plot(1e6*x, 1e6*y, '-', lw=lw, color=dend_color)
        elif (len(c.type.split('apic'))>1):
            ax.plot(1e6*x, 1e6*y, '-', lw=lw, color=apic_color)
        elif (len(c.type.split('axon'))>1) and (axon_color!='None'):
            ax.plot(1e6*x, 1e6*y, '-', lw=lw, color=axon_color)

    # adding a bar for the spatial scale
    if spatial_scale>0:
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        ax.plot(xlim[0]*np.ones(2), ylim[1]-np.array([0,spatial_scale]), 'k-', lw=1)
        ax.annotate(str(spatial_scale)+'$\mu$m', (xlim[0]+1, ylim[1]-1))

    ax.axis('off')
    return fig, ax

def dist_to_soma(comp, soma):
    return np.sqrt((comp.x-soma.x)**2+\
                   (comp.y-soma.y)**2+\
                   (comp.z-soma.z)**2)[0]/brian2.um


def show_animated_time_varying_trace(t, Quant0, SEGMENT_LIST,
                                     fig, ax, graph,
                                     picked_locations = None,
                                     polar_angle=0, azimuth_angle=np.pi/2.,
                                     quant_label='$V_m$ (mV)',
                                     time_label='time (ms)',
                                     segment_condition=None,
                                     colormap=viridis_r,
                                     ms=0.5):
    """

    "picked_locations" should be given as a compartment index
    we highlight the first picked_locations with a special marker because it will usually be the stimulation point
    """
    # preparing animations params
    if segment_condition is None:
        segment_condition = np.empty(Quant0.shape[0], dtype=bool)+True
    Quant = (Quant0[segment_condition]-Quant0[segment_condition].min())/(Quant0[segment_condition].max()-Quant0[segment_condition].min())
        
    # adding inset of time plots and bar legends
    ax2 = graph.inset(ax, rect=[0.1,-0.05,.9,.1])
    ax3 = graph.inset(ax, rect=[0.83,0.8,.03,.2])
    graph.build_bar_legend(np.linspace(Quant0[segment_condition].min(), Quant0[segment_condition].max(), 5), ax3, colormap,
                     color_discretization=30, label=quant_label)
    
    # picking up locations
    if picked_locations is None:
        picked_locations = np.concatenate([[0], np.random.randint(1, Quant.shape[0], 4)])
    for pp, p in enumerate(picked_locations):
        ax2.plot(t, Quant0[segment_condition,:][p,:], 'k:', lw=1)
        ax.scatter([1e6*SEGMENT_LIST['xcoords'][segment_condition][p]],
                   [1e6*SEGMENT_LIST['ycoords'][segment_condition][p]], 
                   s=25+30*(1-np.sign(pp)),
                   c=list(['k']+graph.colors)[pp])
    graph.set_plot(ax2, xlabel=time_label, ylabel=quant_label, num_yticks=2)

    LINES = []
    # plotting each segment
    line = ax.scatter(1e6*SEGMENT_LIST['xcoords'][segment_condition], 1e6*SEGMENT_LIST['ycoords'][segment_condition],
                      color=colormap(Quant[:,0]), s=ms, marker='o')
    LINES.append(line)
    # then highlighted points
    for pp, p in enumerate(picked_locations):
        line, = ax2.plot([t[0]], [Quant0[segment_condition,:][p,0]], 'o',
                         ms=4+4*(1-np.sign(pp)),
                         color=list(['k']+graph.colors)[pp])
        LINES.append(line)
    
    # Init only required for blitting to give a clean slate.
    def init():
        return LINES

    def animate(i):
        LINES[0].set_color(colormap(Quant[:,i]))  # update the data
        for pp, p in enumerate(picked_locations):
            LINES[pp+1].set_xdata([t[i]])
            LINES[pp+1].set_ydata([Quant0[segment_condition,:][p,i]])
        return LINES


    ani = animation.FuncAnimation(fig, animate, np.arange(len(t)),
                                  init_func=init,
                                  interval=50, blit=True)
    return ani



if __name__=='__main__':

    from my_graph import *
    import argparse
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
                                   """ 
                                   Plots a 2D representation of the morphological reconstruction of a single cell
                                   """
                                   ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-lw", "--linewidth",help="", type=float, default=0.2)
    parser.add_argument("-ac", "--axon_color",help="", default='r')
    parser.add_argument("-pa", "--polar_angle",help="", type=float, default=0.)
    parser.add_argument("-aa", "--azimuth_angle",help="", type=float, default=0.)
    parser.add_argument("-wa", "--without_axon",help="", action="store_true")
    parser.add_argument("-m", "--movie_demo",help="", action="store_true")
    parser.add_argument("--filename", '-f', help="filename", type=str,
        default=home+'work/neural_network_dynamics/single_cell_integration/morphologies/Jiang_et_al_2015/L5pyr-j140408b.CNG.swc')
    # filename = home+'work/neural_network_dynamics/single_cell_integration/morphologies/Jiang_et_al_2015/L23pyr-j150123a.CNG.swc'
    args = parser.parse_args()
    
    print('[...] loading morphology')
    morpho = brian2.Morphology.from_swc_file(args.filename)
    print('[...] creating list of compartments')
    COMP_LIST = get_compartment_list(morpho, without_axon=args.without_axon)
    SEGMENT_LIST = get_segment_list(morpho, without_axon=args.without_axon)

    fig, ax = plot_nrn_shape(graph, COMP_LIST,
                             lw=args.linewidth,
                             polar_angle=args.polar_angle, azimuth_angle=args.azimuth_angle,
                             axon_color=args.axon_color)

    if args.movie_demo:
        t = np.arange(100)*0.001
        Quant = np.array([.5*(1-np.cos(20*np.pi*t))*i/len(SEGMENT_LIST['xcoords']) \
                          for i in np.arange(len(SEGMENT_LIST['xcoords']))])*20-70
        ani = show_animated_time_varying_trace(1e3*t, Quant, SEGMENT_LIST,
                                               fig, ax,
                                               polar_angle=args.polar_angle, azimuth_angle=args.azimuth_angle)
        
    graph.show()
