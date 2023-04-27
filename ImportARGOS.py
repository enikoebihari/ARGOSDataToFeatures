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

# Allow outputs to be overwritten
arcpy.env.overwriteOutput = True

# Set input variables (user input)
inputFolder = arcpy.GetParameterAsText(0)
outputSR = arcpy.GetParameterAsText(1)
outputFC = arcpy.GetParameterAsText(2)

# Set input variables (Hard-wired)
#inputFolder = "C:/Users/eniko/Documents/Duuuuuke/2021-22/Advanced GIS/ARGOSTracking/data/ARGOSdata"
#inputFile = 'C:\\Users\\eniko\\Documents\\Duuuuuke\\2021-22\\Advanced GIS\\ARGOSTracking\\data\\ARGOSdata\\1997dg.txt'
#outputSR = arcpy.SpatialReference(54002)
#outputFC = "C:\\Users\\eniko\\Documents\\Duuuuuke\\2021-22\\Advanced GIS\\ARGOSTracking\\scratch\\ARGOStrack.shp"

# Create a list of files from input folder
inputFiles = os.listdir(inputFolder)

# Create feature class to which we will add features
outPath, outFile = os.path.split(outputFC)
arcpy.management.CreateFeatureclass(outPath, 
                                    outFile, 
                                    "POINT", 
                                    "", 
                                    "", 
                                    "", 
                                    outputSR)

# Add TagID, LC, IQ, and Date fields to the output feature class
arcpy.management.AddField(outputFC,"TagID","LONG")
arcpy.management.AddField(outputFC,"LC","TEXT")
arcpy.management.AddField(outputFC,"Date","DATE")

# Create insert cursor
cur = arcpy.da.InsertCursor(outputFC, ["SHAPE@", "TagID", "LC", "Date"])

# Iterate through each input file
for inputFile in inputFiles:
    
    # Skip the readme file
    if inputFile == "README.txt":
        continue
    
    # Give the user a status
    arcpy.AddMessage(f"Working on file {inputFile}")
    
    # Prepend path onto input file
    inputFile = os.path.join(inputFolder, inputFile)
    
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
            # print (tagID,"Date:"+date,"Time:"+time,"Location:"+loc,"Lat:"+obsLat,"Long:"+obsLon)
            
            # Try to convert coordinates to point object
            try:
                # Convert raw coordinate strings to numbers
                if obsLat[-1] == 'N':
                    obsLat = float(obsLat[:-1])
                else:
                    obsLat = float(obsLat[:-1]) * -1
                if obsLon[-1] == 'E':
                    obsLon = float(obsLon[:-1])
                else:
                    obsLon = float(obsLon[:-1]) * -1
                
                # Create point object from lat-long coordinates
                obsPoint = arcpy.Point()
                obsPoint.X = obsLon
                obsPoint.Y = obsLat
                
                # Convert point object to a geometry object with a spatial reference
                inputSR = arcpy.SpatialReference(4326)
                obsPointGeom = arcpy.PointGeometry(obsPoint,inputSR)
                
                # Insert feature into feature class
                feature = cur.insertRow((obsPointGeom,
                                     tagID,
                                     loc,
                                     date.replace(".","/") + " " + time))
        
            # Handle any error
            except Exception as e:
                arcpy.AddWarning(f"Error adding record {tagID} to the output: {e}")
            
        # Move to the next line so the while loop progresses
        lineString = inputFileObj.readline()
        
    #Close the file object
    inputFileObj.close()
    
#Delete the cursor
del cur