"""Colors countries or specific regions in a country."""
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
import webbrowser

from worldmap.zip_extract import zip_extract
from worldmap.deepStringMatching import deepStringMatching

global PATH_MAPZIP, CITYCODE
curpath = os.path.dirname(os.path.abspath(__file__))
CITYCODE = os.path.abspath(os.path.join(curpath,'data','citycode.txt'))
PATH_MAPZIP = os.path.abspath(os.path.join(curpath,'data','SVG_MAPS.zip'))


# %% Main
def plot(county_names, map_name='world', opacity=[], cmap='Set1', filename='custom_map.svg', showfig=True, verbose=True):
    """Color countries.

    Parameters
    ----------
    county_names : list of str
        Names of countries or regions within a county to be colored.
    map_name : str, optional
        Name of the county to be colored. The default is 'world'.
    opacity : list of float [0-1], optional
        Set the opacity for each of the map_name(s). The default is [].
        If values are >1, it is scaled between [0-1]
        0 = full transparancy, 1= no transparancy
    cmap : str, optional
        Colormap to be used. Colors is set on the unique county_names. The default is 'Set1'. All colormaps can be reverted using the "_r": e.g., binary_r
        ['#ffffff','#1f1f1f']: Each map with a specified color
        ['#ff0000']: All maps have a red color
        'Set1'     : Discrete colors (default)
        'Pastel1'  : Discrete colors
        'Paired'   : Discrete colors
        'bwr'      : Blue-white-red
        'RdBu'     : Red-white-Blue
        'binary'   : black-white
        'seismic'  : Blue-white-red
        'rainbow'  : all coors
        'Blues'    : white-to-blue
    filename : str, optional
        filepath to write the output file. The default is 'custom_map.svg'.
    showfig : bool, optional
        Open figure in browser. The default is False.
    verbose : int, optional
        print message to screen. The default is True.

    Returns
    -------
    tuple containing dict (out) with results and the filename (out, filename).

    """
    Param = {}
    Param['county_names'] = county_names
    Param['opacity'] = opacity
    Param['verbose'] = verbose
    Param['map_name'] = map_name
    Param['filename'] = filename
    Param['showfig'] = showfig
    Param['cmap'] = cmap

    # FILES
    [DIROK, DIRMAP] = download_resources()
    if not DIROK: return

    # SETUP COLORS SCHEMES
    if Param['opacity']==[]:
        Param['opacity']=np.ones(len(Param['county_names']))
    else:
        if np.any(np.array(Param['opacity'])>1):
            if Param['verbose']: print('[worldmap] Scaling opacity between [0-1]')
            Param['opacity'] = minmax_scale(np.append([0,np.max(Param['opacity']) * 1.5],Param['opacity']))
            Param['opacity'] = Param['opacity'][2:]

    # Get color schemes
    if 'str' in str(type(Param['cmap'])):
        getcolors=np.array(sns.color_palette(Param['cmap'],len(Param['county_names'])).as_hex())
        # getcolors=colourmap.generate(len(Param['county_names']), cmap=Param['cmap'])
    elif 'list' in str(type(Param['cmap'])) and len(Param['cmap'])==1:
        getcolors=np.repeat(Param['cmap'], len(Param['county_names']))
    else:
        getcolors=Param['cmap']

    # READ MAP FROM DIRECTORY AND MATCH WITH DESIRED MAP
    getsvg = _matchmap(Param['map_name'])

    # PARSE SVG
    [paths, attributes] = svg2paths(os.path.join(DIRMAP,getsvg))
    if Param['verbose']: print('[worldmap] Map loaded and parsed: %s' %(getsvg))

    # Extract city names to color them according the scores
    d = {'county_names':Param['county_names'], 'SVGcity':np.nan, 'opacity': Param['opacity'], 'fill':getcolors, 'attr':np.nan}
    df = pd.DataFrame(d)

    # Retrieve all city/county names
    SVGcounty_names=[]
    for i in range(0,len(attributes)):
        SVGcounty_names = np.append(SVGcounty_names, attributes[i]['title'])

    # Match with best input-names
    [dfmatch,_] = deepStringMatching(SVGcounty_names,Param['county_names'], methodtype='FUZZY', verbose=0)
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

    if Param['verbose']: print('[worldmap] %.0f out of %.0f cities/counties detected and processed.' %(df.shape[0], len(Param['county_names'])))

    # DFOUT
    SVGcounty_namesOUT=[]
    for i in range(0,len(attributesOUT)):
        SVGcounty_namesOUT = np.append(SVGcounty_namesOUT, attributesOUT[i]['title'])
    d = {'county_names':SVGcounty_namesOUT, 'SVGcity':SVGcounty_namesOUT, 'opacity': 1, 'fill':'#CCCCCC', 'attr':attributesOUT}
    dfout = pd.DataFrame(d)
    dfout=pd.concat((df,dfout), axis=0)

    # WRITE TO FILE
    _to_svg(df, attributesOUT, Param)

    # Open figures
    if Param['showfig']: webbrowser.open(os.path.abspath(Param['filename']), new=2)

    del dfout['attr']
    return(dfout, filename)


# %% Loopup available names for map
def county_names(map_name='world'):
    """Retrieve all county_names

    Parameters
    ----------
    map_name : str, optional
        Name of the country. The default is 'world'.

    Returns
    -------
    list of county/country names.

    """
    [DIROK, DIRMAP] = download_resources()
    if not DIROK: return

    getsvg = _matchmap(map_name)
    [paths, attributes] = svg2paths(os.path.join(DIRMAP, getsvg))

    SVGcounty_names=[]
    for i in range(0,len(attributes)):
        SVGcounty_names = np.append(SVGcounty_names, attributes[i]['title'])

    return(SVGcounty_names)


# %% Loopup code for cityname
def map_names():
    """Retrieve all map names.

    Returns
    -------
    list of str containing map names.

    """
    [DIROK, DIRMAP] = download_resources()
    if DIROK:
        dirfiles = os.listdir(DIRMAP)
        getfiles = [s for s in dirfiles if "svg" in s]
        getcounty_names = list(map(lambda x: str.replace(x, "High", ""), getfiles))
        getcounty_names = list(map(lambda x: str.replace(x, ".svg", ""), getcounty_names))
        getcounty_names = list(map(lambda x: str.lower(x), getcounty_names))
        return(getcounty_names, getfiles)


# %% Loopup abbrevation for county_name
def county2code(county_names):
    """Convert county_name to abbrevation code.

    Parameters
    ----------
    county_names : list of str
        list containing county_names.

    Returns
    -------
    list of str containing abbrevations.

    """
    [DIROK, DIRMAP] = download_resources()

    df=pd.read_csv(CITYCODE, sep=';', encoding='latin1')
    try:
        [dfmatch,_]=deepStringMatching(df.Country,county_names,methodtype='FUZZY', verbose=0)
        citymatch = dfmatch.idxmax(axis=0).values
        dfmatch.index=list(df.code)
        citycode = list(dfmatch.idxmax(axis=0).values)
    except:
        idx = np.where(np.isin(df.Country.str.lower(), county_names.lower()))[0]
        if len(idx)!=0:
            citycode = df.code.iloc[idx].values[0]
            citymatch = df.Country.iloc[idx].values[0]

    return(citycode, citymatch)


# %% Loopup county_names for abbrevation
def code2county(codes):
    """Convert abbrevation code to county_name.

    Parameters
    ----------
    codes : list of str.
        list containing codes.

    Returns
    -------
    list of str containing county_names.

    """
    [DIROK, DIRMAP] = download_resources()

    citymatch=''
    codes = str.lower(codes)
    df=pd.read_csv(CITYCODE, sep=';', encoding='latin1')
    idx = np.where(np.isin(df.code.str.lower(), codes))[0]
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


# %% Loopup code for cityname
def _matchmap(map_name):
    out=''
    # Get all map names from directory
    [getcounty_names,getfiles] = map_names()

    # Match name
    try:
        [dfmatch,_]=deepStringMatching(getcounty_names, map_name, methodtype='FUZZY', verbose=0)
        getfiles=np.array(getfiles)
        out=getfiles[np.isin(getcounty_names, dfmatch.idxmax(axis=0)[0])][0]
    except:
        idx = np.where(np.isin(getcounty_names, map_name.lower()))[0]
        if len(idx)!=0:
            out = np.array(getfiles)[idx][0]

    return(out)


# %% Extract the zipped directory of needed
def _extract_zip_files(PATH_MAPZIP):
    DIRMAP = PATH_MAPZIP.replace('.zip','')

    if os.path.isdir(DIRMAP) is False:
        print('[worldmap.extract] Warning: Directory with maps does not exist: %s' %(DIRMAP))
        if os.path.isfile(PATH_MAPZIP):
            zipdir=zip_extract(PATH_MAPZIP)
            DIRMAP = os.path.join(zipdir['dir'],zipdir['file_clean'])

    return(os.path.isdir(DIRMAP), DIRMAP)


# %% Loopup available names for map
def _to_svg(df, attributesOUT, Param):
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
        # dfout
        gettext=('<path id="%s" title="%s" class="%s" d="%s"' %(attributesOUT[i]['id'], attributesOUT[i]['title'], attributesOUT[i]['class'], attributesOUT[i]['d']))
        f.write(gettext + '/>' + '\n')

    f.write('</g>\n')
    f.write('</svg>\n')

    # CLOSE
    f.close()
    if Param['verbose']: print('[worldmap] Fin!')
