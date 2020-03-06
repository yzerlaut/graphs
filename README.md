<div><img src="https://github.com/yzerlaut/datavyz/raw/master/docs/logo.png" alt="datavyz logo" width="45%" align="right" style="margin-left: 10px"></div>

# datavyz

*Get your plots right, all along your analysis workflow. A layer on top of `matplotlib` to achieve flexible & high-standard data visualization across different mediums.*

## Principle

Create a graph environment associated to a specific visualization setting, below "manuscript":

```
import datavyz
ge = datavyz.graph_env('manuscript')
```

And call all of your plotting functions relative to this environment, e.g.:

```
ge.plot(Y=np.random.randn(4, 10),
	sY=np.random.randn(4, 10),
        xlabel='xlabel (xunit)',
        ylabel='ylabel (yunit)',
        title='datavyz demo plot')
ge.show()
```
pops up:

<p align="center">
  <img src="docs/demo.svg"/>
</p>

## Installation

Using *git* to clone the repository and "pip" to install the package in your python environment:

```
pip install git+https://github.com/yzerlaut/datavyz.git
```

## A quick demo of the functionalities

Building a complex multipanel figure with the module.

```
import datavyz

ge = datavyz.graph_env('manuscript')

# a more complex grid of axes:
fig, AX = ge.figure(axes_extents=[\
                                  [[3,1], [1,1]],
                                  [[4,1]],
                                  [[1,1], [2,1], [1,1] ] ],
                     figsize=[.95,.95])
AX2[0].plot(np.random.randn(20))

t = np.linspace(0, 10, 1e3)
y = np.cos(5*t)+np.random.randn(len(t))

# leave first axis empty for drawing
AX2[0][0].axis('off') # space for docs/schematic.svg

# time series plot
AX2[0][1].plot(t, y)
ge.set_plot(AX2[0][1], xlabel='xlabel (xunit)', ylabel='ylabel (yunit)')

# more time series plot
AX2[1][0].plot(t[t>9], y[t>9], label='raw')
AX2[1][0].plot(t[t>9][1:], np.diff(y[t>9]), label='deriv.')
AX2[1][0].plot(t[t>9][1:-1], np.diff(np.diff(y[t>9])), label='2nd deriv.')
ge.set_plot(AX2[1][0], xlabel='xlabel (xunit)', ylabel='ylabel (yunit)')

# scatter plot
ge.scatter(t[::10], t[::10]+np.random.randn(100),
           ax=AX2[2][0], xlabel='ylabel (yunit)')


# bar plot
ge.bar(np.random.randn(8),
       COLORS=[ge.viridis(i/7) for i in range(8)],
        ax=AX2[2][1], xlabel='ylabel (yunit)')

# pie plot
ge.pie([0.25,0.4,0.35], ax=AX2[2][2], ext_labels=['Set 1', 'Set 2', 'Set 3'])


# looping on all plots to add the top left letter:
for i, fig, AX in zip(range(3), [fig1, fig2], [AX1, AX2]):
    for l, ax in zip(list(string.ascii_lowercase), itertools.chain(*AX)):
        ge.top_left_letter(ax, l+'     ')

# saving the figure with all plots
fig2.savefig('fig2.svg')

# generating the figure with the addition of the drawing and saving it "fig.svg"
from datavyz import put_list_of_figs_to_svg_fig
put_list_of_figs_to_svg_fig(['docs/schematic.svg', fig],
                            fig_name='fig.svg',
                            Props={'XCOORD':[0,0], 'YCOORD':[0,0]})

```

<p align="center">
  <img src="docs/multipanel.svg"/>
</p>


## Settings

You can specifiy different environments corresponding to different visualization settings.

For example the setting to produce the above is the when `graph_env` is called with the `"manuscript"` argument is the following:
```
ENVIRONMENTS = {
    'manuscript': {
	'fontsize':9,
	'default_color':'k',
        'single_plot_size':(28., 20.), # mm
        'hspace_size':12., # mm
        'wspace_size':16., # mm
        'left_size':16., # mm
        'right_size':4., # mm
        'top_size':4., # mm
        'bottom_size':17., # mm
    },
    'screen': {
        'size_factor': 1.5,
    }
    'darkbg': { # dark background
        'size_factor': 1.5,
        'default_color': 'lightgray',
    }
}
```

An additional setting `"screen"` has only a "size_factor" key, so it takes the settings of the "manuscript" and expands everything by a factor 1.5 for the display on the screen. An additional setting `"darkbg"` is a display setting for displays with dark bakgrounds.

![calibration](https://github.com/yzerlaut/datavyz/raw/master/docs/calibration.svg)

## Features

We document here the different plotting features covered by the library:

### Pie plots


```
# building data
data = .5+np.random.randn(3)*.4

#plotting
fig, ax = ge.pie(data,
				 ext_labels = ['Data1', 'Data2', 'Data3'],
				 pie_labels = ['%.1f%%' % (100*d/data.sum()) for d in data],
				 ext_labels_distance=1.2,
				 explodes=0.05*np.ones(len(data)),
				 center_circle=0.2,
				 COLORS = [ge.tab20(x) for x in np.linspace(0,1,len(data))],
				 # pie_args=dict(rotate=90), # e.g. for rotation
				 legend=None) 
				 # set legend={} to have it appearing
fig.savefig('./docs/pie-plot.png', dpi=200)
```
Output:
![](docs/pie-plot.png)

### Features plot

```
mg = .)

# data: breast cancer dataset from sklearn
from sklearn.datasets import load_breast_cancer
raw = load_breast_cancer()

# re-arange for plotting
data = {}
for feature, values in zip(raw['feature_names'], raw['data']):
	data[feature+'\n(log)'] = np.log(values)

# plotting
fig, AX = ge.features_plot(data, ms=3,
						   fig_args={'left':.1, 'right':.3, 'bottom':.1, 'top':.1,
									 'hspace':.4, 'wspace':.4})
fig.savefig('docs/features-plot.png', dpi=200)
```
![](docs/features-plot.png)

### Cross-correlation plot

Look at the cross-correlation between several joint measurements and estimate the signficance of the correlation:
```
# building random data
data = {}
for i in range(7):
	data['feature_%s'%(i+1)] = np.random.randn(30)

# plotting
fig = ge.cross_correl_plot(data,
						   features=list(data.keys())[:7])

fig.savefig('./docs/cross-correl-plot.png', dpi=200)
```
Output:

![](docs/cross-correl-plot.png)

### Bar plots

#### Classical bar plot

```
ge.bar(np.random.randn(5), yerr=.3*np.random.randn(5), bottom=-3, COLORS=ge.colors[:5])
```

#### Related sample measurements
```
fig, ax, pval = ge.related_samples_two_conditions_comparison(np.random.randn(10)+2., np.random.randn(10)+2.,
															 xticks_labels=['$\||$cc($V_m$,$V_{ext}$)$\||$', '$cc(V_m,pLFP)$'],
															 xticks_rotation=45, fig_args={'bottom':1.5, 'right':8.})
fig.savefig('docs/related-samples.png', dpi=200)
```

![](docs/related-samples.png)

#### Unrelated sample measurements
```
fig, ax, pval = ge.unrelated_samples_two_conditions_comparison(np.random.randn(10)+2., np.random.randn(10)+2.,
															   xticks_labels=['$\||$cc($V_m$,$V_{ext}$)$\||$', '$cc(V_m,pLFP)$'],
															   xticks_rotation=45, fig_args={'bottom':1.5, 'right':8.})
fig.savefig('docs/unrelated-samples.png', dpi=200)
```

![](docs/unrelated-samples.png)

### Line plots



### Scatter plots

### Surface plots
Typically a data science project involves:
