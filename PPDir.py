#!/usr/bin/python3
##############################################################################
### NZBGET QUEUE/POST-PROCESSING SCRIPT                                    ###
### QUEUE EVENTS: NZB_DOWNLOADED                                           ###

# Post-Processing Directory
#
#
# Allows to set a dedicated post-processing directory.
#
# Instead of post-processing the files directly into the final destination
# directory and extracting the files into an "_unpack" directory within this
# final destination directory, the whole NZBGet post-processing step will
# take place within a (temporary) directory in the defined post-processing
# directory. The files are then moved by this extension script to the final
# destination directory only after NZBGet has finished the post-processing
# (e.g. unpack and cleanup).
#  
# This prevents issues with partially unpacked files already beeing processed
# by subsequent scripts/programs watching the final destination directory.
# For best performance, the post-processing directory should be on the same
# share or drive like the final destination directory.
#  
# NOTE: If you have other post-processing scripts running, this extension script
# should be the first post-processing script to run in order to make sure
# your post-processing scripts will find the files in the final destination
# directory.
#  
# NOTE: This script requires Python to be installed on your system.

##############################################################################
### OPTIONS                                                                ###

# Post-Processing Directory
#
#
# Please use absolute paths. On POSIX you can use "~" as alias for the home directory.
# You can also use ${mainDir} with a relative path (e.g. "${mainDir}/temp")
#PPDir=${mainDir}/temp

### NZBGET QUEUE/POST-PROCESSING SCRIPT                                    ###
##############################################################################

import sys
import os
import re
import shutil
import unicodedata

# errorHandler function
def errorHandler(m, e):
    print('[ERROR] %s. Error: %s'%(m, e))
    sys.exit(94)

# moverecursively function
def moverecursively(source_folder, destination_folder):
    basename = os.path.basename(source_folder)
    dest_dir = os.path.join(destination_folder, basename)
    if not os.path.exists(dest_dir):
        print('[INFO] Moving directory "%s" to "%s"'%(basename, destination_folder))
        try:
            shutil.move(source_folder, destination_folder)
        except Exception as e:
            errorHandler('Cannot move directory', str(e))
    else:
        dst_path = os.path.join(destination_folder, basename)
        for root, dirs, files in os.walk(source_folder):
            for item in files:
                src_file = os.path.join(root, item)
                dst_file = os.path.join(dst_path, item)
                print('[INFO] Moving file "%s" to "%s"'%(item, dst_path))
                if os.path.exists(dst_file):
                    try:
                        os.remove(dst_file)
                    except Exception as e:
                        errorHandler('Cannot move file. Destination file already exists and cannot be overwritten', str(e))
                    try:
                        shutil.move(src_file, dst_file)
                    except Exception as e:
                        errorHandler('Cannot move file', str(e))
                else:
                    try:
                        shutil.move(src_file, dst_path)
                    except Exception as e:
                        errorHandler('Cannot move file', str(e))
            for item in dirs:
                src_path = os.path.join(root, item)
                moverecursively(src_path, dst_path)
            # the current source directory should be empty now, so check and delete it
            if not os.listdir(root):
                try:
                    os.rmdir(root)
                except:
                    print('[WARNING] Cannot delete empty directory "' + root + '"')
    return dest_dir

# first check whether PPDir is set
if (not 'NZBPO_PPDIR' in os.environ):
    print('[ERROR] Option "PPDir" is missing in the NZBGet configuration file. Please check the script settings and save them!')
    sys.exit(94)

# if the script was called by the queue event set the destination directory to the post-processing directory
if os.environ.get('NZBNA_EVENT'):
    ppdir = os.environ.get('NZBPO_PPDIR')
    # remove trailing slashes
    ppdir = re.sub(r'[\/\\]*$', '', ppdir)
    # get the destination directory name from the NZB name and do some sanitisation
    nzbname = os.environ.get('NZBNA_NZBNAME')
    subfolder = unicodedata.normalize('NFKD', nzbname)
    subfolder = re.sub(r'(?u)[^\w\.\ \(\)\[\]\{\}\&\+\-]', '', subfolder)
    # add it to the final destination directory
    ppdir = ppdir + '/' + subfolder
    print('[INFO] Setting post-processing directory to: ' + ppdir)
    print('[NZB] DIRECTORY=' + ppdir)   

# if the script was called for post-processing the files have to be moved from the post-processing directory to the final destination directory
else:
    # first check if the source path exists
    if os.path.exists(os.environ.get('NZBPP_DIRECTORY')):
        destination = ''
        # first check if a category is set and the user has set a destination directory for this category
        n = 1
        while True:
            if os.environ.get('NZBOP_CATEGORY' + str(n) + '_NAME'):
                if os.environ.get('NZBOP_CATEGORY' + str(n) + '_NAME') == os.environ.get('NZBPP_CATEGORY'):
                    destination = os.environ.get('NZBOP_CATEGORY' + str(n) + '_DESTDIR')
                    break
                n = n + 1
            else:
                break
        # if not, set the default destination directory
        if not destination:
            destination = os.environ.get('NZBOP_DESTDIR')
            # if the user has activated the AppendCategoryDir option and a category is set, append the category name as subfolder
            if os.environ.get('NZBOP_APPENDCATEGORYDIR') and os.environ.get('NZBPP_CATEGORY'):
                destination = re.sub(r'[\/\\]*$', '', destination)
                destination = destination + '/' + os.environ.get('NZBPP_CATEGORY')
        # check if a destination is set and move the files
        if destination:
            destination = moverecursively(os.environ.get('NZBPP_DIRECTORY'), destination)
            print('[INFO] All files successfully moved to: ' + destination)
            # set DIRECTORY and FINALDIR to the new final destination directory
            print('[NZB] DIRECTORY=' + destination)
            print('[NZB] FINALDIR=' + destination)
            sys.exit(93)
        else:
            print('[ERROR] Unable to set a final destination directory. Please check your settings!')
            sys.exit(94)
    else:
        print('[INFO] Nothing to move. The download has probably failed or been deleted.')
        sys.exit(93)        