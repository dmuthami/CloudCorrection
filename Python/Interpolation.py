#-------------------------------------------------------------------------------
# Name:        Interpolates to replace cloud pixels 
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
import Utilities
import SpiralSearchMatrix

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

        #Replace cloud pixels with those that are not cloudy from the radar image
        logger.info("Start: "+datetime.now().strftime("-%y-%m-%d_%H-%M-%S"))
        print("Start: "+datetime.now().strftime("-%y-%m-%d_%H-%M-%S"))
        #Loop through the cloud cells only
        
        arrCloudOnly = np.argwhere(arrCloud==1)
        _tuple = arrCloud.shape
        max_rows=_tuple[0]
        max_cols=_tuple[1]
        thresholdSearchMatrix =0
        if max_rows > max_cols :
            thresholdSearchMatrix = max_rows/4
        else:
            thresholdSearchMatrix = max_cols/4
        print("Dimensions : " + str(arrCloudOnly.shape))
        logger.info("Dimensions : " + str(arrCloudOnly.shape))
        y =0
        for m,n in arrCloudOnly:
            DN_value_optical_image = arrRadar[m,n] #Get DN value from radar image
            ## Look for another cell(r,c) in the radar image with the same DN value within a radius/threshold of x cells
            ## Currently x = 100 ad is paased as an argument
            ## The radar image to search is the one we have excluded the cloudy pixels
            ## Return the cell row and column
            returnList = SpiralSearchMatrix.makeSpiralSearchinMatrix(arrRadar,m,n,int(thresholdSearchMatrix),DN_value_optical_image,arrCloud)# for now the threshold is 3 pixels
            if returnList[0] !=0:
                #Replace current cloud DN value of optical image and the band images to new DN value for the returned q,r row
                arrOptical[m,n] = arrOptical[returnList[1],returnList[2]]
                arrBand1[m,n] = arrBand1[returnList[1],returnList[2]]
                arrBand2[m,n] = arrBand2[returnList[1],returnList[2]]
                arrBand3[m,n] = arrBand3[returnList[1],returnList[2]]
                arrBand4[m,n] = arrBand4[returnList[1],returnList[2]]
                    

            else:
                #Replace current cloud DN value of optical image with no data value = -999.0
                arrOptical[m,n] = float(_nodatavalue)
                arrBand1[m,n] = float(_nodatavalue)
                arrBand2[m,n] = float(_nodatavalue)
                arrBand3[m,n] = float(_nodatavalue)
                arrBand4[m,n] = float(_nodatavalue)
            y = y+1
            print(y)
        logger.info("End: "+datetime.now().strftime("-%y-%m-%d_%H-%M-%S"))
        print("End: "+datetime.now().strftime("-%y-%m-%d_%H-%M-%S"))
        
        #Write cloud free raster file to disk
        rows = arrOptical.shape[0] #Original rows
        cols = arrOptical.shape[1] #Original cols
        trans = opticalImage.GetGeoTransform() #Get transformation information from the original file
        proj = opticalImage.GetProjection() #Get Projection Information
        nodatav = float(_nodatavalue) # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _CloudFreeImage+"_"+TRRIFilename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrOptical,outputRasterFile) #Write file to disk
        #Read the image again
        #Execute fillnodata  
        opticalImage = getImage(outputRasterFile,False)
        channelband = opticalImage.GetRasterBand(1)        
        result = gdal.FillNodata(targetBand = channelband, maskBand = None, \
                                 maxSearchDist = int(_maxSearchDist), smoothingIterations =0)
        result=channelband=arrOptical=cloudImage=opticalImage=None #Flush out the results to disk
                                                     
        #Write cloudfree band1 image
        rows = arrBand1.shape[0] #Original rows
        cols = arrBand1.shape[1] #Original cols
        trans = band1Image.GetGeoTransform() #Get transformation information from the original file
        proj = band1Image.GetProjection() #Get Projection Information
        nodatav = float(_nodatavalue) # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _band1Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrBand1,outputRasterFile) #Write file to disk
        #Read the image again
        #Execute fillnodata  
        opticalImage = getImage(outputRasterFile,False)
        channelband = opticalImage.GetRasterBand(1)        
        result = gdal.FillNodata(targetBand = channelband, maskBand = None, \
                                 maxSearchDist = int(_maxSearchDist), smoothingIterations =0)
        result=channelband=arrBand1=band1Image=opticalImage=None #Flush out the results to disk
                                                     
        #Write cloudfree band2 image
        rows = arrBand2.shape[0] #Original rows
        cols = arrBand2.shape[1] #Original cols
        trans = band2Image.GetGeoTransform() #Get transformation information from the original file
        proj = band2Image.GetProjection() #Get Projection Information
        nodatav = float(_nodatavalue) # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _band2Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrBand2,outputRasterFile) #Write file to disk
        #Read the image again
        #Execute fillnodata  
        opticalImage = getImage(outputRasterFile,False)
        channelband = opticalImage.GetRasterBand(1)        
        result = gdal.FillNodata(targetBand = channelband, maskBand = None, \
                                 maxSearchDist = int(_maxSearchDist), smoothingIterations =0)
        result=channelband=arrBand2=band2Image=opticalImage=None #Flush out the results to disk
                                                     
        #Write cloudfree band3 image
        rows = arrBand3.shape[0] #Original rows
        cols = arrBand3.shape[1] #Original cols
        trans = band3Image.GetGeoTransform() #Get transformation information from the original file
        proj = band3Image.GetProjection() #Get Projection Information
        nodatav = float(_nodatavalue) # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _band3Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrBand3,outputRasterFile) #Write file to disk
        #Read the image again
        #Execute fillnodata  
        opticalImage = getImage(outputRasterFile,False)
        channelband = opticalImage.GetRasterBand(1)        
        result = gdal.FillNodata(targetBand = channelband, maskBand = None, \
                                 maxSearchDist = int(_maxSearchDist), smoothingIterations =0)
        result=channelband=arrBand3=band3Image=opticalImage=None #Flush out the results to disk
                                                     
        #Write cloudfree band4 image
        rows = arrBand4.shape[0] #Original rows
        cols = arrBand4.shape[1] #Original cols
        trans = band4Image.GetGeoTransform() #Get transformation information from the original file
        proj = band4Image.GetProjection() #Get Projection Information
        nodatav = float(_nodatavalue) # Get No Data Value
        outputRasterFile = os.path.join(_path, _TRRIFolder, _band4Filename)#output file
        Utilities.checkIfDirectoryExists(os.path.join(_path, _TRRIFolder)) #Check if directory exists
        WriteRaster.writeTIFF(rows,cols,trans,proj,nodatav,arrBand4,outputRasterFile) #Write file to disk
        #Read the image again
        #Execute fillnodata  
        opticalImage = getImage(outputRasterFile,False)
        channelband = opticalImage.GetRasterBand(1)        
        result = gdal.FillNodata(targetBand = channelband, maskBand = None, \
                                 maxSearchDist = int(_maxSearchDist), smoothingIterations =0)
        result=channelband=arrBand4=band4Image=opticalImage=None #Flush out the results to disk

        logger.info( "Completed Cloud Removal raster analysis")
                       
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)

    return ""


def main():
    pass

if __name__ == '__main__':
    main()

    ##Call true function
    interpolate()
