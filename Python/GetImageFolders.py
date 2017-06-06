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

import os,sys
import logging
import traceback
import numpy as np

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

def getAllTIFF_Images(_directory,excludeFolder):
    try:
        rasterList = []
        for root, dirs, files in os.walk(_directory,topdown=True):
            try: 
                if excludeFolder in root:
                    root.remove(excludeFolder)
                              
                for fname in files:
                    if getFileExtension(fname) == "TIF"  :
                        rasterList.append(fname)
                        rasterList.append(root)            
            except:
                ## Return any Python specific errors and any error returned
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]

                pymsg = "PYTHON ERRORS:\n  Inner Try in the Function getAllTIFF_Images(_directory,excludeFolder) \n" + tbinfo + "\nError Info:\n    " + \
                        str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
                ##Write to the error log file
                logger_error.info( pymsg)
                        
        return rasterList
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function getAllTIFF_Images(_directory,excludeFolder) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
        return ""

def getFileExtension(fileName):
    try:
        #Get file extension,
        baseNameList=  fileName.split(".")#Split by period
        fileExtension = baseNameList[int(len(baseNameList) -1)]#get file extension e.g "TIF"
        return fileExtension        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function getFileExtension(fileName) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
        return ""


def outputRasterArray(_directory,excludeFolder):
    try:
        rasterList = getAllTIFF_Images(_directory,excludeFolder) #Get list of raster file
        rasterListLength = len(rasterList) #Get the length of the list
        arr1 = np.array(rasterList) #Convert the list to the array
        arr= arr1.reshape(rasterListLength/2,2) #Reshape the array to dimension m*2
        return arr        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function ouputRasterArray(_directory,excludeFolder) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)
        return ""    

def main():
    pass

if __name__ == '__main__':
    main()
    #Call entry function
    #arr = outputRasterArray("/home/geonode/Documents/Landsat","Reflectance")
    ##Get the numer of rows and columns
    #(max_rows, max_cols) = arr.shape
    #for m in range (0, max_rows):
        #logger.info("Dir : {0} | File : {0}".format(arr[m,1],arr[m,0]))
    
    
    
