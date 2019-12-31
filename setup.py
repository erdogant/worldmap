import setuptools
import versioneer
new_version='0.1.2'

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     install_requires=['numpy','pandas','tqdm','seaborn','sklearn','svgpathtools'],
     python_requires='>=3',
     name='worldmap',
     version=new_version,
#     version=versioneer.get_version(),    # VERSION CONTROL
#     cmdclass=versioneer.get_cmdclass(),  # VERSION CONTROL
     author="Erdogan Taskesen",
     author_email="erdogant@gmail.com",
     description="Color the worldmap",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/erdogant/worldmap",
	 download_url = 'https://github.com/erdogant/worldmap/archive/'+new_version+'.tar.gz',
     packages=setuptools.find_packages(), # Searches throughout all dirs for files to include
     include_package_data=True, # Must be true to include files depicted in MANIFEST.in
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
     ],
 )
