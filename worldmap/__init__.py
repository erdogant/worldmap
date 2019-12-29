from worldmap.worldmap import (
    colormap,
    getmapnames,
	getmaps,
	code2city,
	city2code,
)

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
#__version__ = '0.1.0'

# Automatic version control
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


# module level doc-string
__doc__ = """
WORLDMAP - Color the worldmap.
=====================================================================

**worldmap** 
See README.md file for more information.

"""
