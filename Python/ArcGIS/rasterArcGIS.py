# Name: Cloud Correction
# Description: Cloud removal and cloud shadow correction
# Requirements: Spatial Analyst Extension
# Import system modules
import os, sys
import logging
import traceback
import numpy as np
from osgeo import gdal

##Custom module containing functions
import Configurations
import GetImageFolders
import Utilities
import WriteRaster

try:

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
    Configurations.Configurations_cloudCorrection_error_logfile = os.path.join(os.path.dirname(__file__), 'cloudCorrecttion_error_logfile.log')
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
        configFileLocation=r"/home/geonode/Documents/Python/ArcGIS/Config.ini"

    ##Read from config file
    #If for any reason an exception is thrown here then subsequent code will not be executed
    Configurations.setParameters(configFileLocation)

    #Set workspace
    Configurations.setWorkspace()
    
    ##Get all raster files
    arr = GetImageFolders.ouputRasterArray(Configurations.Configurations_imagesfolder,\
    Configurations.Configurations_excludefolder)
    ##print arr

    ##Get the numer of rows and columns
    (max_rows, max_cols) = arr.shape
    for m in range (0, max_rows):
        dir = arr[m,1]
        file = arr[m,0]
        #print dir
        #print file
        paramList = Utilities.getGainAndOffset(file,\
                                               dir,\
                                               Configurations.Configurations_textfilesuffix)
        if paramList!= []:
            outputDirectory="";
            try:
                ##Compute reflectance image
                directory = paramList[1]
                fileName =  paramList[0]

                #dataset
                ds = gdal.Open(os.path.join(directory, fileName))
                band = ds.GetRasterBand(1)
                #raw image data
                npdata = np.array(band.ReadAsArray())
                
                #Processed image data
                npReflectance = npdata*float(paramList[5]) + float(paramList[6])

                ##Save the Reflectance output to TIFF file
                outputDirectory = os.path.join(directory, "Reflectance")
                Utilities.checkIfDirectoryExists(outputDirectory)
                outputRasterFile = os.path.join(outputDirectory, "Reflectance_" + fileName)

                
                rows = npdata.shape[0] #Original rows
                cols = npdata.shape[1] #Original cols
                trans = ds.GetGeoTransform() #Get transformation information from the original file
                proj = ds.GetProjection() #Get Projection Information
                nodatav = band.GetNoDataValue() # Get No Data Value

                #Save Image
                WriteRaster.writeTIFF(ds,rows,cols,trans,proj,nodatav,npReflectance,outputRasterFile)
                
                logger.info("---------------")
                logger.info (" Raster Input : {0} \n Dir : {1} \n Extension : {2} \n Band No : {3} \n Txt F.Name : {4} \n Gain : {5} \n Offset : {6} \n Reflectance Image : {7}".\
                format(paramList[0],paramList[1],\
                       paramList[2],paramList[3],paramList[4],\
                       paramList[5],paramList[6],\
                       outputRasterFile))
                logger.info ("---------------")                
            except:
                ## Return any Python specific errors and any error returned by the geoprocessor
                ##
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                        str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

                ##For debugging purposes only
                ##To be commented on python script scheduling in Windows
                print pymsg
        

except:
    ## Return any Python specific errors and any error returned by the geoprocessor
    ##
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
            str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

    ##For debugging purposes only
    ##To be commented on python script scheduling in Windows
    print pymsg
