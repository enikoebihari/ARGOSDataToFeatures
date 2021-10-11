# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 08:50:48 2021

@author: eb351
"""

##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2020
## Author: John.Fay@duke.edu (for ENV859)
## Student: eb351@duke.edu
##---------------------------------------------------------------------

# Import modules
import sys, os, arcpy

# Set input variables (Hard-wired)
inputFile = 'C:\\Users\\eniko\\Documents\\Duuuuuke\\2021-22\\Advanced GIS\\ARGOSTracking\\data\\ARGOSdata\\1997dg.txt'
outputFC = "C:\\Users\\eniko\\Documents\\Duuuuuke\\2021-22\\Advanced GIS\\ARGOSTracking\\scratch\\ARGOStrack.shp"