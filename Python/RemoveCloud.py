#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maithya
#
# Created:     29/04/2017
# Copyright:   (c) Maithya 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys
import logging
import traceback
import numpy as np
from osgeo import gdal
import math
from gdalconst import *
from datetime import datetime

##Custom module containing functions
import Configurations
import Utilities
import WriteRaster

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

#Call function to set parameters for radiance
Configurations.setRadiance()

#Call function to set parameters for reflectance
Configurations.setReflectance()

#Call function to set parameters for TRRI
Configurations.setTRRI()

#Set Remove workspace and other parameters
Configurations.setRemoveCloud()

#Path
_path=""
if len(sys.argv)>2:
    _path=sys.argv[2]##Get from console or GUI being user input
else :
    #Read from config file
    _path=Configurations.Configurations_workspace

#TRRI Folder
_TRRIFolder=""
if len(sys.argv)>3:
    _TRRIFolder=sys.argv[3]##Get from console or GUI being user input
else :
    #Read from config file
    _TRRIFolder=Configurations.Configurations_trrifolder

#Filename to band1
_band1Filename=""
if len(sys.argv)>4:
    _band1Filename=sys.argv[4]##Get from console or GUI being user input
else :
    #Read from config file
    _band1Filename=Configurations.Configurations_fileNameB1
    
#Cloud Image
_cloudImage=""
if len(sys.argv)>5:
    _cloudImage=sys.argv[5]##Get from console or GUI being user input
else :
    #Read from config file
    _cloudImage=Configurations.Configurations_cloudImage

#CloudFree Image
_CloudFreeImage=""
if len(sys.argv)>6:
    _CloudFreeImage=sys.argv[6]##Get from console or GUI being user input
else :
    #Read from config file
    _CloudFreeImage=Configurations.Configurations_CloudFree_Image


#max search distance
_maxSearchDist=""
if len(sys.argv)>7:
    _maxSearchDist=sys.argv[7]##Get from console or GUI being user input
else :
    #Read from config file
    _maxSearchDist=Configurations.Configurations_maxSearchDistance

#no data value
_nodatavalue=""
if len(sys.argv)>8:
    _nodatavalue=sys.argv[8]##Get from console or GUI being user input
else :
    #Read from config file
    _nodatavalue=Configurations.Configurations_nodatavalue

#Radar Image
radar_Image=""
if len(sys.argv)>9:
    radar_Image=sys.argv[9]##Get from console or GUI being user input
else :
    #Read from config file
    radar_Image=Configurations.Configurations_radar_Image

def getImage(infilename,readOnly):
    try:
        if (readOnly==True):
            ds = gdal.Open(infilename,GA_ReadOnly)
        else:
            ds = gdal.Open(infilename,GA_Update) 
            
               
        return ds #Return dataset
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function def load_image( infilename ) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info(pymsg)    
        return ""
    
def removeCloud():
    try:
        global _TRRIImage, _CloudImage, _CloudFreeImage, _maxSearchDist, _nodatavalue
        global _path, _band1Filename, _TRRIFolder

        #Get band number
        lst =_band1Filename.split("-")#Split by hyphen*
        TRRIFilename = lst[1]+"-"+lst[2]#get last components. looks like "ALAV2A191273610-O1B2R_U.tif"

        
        #radarPath = os.path.join(_path, "Radar.TIF")
        cloudPath = outputRasterFile = os.path.join(_path, _TRRIFolder, _cloudImage+"_"+TRRIFilename)
        opticalPath = os.path.join(_path, _TRRIFolder, _TRRIFolder+"_"+TRRIFilename)

        #radarImage = getImage(radarPath,True)
        cloudImage = getImage(cloudPath, True)
        opticalImage = getImage(opticalPath,True)

        #Get No datavalue for the optical image
        band = opticalImage.GetRasterBand(1)
        opticalArr = np.array(band.ReadAsArray())        
        rows = opticalArr.shape[0] #Original rows       
        cols = opticalArr.shape[1] #Original cols        
        trans = opticalImage.GetGeoTransform() #Get transformation information from the original file       
        proj = opticalImage.GetProjection() #Get Projection Information
        nodatav = band.GetNoDataValue() # Get No Data Value
        if(nodatav==None):
            nodatav = float(_nodatavalue)        

        #Multiply cloud pixel (cloudArr) with no data value -999= cloudArr2
        cloudBand = cloudImage.GetRasterBand(1)
        cloudArr = np.array(cloudBand.ReadAsArray())    
        cloudArr2 = cloudArr*int(float(_nodatavalue))

        #Add cloudArr2 to the opticalArr to give opticalArr2
        opticalArr2 = cloudArr2 + opticalArr
        opticalArr2[opticalArr2<-900]=float(_nodatavalue)  #Replace all values < -900 with -999

        ##Convert Array to raster (keep the origin and cellsize the same as the input)
        ##Remeber NoDatavalue = -999 or -999.0
        outputRasterFile = os.path.join(_path, _TRRIFolder, _TRRIFolder+"2_"+TRRIFilename)#output file
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,opticalArr2,outputRasterFile)

        ##Create a copy of opticalArr2 
        outputRasterFile = os.path.join(_path, _TRRIFolder,_CloudFreeImage+"_"+TRRIFilename)
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,opticalArr2,outputRasterFile)

        #Read the image again
        #Execute fillnodata
        opticalPath2 = os.path.join(_path, _TRRIFolder,_CloudFreeImage+"_"+TRRIFilename)
        opticalImage2 = getImage(opticalPath2,False)
        channelband = opticalImage2.GetRasterBand(1)        
        result = gdal.FillNodata(targetBand = channelband, maskBand = None, \
                                 maxSearchDist = int(_maxSearchDist), smoothingIterations =0)

        result = None #Flush out the results to disk
        
        radarImage = None
        cloudImage = None
        opticalImage = None
        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function def removeCloud() \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info(pymsg)
    return ""

def main():
    pass

if __name__ == '__main__':
    main()
    #Call function
    removeCloud()
