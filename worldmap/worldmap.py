"""Colors countries in the worldmap or regions for a specific country."""
# --------------------------------------------------
# Name        : worldmap.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : https://github.com/erdogant/worldmap
# Licence     : MIT
# --------------------------------------------------


# %% Libraries
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale
from svgpathtools import svg2paths
import colourmap
import seaborn as sns

from worldmap.zip_extract import zip_extract
from worldmap.deepStringMatching import deepStringMatching

global PATH_MAPZIP, CITYCODE
curpath = os.path.dirname(os.path.abspath(__file__))
CITYCODE = os.path.abspath(os.path.join(curpath,'data','citycode.txt'))
PATH_MAPZIP = os.path.abspath(os.path.join(curpath,'data','SVG_MAPS.zip'))


# %% Main
def colormap(country_names, map_name='world', opacity=[], cmap='Set1', filename='custom_map.svg', verbose=True):
    """Color countries.

    Parameters
    ----------
    country_names : list of str
        DESCRIPTION.
    map_name : TYPE, optional
        DESCRIPTION. The default is 'world'.
    opacity : TYPE, optional
        DESCRIPTION. The default is [].
    cmap : TYPE, optional
        DESCRIPTION. The default is 'Set1'.
    filename : TYPE, optional
        DESCRIPTION. The default is 'custom_map.svg'.
    verbose : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    None.

    """
	# DECLARATIONS
    # Make dictionary to store Parameters
    Param = {}
    Param['country_names'] = country_names
    Param['opacity'] = opacity
    Param['verbose'] = verbose
    Param['map_name'] = map_name
    Param['filename'] = filename
    Param['cmap'] = cmap

    # FILES
    [DIROK, DIRMAP] = download_resources()
    if not DIROK: return

    # SETUP COLORS SCHEMES
    if Param['opacity']==[]:
        Param['opacity']=np.ones(len(Param['country_names']))
    else:
        if np.any(np.array(Param['opacity'])>1):
            if Param['verbose']: print('[worldmap] Scaling opacity between [0-1]')
            Param['opacity'] = minmax_scale(np.append([0,np.max(Param['opacity']) * 1.5],Param['opacity']))
            Param['opacity'] = Param['opacity'][2:]

    # Get color schemes
    if 'str' in str(type(Param['cmap'])):
        getcolors=np.array(sns.color_palette(Param['cmap'],len(Param['country_names'])).as_hex())
        # getcolors=colourmap.generate(len(Param['country_names']), cmap=Param['cmap'])
    elif 'list' in str(type(Param['cmap'])) and len(Param['cmap'])==1:
        getcolors=np.repeat(Param['cmap'], len(Param['country_names']))
    else:
        getcolors=Param['cmap']

    # READ MAP FROM DIRECTORY AND MATCH WITH DESIRED MAP
    getsvg = matchmap(Param['map_name'])

    # PARSE SVG
    [paths, attributes] = svg2paths(os.path.join(DIRMAP,getsvg))
    if Param['verbose']: print('[worldmap] Map loaded and parsed: %s' %(getsvg))

    # Extract city names to color them according the scores
    d = {'country_names':Param['country_names'], 'SVGcity':np.nan, 'opacity': Param['opacity'], 'fill':getcolors, 'attr':np.nan}
    df = pd.DataFrame(d)

    # Retrieve all city/county names
    SVGcountry_names=[]
    for i in range(0,len(attributes)):
        SVGcountry_names = np.append(SVGcountry_names, attributes[i]['title'])

    # Match with best input-names
    # SVGcountry_names=list(map(str.lower,SVGcountry_names))
    # Param['country_names']=list(map(str.lower,Param['country_names']))
    # idxIN = np.where(np.isin(SVGcountry_names, Param['country_names']))[0]
    # attributesIN = np.array(attributes)[idxIN]
    # idxOUT = np.where(np.isin(SVGcountry_names, Param['country_names']))[0]
    # attributesOUT = np.array(attributes)[idxOUT]

    [dfmatch,_] = deepStringMatching(SVGcountry_names,Param['country_names'], methodtype='FUZZY', verbose=0)
    # IN
    SVGcolorCity = dfmatch.idxmax(axis=0).index.values
    dfmatch.reset_index(inplace=True, drop=True)
    idx = dfmatch.idxmax(axis=0).values
    attributesIN = np.array(attributes)[idx]
    # OUT
    idxOUT=np.setdiff1d(np.arange(0,dfmatch.shape[0]),idx)
    attributesOUT = np.array(attributes)[idxOUT]

    # STORE
    df['SVGcity'] = SVGcolorCity
    df['SVGcity'] = df['SVGcity'].str.replace(' ','')
    df['attr'] = attributesIN

    if Param['verbose']: print('[worldmap] %.0f out of %.0f cities/counties detected and processed.' %(df.shape[0], len(Param['country_names'])))

    # DFOUT
    SVGcountry_namesOUT=[]
    for i in range(0,len(attributesOUT)):
        SVGcountry_namesOUT = np.append(SVGcountry_namesOUT, attributesOUT[i]['title'])

    d = {'country_names':SVGcountry_namesOUT, 'SVGcity':SVGcountry_namesOUT, 'opacity': 1, 'fill':'#CCCCCC', 'attr':attributesOUT}
    dfout = pd.DataFrame(d)

    # COMBINE DATAFRAMES
    dfout=pd.concat((df,dfout), axis=0)

    # WRITE TO FILE
    if Param['verbose']: print('[worldmap] Writing custom map to file: %s' %(Param['filename']))

    # OPEN FILE
    f = open(Param['filename'], "w+")
    # f.write('<?xml version="1.0" encoding="utf-8"?>\n')
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
        gettext=('<path id="%s" title="%s" class="%s" d="%s"' %(df.attr.iloc[i]['id'], df.attr.iloc[i]['title'], df.SVGcity.iloc[i], df.attr.iloc[i]['d']))
        f.write(gettext + '/>' + '\n')

    # Write all other countries
    for i in range(0,len(attributesOUT)):
        dfout
        gettext=('<path id="%s" title="%s" class="%s" d="%s"' %(attributesOUT[i]['id'], attributesOUT[i]['title'], attributesOUT[i]['class'], attributesOUT[i]['d']) )
        f.write(gettext + '/>' + '\n')

    f.write('</g>\n')
    f.write('</svg>\n')

    # CLOSE
    f.close()
    if Param['verbose']: print('[worldmap] Done!')

    del dfout['attr']
    return(dfout, filename)

#%% Loopup available names for map
def getmapnames(map_name='world'):
    [DIROK, DIRMAP] = download_resources()
    # [DIROK, DIRMAP] = _extract_zip_files(PATH_MAPZIP)
    if not DIROK: return

    getsvg = matchmap(map_name)
    [paths, attributes] = svg2paths(os.path.join(DIRMAP, getsvg))
    
    SVGcountry_names=[]
    for i in range(0,len(attributes)):
        SVGcountry_names = np.append(SVGcountry_names, attributes[i]['title'])

    return(SVGcountry_names)
    
#%% Loopup code for cityname
def getmaps():
    [DIROK, DIRMAP] = download_resources()
    # [DIROK, DIRMAP] = _extract_zip_files(PATH_MAPZIP)
    if not DIROK: 
        return
    else:
        dirfiles     = os.listdir(DIRMAP)
        getfiles     = [s for s in dirfiles if "svg" in s]
        getcountry_names = list(map(lambda x: str.replace(x, "High", ""), getfiles))
        getcountry_names = list(map(lambda x: str.replace(x, ".svg", ""), getcountry_names))
        getcountry_names = list(map(lambda x: str.lower(x), getcountry_names))
        return(getcountry_names, getfiles)

#%% Loopup code for cityname
def matchmap(map_name):
    out=''
    #Get all map names from directory
    [getcountry_names,getfiles] = getmaps()
    # Match name
    try:
        [dfmatch,_]=deepStringMatching(getcountry_names, map_name, methodtype='FUZZY', verbose=0)
        getfiles=np.array(getfiles)
        out=getfiles[np.isin(getcountry_names, dfmatch.idxmax(axis=0)[0])][0]
    except:
        idx = np.where(np.isin(getcountry_names, map_name.lower()))[0]
        if len(idx)!=0:
            out = np.array(getfiles)[idx][0]
            
    return(out)
    
#%% Loopup code for cityname
def city2code(country_names):
    df=pd.read_csv(CITYCODE, sep=';', encoding='latin1')
    try:
        [dfmatch,_]=deepStringMatching(df.Country,country_names,methodtype='FUZZY', verbose=0)
        citymatch = dfmatch.idxmax(axis=0).values
        dfmatch.index=list(df.code)
        citycode = list(dfmatch.idxmax(axis=0).values)
    except:
        idx = np.where(np.isin(df.Country.str.lower(), country_names.lower()))[0]
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


# %% Import example dataset from github.
def download_resources(url='https://erdogant.github.io/datasets/SVG_MAPS.zip', verbose=3):
    """Import example dataset from github.

    Parameters
    ----------
    url : str
        url-Link to dataset. The default is 'https://erdogant.github.io/datasets/SVG_MAPS.zip'.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    tuple containing import status and resources.

    """
    import wget
    curpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    PATH_TO_DATA = os.path.join(curpath, wget.filename_from_url(url))

    # Check file exists.
    if not os.path.isfile(PATH_TO_DATA):
        if verbose>=3: print('[worldmap] Downloading resources..')
        wget.download(url, curpath)

    # Extract and import local dataset
    [DIROK, DIRMAP] = _extract_zip_files(PATH_TO_DATA)
    # Return
    return DIROK, DIRMAP


# %% Extract the zipped directory of needed
def _extract_zip_files(PATH_MAPZIP):
    DIRMAP = PATH_MAPZIP.replace('.zip','')

    if os.path.isdir(DIRMAP) is False:
        print('[worldmap.extract] Warning: Directory with maps does not exist: %s' %(DIRMAP))
        if os.path.isfile(PATH_MAPZIP):
            zipdir=zip_extract(PATH_MAPZIP)
            DIRMAP = os.path.join(zipdir['dir'],zipdir['file_clean'])

    return(os.path.isdir(DIRMAP), DIRMAP)
