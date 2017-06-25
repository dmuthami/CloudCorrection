# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GetImageFolders
# Purpose:
#
# Author:      Maithya
#
# Created:     27/04/2017
# Copyright:   (c) Maithya 2017
# Licence:     Free
#-------------------------------------------------------------------------------
import os, sys
import logging
import traceback
import numpy as np
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr
import matplotlib.pylab as plt

##Custom module containing functions
import Configurations

#Set-up logging
logger = logging.getLogger('myapp')
Configurations.Configurations_cloudCorrection_logfile = os.path.join(os.path.dirname(__file__), 'cloudCorrection_logfile.log')
hdlr = logging.FileHandler(Configurations.Configurations_cloudCorrection_logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

#Set-up Error Logging
logger_error = logging.getLogger('myError')
Configurations.Configurations_cloudCorrection_error_logfile = os.path.join(os.path.dirname(__file__), 'cloudCorrection_error_logfile.log')
hdlr_error = logging.FileHandler(Configurations.Configurations_cloudCorrection_error_logfile)
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr_error.setFormatter(formatter)
logger_error.addHandler(hdlr_error)
logger_error.setLevel(logging.INFO)

##Obtain script parameter values
##location for configuration file
##Acquire it as a parameter either from terminal, console or via application
if len(sys.argv)>1:
    configFileLocation=sys.argv[1]##Get from console or GUI being user input
else :
    #Read from config file
    configFileLocation=os.path.join(os.path.dirname(__file__), 'Config.ini')

##Read from config file
#If for any reason an exception is thrown here then subsequent code will not be executed
Configurations.setParameters(configFileLocation)

#Set workspace
Configurations.setWorkspace()


def writeTIFF(rows,cols,trans,proj,nodatav,npArray,outputRasterFile):
    try: 
        
        output_raster = gdal.GetDriverByName('GTiff').Create(outputRasterFile,cols, rows, 1
        ,gdal.GDT_Float32)  # Open the file

        output_raster.SetGeoTransform(trans)  # Specify its coordinates
        # Establish its coordinate encoding


        #Seta no data value
        if(nodatav!=None):
            output_raster.GetRasterBand(1).SetNoDataValue(nodatav)
            
        output_raster.SetProjection( proj )   # Exports the coordinate system
                                              # to the file

        output_raster.GetRasterBand(1).WriteArray(npArray)   # Writes my array to the raster

        output_raster = None
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function writeTIFF(rows,cols,trans,proj,nodatav,npArray,fileName,outputDirectory) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
        
    return ""

#Writes as int
def writeTIFF2(rows,cols,trans,proj,nodatav,npArray,outputRasterFile):
    try: 
        
        output_raster = gdal.GetDriverByName('GTiff').Create(outputRasterFile,cols, rows, 1
        ,gdal.GDT_Byte)  # Open the file

        output_raster.SetGeoTransform(trans)  # Specify its coordinates
        # Establish its coordinate encoding


        #Seta no data value
        if(nodatav!=None):
            output_raster.GetRasterBand(1).SetNoDataValue(nodatav)
            
        output_raster.SetProjection( proj )   # Exports the coordinate system
                                              # to the file

        output_raster.GetRasterBand(1).WriteArray(npArray)   # Writes my array to the raster

        output_raster = None
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function writeTIFF2(rows,cols,trans,proj,nodatav,npArray,fileName,outputDirectory) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
        
    return ""

def main():
    pass

if __name__ == '__main__':
    main()
    #Call function
