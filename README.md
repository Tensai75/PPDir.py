# PPDir

### Post-Processing Directory - An Extension Script for NZBGet v24.0 or higher from NZBGet.com

Allows to set a dedicated post-processing directory.

Instead of post-processing the files directly into the final destination directory and extracting the files into an "_unpack" directory within this final destination directory, the whole NZBGet post-processing step will take place within a (temporary) directory in the defined post-processing directory. The files are then moved by this extension script to the final destination directory only after NZBGet has finished the post-processing (e.g. unpack and cleanup).

This prevents issues with partially unpacked files already beeing processed by subsequent scripts/programs watching the final destination directory.
For best performance, the post-processing directory should be on the same share or drive like the final destination directory.

__NOTE:__ If you have other post-processing scripts running, this extension script should be the first post-processing script to run in order to make sure your post-processing scripts will find the files in the final destination directory.

__NOTE:__ This script requires NZBGet v24.0 or higher and Python 3.x to be installed on the system running NZBGet.

See the [NZBGet documentation](https://nzbget.com/documentation/extension-scripts/) for information on how to install extension scripts for NZBGet.

#### Manual installation instructions (until the script is added to the official NZBGet Extension Manager)
1. create an empty folder named `PPDir` inside the NZBGet Scripts folder (ScriptDir)
2. clone this repository into this folder or manually place the `PPDir.py` and the `manifest.json` file into this folder
3. open the NZBGet settings page and click on the `EXTENSION MANAGER` menu item
4. activate the extension `Post-Processing Directory` by clicking on the green "Play" button (if you see an orange "Pause" button, the extension is already activated)
5. go to the options page of the extensions by clicking on the black "Settings" button or on the menu item `POST-PROCESSING DIRECTORY` below the menu item `EXTENSION MANAGER`
6. set the options of the extensions according to your wishes
7. do not forget to save the settings and to reload NZBGet!