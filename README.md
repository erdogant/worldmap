# Worldmap
[![Python](https://img.shields.io/pypi/pyversions/worldmap)](https://img.shields.io/pypi/pyversions/worldmap)
[![PyPI Version](https://img.shields.io/pypi/v/worldmap)](https://pypi.org/project/worldmap/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/erdogant/worldmap/blob/master/LICENSE)

This python package enables to color different countries in the world or the regions per country. For this package, the svg images from https://www.w3.org are utilized, processed and colored.


## Contents
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

## Installation
* Install worldmap from PyPI (recommended). Worldmap is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* Distributed under the Apache 2.0 license.

```
pip install worldmap
```
* Alternatively, install worldmap from the GitHub source:

```bash
git clone https://github.com/erdogant/worldmap.git
cd worldmap
python setup.py install
```  

## Quick Start
- Import worldmap method

```python
import worldmap as worldmap
```

- Simple example to color the different regions in the Netherlands:
```python
names   = ['zeeland','Overijssel', 'flevoland']
opacity = [0.1, 0.2, 0.6]
cmap    = ['#ff0000'] # Different red accents
out = worldmap.colormap(names,opacity=opacity, cmap='Set1', loadmap='netherlands', filename='nederlandMap.svg')
```
<p align="center">
  <img src="https://github.com/erdogant/worldmap/blob/master/docs/figs/figure_netherlands.png" width="300" />
</p>


- Simple example to color the worldmap:
```python

#### Coloring of maps   
names   = ['Nederland']
opacity = [100]
out = worldmap.colormap(names, opacity=opacity, loadmap='world')
```
<p align="center">
  <img src="https://github.com/erdogant/worldmap/blob/master/docs/figs/worldmap.png" width="300" />
</p>


- Retrieve citynames for abbrevations:
```python
NL = worldmap.code2city('NL')
GB = worldmap.code2city('GB')
```

- Retrieve citynames for abbrevations:
```python
locA=worldmap.city2code('Netherlands')
locB=worldmap.city2code('Germany')
```

- Retrieve names in map
```python
countries_world = worldmap.getmapnames(loadmap='world')
region_NL = worldmap.getmapnames(loadmap='netherlands')
regions_BE = worldmap.getmapnames(loadmap='belgium')
```

## Citation
Please cite worldmap in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2019worldmap,
  title={worldmap},
  author={Erdogan Taskesen},
  year={2019},
  howpublished={\url{https://github.com/erdogant/worldmap}},
}
```

## References:
* http://www.w3.org/Consortium/Legal/copyright-software

## Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
See [LICENSE](LICENSE) for details.
