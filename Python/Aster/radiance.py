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

#gain to band1
_gainBand1=""
if len(sys.argv)>7:
    _gainBand1=sys.argv[7]##Get from console or GUI being user input
else :
    #Read from config file
    _gainBand1=Configurations.Configurations_Gain_B1

#gain to band2
_gainBand2=""
if len(sys.argv)>8:
    _gainBand1=sys.argv[8]##Get from console or GUI being user input
else :
    #Read from config file
    _gainBand2=Configurations.Configurations_Gain_B2

#gain to band3
_gainBand3=""
if len(sys.argv)>9:
    _gainBand3=sys.argv[9]##Get from console or GUI being user input
else :
    #Read from config file
    _gainBand3=Configurations.Configurations_Gain_B3

#gain to band4
_gainBand4=""
if len(sys.argv)>10:
    _gainBand4=sys.argv[10]##Get from console or GUI being user input
else :
    #Read from config file
    _gainBand4=Configurations.Configurations_Gain_B4

#offset to band1
_offsetBand1=""
if len(sys.argv)>11:
    _offsetBand1=sys.argv[11]##Get from console or GUI being user input
else :
    #Read from config file
    _offsetBand1=Configurations.Configurations_Offset_B1

#offset to band2
_offsetBand2=""
if len(sys.argv)>12:
    _offsetBand2=sys.argv[12]##Get from console or GUI being user input
else :
    #Read from config file
    _offsetBand2=Configurations.Configurations_Offset_B2

#offset to band3
_offsetBand3=""
if len(sys.argv)>13:
    _offsetBand3=sys.argv[13]##Get from console or GUI being user input
else :
    #Read from config file
    _offsetBand3=Configurations.Configurations_Offset_B3

#offset to band4
_offsetBand4=""
if len(sys.argv)>14:
    _offsetBand4=sys.argv[14]##Get from console or GUI being user input
else :
    #Read from config file
    _offsetBand4=Configurations.Configurations_Offset_B4

#Radiance Folder
_radiancefolder=""
if len(sys.argv)>15:
    _radiancefolder=sys.argv[15]##Get from console or GUI being user input
else :
    #Read from config file
    _radiancefolder=Configurations.Configurations_radiancefolder


def computeRadiance():
    try:
        global _path ,_band1Filename, _band2Filename, _band3Filename,_band4Filename
        global _gainBand1, _gainBand2,_gainBand3,_gainBand4
        global _offsetBand1,_offsetBand2,_offsetBand3,_offsetBand4
        global _radiancefolder

        #Band1
        dsB1 = gdal.Open(os.path.join(_path, _band1Filename))
        band1 = dsB1.GetRasterBand(1)
        npB1 = np.array(band1.ReadAsArray())

        #Save Radiance Image 1
        npB1Radiance = npB1 * float(_gainBand1) +float(_offsetBand1) #Compute radiance image
        rows = npB1.shape[0] #Original rows
        cols = npB1.shape[1] #Original cols
        trans = dsB1.GetGeoTransform() #Get transformation information from the original file
        proj = dsB1.GetProjection() #Get Projection Information
        nodatav = band1.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _radiancefolder, _radiancefolder+"_"+_band1Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _radiancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB1Radiance,outputRasterFile) #Write file to disk
        dsB1 = band1 = npB1 = npB1Radiance = None #Free memory
        
        #Band2
        dsB2 = gdal.Open(os.path.join(_path, _band2Filename))
        band2 = dsB2.GetRasterBand(1)
        npB2 = np.array(band2.ReadAsArray())

        #Save Radiance Image 2
        npB2Radiance = npB2 * float(_gainBand2) +float(_offsetBand2) #Compute radiance image
        rows = npB2.shape[0] #Original rows
        cols = npB2.shape[1] #Original cols
        trans = dsB2.GetGeoTransform() #Get transformation information from the original file
        proj = dsB2.GetProjection() #Get Projection Information
        nodatav = band2.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _radiancefolder, _radiancefolder+"_"+_band2Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _radiancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB2Radiance,outputRasterFile) #Write file to disk
        dsB2 = band2 = npB2 = npB2Radiance = None #Free memory
        
        #Band3
        dsB3 = gdal.Open(os.path.join(_path, _band3Filename))
        band3 = dsB3.GetRasterBand(1)
        npB3 = np.array(band3.ReadAsArray())
        
        #Save Radiance Image 3
        npB3Radiance = npB3 * float(_gainBand3) +float(_offsetBand3) #Compute radiance image
        rows = npB3.shape[0] #Original rows
        cols = npB3.shape[1] #Original cols
        trans = dsB3.GetGeoTransform() #Get transformation information from the original file
        proj = dsB3.GetProjection() #Get Projection Information
        nodatav = band3.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _radiancefolder, _radiancefolder+"_"+_band3Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _radiancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB3Radiance,outputRasterFile) #Write file to disk
        dsB3 = band3 = npB3 = npB3Radiance = None #Free memory        
        
        #Band4
        dsB4 = gdal.Open(os.path.join(_path, _band4Filename))
        band4 = dsB4.GetRasterBand(1)
        npB4 = np.array(band4.ReadAsArray())
        
        #Save Radiance Image 4
        npB4Radiance = npB4 * float(_gainBand4) +float(_offsetBand4) #Compute radiance image
        rows = npB4.shape[0] #Original rows
        cols = npB4.shape[1] #Original cols
        trans = dsB4.GetGeoTransform() #Get transformation information from the original file
        proj = dsB4.GetProjection() #Get Projection Information
        nodatav = band4.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _radiancefolder, _radiancefolder+"_"+_band4Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _radiancefolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npB4Radiance,outputRasterFile) #Write file to disk
        dsB4 = band4 = npB4 = npB4Radiance = None #Free memory
      
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
