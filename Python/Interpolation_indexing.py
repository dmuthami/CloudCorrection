#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maithya
#
# Created:     16/05/2017
# Copyright:   (c) Maithya 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os,sys
import logging
import traceback
import numpy as np
from osgeo import gdal
from gdalconst import *
from datetime import datetime



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

#Set workspace and other parameters
Configurations.setWorkspace()

#Set Compute cloud Parameters
Configurations.setComputeCloud()

#Set Remove workspace and other parameters
Configurations.setRemoveCloud()


#Path
_path=""
if len(sys.argv)>2:
    _path=sys.argv[2]##Get from console or GUI being user input
else :
    #Read from config file
    _path=Configurations.Configurations_path

#TRRI Image
_TRRIImage=""
if len(sys.argv)>3:
    _TRRIImage=sys.argv[3]##Get from console or GUI being user input
else :
    #Read from config file
    _TRRIImage=Configurations.Configurations_TRRI_Image

#Cloud Image
_CloudImage=""
if len(sys.argv)>4:
    _CloudImage=sys.argv[4]##Get from console or GUI being user input
else :
    #Read from config file
    _CloudImage=Configurations.Configurations_Cloud_Image

#TRRI2 Image
_TRRI2Image=""
if len(sys.argv)>5:
    _TRRI2Image=sys.argv[5]##Get from console or GUI being user input
else :
    #Read from config file
    _TRRI2Image=Configurations.Configurations_TRRI2_Image

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

#max search distance
_nodatavalue=""
if len(sys.argv)>8:
    _nodatavalue=sys.argv[8]##Get from console or GUI being user input
else :
    #Read from config file
    _nodatavalue=Configurations.Configurations_nodatavalue
    
    
##Gather information from the original file
##Store it in this global variables      
_cols = 0
_rows = 0
_proj = ""
_trans = ""
_nodatav = ""

#To disable this behaviour and force NumPy to print the entire array, 
#you can change the printing options using set_printoptions.
#np.set_printoptions(threshold='nan')

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
    
def interpolate():
    try:
        global _TRRIImage,_CloudImage,_TRRI2Image,_CloudFreeImage,_maxSearchDist,_nodatavalue
        
        
        #radarPath = os.path.join(_path, "Radar.TIF")
        cloudPath = os.path.join(_path, _CloudImage)
        opticalPath = os.path.join(_path, _TRRIImage)

        #radarImage = getImage(radarPath,True)
        cloudImage = getImage(cloudPath, True)
        opticalImage = getImage(opticalPath,True)

        

        #Get No datavalue for the optical image
        band = opticalImage.GetRasterBand(1)
        opticalArr = np.array(band.ReadAsArray())
        global _rows
        _rows = opticalArr.shape[0] #Original rows
        global _cols
        _cols = opticalArr.shape[1] #Original cols
        global _trans
        _trans = opticalImage.GetGeoTransform() #Get transformation information from the original file
        global _proj
        _proj = opticalImage.GetProjection() #Get Projection Information
                
        global _nodatav
        _nodatav = band.GetNoDataValue() # Get No Data Value
        if(_nodatav==None):
            _nodatav = float(_nodatavalue)

        #Multiply cloud pixel (cloudArr) with no data value -999= cloudArr2
        cloudBand = cloudImage.GetRasterBand(1)
        cloudArr = np.array(cloudBand.ReadAsArray())    
        cloudArr2 = cloudArr*int(float(_nodatavalue))

        #Add cloudArr2 to the opticalArr to give opticalArr2
        opticalArr2 = cloudArr2 + opticalArr
        opticalArr2[opticalArr2<-900]=float(_nodatavalue)  #Replace all values < -900 with -999
        
        ##Convert Array to raster (keep the origin and cellsize the same as the input)
        ##Remeber NoDatavalue = -999 or -999.0
        outputRasterFile = os.path.join(_path, _TRRI2Image)
        WriteRaster.writeTIFF(_rows,_cols,_trans,_proj,_nodatav,opticalArr2,outputRasterFile)

        ##Create a copy of opticalArr2 
        outputRasterFile = os.path.join(_path, _CloudFreeImage)
        WriteRaster.writeTIFF(_rows,_cols,_trans,_proj,_nodatav,opticalArr2,outputRasterFile)
        
        #Read the image again
        #Execute fillnodata
        opticalPath2 = os.path.join(_path, _CloudFreeImage)
        opticalImage2 = getImage(opticalPath,False)
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
        pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)

    return ""

def main():
    pass

if __name__ == '__main__':
    main()

    ##Call true function
    interpolate()
