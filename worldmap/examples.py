# --------------------------------------------------
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : https://github.com/erdogant/worldmap
# --------------------------------------------------

import numpy as np
from worldmap import worldmap

# %% Import class
from worldmap import worldmap
dir(worldmap)


#%%
from worldmap import worldmap

d3 = worldmap()
# Markers only
df = d3.import_example(data='surfspots')
d3.maps(df)

# %%

# Country coloring (worldmap-style) without markers
d3.maps(country_names=['Netherlands', 'France', 'Germany'], cmap='Set1')

# Regional map: Dutch provinces
d3.maps(country_names=['Zeeland', 'Overijssel', 'Flevoland'], map_name='netherlands', cmap='Set1')

# Countries + values (opacity scaled) + markers
d3.maps(df, country_names=['Netherlands', 'Australia', 'USA'], country_values=[10, 5, 20], cmap='Blues')

# Explicit countries dict
d3.maps(df, 
        countries={'World': {'color': '#D3D3D3', 'opacity': 0.4, 'line': 'none', 'linewidth': 0.1},
                   'Netherlands': {'color': '#000FFF', 'opacity': 0.5},
                   'France': {'color': '#FFA500', 'opacity': 1, 'line': 'dashed', 'linewidth': 2},
                   })


# %%
from worldmap import worldmap

# Stepwise workflow
d3 = worldmap(chart='maps', frame=False)
d3.set_node_properties(df)
d3.set_edge_properties(country_names=['Netherlands', 'Belgium'], cmap='Set2')
d3.show()
