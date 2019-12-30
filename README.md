# Worldmap
[![PyPI Version](https://img.shields.io/pypi/v/worldmap)](https://pypi.org/project/worldmap/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/erdoganta/worldmap/blob/master/LICENSE)

This package enables to color the worldmap of different regions in countries using svg images.

## Contents
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

## Installation
* Install worldmap from PyPI (recommended). Worldmap is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
It is distributed under the Apache 2.0 license.

```
pip install worldmap
```
* Alternatively, install worldmap from the GitHub source:

```bash
git clone https://github.com/erdoganta/worldmap.git
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
  <img src="https://github.com/erdoganta/worldmap/blob/master/docs/figs/figure_netherlands.png" width="300" />
</p>


- Simple example to color the worldmap:
```python

#### Coloring of maps   
names   = ['Nederland']
opacity = [100]
out = worldmap.colormap(names, opacity=opacity, loadmap='world')
```
<p align="center">
  <img src="https://github.com/erdoganta/worldmap/blob/master/docs/figs/worldmap.png" width="300" />
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
@misc{erdoganta2019worldmap,
  title={worldmap},
  author={Erdogan Taskesen},
  year={2019},
  howpublished={\url{https://github.com/erdoganta/worldmap}},
}
```

## Maintainers
* Erdogan Taskesen, github: [erdoganta](https://github.com/erdoganta)
See [LICENSE](LICENSE) for details.
