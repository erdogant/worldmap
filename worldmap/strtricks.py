"""
This module contains a set of functions related to strings
>
> strcat        : String concatenation for a 1xN list
> strcat_array  : String concatenation for a MxN array
> strrep        : String replacement for array
> repmat        : Repeat char NxM times
> find          : Find the location of a input character in a string


 EXAMPLE
   
--------------------------------------------------------------------------
 Name        : strtricks.py
 Author      : E.Taskesen
 Contact     : erdogant@gmal.com
 Date        : Sep. 2017
--------------------------------------------------------------------------
"""

#%% Libraries
import pandas as pd
import numpy as np
import re

#%% Concatenates list
# INPUT: List of strings or char: string=["aap","boom","mies"] or string="aap"
def strcat(string,delim=" "):
    out = ''
    if (type(string)==list):
        out=delim.join(list(string))
    else:
        out = string+delim
    #end

    # Remove last delim char
    #out=out[0:len(out)-len(delim)]
    # Return
    return out

#%% Concatenates pandas array
def strcat_array(data,delim=","):
    out=data.astype(str).apply(lambda x: delim.join(x), axis=1)
    # Remove first delim
#    out=out[1:len(out)]
    return out

#%% Changes char over list
def strrep(out,strFrom, strTo):
    for i in range(0,len(out)):
        out[i]=out[i].replace(strFrom,strTo)
    # return
    return out

#%% Replaces [char] or [string] to [NaN] in full pandas dataframe
def strrep_to_nan(out,strFrom):
    out = out.apply(lambda x: x.str.strip()).replace(strFrom, np.nan)
    # return
    return out

#%% Repeat str for #rows and #cols
def repmat(getstr, rows, cols):
    # INPUT:  repmat("?", 10, 5):
    # OUTPUT: Pandas dataframe
    # Convert to list: out = out.values.tolist()[0]
    #
    # Multiplyl str
    out = [getstr] * rows
    # Multiple rows
    out = [out] * cols
    # Convert to pandas dataframe
    out = pd.DataFrame(out)
    # return
    return out

#%% Find char in string and return indexes
def find(getstr, ch):
     return [i for i, ltr in enumerate(getstr) if ltr == ch]

#%%