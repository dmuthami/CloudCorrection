
#-------------------------------------------------------------------------------
# Name:        Configurations
# Purpose:
#
# Author:      Maithya
#
# Created:     29/09/2014
# Copyright:   (c) Maithya 2014
# Licence:     GPL
#-------------------------------------------------------------------------------
import os, sys
import logging
import ConfigParser

#Import global traceback here
import traceback


#Workspace global variables
Configurations_cloudCorrection_logfile = ""
Configurations_cloudCorrection_error_logfile = ""

#Workspace global variables
Configurations_workspace = ""
Configurations_radiancefolder = ""
Configurations_reflectancefolder = ""
Configurations_fileNameB1 = ""
Configurations_fileNameB2 = ""
Configurations_fileNameB3 = ""
Configurations_fileNameB4 = ""


#Radiance global variables
Configurations_Gain_B1 = ""
Configurations_Gain_B2 = ""
Configurations_Gain_B3 = ""
Configurations_Gain_B4 = ""
Configurations_Offset_B1 = ""
Configurations_Offset_B2 = ""
Configurations_Offset_B3 = ""
Configurations_Offset_B4 = ""

#Reflectance global variables
Configurations_d = ""
Configurations_ESUN_B1 = ""
Configurations_ESUN_B2 = ""
Configurations_ESUN_B3 = ""
Configurations_ESUN_B4 = ""
Configurations_theta = ""

#TRRI global variables
Configurations_trrifolder = ""
Configurations_cloudthreshold = ""
Configurations_cloudImage = ""

#removeCloud global variables
Configurations_CloudFree_Image = ""
Configurations_maxSearchDistance = ""
Configurations_nodatavalue = ""
Configurations_radar_Image = ""

#Set-up logging
logger = logging.getLogger('myapp')
Configurations_cloudCorrection_logfile = os.path.join(os.path.dirname(__file__), 'cloudCorrection_logfile.log')
hdlr = logging.FileHandler(Configurations_cloudCorrection_logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

#Set-up Error Logging
logger_error = logging.getLogger('myError')
Configurations_cloudCorrection_error_logfile = os.path.join(os.path.dirname(__file__), 'cloudCorrection_error_logfile.log')
hdlr_error = logging.FileHandler(Configurations_cloudCorrection_error_logfile)
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr_error.setFormatter(formatter)
logger_error.addHandler(hdlr_error)
logger_error.setLevel(logging.INFO)

def setParameters(configFileLocation):

    #Dirty way of working with global variables
    global Configurations_Config #Set global variable.Usually not favourable in Python
    global Configurations_Sections #Set global variable.Usually not favourable in Python

    Configurations_Config = ConfigParser.ConfigParser() #instantiate ini parser object

    #Read the Config file
    Configurations_Config.read(configFileLocation)

    return ""

##Set parameters for workspace
def setWorkspace():

    #read workspace location from Config file location
    global Configurations_workspace # Needed to modify global copy of Configurations_workspace
    Configurations_workspace = Configurations_Config.get('Workspace', 'workspace')
    logger.info("Configurations_workspace : "+ Configurations_workspace)

    #read radiance folder from Config file location
    global Configurations_radiancefolder # Needed to modify global copy of Configurations_radiancefolder
    Configurations_radiancefolder = Configurations_Config.get('Workspace', 'radiancefolder')
    logger.info("Configurations_radiancefolder : "+ Configurations_radiancefolder)

    #read reflectance folder from Config file location
    global Configurations_reflectancefolder # Needed to modify global copy of Configurations_reflectancefolder
    Configurations_reflectancefolder = Configurations_Config.get('Workspace', 'reflectancefolder')
    logger.info("Configurations_reflectancefolder : "+ Configurations_reflectancefolder)

    return ""

##Set parameters for reading radiance parameters
def setRadiance():

    #read Gain_B1 from Config file location
    global Configurations_Gain_B1 # Needed to modify global copy of Configurations_Gain_B1
    Configurations_Gain_B1 = Configurations_Config.get('Radiance', 'Gain_B1')
    logger.info("Configurations_Gain_B1 : "+Configurations_Gain_B1)

    #read Gain_B2 from Config file location
    global Configurations_Gain_B2 # Needed to modify global copy of Configurations_Gain_B1
    Configurations_Gain_B2 = Configurations_Config.get('Radiance', 'Gain_B2')
    logger.info("Configurations_Gain_B2 : "+Configurations_Gain_B2)

    #read Gain_B3 from Config file location
    global Configurations_Gain_B3 # Needed to modify global copy of Configurations_Gain_B1
    Configurations_Gain_B3 = Configurations_Config.get('Radiance', 'Gain_B3')
    logger.info("Configurations_Gain_B3 : "+Configurations_Gain_B3)

    #read Gain_B4 from Config file location
    global Configurations_Gain_B4 # Needed to modify global copy of Configurations_Gain_B1
    Configurations_Gain_B4 = Configurations_Config.get('Radiance', 'Gain_B4')
    logger.info("Configurations_Gain_B4 : "+Configurations_Gain_B4)

    #read Offset_B1 from Config file location
    global Configurations_Offset_B1 # Needed to modify global copy of Configurations_Offset_B1
    Configurations_Offset_B1 = Configurations_Config.get('Radiance', 'Offset_B1')
    logger.info("Configurations_Offset_B1 : "+Configurations_Offset_B1)

    #read Offset_B2 from Config file location
    global Configurations_Offset_B2 # Needed to modify global copy of Configurations_Offset_B2
    Configurations_Offset_B2 = Configurations_Config.get('Radiance', 'Offset_B2')
    logger.info("Configurations_Offset_B2 : "+Configurations_Offset_B2)

    #read Offset_B3 from Config file location
    global Configurations_Offset_B3 # Needed to modify global copy of Configurations_Offset_B3
    Configurations_Offset_B3 = Configurations_Config.get('Radiance', 'Offset_B3')
    logger.info("Configurations_Offset_B3 : "+Configurations_Offset_B3)

    #read Offset_B4 from Config file location
    global Configurations_Offset_B4 # Needed to modify global copy of Configurations_Offset_B4
    Configurations_Offset_B4 = Configurations_Config.get('Radiance', 'Offset_B4')
    logger.info("Configurations_Offset_B4 : "+Configurations_Offset_B4)

    #read fileNameB1 from Config file location
    global Configurations_fileNameB1 # Needed to modify global copy of Configurations_fileNameB1
    Configurations_fileNameB1 = Configurations_Config.get('Radiance', 'fileNameB1')
    logger.info("Configurations_fileNameB1 : "+Configurations_fileNameB1)

    #read fileNameB2 from Config file location
    global Configurations_fileNameB2 # Needed to modify global copy of Configurations_fileNameB2
    Configurations_fileNameB2 = Configurations_Config.get('Radiance', 'fileNameB2')
    logger.info("Configurations_fileNameB2 : "+Configurations_fileNameB2)

    #read fileNameB3 from Config file location
    global Configurations_fileNameB3 # Needed to modify global copy of Configurations_fileNameB3
    Configurations_fileNameB3 = Configurations_Config.get('Radiance', 'fileNameB3')
    logger.info("Configurations_fileNameB3 : "+Configurations_fileNameB3)    

    #read fileNameB4 from Config file location
    global Configurations_fileNameB4 # Needed to modify global copy of Configurations_fileNameB4
    Configurations_fileNameB4 = Configurations_Config.get('Radiance', 'fileNameB4')
    logger.info("Configurations_fileNameB4 : "+Configurations_fileNameB4)

    return ""

##Set parameters for reflectance
def setReflectance():

    #read d  from Config file location
    global Configurations_d # Needed to modify global copy of Configurations_d
    Configurations_d = Configurations_Config.get('Reflectance', 'd')
    logger.info("Configurations_d : "+ Configurations_d)

    #read ESUN_B1  from Config file location
    global Configurations_ESUN_B1 # Needed to modify global copy of Configurations_ESUN_B1
    Configurations_ESUN_B1 = Configurations_Config.get('Reflectance', 'ESUN_B1')
    logger.info("Configurations_ESUN_B1 : "+ Configurations_ESUN_B1)

    #read ESUN_B2 from Config file location
    global Configurations_ESUN_B2 # Needed to modify global copy of Configurations_ESUN_B2
    Configurations_ESUN_B2 = Configurations_Config.get('Reflectance', 'ESUN_B2')
    logger.info("Configurations_ESUN_B2 : "+ Configurations_ESUN_B2)

    #read ESUN_B3  from Config file location
    global Configurations_ESUN_B3 # Needed to modify global copy of Configurations_ESUN_B3
    Configurations_ESUN_B3 = Configurations_Config.get('Reflectance', 'ESUN_B3')
    logger.info("Configurations_ESUN_B3 : "+ Configurations_ESUN_B3)

    #read ESUN_B4  from Config file location
    global Configurations_ESUN_B4 # Needed to modify global copy of Configurations_d
    Configurations_ESUN_B4 = Configurations_Config.get('Reflectance', 'ESUN_B4')
    logger.info("Configurations_ESUN_B4 : "+ Configurations_ESUN_B4)

    #read theta  from Config file location
    global Configurations_theta # Needed to modify global copy of Configurations_theta
    Configurations_theta = Configurations_Config.get('Reflectance', 'theta')
    logger.info("Configurations_theta : "+ Configurations_theta)

    return ""

##Set parameters for TRRI
def setTRRI():

    #read TRRI folder location from Config file location
    global Configurations_trrifolder # Needed to modify global copy of Configurations_trrifolder
    Configurations_trrifolder = Configurations_Config.get('TRRI', 'trrifolder')
    logger.info("Configurations_trrifolder : "+ Configurations_trrifolder)

    #read cloud threshold from Config file location
    global Configurations_cloudthreshold # Needed to modify global copy of Configurations_cloudthreshold
    Configurations_cloudthreshold = Configurations_Config.get('TRRI', 'cloudthreshhold')
    logger.info("Configurations_cloudthreshold : "+ Configurations_cloudthreshold)

    #read cloud image from Config file location
    global Configurations_cloudImage # Needed to modify global copy of Configurations_cloudImage
    Configurations_cloudImage = Configurations_Config.get('TRRI', 'cloudImage')
    logger.info("Configurations_cloudImage : "+ Configurations_cloudImage)

    return ""

##Set parameters for Remove cloud
def setRemoveCloud():

    #read Cloud Free Image FileName from Config file location
    global Configurations_CloudFree_Image # Needed to modify global copy of Configurations_trrifolder
    Configurations_CloudFree_Image = Configurations_Config.get('RemoveCloud', 'CloudFree_Image')
    logger.info("Configurations_CloudFree_Image : "+ Configurations_CloudFree_Image)

    #read Maximum Search Distance from Config file location
    global Configurations_maxSearchDistance # Needed to modify global copy of Configurations_maxSearchDistance
    Configurations_maxSearchDistance = Configurations_Config.get('RemoveCloud', 'maxSearchDistance')
    logger.info("Configurations_maxSearchDistance : "+ Configurations_maxSearchDistance)

    #read Cloud Free Image FileName from Config file location
    global Configurations_nodatavalue # Needed to modify global copy of Configurations_trrifolder
    Configurations_nodatavalue = Configurations_Config.get('RemoveCloud', 'nodatavalue')
    logger.info("Configurations_nodatavalue : "+ Configurations_nodatavalue)    

    #read Radar Image FileName from Config file location
    global Configurations_radar_Image # Needed to modify global copy of Configurations_radar_Image
    Configurations_radar_Image = Configurations_Config.get('RemoveCloud', 'radar_Image')
    logger.info("Configurations_radar_Image : "+ Configurations_radar_Image)
    
    return ""
def main():
    pass

if __name__ == '__main__':
    main()
    #Call function to initialize variables for tool execution
    #configFileLocation = "/home/geonode/Documents/Python/Aster/Config.ini"
    #setParameters(configFileLocation)

    #Call function to set parameters for workspace
    #setWorkspace()

    #Call function to set parameters for radiance
    #setRadiance()

    #Call function to set parameters for reflectance
    #setReflectance()

    #Call function to set parameters for TRRI
    #setTRRI()

    #Call function to set parameters for Remove Cloud
    #setRemoveCloud()

