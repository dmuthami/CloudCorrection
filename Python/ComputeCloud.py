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

##Custom module containing functions
import Configurations
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

#Set Compute cloud Parameters
Configurations.setComputeCloud()

#Path
_path=""
if len(sys.argv)>2:
    _path=sys.argv[2]##Get from console or GUI being user input
else :
    #Read from config file
    _path=Configurations.Configurations_path

#Filename to band2
_band2Filename=""
if len(sys.argv)>3:
    _band2Filename=sys.argv[3]##Get from console or GUI being user input
else :
    #Read from config file
    _band2Filename=Configurations.Configurations_band2

#Filename to band3
_band3Filename=""
if len(sys.argv)>4:
    _band3Filename=sys.argv[4]##Get from console or GUI being user input
else :
    #Read from config file
    _band3Filename=Configurations.Configurations_band3

#Filename to band4
_band4Filename=""
if len(sys.argv)>5:
    _band4Filename=sys.argv[5]##Get from console or GUI being user input
else :
    #Read from config file
    _band4Filename=Configurations.Configurations_band4

#Filename to band5
_band5Filename=""
if len(sys.argv)>6:
    _band5Filename=sys.argv[6]##Get from console or GUI being user input
else :
    #Read from config file
    _band5Filename=Configurations.Configurations_band5

#Filename to band6
_band6Filename=""
if len(sys.argv)>7:
    _band6Filename=sys.argv[7]##Get from console or GUI being user input
else :
    #Read from config file
    _band6Filename=Configurations.Configurations_band6

#Filename to band7
_band7Filename=""
if len(sys.argv)>8:
    _band6Filename=sys.argv[8]##Get from console or GUI being user input
else :
    #Read from config file
    _band7Filename=Configurations.Configurations_band7

#TRRI Image
_TRRIImage=""
if len(sys.argv)>9:
    _TRRIImage=sys.argv[9]##Get from console or GUI being user input
else :
    #Read from config file
    _TRRIImage=Configurations.Configurations_TRRI_Image

#Cloud Image
_CloudImage=""
if len(sys.argv)>10:
    _CloudImage=sys.argv[10]##Get from console or GUI being user input
else :
    #Read from config file
    _CloudImage=Configurations.Configurations_Cloud_Image

#Cloud Threshold Value
_cloudThresholdValue=""
if len(sys.argv)>11:
    _cloudThresholdValue=sys.argv[11]##Get from console or GUI being user input
else :
    #Read from config file
    _cloudThresholdValue=Configurations.Configurations_cloudThresholdValue
    


def computeCloud():
    try:
        global _path , _band2Filename, _band3Filename,_band4Filename,_band5Filename,_band2Filename,_band7Filename
        global _CloudImage, _cloudThresholdValue,_TRRIImage
        #Band2
        dsB2 = gdal.Open(os.path.join(_path, _band2Filename))
        band2 = dsB2.GetRasterBand(1)
        npB2 = np.array(band2.ReadAsArray())
        
        #Band3
        dsB3 = gdal.Open(os.path.join(_path, _band3Filename))
        band3 = dsB3.GetRasterBand(1)
        npB3 = np.array(band3.ReadAsArray())
        dsB3 = None
        
        #Band4
        dsB4 = gdal.Open(os.path.join(_path, _band4Filename))
        band4 = dsB4.GetRasterBand(1)
        npB4 = np.array(band4.ReadAsArray())
        dsB4= None

        #Band5
        dsB5 = gdal.Open(os.path.join(_path, _band5Filename))
        band5 = dsB5.GetRasterBand(1)
        npB5 = np.array(band5.ReadAsArray())
        dsB5 = None

        #Band6
        dsB6 = gdal.Open(os.path.join(_path, _band6Filename))
        band6 = dsB6.GetRasterBand(1)
        npB6 = np.array(band6.ReadAsArray())
        dsB6 = None

        #Band7
        dsB7 = gdal.Open(os.path.join(_path, _band7Filename))
        band7 = dsB7.GetRasterBand(1)
        npB7 = np.array(band7.ReadAsArray())
        dsB7 = None
        
        #Compute Cloud
        npTRRI =  (npB2 + 2*(npB3+npB4+npB5+npB6)+npB7)/2
        npB3=npB4=npB5=npB6=npB7=None #Garbage collection

        
        
        #Save TRRI Image
        rows = npB2.shape[0] #Original rows
        cols = npB2.shape[1] #Original cols
        trans = dsB2.GetGeoTransform() #Get transformation information from the original file
        proj = dsB2.GetProjection() #Get Projection Information
        nodatav = band2.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIImage)
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npTRRI,outputRasterFile)

    
        npTRRI[npTRRI<float(_cloudThresholdValue)]=0.  #E.g Replace all values < 1.3 with 0.0
        npTRRI[npTRRI>=float(_cloudThresholdValue)]=1.  #E.g Replace all values >= 1.3 with 1.0
               
        #Convert to unsigned 8 bit
        npCloud =  npTRRI.astype(int)

        #Save cloud image
        outputRasterFile = os.path.join(_path, _CloudImage)
        WriteRaster.writeTIFF2(rows,cols,trans,proj,nodatav,npCloud,outputRasterFile)
      
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function def computeCloud() \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info(pymsg)
    return ""

def main():
    pass

if __name__ == '__main__':
    main()
    #Call function
    computeCloud()
