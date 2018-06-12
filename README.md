# PPDir.py

### Post-Processing Directory - An Extension Script for NZBGet

Allows to set a dedicated post-processing directory.

Instead of post-processing the files directly into the final destination directory and extracting the files into an "_unpack" directory within this final destination directory, the whole NZBGet post-processing step will take place within a (temporary) directory in the defined post-processing directory. The files are then moved by this extension script to the final destination directory only after NZBGet has finished the post-processing (e.g. unpack and cleanup).

This prevents issues with partially unpacked files already beeing processed by subsequent scripts/programs watching the final destination directory.

__NOTE:__ If you have other post-processing scripts running, this extension script should be the first post-processing script to run in order to make sure your post-processing scripts will find the files in the final destination directory.

__NOTE:__ This script requires Python to be installed on the system running NZBGet.

See the [NZBGet documentation](https://nzbget.net/extension-scripts) for information on how to install extension scripts for NZBGet.