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

#Call function to set parameters for radiance
Configurations.setRadiance()

#Call function to set parameters for reflectance
Configurations.setReflectance()

#Call function to set parameters for TRRI
Configurations.setTRRI()

#Set Remove workspace and other parameters
Configurations.setRemoveCloud()


#Path
_path=""
if len(sys.argv)>2:
    _path=sys.argv[2]##Get from console or GUI being user input
else :
    #Read from config file
    _path=Configurations.Configurations_workspace

#TRRI Folder
_TRRIFolder=""
if len(sys.argv)>3:
    _TRRIFolder=sys.argv[3]##Get from console or GUI being user input
else :
    #Read from config file
    _TRRIFolder=Configurations.Configurations_trrifolder

#Filename to band1
_band1Filename=""
if len(sys.argv)>4:
    _band1Filename=sys.argv[4]##Get from console or GUI being user input
else :
    #Read from config file
    _band1Filename=Configurations.Configurations_fileNameB1

#Filename to band2
_band2Filename=""
if len(sys.argv)>5:
    _band2Filename=sys.argv[5]##Get from console or GUI being user input
else :
    #Read from config file
    _band2Filename=Configurations.Configurations_fileNameB2

#Filename to band3
_band3Filename=""
if len(sys.argv)>6:
    _band3Filename=sys.argv[6]##Get from console or GUI being user input
else :
    #Read from config file
    _band3Filename=Configurations.Configurations_fileNameB3

#Filename to band4
_band4Filename=""
if len(sys.argv)>7:
    _band4Filename=sys.argv[7]##Get from console or GUI being user input
else :
    #Read from config file
    _band4Filename=Configurations.Configurations_fileNameB4
    
#Cloud Image
_cloudImage=""
if len(sys.argv)>8:
    _cloudImage=sys.argv[8]##Get from console or GUI being user input
else :
    #Read from config file
    _cloudImage=Configurations.Configurations_cloudImage

#CloudFree Image
_CloudFreeImage=""
if len(sys.argv)>9:
    _CloudFreeImage=sys.argv[9]##Get from console or GUI being user input
else :
    #Read from config file
    _CloudFreeImage=Configurations.Configurations_CloudFree_Image


#max search distance
_maxSearchDist=""
if len(sys.argv)>10:
    _maxSearchDist=sys.argv[10]##Get from console or GUI being user input
else :
    #Read from config file
    _maxSearchDist=Configurations.Configurations_maxSearchDistance

#no data value
_nodatavalue=""
if len(sys.argv)>11:
    _nodatavalue=sys.argv[11]##Get from console or GUI being user input
else :
    #Read from config file
    _nodatavalue=Configurations.Configurations_nodatavalue

#Radar image
_radar_Image=""
if len(sys.argv)>12:
    _radar_Image=sys.argv[12]##Get from console or GUI being user input
else :
    #Read from config file
    _radar_Image=Configurations.Configurations_radar_Image    
    
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
    
def getNumpyArray(ds):

    try:
        band = ds.GetRasterBand(1)
        channel = np.array(band.ReadAsArray())        
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
        global _TRRIImage, _CloudImage, _CloudFreeImage, _maxSearchDist, _nodatavalue
        global _band1Filename,_band2Filename,_band3Filename,_band4Filename
        global _path, _TRRIFolder, _radar_Image
        
        #Get band number
        lst =_band1Filename.split("-")#Split by hyphen*
        TRRIFilename = lst[1]+"-"+lst[2]#get last components. looks like "ALAV2A191273610-O1B2R_U.tif"

        #Get paths to the images
        radarPath = os.path.join(_radar_Image)
        cloudPath = os.path.join(_path, _TRRIFolder, _cloudImage+"_"+TRRIFilename)
        opticalPath = os.path.join(_path, _TRRIFolder, _TRRIFolder+"_"+TRRIFilename)
        band1Path = os.path.join(_path, _band1Filename)
        band2Path = os.path.join(_path, _band2Filename)
        band3Path = os.path.join(_path, _band3Filename)
        band4Path = os.path.join(_path, _band4Filename)

        #Get image
        radarImage = getImage(radarPath,True)
        cloudImage = getImage(cloudPath, True)
        opticalImage = getImage(opticalPath,True)
        band1Image = getImage(band1Path,True)
        band2Image = getImage(band2Path,True)
        band3Image = getImage(band3Path,True)
        band4Image = getImage(band4Path,True)

        #Get array
        arrRadar = getNumpyArray(radarImage)
        arrCloud = getNumpyArray(cloudImage)
        arrOptical = getNumpyArray(opticalImage)
        arrBand1 = getNumpyArray(band1Image)
        arrBand2 = getNumpyArray(band2Image)
        arrBand3 = getNumpyArray(band3Image)
        arrBand4 = getNumpyArray(band4Image)

        ##Convert arrCloud
        arrCloudCopy = np.copy(arrCloud).astype(float)
        arrCloudCopy[arrCloudCopy==1.]=99. #convert 1 to 99
        arrCloudCopy[arrCloudCopy==0.]=1. #convert 0 to 1
        arrCloudCopy[arrCloudCopy==99.]=0.#Convert 99 to 0
        ##Cloud pixels is now 0
        #Exclude the same cloud pixels from the radar image
        arrRadarCopy = np.copy(arrRadar)
        arrRadar2= np.multiply(arrRadarCopy,arrCloudCopy)
        #arrRadar2 = arrRadar2*arrCloudCopy
        
        #Convert 0. to 999.
        arrRadar2[arrRadar2==0.]=999.
        arrCloudCopy=arrRadarCopy=None#free memory

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
                returnList = makeSpiralSearchinMatrix(arrRadar2,m,n,367,DN_value_optical_image)# for now the threshold is 3 pixels
                if returnList[0] !=0:
                    #Set current DN value of optical image and the band images to new DN value for the returned q,r row
                    arrOptical[m,n] = arrOptical[returnList[1],returnList[2]]
                    arrBand1[m,n] = arrBand1[returnList[1],returnList[2]]
                    arrBand2[m,n] = arrBand2[returnList[1],returnList[2]]
                    arrBand3[m,n] = arrBand3[returnList[1],returnList[2]]
                    arrBand4[m,n] = arrBand4[returnList[1],returnList[2]]
                    
                    #logger.info("OGN DN Value : {0} Old Row : {1} Old Col : {2} |  New DN Value : {3}  New Row : {4}  New Col : {5} ".\
                    #format(DN_value_optical_image,m,n,returnList[0],returnList[1],returnList[2]))
                #else:
                    #logger.info("---(Row,Col) = "+str(m)+","+str(n)+"--Null Return List : "+str(returnList))
            y = y+1
            print(y)
            it.iternext()
        print y
        print datetime.now().strftime("-%y-%m-%d_%H-%M-%S")
        print "Completed Cloud Removal raster analysis"
        logger.info(strOutput)

        #Write cloud free raster file to disk
        rows = arrOptical.shape[0] #Original rows
        cols = arrOptical.shape[1] #Original cols
        trans = opticalImage.GetGeoTransform() #Get transformation information from the original file
        proj = opticalImage.GetProjection() #Get Projection Information
        nodatav = opticalImage.GetRasterBand(1).GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _CloudFreeImage+"_"+TRRIFilename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrOptical,outputRasterFile) #Write file to disk

        #Write cloudfree band2 image
        rows = arrBand2.shape[0] #Original rows
        cols = arrBand2.shape[1] #Original cols
        trans = band2Image.GetGeoTransform() #Get transformation information from the original file
        proj = band2Image.GetProjection() #Get Projection Information
        nodatav = band2Image.GetRasterBand(1).GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _band2Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrBand2,outputRasterFile) #Write file to disk

        #Write cloudfree band3 image
        rows = arrBand3.shape[0] #Original rows
        cols = arrBand3.shape[1] #Original cols
        trans = band3Image.GetGeoTransform() #Get transformation information from the original file
        proj = band3Image.GetProjection() #Get Projection Information
        nodatav = band3Image.GetRasterBand(1).GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _band3Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrBand3,outputRasterFile) #Write file to disk

        #Write cloudfree band4 image
        rows = arrBand4.shape[0] #Original rows
        cols = arrBand4.shape[1] #Original cols
        trans = band4Image.GetGeoTransform() #Get transformation information from the original file
        proj = band4Image.GetProjection() #Get Projection Information
        nodatav = band4Image.GetRasterBand(1).GetNoDataValue() # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _band4Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrBand4,outputRasterFile) #Write file to disk
        
                       
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
