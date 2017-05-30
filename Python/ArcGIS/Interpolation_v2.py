#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maithya
#
# Created:     16/05/2017
# Copyright:   (c) Maithay 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os,sys
import logging
import traceback
import numpy as np
from osgeo import gdal

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

#Set workspace and other parameters
Configurations.setWorkspace()

#Path to the interpolation folder
_path = r"/home/geonode/Documents/Images"

##Gather information from the original file
##Store it in this global variables      
_cols = 0
_rows = 0
_proj = ""
_trans = ""
_nodatav = ""
_outFile = ""

def save_image( npdata, outfilename ) :
    try:
        #Create file using information from Original File
        rasterFilePath = os.path.join(_path, outfilename)
        outDrive = gdal.GetDriverByName("GTiff")  
        outRaster = outDrive.Create(str(rasterFilePath),_rows_cols_,1,gdal.GDT_Float64)

        #Write array to the file
        outRaster.GetRasterBand(1).WriteArray(npdata)

        #Seta no data value
        outRaster.GetRasterBand(1).SetNoDataValue(_nodatav)

        #GeoReference the image
        outRaster.SetGeoTransform(_trans)

        #Write projection information
        outRaster.SetProjection(_proj)
        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function save_image( npdata, outfilename) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)

def load_image3( infilename) :

    try:
        ds = gdal.Open(infilename)
        band = ds.GetRasterBand(1)
        channel = np.array(band.ReadAsArray())
        _rows = channel.shape[0] #Original rows
        _cols = channel.shape[1] #Original cols
        _trans = ds.GetGeoTransform() #Get transformation information from the original file
        _proj = ds.GetProjection() #Get Projection Information
        _nodatav = band.GetNoDataValue() # Get No Data Value
        
        logger.info("Image shape : {0}  Type : {1}".format(channel.shape,channel.dtype))
        
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
        inOpticalImage = os.path.join(_path, "TRRI_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
        inRadar = os.path.join(_path, "Radar.TIF")
        inCloud = os.path.join(_path, "cloud_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")

        ## Convert Rasters to respective numpy arrays
        arrOptical = load_image3(inOpticalImage)
        arrRadar =load_image3(inRadar)
        arrCloud =load_image3(inCloud)


        ##This will get you the number of rows and columns in your array for the cloud image
        ##Image has 1, 0 representing cloud and non-cloud pixels respectively
        #(max_rows, max_cols,bv) = arrCloud.shape
        _tuple =arrCloud.shape
        max_rows=_tuple[0]
        max_cols=_tuple[1]

        ## Loop thru all the cells in the cloud array
        ## Check for cell values that are 1 and ignore the onces that are zero
        ## 1= cloud cell
        ## 0= Non cloud cell
        for m in range (0, max_rows):
            for n in range (0, max_cols):
                cell_value = arrCloud.item(m,n)
                if cell_value== 1: #Cloud pixel
                    DN_value_optical_image = arrRadar.item(m,n) #Get DN value from radar image
                    ##Look for another cell(r,c) in the radar image with the same DN value within a radius/threshold of x cells
                    ##Return the cell row and column
                    returnList = makeSpiralSearchinMatrix(arrRadar,m,n,12,DN_value_optical_image)# for now the threshold is 12 pixels

                    if returnList[0] !=0:
                        #Set current DN value of optical image to new DN value for the returned q,r row
                        arrOptical[m,n] = arrOptical[returnList[1],returnList[2]]
                        logger.info("OGN DN Value : {0} Old Row : {1} Old Col : {2} |  New DN Value : {3}  New Row : {4}  New Col : {5} ".\
                        format(DN_value_optical_image,m,n,returnList[0],returnList[1],returnList[2]))

                    #print returnList

        ##Convert Array to raster (keep the origin and cellsize the same as the input)

        _outFile = "outputfile.tif" #Get the file name from the infilename
        save_image( arrOptical, _outFile )
        
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
                    i+=1

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
                    j+=1

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
                        k-=1
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
                        k-=1

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
