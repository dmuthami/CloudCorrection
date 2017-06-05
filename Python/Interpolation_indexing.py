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
        
        inRadar = os.path.join(_path, "Radar.TIF")
        inCloud = os.path.join(_path, "Cloud_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        inOpticalImage = os.path.join(_path, "TRRI_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")

        ## Convert Rasters to respective numpy arrays
        arrOptical = load_image3(inOpticalImage)
        arrRadar =load_image3(inRadar)
        arrCloud =load_image3(inCloud)

        inRadar = None
        inCloud = None
        inOpticalImage = None
        ##This will get you the number of rows and columns in your array for the cloud image
        ##Image has 1, 0 representing cloud and non-cloud pixels respectively
        #(max_rows, max_cols,bv) = arrCloud.shape
        _tuple =arrCloud.shape
        max_rows=_tuple[0]
        max_cols=_tuple[1]

        logger.info("Radar Array : "+str(arrRadar.shape)+"  Type : "+str(arrRadar.dtype))
        logger.info("Cloud Array : "+str(arrCloud.shape)+"  Type : "+str(arrCloud.dtype))
        logger.info("Optical Array : "+str(arrOptical.shape)+"  Type : "+str(arrOptical.dtype))
       
        #Get all cloud pixels
        #logger.info(arrCloud)

        ##Convert arrCloud
        arrCloudCopy = np.copy(arrCloud)
        arrCloudCopy[arrCloudCopy==1]=99 #convert 1 to 99
        arrCloudCopy[arrCloudCopy==0]=1 #convert 0 to 1
        arrCloudCopy[arrCloudCopy==99]=0#Convert 99 to 0
        ##Cloud pixels is now 0
        #Exclude the same cloud pixels from the radar image
        arrRadar2 = np.copy(arrRadar)
        arrRadar2 = arrRadar2*arrCloudCopy
        
        #Convert 0. to 999.
        arrRadar2[arrRadar2==0.]=999.
        arrCloudCopy=None#free memory
        
        
        #Replace cloud pixels with those that are not cloudy from the radar image
        print datetime.now().strftime("-%y-%m-%d_%H-%M-%S")
        y =0
        str_list=[]
        it = np.nditer(arrCloud,flags=['multi_index'])
        while not it.finished:
            #str_list.append("%d <%s>" %(it[0],it.multi_index)),
            if it[0]==1:#Cloud pixel
                m = it.multi_index[0]
                n = it.multi_index[1]
                DN_value_optical_image = arrRadar.item(m,n) #Get DN value from radar image
                ## Look for another cell(r,c) in the radar image with the same DN value within a radius/threshold of x cells
                ## Currently x = 100 ad is paased as an argument
                ## The radar image to search is the one we have excluded the cloudy pixels
                ## Return the cell row and column
                returnList = makeSpiralSearchinMatrix(arrRadar2,m,n,100,DN_value_optical_image)# for now the threshold is 3 pixels
                if returnList[0] !=0:
                    #Set current DN value of optical image to new DN value for the returned q,r row
                    arrOptical[m,n] = arrOptical[returnList[1],returnList[2]]
                    #logger.info("OGN DN Value : {0} Old Row : {1} Old Col : {2} |  New DN Value : {3}  New Row : {4}  New Col : {5} ".\
                    #format(DN_value_optical_image,m,n,returnList[0],returnList[1],returnList[2]))
                #else:
                    #logger.info("---(Row,Col) = "+str(m)+","+str(n)+"--Null Return List : "+str(returnList))
            y = y+1
            print(y)
            it.iternext()
        print y
        print datetime.now().strftime("-%y-%m-%d_%H-%M-%S")
        print "Completed raster analysis"
        #strOutput =''.join(str_list)
        logger.info(strOutput)

        
        ##Convert Array to raster (keep the origin and cellsize the same as the input)
        global _rows        
        global _cols        
        global _trans        
        global _proj        
        global _nodatav
        outputRasterFile = os.path.join(_path, "CloudFree_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        WriteRaster.writeTIFF(_rows,_cols,_trans,_proj,_nodatav,arrOptical,outputRasterFile)
                       
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
