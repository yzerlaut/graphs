<div><img src="https://github.com/yzerlaut/datavyz/raw/master/docs/logo.png" alt="datavyz logo" width="45%" align="right" style="margin-left: 10px"></div>

# datavyz

*Get your plots right, all along your analysis workflow. A layer on top of `matplotlib` to achieve flexible & high-standard data visualization across different mediums.*


## Overview: a quick tour of the functionalities

```
import datavyz

ge = datavyz.graph_env('manuscript')

fig1, AX1 = ge.figure(axes=(2,2)) # just a 2x2 grid of axes

# a more complex grid of axes:
fig2, AX2 = ge.figure(axes_extents=[\
                                   [[3,1], [1,1]],
                                   [[4,1]],
                                   [[1,1], [2,1], [1,1] ] ],
                      figsize=[.95,.95])
AX2[0].plot(np.random.randn(20))

# now 
for i, fig, AX in zip(range(2), [fig1, fig2], [AX1, AX2]):
   for l, ax in zip(list(string.ascii_lowercase), itertools.chain(*AX)):
       ge.top_left_letter(ax, l+'     ')
       ge.set_plot(ax, xlabel='xlabel (xunit)', ylabel='ylabel (yunit)', grid=True)

   fig.savefig('fig%i.svg' % int(i+1))
```

![calibration](docs/calibration.svg)


## Installation

Using =git= to clone the repository and "pip" to install the package in your python environment:

```
git clone https://github.com/yzerlaut/datavyz.git
pip install -r datavyz/requirements.txt
pip install datavyz/
```


## Use

After installation, import the module and create a specific graph environment with:

```
from datavyz import graph_env
ge = graph_env('manuscript') # for a figure export to A4 manuscript size
```

```
sge = graph_env('screen') # env to scale the figure display on screen monitor
sge.hist(np.random.randn(100))
sge.show()
```

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
        'bottom_size':20., # mm
    },
    'screen': {
        'size_factor': 1.5,
    }
}
```

An additional setting `"screen"` has only a "size_factor" key, so it takes the settings of the "manuscript" and expands everything by a factor 1.5 for the display on the screen.

## Features

We document here the different plotting features covered by the library:

### Pie plots


```
# building data
data = .5+np.random.randn(3)*.4

#plotting
fig, ax = mg.pie(data,
				 ext_labels = ['Data1', 'Data2', 'Data3'],
				 pie_labels = ['%.1f%%' % (100*d/data.sum()) for d in data],
				 ext_labels_distance=1.2,
				 explodes=0.05*np.ones(len(data)),
				 center_circle=0.2,
				 COLORS = [mg.tab20(x) for x in np.linspace(0,1,len(data))],
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
fig, AX = mg.features_plot(data, ms=3,
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
fig = mg.cross_correl_plot(data,
						   features=list(data.keys())[:7])

fig.savefig('./docs/cross-correl-plot.png', dpi=200)
```
Output:

![](docs/cross-correl-plot.png)

### Bar plots

#### Classical bar plot

```
mg.bar(np.random.randn(5), yerr=.3*np.random.randn(5), bottom=-3, COLORS=mg.colors[:5])
```

#### Related sample measurements
```
fig, ax, pval = mg.related_samples_two_conditions_comparison(np.random.randn(10)+2., np.random.randn(10)+2.,
															 xticks_labels=['$\||$cc($V_m$,$V_{ext}$)$\||$', '$cc(V_m,pLFP)$'],
															 xticks_rotation=45, fig_args={'bottom':1.5, 'right':8.})
fig.savefig('docs/related-samples.png', dpi=200)
```

![](docs/related-samples.png)

#### Unrelated sample measurements
```
fig, ax, pval = mg.unrelated_samples_two_conditions_comparison(np.random.randn(10)+2., np.random.randn(10)+2.,
															   xticks_labels=['$\||$cc($V_m$,$V_{ext}$)$\||$', '$cc(V_m,pLFP)$'],
															   xticks_rotation=45, fig_args={'bottom':1.5, 'right':8.})
fig.savefig('docs/unrelated-samples.png', dpi=200)
```

![](docs/unrelated-samples.png)

### Line plots



### Scatter plots

### Surface plots
Typically a data science project involves:
