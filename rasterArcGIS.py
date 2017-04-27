# Name: Reclasify using Remap Table
# Description: Reclassifies the values of the input raster using a remap table.
# Requirements: Spatial Analyst Extension
# Import system modules
import os, sys
import arcpy
import traceback
from arcpy import env
from arcpy.sa import *

##Custom module containing functions
import Configurations

try:
    # Set environment settings
    arcpy.env.overwriteOutput = True

    imagefolder = "LC08_L1TP_166063_20170112_20170311_01_T1"

    ##Create dictionary
    ## In Each key is the raster name while value is the REFLECTANCE_MULT_BAND_x
    ##
    dictREFLECTANCE_MULT_BAND_x =\
    {'LC08_L1TP_166063_20170112_20170311_01_T1_B1.TIF': '2.0000E-05',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B2.TIF': '2.0000E-05', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B3.TIF': '2.0000E-05',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B4.TIF': '2.0000E-05', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B5.TIF': '2.0000E-05',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B6.TIF': '2.0000E-05', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B7.TIF': '2.0000E-05',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B8.TIF': '2.0000E-05', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B9.TIF': '2.0000E-05',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B10.TIF': '2.0000E-05',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B11.TIF': '2.0000E-05'}

    ##Create dictionary
    ## In Each key is the raster name while value is the REFLECTANCE_MULT_BAND_x
    ##
    dictREFLECTANCE_ADD_BAND_x =\
    {'LC08_L1TP_166063_20170112_20170311_01_T1_B1.TIF': '-0.100000',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B2.TIF': '-0.100000', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B3.TIF': '-0.100000',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B4.TIF': '-0.100000', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B5.TIF': '-0.100000',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B6.TIF': '-0.100000', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B7.TIF': '-0.100000',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B8.TIF': '-0.100000', \
    'LC08_L1TP_166063_20170112_20170311_01_T1_B9.TIF': '-0.100000',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B10.TIF': '-0.100000',\
    'LC08_L1TP_166063_20170112_20170311_01_T1_B11.TIF': '-0.100000'}

    # Set environment settings
    env.workspace = r"E:\GIS Data\DAVVOC\Maithya\Images"

    ##Obtain script parameter values
    ##location for configuration file
    ##Acquire it as a parameter either from terminal, console or via application
    configFileLocation=arcpy.GetParameterAsText(0)#Get from console or GUI being user input
    if configFileLocation =='': #Checks if supplied parameter is null
        #Defaults to below hard coded path if the parameter is not supplied. NB. May throw exceptions if it defaults to path below
        # since path below might not  be existing in your system with the said file name required
        configFileLocation=r"E:\GIS Data\DAVVOC\Maithya\Python\Config.ini"

    ##Read from config file
    #If for any reason an exception is thrown here then subsequent code will not be executed
    Configurations.setParameters(configFileLocation)

    #Set workspace
    Configurations.setWorkspace()
    env.workspace = Configurations.Configurations_workspace

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    #??' = M?Qcal + A?
    s = "/";
    try:
        for k, v in dictREFLECTANCE_MULT_BAND_x.items():
            inRasterSeq = (env.workspace, imagefolder, k)
            inRas =s.join(inRasterSeq)
            z = float(dictREFLECTANCE_ADD_BAND_x.get(k))
            outRas = Raster(inRas)*float(v) + z

            # Save the output
            outRasterSeq = (env.workspace, imagefolder,"Output","Reflectance", k)
            outRasPath =s.join(outRasterSeq)
            outRas.save(outRasPath)
            print("Raster : {0},  REFLECTANCE_MULT_BAND_x : {1}, | \
            Raster : {0},  REFLECTANCE_ADD_BAND_x : {2} ".format(k, v, z))
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
    print "Success : Perfect in Every Other Way"
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