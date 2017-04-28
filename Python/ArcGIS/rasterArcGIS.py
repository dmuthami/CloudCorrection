# Name: Cloud Correction
# Description: Cloud removal and cloud shadow correction
# Requirements: Spatial Analyst Extension
# Import system modules
import os, sys
import arcpy
import traceback
from arcpy import env
from arcpy.sa import *

##Custom module containing functions
import Configurations
import GetImageFolders
import Utilities

try:

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
    env.workspace = Configurations.Configurations_workspace

    # Set environment settings
    arcpy.env.overwriteOutput = True

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    ##Get all directories
    #GetImageFolders.getAllFolders(Configurations.Configurations_workspace);

    ##Get all raster files
    _rasterFiles = GetImageFolders.getAllRasters(Configurations.Configurations_imagesfolder,\
    Configurations.Configurations_excludefolder);

    ##Loop through the raster list and print the file name
    for ras in _rasterFiles:
        ##Get respective metadata file
        paramList = Utilities.getGainAndOffset(os.path.basename(ras),os.path.dirname(ras),Configurations.Configurations_textfilesuffix)
        ##paramList as follows
        ## basename: 0
        ## directoryName : 1
        ## fileExtension : 2
        ## bandNumber : 3
        ## textfile for metadata : 4
        ## gain : 5
        ## offset :6
        if paramList!= []:
            ##Conduct reflectance but safely using error handling methods
            ##??' = M?Qcal + A?
            outputDirectory="";
            try:
                ##Compute reflectance image
                directory = paramList[1]
                fileName =  paramList[0]
                reflectanceImage = Raster(os.path.join(directory, fileName))*float(paramList[5]) + float(paramList[6])
                ## Save the output
                #Call function to check if "os.path.isdir"
                outputDirectory = os.path.join(directory, "Reflectance")
                Utilities.checkIfDirectoryExists(outputDirectory)
                reflectanceImageSeq = os.path.join(outputDirectory, "Reflectance_" + fileName)
                reflectanceImage.save(reflectanceImageSeq)
                print ("---------------")
                print (" Raster Input : {0} \n Dir : {1} \n Extension : {2} \n Band No : {3} \n Txt F.Name : {4} \n Gain : {5} \n Offset : {6} \n Reflectance Image : {7}".\
                format(paramList[0],paramList[1],paramList[2],paramList[3],paramList[4],paramList[5],paramList[6],reflectanceImageSeq))
                print ("---------------")
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

        ##Get REFLECTANCE_MULT_BAND_x and REFLECTANCE_ADD_BAND_x

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