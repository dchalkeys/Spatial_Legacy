
# Author: Dylan Albrecht
# Date: 7/26/23
# Purpose: Sequentially number gravesites within each lot by decreasing latitude.

import arcpy
from arcpy import env

# Declare workspace environment
#arcpy.env.workspace = r''

# Allow overwrites
arcpy.env.overwriteOutput = True

# Set variable for Lots
#Lots = r''

# set variable for Gravesites
#Gravesites = r''

# Add field for centroid latitude
arcpy.management.CalculateGeometryAttributes('Gravesites', 'CENTROID_Y')

# Sort by descending latitude
arcpy.Sort_management('Gravesites', 'Gravesites_Sort', [['CENTROID_Y', 'DESCENDING']])

# Declare fields for Gravesites
Gravesites_fields = ['graveid' , 'CENTROID_Y']

# Declare fields for Lots
Lots_fields = ['OBJECTID']

# Convert Gravesites feature class to feature layer
arcpy.MakeFeatureLayer_management('Gravesites_Sort', 'Gravesites_layer')

# Convert Lots feature class to feature layer
arcpy.MakeFeatureLayer_management('Lots', 'Lots_layer')

# Define sequential numbering function
def autoIncrement():
            global rec
            pStart    = 1 
            pInterval = 1 
            if (rec == 0): 
                rec = pStart 
            else: 
                rec += pInterval 
            return rec

# Iterate through Lots layer selecting each
with arcpy.da.SearchCursor('Lots_layer', 'Lots_fields') as cursor1:
    for row in cursor1:
        select = "OBJECTID = {}".format(row[0])
        arcpy.management.SelectLayerByAttribute('Lots_layer', 'NEW_SELECTION', select)
        
        # Select gravesites within selected lot
        arcpy.management.SelectLayerByLocation('Gravesites_layer', 'HAVE_THEIR_CENTER_IN', 'Lots_layer','','NEW_SELECTION')
    
        # Define counter and set to 0
        rec=0
        
        # Iterate through selected gravesites applying sequential numbers in order of decreasing latitude
        cursor2 = arcpy.UpdateCursor('Gravesites_layer', Gravesites_fields)
        for row in cursor2:
            row.setValue(row[0], autoIncrement())
            cursor2.updateRow(row)

        # Clear selections
        arcpy.management.SelectLayerByAttribute('Lots_layer', 'CLEAR_SELECTION')
        arcpy.management.SelectLayerByAttribute('Gravesites_layer', 'CLEAR_SELECTION')

