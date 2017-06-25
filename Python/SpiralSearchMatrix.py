#-------------------------------------------------------------------------------
# Name:        Interpolates to replace cloud pixels
# Purpose:
#
# Author:      Maithya
#
# Created:     16/05/2017
# Copyright:   (c) Maithya 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os,sys
import logging
import traceback
import numpy as np
from datetime import datetime

##Custom module containing functions
import Configurations
import WriteRaster
import Utilities

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


def makeSpiralSearchinMatrix(arrRadar,row,col,length,DN_value_optical_image,arrCloud):
    ##DNValue,Row,Col
    returnList=[0,0,0]
    try:
        threshold = length - 1;
        rowStart=row-threshold;
        if(rowStart)<0:
            rowStart = 0
        rowLength=(2 * threshold) + rowStart;

        colStart=col - threshold
        if(colStart)<0:
            colStart = 0
        colLength = (2 * threshold) + colStart;

        DN_value = 0 #Initialize variable
        breakAgain = 0 # Variable determines if there is need to break again from the outer
                        # While loop
        while (rowStart <= rowLength and  colStart <= colLength):
            try:
                #Top Boundary
                i = rowStart
                while(i<= colLength):
                    DN_value = arrRadar.item(rowStart,i)
                    #print DN_value
                    if(row != rowStart and col != i):
                        if(DN_value==DN_value_optical_image and rowStart>=0 and i>=0 ):
                            returnList[0]=DN_value
                            returnList[1]=rowStart
                            returnList[2]=i
                            if arrCloud[rowStart,i]!=1:#Check we are not replacing with another Cloud pixel
                                breakAgain =1
                                break
                    i+=1
                if (breakAgain ==1):
                    break

                #Right Boundary
                j = rowStart + 1
                while(j<= colLength):
                    DN_value = arrRadar.item(j,colLength)
                    #print DN_value
                    if( row!= j and col != colLength):
                        if(DN_value==DN_value_optical_image and j>=0 and colLength>=0):
                            returnList[0]=DN_value
                            returnList[1]=j
                            returnList[2]=colLength
                            if arrCloud[j,colLength]!=1:#Check we are not replacing with another Cloud pixel
                                breakAgain =1
                                break
                    j+=1
                if (breakAgain ==1):
                    break

                #Bottom Boundary
                if(rowStart+1 <= rowLength ):
                    k = colLength-1
                    while(k >= colStart):
                        DN_value = arrRadar.item(rowLength,k)
                        #print DN_value
                        if( row!= rowLength and col != k):
                            if(DN_value==DN_value_optical_image and rowLength>=0 and k >=0):
                                returnList[0]=DN_value
                                returnList[1]=rowLength
                                returnList[2]=k
                                if arrCloud[rowLength,k]!=1:#Check we are not replacing with another Cloud pixel
                                    breakAgain = 1
                                    break
                        k-=1

                if (breakAgain ==1):
                    break

                #Left boundary
                if(colStart+1 <= colLength ):
                    k = rowLength-1
                    while(k > rowStart):
                        DN_value = arrRadar.item(k,colStart)
                        #print DN_value
                        if( row!= k and col != colStart):
                            if(DN_value==DN_value_optical_image and k >=0 and colStart>=0):
                                returnList[0]=DN_value
                                returnList[1]=k
                                returnList[2]=colStart
                                if arrCloud[k,colStart]!=1:#Check we are not replacing with another Cloud pixel
                                    breakAgain = 1
                                    break
                        k-=1

                if (breakAgain ==1):
                    break
            except:
                ## Return any Python specific errors and any error returned
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                        str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
                ##Write to the error log file
                #logger_error.info( pymsg)
            rowStart+=1
            rowLength-=1
            colStart+=1
            colLength-=1
            breakAgain = 0 #Reset
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n Main FunctionTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)

    return returnList

def main():
    pass

if __name__ == '__main__':
    main()

    ##Call true function
    makeSpiralSearchinMatrix()
