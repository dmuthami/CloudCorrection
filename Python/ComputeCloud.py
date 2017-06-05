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


def computeCloud():
    try:
        _path = "/home/geonode/Documents/Landsat/LC08_L1TP_166063_20170112_20170311_01_T1/Reflectance"

        #Band2
        dsB2 = gdal.Open(os.path.join(_path, "Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B2.TIF"))
        band2 = dsB2.GetRasterBand(1)
        npB2 = np.array(band2.ReadAsArray())
        
        #Band3
        dsB3 = gdal.Open(os.path.join(_path, "Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B3.TIF"))
        band3 = dsB3.GetRasterBand(1)
        npB3 = np.array(band3.ReadAsArray())
        dsB3 = None
        
        #Band4
        dsB4 = gdal.Open(os.path.join(_path, "Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B4.TIF"))
        band4 = dsB4.GetRasterBand(1)
        npB4 = np.array(band4.ReadAsArray())
        dsB4= None

        #Band5
        dsB5 = gdal.Open(os.path.join(_path, "Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B5.TIF"))
        band5 = dsB5.GetRasterBand(1)
        npB5 = np.array(band5.ReadAsArray())
        dsB5 = None

        #Band6
        dsB6 = gdal.Open(os.path.join(_path, "Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B6.TIF"))
        band6 = dsB6.GetRasterBand(1)
        npB6 = np.array(band6.ReadAsArray())
        dsB6 = None

        #Band7
        dsB7 = gdal.Open(os.path.join(_path, "Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B7.TIF"))
        band7 = dsB7.GetRasterBand(1)
        npB7 = np.array(band7.ReadAsArray())
        dsB7 = None
        
        
        npTRRI =  (npB2 + 2*(npB3+npB4+npB5+npB6)+npB7)/2
        npB3=npB4=npB5=npB6=npB7=None

        #Save TRRI Image
        rows = npB2.shape[0] #Original rows
        cols = npB2.shape[1] #Original cols
        trans = dsB2.GetGeoTransform() #Get transformation information from the original file
        proj = dsB2.GetProjection() #Get Projection Information
        nodatav = band2.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, "TRRI_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npTRRI,outputRasterFile)

    
        npTRRI[npTRRI<1.3]=0.  #Repalce all values < 1.0 with 0.0
        npTRRI[npTRRI>=1.3]=1.  #Repalce all values >= 1.0 with 1.0
               
        #Convert to unsigned 8 bit
        npCloud =  npTRRI.astype(int)

        #Save cloud image
        outputRasterFile = os.path.join(_path, "Cloud_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        WriteRaster.writeTIFF2(rows,cols,trans,proj,nodatav,npCloud,outputRasterFile)
      
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function def load_image( infilename ) \n" + tbinfo + "\nError Info:\n    " + \
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
