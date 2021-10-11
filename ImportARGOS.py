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

#%% Construct a while loop to iterate through all lines in the datafile

# Open the ARGOS data file for reading
inputFileObj = open(inputFile,'r')

# Get the first line of data, so we can use a while loop
lineString = inputFileObj.readline()

# Start the while loop
while lineString:
    
    # Set code to run only if the line contains the string "Date: "
    if ("Date :" in lineString):
        
        # Parse the line into a list
        lineData = lineString.split()
        
        # Extract attributes from the datum header line
        tagID = lineData[0]
        date = lineData[3]
        time = lineData[4]
        loc = lineData[7]
        
        # Extract location info from the next line
        line2String = inputFileObj.readline()
        
        # Parse the line into a list
        line2Data = line2String.split()
        
        # Extract the date we need to variables
        obsLat = line2Data[2]
        obsLon= line2Data[5]
        
        # Print results to see how we're doing
        print (tagID,"Date:"+date,"Time:"+time,"Location:"+loc,"Lat:"+obsLat,"Long:"+obsLon)
        
    # Move to the next line so the while loop progresses
    lineString = inputFileObj.readline()
    
#Close the file object
inputFileObj.close()