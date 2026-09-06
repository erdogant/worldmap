from d3blocks.d3blocks import D3Blocks as worldmap

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '1.0.1'

# module level doc-string
__doc__ = """
worldmap
=====================================================================

Description
-----------
Interactive world map with optional country coloring (choropleth) and
lon/lat markers. Country coloring follows the same idea as the worldmap
package: pass names (fuzzy-matched to the map) plus optional colors,
opacity, or numeric values.

Example
-------
>>> from d3blocks import D3Blocks
>>> d3 = D3Blocks()
>>> # Markers only
>>> df = d3.import_example('surfspots')
>>> d3.maps(df)
>>>
>>> # Country coloring (worldmap-style) without markers
>>> d3.maps(country_names=['Netherlands', 'France', 'Germany'], cmap='Set1')
>>>
>>> # Regional map: Dutch provinces
>>> d3.maps(country_names=['Zeeland', 'Overijssel', 'Flevoland'],
...         map_name='netherlands', cmap='Set1')
>>>
>>> # Countries + values (opacity scaled) + markers
>>> d3.maps(df,
...         country_names=['Netherlands', 'Australia', 'USA'],
...         country_values=[10, 5, 20],
...         cmap='Blues')
>>>
>>> # Explicit countries dict
>>> d3.maps(df, countries={
...     'World': {'color': '#D3D3D3', 'opacity': 0.4, 'line': 'none', 'linewidth': 0.1},
...     'Netherlands': {'color': '#000FFF', 'opacity': 0.5},
...     'France': {'color': '#FFA500', 'opacity': 1, 'line': 'dashed', 'linewidth': 2},
... })
>>>
>>> # Stepwise workflow
>>> d3 = D3Blocks(chart='maps', frame=False)
>>> d3.set_node_properties(df)
>>> d3.set_edge_properties(country_names=['Netherlands', 'Belgium'], cmap='Set2')
>>> d3.show()

References
----------
https://github.com/d3blocks/d3blocks

"""
