
#-------------------------------------------------------------------------------
# Name:        Configurations
# Purpose:
#
# Author:      dmuthami
#
# Created:     29/09/2014
# Copyright:   (c) dmuthami 2014
# Licence:     GPL
#-------------------------------------------------------------------------------
import ConfigParser

#Import global traceback here
import traceback

import logging

#Workspace global variables
Configurations_cat_logfile = ""

#Workspace global variables
Configurations_workspace = ""

def setParameters(configFileLocation):

    #Dirty way of working with global variables
    global Configurations_Config #Set global variable.Usually not favourable in Python
    global Configurations_Sections #Set global variable.Usually not favourable in Python

    Configurations_Config = ConfigParser.ConfigParser() #instantiate ini parser object

    #Read the Config file
    Configurations_Config.read(configFileLocation)


    #Call function to set parameters for outputting to sde table
    setWorkspace()

    return ""

##Set parameters for writinng to output sde table
def setWorkspace():

    #read workspace location from Config file location
    global Configurations_workspace # Needed to modify global copy of Configurations_workspace
    Configurations_workspace = Configurations_Config.get('Workspace', 'workspace')

    return ""


def main():
    pass

if __name__ == '__main__':
    main()
    #Call function to initialize variables for tool execution
    setParameters(configFileLocation)
