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

#Path
_path=""
if len(sys.argv)>2:
    _path=sys.argv[2]##Get from console or GUI being user input
else :
    #Read from config file
    _path=Configurations.Configurations_workspace

#Filename to band1
_band1Filename=""
if len(sys.argv)>3:
    _band1Filename=sys.argv[3]##Get from console or GUI being user input
else :
    #Read from config file
    _band1Filename=Configurations.Configurations_fileNameB1
    
#Filename to band2
_band2Filename=""
if len(sys.argv)>4:
    _band2Filename=sys.argv[4]##Get from console or GUI being user input
else :
    #Read from config file
    _band2Filename=Configurations.Configurations_fileNameB2

#Filename to band3
_band3Filename=""
if len(sys.argv)>5:
    _band3Filename=sys.argv[5]##Get from console or GUI being user input
else :
    #Read from config file
    _band3Filename=Configurations.Configurations_fileNameB3
    
#Filename to band4
_band4Filename=""
if len(sys.argv)>6:
    _band4Filename=sys.argv[6]##Get from console or GUI being user input
else :
    #Read from config file
    _band4Filename=Configurations.Configurations_fileNameB4

#d parameter
_d=""
if len(sys.argv)>7:
    _d=sys.argv[7]##Get from console or GUI being user input
else :
    #Read from config file
    _d=Configurations.Configurations_d

#_ESUN_B1 parameter
_ESUN_B1=""
if len(sys.argv)>8:
    _ESUN_B1=sys.argv[8]##Get from console or GUI being user input
else :
    #Read from config file
    _ESUN_B1=Configurations.Configurations_ESUN_B1

#_ESUN_B2 parameter
_ESUN_B2=""
if len(sys.argv)>9:
    _ESUN_B2=sys.argv[9]##Get from console or GUI being user input
else :
    #Read from config file
    _ESUN_B2=Configurations.Configurations_ESUN_B2

#_ESUN_B3 parameter
_ESUN_B3=""
if len(sys.argv)>10:
    _ESUN_B3=sys.argv[10]##Get from console or GUI being user input
else :
    #Read from config file
    _ESUN_B3=Configurations.Configurations_ESUN_B3

#_ESUN_B4 parameter
_ESUN_B4=""
if len(sys.argv)>11:
    _ESUN_B4=sys.argv[11]##Get from console or GUI being user input
else :
    #Read from config file
    _ESUN_B4=Configurations.Configurations_ESUN_B4

#_theta parameter
_theta=""
if len(sys.argv)>12:
    _theta=sys.argv[12]##Get from console or GUI being user input
else :
    #Read from config file
    _theta=Configurations.Configurations_theta
    
#Radiance Folder
_radiancefolder=""
if len(sys.argv)>13:
    _radiancefolder=sys.argv[13]##Get from console or GUI being user input
else :
    #Read from config file
    _radiancefolder=Configurations.Configurations_radiancefolder


#Reflectance Folder
_reflectancefolder=""
if len(sys.argv)>14:
    _reflectancefolder=sys.argv[14]##Get from console or GUI being user input
else :
    #Read from config file
    _reflectancefolder=Configurations.Configurations_reflectancefolder


def computeRadiance():
    try:
        global _path ,_band1Filename, _band2Filename, _band3Filename,_band4Filename
        global _d, _ESUN_B1,_ESUN_B2,_ESUN_B3,_ESUN_B4,_theta
        global _radiancefolder, _reflectancefolder
        
        #Band1
        dsB1 = gdal.Open(os.path.join(_path, _radiancefolder ,_radiancefolder+"_"+_band1Filename)) #Go the radiance folder
        band1 = dsB1.GetRasterBand(1)
        npB1 = np.array(band1.ReadAsArray())

        #Save Reflectance Image 1
        npB1Reflectance = npB1 * (math.pi *math.pow(float(_d),2))/float(_ESUN_B1)*math.sin(float(_theta)) #Compute reflectance image
        rows = npB1.shape[0] #Original rows
        cols = npB1.shape[1] #Original cols
        trans = dsB1.GetGeoTransform() #Get transformation information from the original file
        proj = dsB1.GetProjection() #Get Projection Information
        nodatav = band1.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _reflectancefolder, _reflectancefolder+"_"+_band1Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _reflectancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB1Reflectance,outputRasterFile) #Write file to disk
        dsB1 = band1 = npB1 = npB1Reflectance = None #Free memory
        
        #Band2
        dsB2 = gdal.Open(os.path.join(_path, _radiancefolder ,_radiancefolder+"_"+_band2Filename))
        band2 = dsB2.GetRasterBand(1)
        npB2 = np.array(band2.ReadAsArray())

        #Save Reflectance Image 2
        npB2Reflectance = npB2 * (math.pi *math.pow(float(_d),2))/float(_ESUN_B2)*math.sin(float(_theta)) #Compute reflectance image
        rows = npB2.shape[0] #Original rows
        cols = npB2.shape[1] #Original cols
        trans = dsB2.GetGeoTransform() #Get transformation information from the original file
        proj = dsB2.GetProjection() #Get Projection Information
        nodatav = band2.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _reflectancefolder, _reflectancefolder+"_"+_band2Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _reflectancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB2Reflectance,outputRasterFile) #Write file to disk
        dsB2 = band2 = npB2 = npB2Reflectance = None #Free memory
        
        #Band3
        dsB3 = gdal.Open(os.path.join(_path, _radiancefolder ,_radiancefolder+"_"+_band3Filename))
        band3 = dsB3.GetRasterBand(1)
        npB3 = np.array(band3.ReadAsArray())
        
        #Save Reflectance Image 3
        npB3Reflectance = npB3 * (math.pi *math.pow(float(_d),2))/float(_ESUN_B3)*math.sin(float(_theta)) #Compute reflectance image
        rows = npB3.shape[0] #Original rows
        cols = npB3.shape[1] #Original cols
        trans = dsB3.GetGeoTransform() #Get transformation information from the original file
        proj = dsB3.GetProjection() #Get Projection Information
        nodatav = band3.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _reflectancefolder, _reflectancefolder+"_"+_band3Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _reflectancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB3Reflectance,outputRasterFile) #Write file to disk
        dsB3 = band3 = npB3 = npB3Reflectance = None #Free memory
        
        #Band4
        dsB4 = gdal.Open(os.path.join(_path, _radiancefolder ,_radiancefolder+"_"+_band4Filename))
        band4 = dsB4.GetRasterBand(1)
        npB4 = np.array(band4.ReadAsArray())
        
        #Save Reflectance Image 4
        npB4Reflectance = npB4 * (math.pi *math.pow(float(_d),2))/float(_ESUN_B4)*math.sin(float(_theta)) #Compute reflectance image
        rows = npB4.shape[0] #Original rows
        cols = npB4.shape[1] #Original cols
        trans = dsB4.GetGeoTransform() #Get transformation information from the original file
        proj = dsB4.GetProjection() #Get Projection Information
        nodatav = band4.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _reflectancefolder, _reflectancefolder+"_"+_band4Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _reflectancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB4Reflectance,outputRasterFile) #Write file to disk
        dsB4 = band4 = npB4 = npB4Reflectance = None #Free memory
      
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
    computeRadiance()
