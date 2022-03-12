from worldmap.worldmap import (
    plot,
    code2county,
    county2code,
    list_county_names,
    list_map_names,
    )

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.7'

# module level doc-string
__doc__ = """
worldmap
=====================================================================

Description
-----------
worldmap is to plot and color countries or specific regions in a country using offline approaches.

Example
-------
>> # Import library
>> import worldmap as wm
>>
>> # Set the regions to plot
>> region = ['zeeland','Overijssel', 'flevoland']
>>
> # Color the regions
>> opacity = [0.1, 0.2, 0.6]
>>
>> # Create the SVG
>> results = wm.plot(region, opacity=opacity, cmap='Set1', map_name='netherlands')

References
----------
* https://github.com/erdogant/worldmap
* http://www.amcharts.com/svg-maps/

"""
