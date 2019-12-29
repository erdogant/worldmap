""" This function extracts the content of a zipfile into a tmp directory

	A= zip_extract(path_of_file, <optional>)

 INPUT:
   path_of_file:  String, e.g., 
                  './my_directory/deeper/myfile.zip'

 OPTIONAL

   verbose:        Boolean [True,False]
                   False: No (default)
                   True: Yes

 OUTPUT
	output

 DESCRIPTION
   Extracts the content of a zipfile into a tmp directory

 EXAMPLE
   from etlearn.helpers.zip_extract import zip_extract

   A = extract('./mydir/files.zip')

 SEE ALSO

"""

#--------------------------------------------------------------------------
# Name        : zip.py
# Version     : 1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Aug. 2018
#--------------------------------------------------------------------------

#from matplotlib.pyplot import plot
import os
import zipfile

#%%
def zip_extract(path_of_file, unpack=True, verbose=3):
	# DECLARATIONS
    out = dict()
    config = dict()
    config['verbose'] = verbose
    config['unpack'] = unpack

    # Setting up tempdirectory to unzip files
    [pathname, filenameRAW]=os.path.split(path_of_file)
    filename = filenameRAW[0:filenameRAW.find('.')]
    # pathname = pathname+'/tmp/'

    # Make tempdirectory
    if not os.path.isdir(pathname):
        os.mkdir(pathname)
        if config['verbose']>=3: print('[EXTRACT FILES] Directory is created: %s' %pathname)
    else:
        if config['verbose']>=3: print('[EXTRACT FILES] Directory already exists and will be used: %s' %pathname)
    
    # Extracting files
    if config['unpack']:
        if config['verbose']>=3: print('[EXTRACT FILES] Extracting %s..' %(filenameRAW))
        zip_ref = zipfile.ZipFile(path_of_file, 'r')
        zip_ref.extractall(pathname)
        zip_ref.close()
        
    # Return info
    out['dir']=pathname
    out['file']=filenameRAW
    out['file_clean']=filename
    out['path']=path_of_file
    
    if config['verbose']>=3: print('[EXTRACT FILES] Done!')
    return(out)
