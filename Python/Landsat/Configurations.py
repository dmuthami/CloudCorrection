
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
import ConfigParser

#Import global traceback here
import traceback

import logging

#Workspace global variables
Configurations_cloudCorrection_logfile = ""
Configurations_cloudCorrection_error_logfile = ""

#Workspace global variables
Configurations_workspace = ""
Configurations_imagesfolder = ""
Configurations_excludefolder = ""

#Arguments global variables
Configurations_textfilesuffix = ""
Configurations_reflectanceprefix = ""

#Reflectance global variables
Configurations_reflectancefolder = ""

#Compute cloud global variables
Configurations_path = ""
Configurations_band2 = ""
Configurations_band3 = ""
Configurations_band4 = ""
Configurations_band5 = ""
Configurations_band6 = ""
Configurations_band7 = ""
Configurations_TRRI_Image = ""
Configurations_Cloud_Image = ""
Configurations_cloudThresholdValue = ""

#Remove cloud global variables
Configurations_TRRI2_Image = ""
Configurations_CloudFree_Image  = ""
Configurations_maxSearchDistance  = ""
Configurations_nodatavalue  = ""

def setParameters(configFileLocation):

    #Dirty way of working with global variables
    global Configurations_Config #Set global variable.Usually not favourable in Python
    global Configurations_Sections #Set global variable.Usually not favourable in Python

    Configurations_Config = ConfigParser.ConfigParser() #instantiate ini parser object

    #Read the Config file
    Configurations_Config.read(configFileLocation)


    #Call function to set parameters for workspace
    setWorkspace()

    #Call function to set parameters for images
    setArguments()

    return ""

##Set parameters for writinng to output sde table
def setWorkspace():

    #read workspace location from Config file location
    global Configurations_workspace # Needed to modify global copy of Configurations_workspace
    Configurations_workspace = Configurations_Config.get('Workspace', 'workspace')

    #read images folder from Config file location
    global Configurations_imagesfolder # Needed to modify global copy of Configurations_imagesfolder
    Configurations_imagesfolder = Configurations_Config.get('Workspace', 'imagesfolder')

    #read exclude folder from Config file location
    global Configurations_excludefolder # Needed to modify global copy of Configurations_excludefolder
    Configurations_excludefolder = Configurations_Config.get('Workspace', 'excludefolder')

    return ""

##Set parameters for writinng to output sde table
def setArguments():

    #read text file suffix from Config file location
    global Configurations_textfilesuffix # Needed to modify global copy of Configurations_textfilesuffix
    Configurations_textfilesuffix = Configurations_Config.get('Arguments', 'textfilesuffix')

    return ""

##Set parameters for Reflectance computation
def setReflectance():

    #read reflectance folder from Config file location
    global Configurations_reflectancefolder # Needed to modify global copy of Configurations_reflectancefolder
    Configurations_reflectancefolder = Configurations_Config.get('Reflectance', 'reflectancefolder')

    #read reflectance prefix from Config file location
    global Configurations_reflectanceprefix # Needed to modify global copy of Configurations_reflectanceprefix
    Configurations_reflectanceprefix = Configurations_Config.get('Reflectance', 'reflectanceprefix')
    
    return ""

##Set parameters for Compute Cloud computation
def setComputeCloud():

    #read path reflectance folder from Config file location
    global Configurations_path # Needed to modify global copy of Configurations_path
    Configurations_path = Configurations_Config.get('ComputeCloud', 'path')

    #read band 2 from Config file location
    global Configurations_band2 # Needed to modify global copy of Configurations_band2
    Configurations_band2 = Configurations_Config.get('ComputeCloud', 'band2')
                                                     
    #read band 3 from Config file location
    global Configurations_band3 # Needed to modify global copy of Configurations_band3
    Configurations_band3 = Configurations_Config.get('ComputeCloud', 'band3')
                                                                 
    #read band 2 from Config file location
    global Configurations_band4 # Needed to modify global copy of Configurations_band4
    Configurations_band4 = Configurations_Config.get('ComputeCloud', 'band4')
                                                                 
    #read band 5 from Config file location
    global Configurations_band5 # Needed to modify global copy of Configurations_band5
    Configurations_band5 = Configurations_Config.get('ComputeCloud', 'band5')
                                                                 
    #read band 6 from Config file location
    global Configurations_band6 # Needed to modify global copy of Configurations_band6
    Configurations_band6 = Configurations_Config.get('ComputeCloud', 'band6')
                                                                 
    #read band 7 from Config file location
    global Configurations_band7 # Needed to modify global copy of Configurations_band7
    Configurations_band7 = Configurations_Config.get('ComputeCloud', 'band7')

    #read TRRI Mage Path from Config file location
    global Configurations_TRRI_Image # Needed to modify global copy of Configurations_TRRI_Image
    Configurations_TRRI_Image = Configurations_Config.get('ComputeCloud', 'TRRI_Image')

    #read Cloud Mage Path from Config file location
    global Configurations_Cloud_Image # Needed to modify global copy of Configurations_Cloud_Image
    Configurations_Cloud_Image = Configurations_Config.get('ComputeCloud', 'Cloud_Image')

    #read Cloud Threshold Value Path from Config file location
    global Configurations_cloudThresholdValue # Needed to modify global copy of Configurations_cloudThresholdValue
    Configurations_cloudThresholdValue = Configurations_Config.get('ComputeCloud', 'cloudThresholdValue')
                                                                                                                 
    return ""

##Set parameters for Remove Cloud computation
def setRemoveCloud():
    
    #read TRRI2 Image from Config file location
    global Configurations_TRRI2_Image # Needed to modify global copy of Configurations_TRRI2_Image
    Configurations_TRRI2_Image = Configurations_Config.get('RemoveCloud', 'TRRI2_Image')

    #read cloud free image from Config file location
    global Configurations_CloudFree_Image # Needed to modify global copy of Configurations_reflectanceprefix
    Configurations_CloudFree_Image = Configurations_Config.get('RemoveCloud', 'CloudFree_Image')

    #read max Search Distance from Config file location
    global Configurations_maxSearchDistance # Needed to modify global copy of Configurations_maxSearchDistance
    Configurations_maxSearchDistance = Configurations_Config.get('RemoveCloud', 'maxSearchDistance')

     #read max no data value from Config file location
    global Configurations_nodatavalue # Needed to modify global copy of Configurations_maxSearchDistance
    Configurations_nodatavalue = Configurations_Config.get('RemoveCloud', 'nodatavalue')
     
    return ""
                                                                 
def main():
    pass

if __name__ == '__main__':
    main()
    #Call function to initialize variables for tool execution
    setParameters(configFileLocation)
