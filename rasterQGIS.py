# Name: Reclasify using Remap Table
# Description: Reclassifies the values of the input raster using a remap table.
# Requirements: Spatial Analyst Extension
# Import system modules
import os, sys
import traceback
from qgis.core import *

try:
    # supply path to qgis install location
    QgsApplication.setPrefixPath("C:/OSGeo4W/bin", True)

    # create a reference to the QgsApplication, setting the
    # second argument to False disables the GUI
    qgs = QgsApplication([], False)

    # load providers
    qgs.initQgis()

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



    #??' = M?Qcal + A?
    s = "/";
    try:
        for k, v in dictREFLECTANCE_MULT_BAND_x.items():
            inRasterSeq = (env.workspace, imagefolder, k)
            inRas =s.join(inRasterSeq)
            z = float(dictREFLECTANCE_ADD_BAND_x.get(k))
            #outRas = Raster(inRas)*float(v) + z

            ## Save the output
            #outRasterSeq = (env.workspace, imagefolder,"Output","Reflectance", k)
            #outRasPath =s.join(outRasterSeq)
            #outRas.save(outRasPath)
            #print("Raster : {0},  REFLECTANCE_MULT_BAND_x : {1}, | \
            #Raster : {0},  REFLECTANCE_ADD_BAND_x : {2} ".format(k, v, z))
        print "Wow"
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows
        print "\n" +msgs
    print "Success : Perfect in Every Other Way"

    # When your script is complete, call exitQgis() to remove the provider and
    # layer registries from memory
    qgs.exitQgis()
except:
    ## Return any Python specific errors and any error returned by the geoprocessor
    ##
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
            str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

    ##For debugging purposes only
    ##To be commented on python script scheduling in Windows
    print "\n" +msgs