""" This function links small ALIAS words to longer input strings based on EXACT and FUZZY similarity

	[dist_matrix, bin_match] = deepStringMatching(data, alias, <optional>)
    v1.4
 
 INPUT:
   data=         : String array [list]

   alias=        : String: List of strings for which you seek a match in data
                   [] default

 OPTIONAL

   methodtype=   : [String]: There are 3 catagories
                   ['complete'] (default)   [Simple]->[advanced]->[Fuzzy]
                   ['EXACT-FAST']           [Simple]   substring mapping
                   ['EXACT-ACC']            [Advanced] substring mapping
                   ['FUZZY']                [Fuzzy]    substring mapping

   clean=        : [String]: ALIAS and DATA are cleaned as following (any combination is possible, clean=['numeric','lower-strip']):
                   ['complete'] (default) # All below
                   ['numeric']            # Removal of numerical values
                   ['lower-strip']        # Lower char and strip spaces at ends
                   ['alias-specific']     # Smart cleaning: adjust cleaning steps per ALIAS
                   [''] (None)

   scoreOK=      : [Float]: [0,..,1] Strings are always included when score is >=
                   [1] (default)
                   [1, 0.6, 0.9] # list of cutt-off scores. Must be length of input-parameter-alias

   remwords=     : [String]: List of strings that are a-priori removed from [data] and [magnet]
                   [] default

   minchar=      : [Integer]: Minimum number of chars (<=) that a word must contain, otherwise removed fron string
                   [3] default

   maxchar=      : [Integer]: Maximum number of chars (>=) that a word must contain, otherwise removed fron string
                   [15] default
                  
   verbose= : [Boolean] [0,1]
                   [1]: Yes (default)
                   [0]: No 

 OUTPUT
	output

 DESCRIPTION
   Detect similar words

 EXAMPLE
   %reset -f
   import pandas as pd
   import numpy as np
   from GENERAL.tictoc import tic, toc
   from TEXTMINING.deepStringMatching import deepStringMatching

# EXAMPLE 1
   data              = pd.read_csv("../DATA/OTHER/marketing_data_online_retail_small.csv",sep=';')
   data              = data.Description
   alias             = ['lantern','cream cupid hearts coat hanger','tlight holder','light']
   [outDIST1,outBIN] = deepStringMatching(data,alias)
   [outDIST,outBIN] = deepStringMatching(data,alias, scoreOK=0.9)
   [outDIST,outBIN] = deepStringMatching(data[0:150],data[0:150], scoreOK=0.9, clean='')
   [outDIST,outBIN] = deepStringMatching(data[0:50],data[0:50], scoreOK=[1,0.7,0.8,1])
   toc()

   alias=['Mc-donalds','Mc donalds','Mcdonalds','Mc-d on-al-ds']
   data = ['Mc-donalds','Mc donalds','Mcdonalds','M_c-d-o-na-l_ds','text in front Mcdonalds','text in front Mcdonalds and in back','front Mc donalds back','mcdon','front Mc donaldsAmsterdam back']
   [outDIST,outBIN] = deepStringMatching(data,alias,methodtype='FUZZY')
   outDIST.plot(rot=25, fontsize=18)
   from imagesc import imagesc
   imagesc(outDIST, cmap='Set1', annot=True, linewidth=1)

   
   from tsneBH import tsneBH
   from scatter import scatter
   from clusteval import clusteval
   from HDBSCAN import HDBSCAN
   [outDIST,outBIN] = deepStringMatching(data[0:500],data[0:500], methodtype='FUZZY', clean='complete')
   outxy = tsneBH(outDIST.values)
   labx  = clusteval(outxy)
   labx  = HDBSCAN(outxy)
   scatter(outxy[:,0],outxy[:,1], labx=labx['labx'], labx_txt=outDIST.columns.str.lower().str.strip().values, labx_type='', size=150)


 SEE ALSO
   lcs (longest common string)
   pip install fuzzywuzzy[speedup] #  python-Levenshtein matching
   fuzzywuzzy

"""

#--------------------------------------------------------------------------
# Name        : deepStringMatching.py
# Version     : 1.0
# Author      : E.Taskesen
# Date        : Dec. 2017
#--------------------------------------------------------------------------

#%% Global libraries
#import multiprocessing
import numpy as np
import pandas as pd
from tqdm import tqdm
import worldmap.utils.stringPreprocessing as stringPreprocessing

checkLen = np.vectorize(len) # To check length in arrays
from fuzzywuzzy import fuzz

#%%
def deepStringMatching(data, alias, remwords=[], minchar=2, maxchar=25, maxlen=200, scoreOK=1, clean=['complete'], methodtype=['complete'], verbose=1):
	#%% DECLARATIONS
    outBIN  = []

    # Make dictionary to store Parameters
    Param = {}
    Param['verbose']      = verbose
    Param['minchar']      = minchar      # Minimum number characters for a string
    Param['maxchar']      = maxchar      # Maximum number characters for a string
    Param['maxlen']       = maxlen       # Maximum length of a string in the array
    Param['sepchar']      = ' '          # Seperation character between words in line
    Param['clean']        = clean        # Clean input lists: ['complete','numeric','lower-strip']
    Param['scoreOK']      = scoreOK      # Every score of >= [scoreOK] will be added, whatever the P-value is
    Param['methodtype']   = methodtype   # Choose method type of mappping

    #%% Set methodtype
    if len(alias)==0:
        print("WARNING: ALIAS must contain a list of strings! <return>")
        return
    #end

    #%% INPUT CHECK
    if Param['verbose']: print(">Input check..")

    data     = stringPreprocessing.typecheck(data, Param['maxlen'])
    alias    = stringPreprocessing.typecheck(alias, Param['maxlen'])
    remwords = stringPreprocessing.typecheck(remwords, Param['maxlen'])

    Param['maxlen']  = np.max((Param['maxlen'],np.max(checkLen(alias))))
    Param['maxchar'] = np.max((Param['maxchar'],np.max(checkLen(alias))))    


    if Param['methodtype']=='FUZZY':
        Param['scoreOK']=0
    #end
    
    if 'int' in str(type(Param['scoreOK'])) or 'float' in str(type(Param['scoreOK'])):
        Param['scoreOK'] = np.ones(len(alias), dtype='float')*Param['scoreOK']
    else:
        Param['scoreOK'] = np.array(Param['scoreOK'])
    #end
    # Set NaN and values >0.99 at 1
    Param['scoreOK'][np.where(np.isnan(Param['scoreOK']))[0]]=1
    Param['scoreOK'][np.where(Param['scoreOK']>0.99)[0]]=1
    
        
    #%% Remove words from EXCLUDE LIST
    data = stringPreprocessing.stringRemWords(data, remwords)
    
    #%% Remove numbers in string
    if np.any(np.in1d(Param['clean'], ['complete','numeric'])):
        if Param['verbose']: print(">String cleaning (removal of numbers)..")
        data  = stringPreprocessing.delnumstring(data)
        alias = stringPreprocessing.delnumstring(alias)
    #end

    #%% Cleaning, Lower/strip from DATA
#    if np.any(np.in1d(Param['clean'], ['complete','lower-strip'])):
    if Param['verbose']: print(">String cleaning (lower/strip)..")
    data  = stringPreprocessing.stringClean(data)
    alias = stringPreprocessing.stringClean(alias)
        
    #%% Compute EXACT matching between string-in-data and alias
    outDIST = pd.DataFrame(index=data, data=False, columns=alias)
    outBIN  = np.zeros((len(data),len(alias)), dtype=bool)

    #%% COMPUTE EXACT MATCHES WITHOUT STRING PRE-CLEANING
    if np.any(np.in1d(Param['methodtype'], ['complete','EXACT-FAST'])):
        if Param['verbose']: print(">Start EXACT matching (warming-up) [%d rows].." %(outDIST.shape[0]))
        idx = np.where(outDIST.sum(axis=1)==0)[0]
        if len(idx)>0:
            outBIN[idx,:] = distance(data[idx], alias, Param, extensive=0)

    #%% COMPUTE EXACT MATCHES WITH STRING PRE-CLEANING
    if np.any(np.in1d(Param['methodtype'], ['complete','EXACT-ACC'])):
        idx = np.where(outDIST.sum(axis=1)==0)[0]
        if Param['verbose']: print("\n>Start EXACT matching (extensive) [%d rows].." %(len(idx)))
        if len(idx)>0:
            outBIN[idx,:] = distance(data[idx], alias, Param, extensive=1)
    
    #%% COMPUTE Levensthein distance WITH STRING PRE-CLEANING
    outDIST = pd.DataFrame(index=data, data=outBIN, columns=alias).astype(float)

    # Get only rows that did not lead in any hit
    idx = np.where(outDIST.sum(axis=1)==0)[0]
    # Get only columns to requires Levenstehin distance
    getidx=np.where(Param['scoreOK']<1)[0]

    # If any column (alias) and requires matching and there are rows unmatched, and if it is desired:
    if len(getidx)>0 and len(idx)>0 and np.any(np.in1d(Param['methodtype'], ['complete','FUZZY'])):
        if Param['verbose']: print("\n>Start FUZZY matching (extensive) [%d rows, %d columns].." %(len(idx),len(getidx)))
        try:
            outDIST.iloc[idx,getidx] = distanceLS(data[idx], alias[getidx], Param)
        except:
            print("\n>***WARNING: DATA MUST BE LOWERED AND TRIMMED FOR LEVENSTHEIN DISTANCE COMPUTATIONS***, Next time use: clean=['lower-strip']")
            data  = stringPreprocessing.stringClean(data)
            alias = stringPreprocessing.stringClean(alias)
            outBIN[idx,getidx] = distance(data[idx], alias[getidx], Param, extensive=1)

    #%% BINARIZE
    outBIN = pd.DataFrame(index=data, data=outBIN, columns=alias).astype(bool)

    #%% Return
    return(outDIST, outBIN)

#%% EXACT matching
def distance(data, alias, Param, extensive=0):
#    out = pd.DataFrame(index=range(0,len(data)), data=False, columns=alias)
    out = np.zeros((len(data),len(alias)), dtype=bool)
    for i in tqdm(range(0,len(alias))):
        # Advanced pre-processing based on alias
        if extensive==1 and np.any(np.in1d(Param['clean'], ['complete','alias-specific'])):
            # Matching with respect to ALIAS
            [dataPR, aliasPR] = stringPreprocessing.stringPreprocessing(data, [alias[i]], sepchar=Param['sepchar'])
            # Now remove, words with min-max-size, this step MUST be 
            dataPR            = stringPreprocessing.stringMinMaxSize(dataPR, minchar=Param['minchar'], maxchar=Param['maxchar'], sepchar=Param['sepchar'])
            df                = pd.DataFrame(index=range(0,len(data)),data=dataPR, columns=['data'])
            aliasPR           = aliasPR[0]
        else:
            df                = pd.DataFrame(index=range(0,len(data)), data=data, columns=['data'])
            aliasPR = alias[i]

        # CHeck existence in the MIDDLE
        getidx1=df.data[df['data'].str.contains(' '+aliasPR+' ')].index
        # CHeck existence in FRONT
        getidx2=df.data[df['data'].str[:len(aliasPR)+1].str.strip()==aliasPR].index
        # CHeck existence in BACK
        getidx3=df.data[df['data'].str[-len(aliasPR)-1:].str.strip()==aliasPR].index
        # Get unique
        getidx=np.unique(np.concatenate((getidx1,getidx2,getidx3)))

        # StoreS
#        out[alias[i]].iloc[getidx] = True
        out[getidx,i] = True
#        out[alias[i]].iloc[getidx] = np.ones((2,len(getidx)),dtype=bool)

    return(out)

#%% Group words based on NULL distribution
def distanceLS(data, alias, Param):
#    data=data[idx]
#    alias=alias[getidx]
    
    # Estimate distribution from emperical null-distribution
    out = np.zeros((data.shape[0],len(alias)))*np.nan
    # Compute score
    for i in tqdm(range(0,len(alias))):
        # Split strings and advanced cleaning for that is specific for the alias
        [dataPR, aliasPR] = stringPreprocessing.stringPreprocessing(data, [alias[i]], sepchar=Param['sepchar'])
        dataPR            = stringPreprocessing.stringMinMaxSize(dataPR, minchar=Param['minchar'], maxchar=Param['maxchar'], sepchar=Param['sepchar'])
        df                = pd.DataFrame(data=dataPR, columns=['data'])
        df['alias']       = aliasPR[0]
        
        # Compute score
        out[:,i] = (df.apply(fpartial, axis=1).values / 100 ) 
    #end
    return(out)

#%% PARTIAL FUZZSCORE
def fpartial(x):
#    return fuzz.ratio(str(x["alias"]),str(x["data"])) # Also take length of string into account -> uber <-> "pubermarkt test" = 42
    return fuzz.token_set_ratio(str(x["alias"]),str(x["data"])) # Whole word match (best practice for ALIAS mapping short->withstring) -> uber <-> "pubermarkt test" = 57
#    return fuzz.partial_token_set_ratio(str(x["alias"]),str(x["data"])) # Partial word match (best practise to create distance matrix)  -> uber <-> "pubermarkt test" = 100

#%% 