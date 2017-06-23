# Name: Cloud Correction
# Description: Cloud removal and cloud shadow correction
# Requirements: Spatial Analyst Extension
# Import system modules
import os, sys
import logging
import traceback
import numpy as np
from osgeo import gdal

##Custom module containing functions
import Configurations
import Radiance
import Reflectance
import TRRI
import Interpolation_Indexing as Interpolation

try:

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

    #Set workspace
    Configurations.setWorkspace()

    #Compute Radiance
    Radiance.computeRadiance()

    #Compute Reflectance
    Reflectance.computeReflectance()

    #compute TRRI
    TRRI.computeTRRI()

    #compute intepolation
    Interpolation.interpolate()
    
except:
    ## Return any Python specific errors and any error returned by the geoprocessor
    ##
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
            str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"

    ##For debugging purposes only
    ##To be commented on python script scheduling in Windows
    print pymsg
