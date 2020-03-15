# %%
import worldmap

# %% Retrieve availble maps that can be used to superimpose data on top of it
[availableMaps,filenames] = worldmap.getmaps()

# %% Retrieve names in map
country_names = worldmap.getmapnames(map_name='world')
country_names = worldmap.getmapnames(map_name='netherlands')
country_names = worldmap.getmapnames(map_name='belgium')
country_names = worldmap.getmapnames(map_name='new zealand')

# %% Retrieve citynames for abbrevations
out = worldmap.code2city('NL')
out = worldmap.code2city('GB')

# %% Retrieve abbrevations for city names
out = worldmap.city2code('Netherlands')
out = worldmap.city2code('Germany')

# %% Coloring of maps
country_names = ['Norway','Nederland','Dominican Republic','Salvador']
opacity = [10, 25, 5, 100]
out = worldmap.colormap(country_names, opacity=opacity, map_name='world')

country_names = ['Nederland', 'belgium']
cmap = ['#0f0f0f','#0f0f0f']
out = worldmap.colormap(country_names, cmap=cmap, map_name='world')

country_names = ['zeeland','Overijssel', 'flevoland']
opacity = [0.4, 0.6, 0.9]
out = worldmap.colormap(country_names,opacity=opacity, cmap='Set1', map_name='netherlands', filename='c://temp/nederlandMap.svg')
