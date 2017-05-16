#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maithya
#
# Created:     27/04/2017
# Copyright:   (c) Maithya 2017
# Licence:     Free
#-------------------------------------------------------------------------------
import arcpy
import os

def getAllFolders(_directory):
    for dirName, subdirList, fileList in os.walk(_directory):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\t%s' % fname)
    return ""

def getAllRasters(imagesfolder,excludeFolder):
    rasters = []
    for dirpath, dirnames, filenames in arcpy.da.Walk(
        imagesfolder, topdown=True, datatype="RasterDataset"):
        # Disregard any folder named 'Output' in creating list
        #  of rasters
        if excludeFolder in dirnames:
            dirnames.remove(excludeFolder)
        for filename in filenames:
            rasters.append(os.path.join(dirpath, filename))

    return rasters

def main():
    pass

if __name__ == '__main__':
    main()
    #Call entry function