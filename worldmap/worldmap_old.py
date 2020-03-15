""" This function colors maps, either countries in the worldmap or counties for a specific country

    import worldmap as worldmap

	A= worldmap.colormap(names, <optional>)

 INPUT:
   names:          List of strings: 
                   ['Nederland', 'belgium']             # if world is choosen
                   ['zeeland','brabant', 'flevoland']   # if netherlands is choosen

 OPTIONAL:

   loadmap:        String: Specify for the map to be used. If a country-map is loaded, names become county names, otherwise specify the country names.
                   'worldmap' (default)
                   'netherlands'
                   http://www.amcharts.com/svg-maps/ or all maps
                   
   opacity:        List or numpy array of floats: Specify for each country the opacity to be colored. Note that, if values are >1, it is scaled between [0-1]
                   [] (default) All countries have maximum=1 opacity
                   [0.1, 0.8, ...]

   dirmap:         String: Specify the direcory where the SVG maps are stored.
                   '../DATA/MAPS/' (default)

   filename:       String: Specify the filename to output the custom map.
                   'custom_map.svg' (default)

   cmap:           String: Colormap https://matplotlib.org/examples/color/colormaps_reference.html
                   ['#ffffff','#1f1f1f']: Each map with a specified color
                   ['#ff0000']: All maps have a red color

                   'Set1'       Discrete colors (default)
                   'Pastel1'    Discrete colors 
                   'Paired'     Discrete colors
                   'bwr'        Blue-white-red 
                   'RdBu'       Red-white-Blue
                   'binary' or 'binary_r'
                   'seismic'    Blue-white-red 
                   'rainbow'
                   'Blues'      white-to-blue
                   or a custom colormap:


  verbose:        Boolean [0,1] or [True,False]
                   False: No (default)
                   True: Yes

 OUTPUT
	output

 DESCRIPTION
   1. Download SVG map at: http://www.amcharts.com/svg-maps/
   2. Specifcy the countries of counties that you want to color
   3. Run function!



"""

#--------------------------------------------------------------------------
# Name        : worldmap.py
# Version     : 1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Aug. 2018
#--------------------------------------------------------------------------

#%% Libraries
import os

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import minmax_scale
from svgpathtools import svg2paths
# import webbrowser

from worldmap.zip_extract import zip_extract
from worldmap.deepStringMatching import deepStringMatching

global PATH_MAPZIP, CITYCODE
curpath = os.path.dirname(os.path.abspath( __file__ ))
CITYCODE = os.path.abspath(os.path.join(curpath,'data/citycode.txt'))
PATH_MAPZIP = os.path.abspath(os.path.join(curpath,'data/SVG_MAPS.zip'))

#%% Extract the zipped directory of needed
def extract_zip_files(PATH_MAPZIP):
    DIRMAP = PATH_MAPZIP.replace('.zip','')
    
    if os.path.isdir(DIRMAP)==False:
        print('[MAPS] Warning: Directory with maps does not exist: %s' %(DIRMAP))
        if os.path.isfile(PATH_MAPZIP):
            zipdir=zip_extract(PATH_MAPZIP)
            DIRMAP = os.path.join(zipdir['dir'],zipdir['file_clean'])

    return(os.path.isdir(DIRMAP), DIRMAP)

#%% Main
def colormap(names, loadmap='world', opacity=[], cmap='Set1', filename='custom_map.svg', verbose=True):
	# DECLARATIONS
    # Make dictionary to store Parameters
    Param = {}
    Param['citynames'] = names
    Param['opacity']   = opacity
    Param['verbose']   = verbose
    Param['loadmap']   = loadmap
    Param['filename']  = filename
    Param['cmap']      = cmap

    # FILES
    [DIROK, DIRMAP] = extract_zip_files(PATH_MAPZIP)
    if not DIROK: return
        
    # SETUP COLORS SCHEMES
    if Param['opacity']==[]:
        Param['opacity']=np.ones(len(Param['citynames']))
    else:
        if np.any(np.array(Param['opacity'])>1):
            if Param['verbose']: print('[MAPS] Scaling opacity between [0-1]')
            Param['opacity']=minmax_scale(np.append([0,np.max(Param['opacity'])*1.5],Param['opacity']))
            Param['opacity']=Param['opacity'][2:]

    # Get color schemes
    if 'str' in str(type(Param['cmap'])):
        getcolors=np.array(sns.color_palette(Param['cmap'],len(Param['citynames'])).as_hex())
    elif 'list' in str(type(Param['cmap'])) and len(Param['cmap'])==1:
        getcolors=np.repeat(Param['cmap'], len(Param['citynames']))
    else:
        getcolors=Param['cmap']
        
    # READ MAP FROM DIRECTORY AND MATCH WITH DESIRED MAP
    getsvg = matchmap(Param['loadmap'])
    
    # PARSE SVG
    [paths, attributes] = svg2paths(os.path.join(DIRMAP,getsvg))
    if Param['verbose']: print('[MAPS] Map loaded and parsed: %s' %(getsvg))

    # Extract city names to color them according the scores
    d = {'citynames':Param['citynames'], 'SVGcity':np.nan, 'opacity': Param['opacity'], 'fill':getcolors, 'attr':np.nan}
    df = pd.DataFrame(d)
    
    # Retrieve all city/county names
    SVGcitynames=[]
    for i in range(0,len(attributes)):
        SVGcitynames = np.append(SVGcitynames, attributes[i]['title'])

    # Match with best input-names
    # SVGcitynames=list(map(str.lower,SVGcitynames))
    # Param['citynames']=list(map(str.lower,Param['citynames']))
    # idxIN = np.where(np.isin(SVGcitynames, Param['citynames']))[0]
    # attributesIN = np.array(attributes)[idxIN]
    # idxOUT = np.where(np.isin(SVGcitynames, Param['citynames']))[0]
    # attributesOUT = np.array(attributes)[idxOUT]
    
    [dfmatch,_]  = deepStringMatching(SVGcitynames,Param['citynames'], methodtype='FUZZY', verbose=0)
    # IN
    SVGcolorCity = dfmatch.idxmax(axis=0).index.values
    dfmatch.reset_index(inplace=True, drop=True)
    idx          = dfmatch.idxmax(axis=0).values
    attributesIN = np.array(attributes)[idx]
    # OUT
    idxOUT=np.setdiff1d(np.arange(0,dfmatch.shape[0]),idx)
    attributesOUT = np.array(attributes)[idxOUT]

    # STORE
    df['SVGcity'] = SVGcolorCity
    df['SVGcity'] = df['SVGcity'].str.replace(' ','')
    df['attr']    = attributesIN
    
    if Param['verbose']: print('[MAPS] %.0f out of %.0f cities/counties detected and processed.' %(df.shape[0], len(Param['citynames'])))

    # DFOUT
    SVGcitynamesOUT=[]
    for i in range(0,len(attributesOUT)):
        SVGcitynamesOUT = np.append(SVGcitynamesOUT, attributesOUT[i]['title'])

    d = {'citynames':SVGcitynamesOUT, 'SVGcity':SVGcitynamesOUT, 'opacity': 1, 'fill':'#CCCCCC', 'attr':attributesOUT}
    dfout = pd.DataFrame(d)
    
    # COMBINE DATAFRAMES
    dfout=pd.concat((df,dfout), axis=0)
    
    # WRITE TO FILE
    if Param['verbose']: print('[MAPS] Writing custom map to file: %s' %(Param['filename']))
    
    # OPEN FILE
    f = open(Param['filename'], "w+")
#    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<?xml version="1.0" encoding="latin1"?>\n')
    f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:amcharts="http://amcharts.com/ammap" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">\n\n\n')
    f.write('<defs>\n')

    # WRITE THE COLORSCHEME STYLES
    f.write('<style type="text/css">\n')
    for i in range(0,df.shape[0]):
    	f.write('       .'+df.SVGcity.iloc[i]+'\n')
    	f.write('		{\n')
    	f.write('					fill: '+str(df.fill.iloc[i])+';\n')
    	f.write('					fill-opacity: '+str(df.opacity.iloc[i])+';\n')
    	f.write('					stroke:white;\n')
    	f.write('					stroke-opacity: 1;\n')
    	f.write('					stroke-width:0.5;\n')
    	f.write('		}\n')
    #end

    # WRITE DEFAULT SETTINGS FOR ALL OTHER COUNTRIES
    f.write('       .land\n')
    f.write('		{\n')
    f.write('					fill: #CCCCCC;\n')
    f.write('					fill-opacity: 1;\n')
    f.write('					stroke:white;\n')
    f.write('					stroke-opacity: 1;\n')
    f.write('					stroke-width:0.5;\n')
    f.write('		}\n')

    f.write('</style>\n')
    f.write('</defs>\n')

    # WRITE THE COORDINATES OF THE CITIES/COUNTRIES
    f.write('<g>\n')

    # WRITE SELECTED COUNTRIES
    for i in range(0,df.shape[0]):
        gettext=('<path id="%s" title="%s" class="%s" d="%s"' %(df.attr.iloc[i]['id'], df.attr.iloc[i]['title'], df.SVGcity.iloc[i], df.attr.iloc[i]['d']) )
        f.write(gettext+'/>'+'\n')

    # Write all other countries 
    for i in range(0,len(attributesOUT)):
        dfout
        gettext=('<path id="%s" title="%s" class="%s" d="%s"' %(attributesOUT[i]['id'], attributesOUT[i]['title'], attributesOUT[i]['class'], attributesOUT[i]['d']) )
        f.write(gettext+'/>'+'\n')
    
    f.write('</g>\n')
    f.write('</svg>\n')

    # CLOSE
    f.close()    
    if Param['verbose']: print('[MAPS] Done!')

    # END
    del dfout['attr']

    # Show figure
    # if Param['showfig']:
    #     try:
    #         webbrowser(filename)
    #     except:
    #         print('[MAP] Could not show figure.')

    return(dfout, filename)

#%% Loopup available names for map
#def getmapnames(loadmap='world', dirmap='../DATA/MAPS/SVG_MAPS/'):
def getmapnames(loadmap='world'):
    [DIROK, DIRMAP] = extract_zip_files(PATH_MAPZIP)
    if not DIROK: return

    getsvg = matchmap(loadmap)
    [paths, attributes] = svg2paths(os.path.join(DIRMAP, getsvg))
    
    SVGcitynames=[]
    for i in range(0,len(attributes)):
        SVGcitynames = np.append(SVGcitynames, attributes[i]['title'])

    return(SVGcitynames)
    
#%% Loopup code for cityname
#def getmaps(dirmap='../DATA/MAPS/SVG_MAPS/'):
def getmaps():

    [DIROK, DIRMAP] = extract_zip_files(PATH_MAPZIP)
    if not DIROK: return
    
    dirfiles     = os.listdir(DIRMAP)
    getfiles     = [s for s in dirfiles if "svg" in s]
    getcitynames = list(map(lambda x: str.replace(x, "High", ""), getfiles))
    getcitynames = list(map(lambda x: str.replace(x, ".svg", ""), getcitynames))
    getcitynames = list(map(lambda x: str.lower(x), getcitynames))
    return(getcitynames, getfiles)

#%% Loopup code for cityname
def matchmap(loadmap):
    out=''
    #Get all map names from directory
    [getcitynames,getfiles] = getmaps()
    # Match name
    try:
        [dfmatch,_]=etlearn.textmining.deepStringMatching(getcitynames, loadmap, methodtype='FUZZY', verbose=0)
        getfiles=np.array(getfiles)
        out=getfiles[np.isin(getcitynames, dfmatch.idxmax(axis=0)[0])][0]
    except:
        idx = np.where(np.isin(getcitynames, loadmap.lower()))[0]
        if len(idx)!=0:
            out = np.array(getfiles)[idx][0]
            
    return(out)
    
#%% Loopup code for cityname
def city2code(citynames):
    df=pd.read_csv(CITYCODE, sep=';', encoding='latin1')
    try:
        [dfmatch,_]=deepStringMatching(df.Country,citynames,methodtype='FUZZY', verbose=0)
        citymatch = dfmatch.idxmax(axis=0).values
        dfmatch.index=list(df.code)
        citycode = list(dfmatch.idxmax(axis=0).values)
    except:
        idx = np.where(np.isin(df.Country.str.lower(), citynames.lower()))[0]
        if len(idx)!=0:
            citycode = df.code.iloc[idx].values[0]
            citymatch = df.Country.iloc[idx].values[0]
            
    return(citycode, citymatch)

#%% Loopup cityname for citycode
def code2city(citycodes):
    citymatch=''
    citycodes = str.lower(citycodes)
    df=pd.read_csv(CITYCODE, sep=';', encoding='latin1')
    idx = np.where(np.isin(df.code.str.lower(), citycodes))[0]
    if len(idx)!=0:
        citymatch = df.Country.iloc[idx].values[0]
        citycode = df.code.iloc[idx].values[0]
    return(citycode, citymatch)    
