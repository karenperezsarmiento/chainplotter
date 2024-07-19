# Chainplotter

[![A rectangular badge, half black half purple containing the text made at Code Astro](https://img.shields.io/badge/Made%20at-Code/Astro-blueviolet.svg)](https://semaphorep.github.io/codeastro/)
[![Rectangular badge for the documentation at ReadTheDocs](https://img.shields.io/readthedocs/chainplotter/latest
)](https://chainplotter.readthedocs.io/en/latest/)
[![Rectangular badge for the pypy installation site](https://img.shields.io/pypi/v/chainplotter)](https://pypi.org/project/chainplotter/)

Cosmosis chains are incompatible with the plotting tool getdist. Chainplotter takes cosmosis output chains and returns a getdist.MCSamples object that can be plotted using getdist. Chainplotter currently may only work with the Dark Energy Survey (DES) year 3 (Y3) cosmosis chains.

## How to Install: 

```
pip install chainplotter
```

## How to Use: 

Input cosmosis chain file into loadCosmosisMCSamples(filename) (Note: Must be done without '.txt')
loadCosmosisMCSamples.mc_samples is an object of type getdist.MCSamples that then can be plotted with getdist.

```
from chainplotter import cosmosis_getdist
from getdist import plots

samples = cosmosis_getdist.loadCosmosisMCSamples("../example_data/chain_3x2pt_wcdm_SR_maglim")
g = plots.get_subplot_plotter()
g.triangle_plot(samples.mc_samples)
```
PyPI installation [here](https://pypi.org/project/chainplotter/).

See detailed documentation [here](https://chainplotter.readthedocs.io/en/latest/).
