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

#Call function to set parameters for TRRI
Configurations.setTRRI()

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

#Reflectance Folder
_reflectancefolder=""
if len(sys.argv)>7:
    _reflectancefolder=sys.argv[7]##Get from console or GUI being user input
else :
    #Read from config file
    _reflectancefolder=Configurations.Configurations_reflectancefolder

#Reflectance Folder
_TRRIFolder=""
if len(sys.argv)>7:
    _TRRIFolder=sys.argv[7]##Get from console or GUI being user input
else :
    #Read from config file
    _TRRIFolder=Configurations.Configurations_trrifolder

#Cloud Thresholld
_cloudthreshold=""
if len(sys.argv)>8:
    _cloudthreshold=sys.argv[8]##Get from console or GUI being user input
else :
    #Read from config file
    _cloudthreshold=Configurations.Configurations_cloudthreshold



#Cloud Image
_cloudImage=""
if len(sys.argv)>9:
    _cloudImage=sys.argv[9]##Get from console or GUI being user input
else :
    #Read from config file
    _cloudImage=Configurations.Configurations_cloudImage
    
def computeTRRI():
    try:
        global _path ,_band1Filename, _band2Filename, _band3Filename,_band4Filename
        global  _reflectancefolder, _TRRIFolder, _cloudthreshold, _cloudImage
        
        #Band1
        dsB1 = gdal.Open(os.path.join(_path, _reflectancefolder ,_reflectancefolder+"_"+_band1Filename)) #Go the radiance folder
        band1 = dsB1.GetRasterBand(1)
        npB1 = np.array(band1.ReadAsArray())

        
        #Band2
        dsB2 = gdal.Open(os.path.join(_path, _reflectancefolder ,_reflectancefolder+"_"+_band2Filename))
        band2 = dsB2.GetRasterBand(1)
        npB2 = np.array(band2.ReadAsArray())

        
        #Band3
        dsB3 = gdal.Open(os.path.join(_path, _reflectancefolder ,_reflectancefolder+"_"+_band3Filename))
        band3 = dsB3.GetRasterBand(1)
        npB3 = np.array(band3.ReadAsArray())
       
        
        #Band4
        dsB4 = gdal.Open(os.path.join(_path, _reflectancefolder ,_reflectancefolder+"_"+_band4Filename))
        band4 = dsB4.GetRasterBand(1)
        npB4 = np.array(band4.ReadAsArray())

        #ALOS AVNIR-2 Images; TRRI= (b1+2*(b2+b3)+b4)/2
        npTRRI= ((npB1+2.*(npB2+npB3)+npB4)/2.)*100.;

        #Get band number
        lst =_band1Filename.split("-")#Split by hyphen*
        TRRIFilename = lst[1]+"-"+lst[2]#get last components. looks like "ALAV2A191273610-O1B2R_U.tif"
        
        #Save TRRI Image
        rows = npB1.shape[0] #Original rows
        cols = npB2.shape[1] #Original cols
        trans = dsB1.GetGeoTransform() #Get transformation information from the original file
        proj = dsB1.GetProjection() #Get Projection Information
        nodatav = band1.GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _TRRIFolder+"_"+TRRIFilename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,npTRRI,outputRasterFile) #Write file to disk

        #Free memory
        dsB1 = band1 = npB1 =  None #Band1
        dsB2 = band2 = npB2 =  None #Band1
        dsB3 = band3 = npB3 =  None #Band1        
        dsB4 = band4 = npB4 =  None #Band1

        #Cloud computation
        npTRRI[npTRRI<float(_cloudthreshold)]=0.  #E.g Replace all values < 55. with 0.0
        npTRRI[npTRRI>=float(_cloudthreshold)]=1.  #E.g Replace all values >= 55. with 1.0

        #Convert to unsigned 8 bit
        npCloud =  npTRRI.astype(int)

        #Save cloud image
        outputRasterFile = os.path.join(_path, _TRRIFolder, _cloudImage+"_"+TRRIFilename)#output file
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
    computeTRRI()
