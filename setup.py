import setuptools
import re

# versioning ------------
VERSIONFILE="worldmap/__init__.py"
getversion = re.search( r"^__version__ = ['\"]([^'\"]*)['\"]", open(VERSIONFILE, "rt").read(), re.M)
if getversion:
    new_version = getversion.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Setup ------------
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     install_requires=['wget','matplotlib','numpy','pandas','svgpathtools','colourmap','tqdm','fuzzywuzzy[speedup]','sklearn','seaborn'],
     python_requires='>=3',
     name='worldmap',
     version=new_version,
     author="Erdogan Taskesen",
     author_email="erdogant@gmail.com",
     description="worldmap is to plot and color countries or specific regions in a country using offline approaches.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/erdogant/worldmap",
	 download_url = 'https://github.com/erdogant/worldmap/archive/'+new_version+'.tar.gz',
     packages=setuptools.find_packages(), # Searches throughout all dirs for files to include
     include_package_data=True, # Must be true to include files depicted in MANIFEST.in
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
