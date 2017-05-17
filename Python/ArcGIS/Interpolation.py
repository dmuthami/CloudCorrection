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
import arcpy
import os
import traceback
from arcpy import env
from arcpy.sa import *
import numpy

##Custom module containing functions
import Configurations

##Obtain script parameter values
##location for configuration file
##Acquire it as a parameter either from terminal, console or via application
configFileLocation=arcpy.GetParameterAsText(0)#Get from console or GUI being user input
if configFileLocation =='': #Checks if supplied parameter is null
    #Defaults to below hard coded path if the parameter is not supplied. NB. May throw exceptions if it defaults to path below
    # since path below might not  be existing in your system with the said file name required
    configFileLocation=r"E:\GIS Data\DAVVOC\Maithya\Python\ArcGIS\Config.ini"

##Read from config file
#If for any reason an exception is thrown here then subsequent code will not be executed
Configurations.setParameters(configFileLocation)

#Set workspace
Configurations.setWorkspace()
#env.workspace = Configurations.Configurations_workspace
env.workspace = r"E:\GIS Data\DAVVOC\Maithya\Images\LC08_L1TP_166063_20170112_20170311_01_T1\Reflectance"

# Set environment settings
arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")


def interpolate():
    inRas = Raster("TRRI_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
    inRadar = Raster("Radar.TIF")
    inCloud = Raster("cloud_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")

    # Convert Raster to numpy array
    arr = arcpy.RasterToNumPyArray(inRas)
    arrRadar =arcpy.RasterToNumPyArray(inRadar)
    arrCloud =arcpy.RasterToNumPyArray(inCloud)


    #This will get you the number of rows and columns in your array
    (max_rows, max_cols) = arr.shape
  # Loop thru all the cells in array
    for m in range (0, max_rows):
        for n in range (0, max_cols):
            cell_value = arrCloud.item(m,n)
            # do your process here...
            if cell_value== 1: #Cloud pixel
                #Get DN value from radar image
                DN_value_radar_image = arrRadar.item(m,n)
                #Look for another cell(r,c) with the same DN value within a radius/threshold of 12 cells
                #Return the cell row and column
                returnList = makeSpiralSearchinMatrix(arrRadar,m,n,12,DN_value_radar_image)
                if returnList[0] !=0:
                    print (" Old DN Value : {0} Old Row : {1} Old Col : {2} |  New DN Value : {3} \n New Row : {4} \n New Col : {5} ".\
                    format(DN_value_radar_image,m,n,paramList[0],paramList[1],paramList[2]))
                print returnList
                #Set the DN of the current cell C(m,n) to inRas(r,c)
                #arr.item(m,n) = returnList[0]
    return ""

def makeSpiralSearchinMatrix(arrRadar,row,col,length,DN_value_radar_image):
    ##DNValue,Row,Col
    returnList=[0,0,0]
    try:
        threshold = length - 1;
        rowStart=row-threshold;
        rowLength=(2 * threshold) + rowStart;

        colStart=col - threshold
        colLength = (2 * threshold) + colStart;

        while (rowStart <= rowLength and  colStart <= colLength):
            #Top Boundary
            i = rowStart
            while(i<= colLength):
                DN_value = arrRadar.item(rowStart,i)
                #print DN_value
                if(row != rowStart and col != i):
                    if(DN_value==DN_value_radar_image):
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
                    if(DN_value==DN_value_radar_image):
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
                        if(DN_value==DN_value_radar_image):
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
                        if(DN_value==DN_value_radar_image):
                            returnList[0]=DN_value
                            returnList[1]=k
                            returnList[2]=colStart
                    k-=1

            rowStart+=1
            rowLength-=1
            colStart+=1
            colLength-=1
            #print "Wow"
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        msgs = "Geoprocesssing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##dd custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print pymsg
        print "\n" +msgs

    return returnList

def main():
    pass

if __name__ == '__main__':
    main()
    x = numpy.array([\
        [1, 2, 3, 4, 5],\
        [6, 7, 8, 9, 10],\
        [11, 12, 13, 14, 15],\
        [16, 17, 18, 19, 20],\
        [21, 22, 23, 24, 25]\
    ],numpy.int32)
    #Call function
    #makeSpiralSearchinMatrix(x,4,4,5,"")

    ##Call true function
    interpolate()