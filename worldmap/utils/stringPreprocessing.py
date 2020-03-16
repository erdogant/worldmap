""" This function provides many string preprocessing options on array of strings

	A = stringPreprocessing(data, <optional>)
    v1.0
 
 INPUT:
   data=         : String array [list]


 OPTIONAL

   minchar=      : [Integer]: Minimum number of chars (<=) that a word must contain, otherwise removed fron string
                   [3] default

   maxchar=      : [Integer]: Maximum number of chars (>=) that a word must contain, otherwise removed fron string
                   [15] default

 OUTPUT
	output

 DESCRIPTION
   Preprocessing of strings

 EXAMPLE
   %reset -f
   import sys, os, importlib
   sys.path.append('D://Dropbox/BDR/toolbox_PY/general/')
   print(os.getcwd())
   import stringPreprocessing as bdr
   importlib.reload(bdr)
   import pandas as pd
   import numpy as np

 EXAMPLE 1
   data = ['lantern','cream cupid-hearts coat hanger','tli--ght holder','li-ght']
   data  = bdr.stringPreprocessing(data)

 SEE ALSO
   lcs
"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : stringPreprocessing.py
# Version     : 1.0
# Author      : E.Taskesen
# Date        : Dec. 2017
#--------------------------------------------------------------------------

#%% Global libraries
import numpy as np
import pandas as pd
import re
from tqdm import tqdm
import worldmap.utils.strtricks as strtricks # Some string tricks

checkLen = np.vectorize(len) # To check length in arrays

#%% Check datatypes and make them consistent
def typecheck(data, maxlen):
    if 'str' in str(type(data)):
        data=[data]
    #end

    if 'pandas' in str(type(data)):
        data = np.array(data)
        data = data.astype(str)
    elif 'list' in str(type(data)):
        data = np.array(data)
    elif 'numpy' in str(type(data)):
        data = data.astype(str)       
    #end

    # Cut string at maxlen chars
    data = data.astype('U'+str(maxlen))
    
    return(data)

#%% Removing words: NUMPY input
def stringRemWords(data, remwords):
    if len(remwords)>0:
        remwords = np.char.lower(remwords)
        remwords = np.char.strip(remwords)
        data     = np.char.lower(data)
        data     = np.char.strip(data)
        
        for i in range(0,len(remwords)):
            data=np.char.replace(data,remwords[i],'')
        #end
    #end
    return(data)

#%% Cleaning strings
def stringMinMaxSize(data, minchar=5, maxchar=25, sepchar=' '):
    # Get unique strings [for performance]
    data   = np.char.lower(data)
    data   = np.char.strip(data)
    uidata = np.unique(data)


#    df = pd.DataFrame(data=data, columns=['data'], dtype='str')
#    shortword = re.compile(r'\W*\b\w{1,'+str(minchar)+'}\b')
#    out = df.apply(del_short_string, axis=1).values.astype(str)

#    shortword = re.compile(r'\W*\b\w{1,2+}\b')
#    shortword.sub('', data[1])

    # Remove words that contain < chars
    for i in range(0,len(uidata)):
        # Get unqiue string
        getstr  = str(uidata[i]).split(sepchar)
        #length
        lenstr  = checkLen(getstr)
        keepidx = np.all([lenstr>=minchar,lenstr<=maxchar],axis=0)
        getstr  = np.array(getstr)[keepidx]
        # Store in data for all the same strings
        I = (data==uidata[i])
        data[I] = ' '.join(list(getstr))
    #end

    # Trim spaces
    data=np.char.strip(data)
    # Cleaning envoirement
    return(data)

#%% SMART pre-processing of strings
def stringPreprocessing(data, alias, sepchar=' '):
#    alias = [alias[i]]
#    sepchar=Param['sepchar']
    # Prepration
#    uidata   = np.char.strip(np.unique(data))
    df       = pd.DataFrame(data, columns=['data'])
#    ngrams=1
    #df.data  = df.data.str.split(pat=sepchar, expand=False)

    # Run across all ALIAS words to check whether there is a space or other split-up
    for i in range(0,len(alias)):
        #alias[i] = np.char.strip(alias[i])
        idxChar1 = strtricks.find(alias[i], ' ')
        idxChar2 = strtricks.find(alias[i], '-')
        idxChar  = np.unique(np.concatenate((idxChar1,idxChar2))).astype(int)

        # If there are any spaces or '-'
        if len(idxChar)>0:
            for k in range(0,len(idxChar)):
                # Make different char-variants that most likely mean the same
                charfront = alias[i][idxChar[k]-2]+alias[i][idxChar[k]-1]
                charback  = alias[i][idxChar[k]+1]
                if idxChar[k]+2 < len(alias[i]):  
                    charback = charback + alias[i][idxChar[k]+2]
                #end

                # Make different variants of seperator for input-names
                strvariant1 = charfront + ' ' + charback
                strvariant2 = charfront + '-' + charback
                strvariant3 = charfront + ''  + charback
                strvariant4 = charfront + '_' + charback
                
                # Get seperation char + and - 1 char
                oldchar = charfront+alias[i][idxChar[k]]+charback
                newchar = charfront+'-'+charback
                
                # String replace
#                df.data.replace(to_replace={strvariant1, strvariant2, strvariant3, strvariant4}, value=newchar, regex=True)               
#                string = re.sub(r'strvariant1, newchar, list(data))

                # Replace input-names
                df.data = df.data.str.replace(strvariant1,newchar)
                df.data = df.data.str.replace(strvariant2,newchar)
                df.data = df.data.str.replace(strvariant3,newchar)
                df.data = df.data.str.replace(strvariant4,newchar)

                # Replace ALIAS
                alias = np.char.replace(alias,oldchar,newchar)
            #end
        #end

        # If it contains one word without any seperation of space of '-'
        # Check the otherway arround, start looking in data for strings with at most 1 split.
        # Only check for those that contain at most 1 split = 2 seperate words
        if len(alias[i])<=4:
            # Do not make ngrams larger then 3 if alias only contains 3 chars, otherwise 4 char words can not be catched
            aliasGrams = ngrams(alias[i],3)
        else:
            aliasGrams = ngrams(alias[i],4)
        #end            

        for k in range(0,len(aliasGrams)):
            splitchar1 = aliasGrams[k][0] + ' ' + aliasGrams[k][1:]
            splitchar2 = aliasGrams[k][0] + '-' + aliasGrams[k][1:]
            splitchar3 = aliasGrams[k][0] + '_' + aliasGrams[k][1:]
            
#            df.data.replace(to_replace={splitchar1, splitchar2, splitchar3}, value=aliasGrams[k], regex=True)

            df.data = df.data.str.replace(splitchar1,aliasGrams[k])
            df.data = df.data.str.replace(splitchar2,aliasGrams[k])
            df.data = df.data.str.replace(splitchar3,aliasGrams[k])
        #end

        # Replace in front
        splitchar1 = '-'+alias[i][:3]
        splitchar2 = '_'+alias[i][:3]
        newchar    = ' '+alias[i][:3]
        df.data    = df.data.str.replace(splitchar1,newchar)
        df.data    = df.data.str.replace(splitchar2,newchar)
#        df.data.replace(to_replace={splitchar1, splitchar2}, value=newchar, regex=True)
        
        # Replace in back
        splitchar1 = alias[i][-3:]+'-'
        splitchar2 = alias[i][-3:]+'_'
        newchar    = alias[i][-3:]+' '
        df.data    = df.data.str.replace(splitchar1,newchar)
        df.data    = df.data.str.replace(splitchar2,newchar)
#        df.data.replace(to_replace={splitchar1, splitchar2}, value=newchar, regex=True)
        
#        data = np.char.replace(data,'-'+alias[i][:3],' '+alias[i][:3])
#        data = np.char.replace(data,'_'+alias[i][:3],' '+alias[i][:3])
    #end
    
    # Make words consistent to remove the '-' so that it also will match words without a '-'
    df.data = df.data.str.replace('-','')
    df.data = df.data.str.replace('_','')

    # Remove all - and _ from alias
    alias = np.char.replace(alias,'-','')
    alias = np.char.replace(alias,'_','')

    data = df.data.values.astype(str)
    return(data, alias)

#%% Cleaning strings
def stringClean(data):
    # Make consistent
    data=np.char.replace(data,' & ','&')
    data=np.char.replace(data,' &','&')
    data=np.char.replace(data,'& ','&')
    # Replace by space
    data=np.char.replace(data,'/',' ')
    data=np.char.replace(data,',',' ')
    data=np.char.replace(data,';',' ')
    data=np.char.replace(data,'*',' ')
    data=np.char.replace(data,'"',' ')
    data=np.char.replace(data,'#',' ')
    data=np.char.replace(data,'.',' ') # websites
    data=np.char.replace(data,"+",' ')
    data=np.char.replace(data,"<",' ')
    data=np.char.replace(data,">",' ')
    # Remove
    data=np.char.replace(data,'!','')
    data=np.char.replace(data,'$','')
    data=np.char.replace(data,"'",'')
    data=np.char.replace(data,"(",'')
    data=np.char.replace(data,")",'')
    data=np.char.replace(data,"{",'')
    data=np.char.replace(data,"}",'')
    data=np.char.replace(data,"[",'')
    data=np.char.replace(data,"]",'')
    data=np.char.replace(data,"?",'')
    data=np.char.replace(data,"@",'')
    data=np.char.replace(data,":",'')
    # Trim
    data   = np.char.lower(data)
    data   = np.char.strip(data)
    return(data)

#%% Cleaning strings
def delnumstring(data):
    data = pd.DataFrame(data=data,columns=['data'])
    data.data = data.data.str.replace('\d+','')
    #delnumstring = np.vectorize(del_num_in_string)
    #data = delnumstring(data)
    return data.data.values.astype(str)

#%% DELETE SHORT WORDS IN STRING
def del_short_string(x):
#    shortword = re.compile(r"\W*\b\w{1," + str(minchar) + "}\b")
    shortword = re.compile(r'\W*\b\w{1,3+}\b')
    return shortword.sub('', x["data"])
    
#%% DELETE NUMBERS IN STRING
def del_num_in_string(x):
    return ''.join(filter(lambda x: not x.isdigit(), x))

#%% NGRAMS
def ngrams(data, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', data)
    ngrams = zip(*[string[k:] for k in range(n)])
    return [''.join(ngram) for ngram in ngrams]
