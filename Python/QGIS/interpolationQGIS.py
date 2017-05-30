#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      dmuthami
#
# Created:     28/05/2017
# Copyright:   (c) dmuthami 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from qgis.core import *

# supply path to qgis install location
QgsApplication.setPrefixPath(r"C:\OSGeo4W\bin", True)

# create a reference to the QgsApplication, setting the
# second argument to False disables the GUI
qgs = QgsApplication([], False)

# load providers
qgs.initQgis()

# Write your code here to load some layers, use processing algorithms, etc.

# When your script is complete, call exitQgis() to remove the provider and
# layer registries from memory
qgs.exitQgis()

def main():
    pass

if __name__ == '__main__':
    main()
