#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maithya
#
# Created:     27/04/2017
# Copyright:   (c) Maithya 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys
import logging
import traceback
import numpy as np
from osgeo import gdal

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

def getGainAndOffset(baseName,directoryName,textSuffix):
    try:
        ##List as follows
        ## basename
        ## directoryName
        ## fileExtension
        ## bandNumber
        ## textfile for metadata
        ## gain
        ## offset
        paramList=[]

        ##Raster File Name : LC08_L1TP_166063_20170418_20170418_01_RT_B8.TIF | Directory : E:\GIS Data\DAVVOC\Maithya\Images\LC08_L1TP_166063_20170418_20170418_01_RT

        #Get band number
        band =baseName.split("_")#Split by underscore*
        s = band[int(len(band) -1)]#get last component. looks like "B8.TIF"
        band =s.split(".")#Split by period*
        s = band[0]#Get first element in the list . looks like "B8"
        bandNumber = s[1:] #get the band number

        #Construct textfile name
        directorypath = directoryName.split(os.path.sep) #Split using OS separator
        commonFileName = directorypath[int(len(directorypath) -1)]#get common file name
        textfile =commonFileName + textSuffix

        filepath = os.path.join(directoryName, textfile)
        gainAndOffset = readGainAndOffsetFromMetadataFile(filepath,bandNumber)
        if  gainAndOffset != []:
                paramList.append(baseName)
                paramList.append(directoryName)
                paramList.append("TIF")
                paramList.append(bandNumber)
                paramList.append(textfile)
                paramList.append(gainAndOffset[0])
                paramList.append(gainAndOffset[1])
                
        #
        return paramList        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function getGainAndOffset(baseName,directoryName,textSuffix) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
        return []
        

def readGainAndOffsetFromMetadataFile(filepath,bandNumber):
    try:
        gainAndOffset=[]
        s = ""
        paramOfInterest = ""
        multiBand = ""
        addBand = ""

        with open(filepath) as f:
            for line in f:
                s =line.rstrip().lstrip()
                param = s.split("=")

                paramOfInterest =str(param[0]).rstrip().lstrip()
                multiBand = "REFLECTANCE_MULT_BAND_"+ bandNumber
                addBand = "REFLECTANCE_ADD_BAND_"+ bandNumber

                if paramOfInterest== multiBand:
                    gainAndOffset.append(param[1])
                if paramOfInterest== addBand:
                    gainAndOffset.append(param[1])
                #print(s)

        return gainAndOffset        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function readGainAndOffsetFromMetadataFile(filepath,bandNumber) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
        return []
        
def checkIfDirectoryExists(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function checkIfDirectoryExists(dir)\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
    return ""

def main():
    pass

if __name__ == '__main__':
    main()
