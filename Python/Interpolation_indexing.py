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

#Path to the interpolation folder
_path = r"/home/geonode/Documents/Landsat/LC08_L1TP_166063_20170112_20170311_01_T1/Reflectance"

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
    
def load_image3( infilename) :

    try:
        ds = gdal.Open(infilename)
        band = ds.GetRasterBand(1)
        channel = np.array(band.ReadAsArray())
        global _rows
        _rows = channel.shape[0] #Original rows
        global _cols
        _cols = channel.shape[1] #Original cols
        global _trans
        _trans = ds.GetGeoTransform() #Get transformation information from the original file
        global _proj
        _proj = ds.GetProjection() #Get Projection Information
        global _nodatav
        _nodatav = band.GetNoDataValue() # Get No Data Value
        
        return channel #Return Numpy Array
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
        
        radarPath = os.path.join(_path, "Radar.TIF")
        cloudPath = os.path.join(_path, "Cloud_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        opticalPath = os.path.join(_path, "TRRI_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")

        radarImage = getImage(radarPath,True)
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
            _nodatav = -999.

        #Multiply cloud pixel (cloudArr) with no data value -999= cloudArr2
        cloudBand = cloudImage.GetRasterBand(1)
        cloudArr = np.array(cloudBand.ReadAsArray())    
        cloudArr2 = cloudArr*-999

        #Add cloudArr2 to the opticalArr to give opticalArr2
        opticalArr2 = cloudArr2 + opticalArr
        opticalArr2[opticalArr2<-900]=-999.  #Replace all values < -900 with -999
        
        ##Convert Array to raster (keep the origin and cellsize the same as the input)
        ##Remeber NoDatavalue = -999 or -999.0
        outputRasterFile = os.path.join(_path, "TRRI2_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        WriteRaster.writeTIFF(_rows,_cols,_trans,_proj,_nodatav,opticalArr2,outputRasterFile)

        ##Create a copy of opticalArr2 
        outputRasterFile = os.path.join(_path, "CloudFree_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        WriteRaster.writeTIFF(_rows,_cols,_trans,_proj,_nodatav,opticalArr2,outputRasterFile)
        
        #Read the image again
        #Execute fillnodata
        opticalPath2 = os.path.join(_path, "CloudFree_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        opticalImage2 = getImage(opticalPath,False)
        channelband = opticalImage2.GetRasterBand(1)        
        result = gdal.FillNodata(targetBand = channelband, maskBand = None, \
                                 maxSearchDist = 1000, smoothingIterations =0)

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

def makeSpiralSearchinMatrix(arrRadar,row,col,length,DN_value_optical_image):
    ##DNValue,Row,Col
    returnList=[0,0,0]
    try:
        threshold = length - 1;
        rowStart=row-threshold;
        rowLength=(2 * threshold) + rowStart;

        colStart=col - threshold
        colLength = (2 * threshold) + colStart;

        DN_value = 0 #Initialize variable
        breakAgain = 0 # Variable determines if there is need to break again from the outer
                        # While loop
        while (rowStart <= rowLength and  colStart <= colLength):
            try:
                #Top Boundary
                i = rowStart
                while(i<= colLength):
                    DN_value = arrRadar.item(rowStart,i)
                    #print DN_value
                    if(row != rowStart and col != i):
                        if(DN_value==DN_value_optical_image and rowStart>=0 and i>=0 ):
                            returnList[0]=DN_value
                            returnList[1]=rowStart
                            returnList[2]=i
                            breakAgain =1
                            break
                    i+=1
                if (breakAgain ==1):
                    break

                #Right Boundary
                j = rowStart + 1
                while(j<= colLength):
                    DN_value = arrRadar.item(j,colLength)
                    #print DN_value
                    if( row!= j and col != colLength):
                        if(DN_value==DN_value_optical_image and j>=0 and colLength>=0):
                            returnList[0]=DN_value
                            returnList[1]=j
                            returnList[2]=colLength
                            breakAgain =1
                            break
                    j+=1
                if (breakAgain ==1):
                    break                

                #Bottom Boundary
                if(rowStart+1 <= rowLength ):
                    k = colLength-1
                    while(k >= colStart):
                        DN_value = arrRadar.item(rowLength,k)
                        #print DN_value
                        if( row!= rowLength and col != k):
                            if(DN_value==DN_value_optical_image and rowLength>=0 and k >=0):
                                returnList[0]=DN_value
                                returnList[1]=rowLength
                                returnList[2]=k
                                breakAgain = 1
                                break
                        k-=1
                        
                if (breakAgain ==1):
                    break
                
                #Left boundary
                if(colStart+1 <= colLength ):
                    k = rowLength-1
                    while(k > rowStart):
                        DN_value = arrRadar.item(k,colStart)
                        #print DN_value
                        if( row!= k and col != colStart):
                            if(DN_value==DN_value_optical_image and k >=0 and colStart>=0):
                                returnList[0]=DN_value
                                returnList[1]=k
                                returnList[2]=colStart
                                breakAgain = 1
                                break
                        k-=1
                        
                if (breakAgain ==1):
                    break
            except:
                ## Return any Python specific errors and any error returned
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                        str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
                ##Write to the error log file
                logger_error.info( pymsg)
            rowStart+=1
            rowLength-=1
            colStart+=1
            colLength-=1
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)

    return returnList

def main():
    pass

if __name__ == '__main__':
    main()

    ##Call true function
    interpolate()
