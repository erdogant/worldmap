# Worldmap

[![Python](https://img.shields.io/pypi/pyversions/worldmap)](https://img.shields.io/pypi/pyversions/worldmap)
[![PyPI Version](https://img.shields.io/pypi/v/worldmap)](https://pypi.org/project/worldmap/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/googletrends/blob/master/LICENSE)
[![Github Forks](https://img.shields.io/github/forks/erdogant/worldmap.svg)](https://github.com/erdogant/worldmap/network)
[![GitHub Open Issues](https://img.shields.io/github/issues/erdogant/worldmap.svg)](https://github.com/erdogant/worldmap/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Downloads](https://pepy.tech/badge/worldmap/month)](https://pepy.tech/project/worldmap/month)
[![Downloads](https://pepy.tech/badge/worldmap)](https://pepy.tech/project/worldmap)
<!---[![BuyMeCoffee](https://img.shields.io/badge/buymea-coffee-yellow.svg)](https://www.buymeacoffee.com/erdogant)-->
<!---[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)-->

The ``worldmap`` python package enables to color different countries in the world or the regions per country. For this package, the svg images from https://www.w3.org are utilized, processed and colored.

# 
**Star this repo if you like it! ⭐️**
#


## Installation

```bash
pip install worldmap
```

```python
import worldmap as worldmap
```

- Simple example to color the different regions in the Netherlands:
```python
names   = ['zeeland','Overijssel', 'flevoland']
opacity = [0.1, 0.2, 0.6]
cmap    = ['#ff0000'] # Different red accents
out = worldmap.colormap(names,opacity=opacity, cmap='Set1', loadmap='netherlands')
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
abbr_1 = worldmap.city2code('Netherlands')
abbr_2 = worldmap.city2code('Germany')
```

- Retrieve names in map
```python
countries_world = worldmap.getmapnames(loadmap='world')
region_NL = worldmap.getmapnames(loadmap='netherlands')
regions_BE = worldmap.getmapnames(loadmap='belgium')
```

### Citation
Please cite worldmap in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2019worldmap,
  title={worldmap},
  author={Erdogan Taskesen},
  year={2019},
  howpublished={\url{https://github.com/erdogant/worldmap}},
}
```

### References:
* http://www.w3.org/Consortium/Legal/copyright-software

### Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)

### Contribute
* All kinds of contributions are welcome!
* If you wish to buy me a <a href="https://www.buymeacoffee.com/erdogant">Coffee</a> for this work, it is very appreciated :)

### Licence
See [LICENSE](LICENSE) for details.

