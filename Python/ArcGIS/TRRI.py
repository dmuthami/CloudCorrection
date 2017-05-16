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
import arcpy
import os
import traceback
from arcpy import env
from arcpy.sa import *

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



def computeCloud():
    B1= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B1.TIF")
    B2= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B2.TIF")
    B3= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B3.TIF")
    B4= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B4.TIF")
    B5= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B5.TIF")
    B6= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B6.TIF")
    B7= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B7.TIF")
    B8= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B8.TIF")
    B9= Raster("Reflectance_LC08_L1TP_166063_20170112_20170311_01_T1_B9.TIF")

    TRRI =  (B2 + 2*(B3+B4+B5+B6)+B7)/2
    cloud =  Con(TRRI >= 2, 1,0)
    TRRI.save("TRRI_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")
    cloud.save("cloud_LC08_L1TP_166063_20170112_20170311_01_T1.TIF")

    print env.workspace
    return ""

def main():
    pass

if __name__ == '__main__':
    main()
    #Call function
    computeCloud()