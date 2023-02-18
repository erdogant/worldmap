.. include:: add_top.add

Input
###########################

The input for ``worldmap`` is described in the docstrings :func:`worldmap.worldmap.plot` and is as following:

.. automodule:: worldmap.worldmap.plot
    :members:
    :undoc-members:


Output
###########################

The output of ``worldmap`` :func:`worldmap.worldmap.plot` is a ``tuple`` containing the following information:

	* pd.DataFrame	 : Dataframe with the plotted regions, and colors
	* filename	 : Filename

.. code:: python
	
	print(results[0])

	#     county_names        SVGcity  opacity     fill
	# 0        zeeland        zeeland      0.4  #e41a1c
	# 1     Overijssel     overijssel      0.6  #377eb8
	# 2      flevoland      flevoland      0.9  #4daf4a
	# 3        Drenthe        Drenthe      1.0  #CCCCCC
	# 4      Friesland      Friesland      1.0  #CCCCCC
	# 5     Gelderland     Gelderland      1.0  #CCCCCC
	# 6      Groningen      Groningen      1.0  #CCCCCC
	# 7        Limburg        Limburg      1.0  #CCCCCC
	# 8  Noord-Brabant  Noord-Brabant      1.0  #CCCCCC
	# 9  Noord-Holland  Noord-Holland      1.0  #CCCCCC
	# 10       Utrecht        Utrecht      1.0  #CCCCCC
	# 11  Zuid-Holland   Zuid-Holland      1.0  #CCCCCC

	print(results[1])
	'Netherlands_map.svg'



.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>


.. include:: add_bottom.add