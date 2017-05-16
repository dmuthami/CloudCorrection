#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maithya
#
# Created:     27/04/2017
# Copyright:   (c) Maithya 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os

def getGainAndOffset(baseName,directoryName,textSuffix):
    ##List as folllows
    ## basename
    ## directoryName
    ## fileExtension
    ## bandNumber
    ## textfile for metadata
    ## gain
    ## offset
    paramList=[]

    #Raster File Name : LC08_L1TP_166063_20170418_20170418_01_RT_B8.TIF | Directory : E:\GIS Data\DAVVOC\Maithya\Images\LC08_L1TP_166063_20170418_20170418_01_RT

    #Get file extension,
    baseNameList=  baseName.split(".")#Split by period
    fileExtension = baseNameList[int(len(baseNameList) -1)]#get file extension e.g "TXT"

    #Get band number
    band =baseName.split("_")#Split by underscore*
    s = band[int(len(band) -1)]#get last component. looks like "B8.TIF"
    band =s.split(".")#Split by period*
    s = band[0]#Get first element in the list . looks like "B8"
    bandNumber = s[1:] #get the band number

    #Construct textfile name
    directorypath = directoryName.split("\\") #Split using backslash
    commonFileName = directorypath[int(len(directorypath) -1)]#get common file name
    textfile =commonFileName + textSuffix

    #Read metadatafile and get gain and offset parameters
    if fileExtension  == "TIF"  :
        filepath = os.path.join(directoryName, textfile)
        gainAndOffset = readGainAndOffsetFromMetadataFile(filepath,bandNumber)
        if  gainAndOffset != []:
            paramList.append(baseName)
            paramList.append(directoryName)
            paramList.append(fileExtension)
            paramList.append(bandNumber)
            paramList.append(textfile)
            paramList.append(gainAndOffset[0])
            paramList.append(gainAndOffset[1])
    #
    return paramList

def readGainAndOffsetFromMetadataFile(filepath,bandNumber):
    gainAndOffset=[]
    s = ""
    paramOfInterest = ""
    multiBand = ""
    addBand = ""

    with open(filepath) as f:
        for line in f:
            s =line.rstrip().lstrip()
            param = s.split("=")

            paramOfInterest =str(param[0]).rstrip().lstrip()
            multiBand = "REFLECTANCE_MULT_BAND_"+ bandNumber
            addBand = "REFLECTANCE_ADD_BAND_"+ bandNumber

            if paramOfInterest== multiBand:
                gainAndOffset.append(param[1])
            if paramOfInterest== addBand:
                gainAndOffset.append(param[1])
            #print(s)

    return gainAndOffset

def checkIfDirectoryExists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return ""

def main():
    pass

if __name__ == '__main__':
    main()
