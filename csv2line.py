#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-04 17:00:01
# @Author  : imcake (imc4k3@gmail.com)
# @Link    : https://github.com/imcake


import csv
import sys
import arcpy
from math import radians, cos, sin, asin, sqrt
from math import *

##############################################
# NEED TO KNOW
# This code illustrate change a labeled od csv
# file with od volumn, each od line has an o_label,
# a d_label and a vulumn fields.
#
# There should be a wgs84 project file(.prj file)
# in the workspace named as 'WGS1984.prj'.
#
# If need pass other labels into shapefile,
# should first add label index vabiable in the
# VABIABLES BLOCK, alse add new field as line 68,
# and add filed name when insert into new shapefile
# as in line 76. Also specify the new field value
# as line 91 and 92, and add insert vabiables in
# line 94.
##################################################

# NEED THE 3D AND SPATIAL LICENSE OF ARCGIS
csv.field_size_limit(sys.maxsize)
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")

##########################################
# NEED THE CHANGE THE VABIABLES BELOW
##########################################
path = "E:/*******"  # need to change the workspace path
lines = "test.shp"  # output shapefile name
csv_file = 'test.csv'  # input csv file name
p1_lng_index = 1
p1_lat_index = 2
p2_lng_index = 4
p2_lat_index = 5
p1_label_index = 0
p2_label_index = 3
total_index = 6
#########################################
# VABIABLES DONE
#########################################

arcpy.env.workspace = path
data_path = path
geometry_type = "POLYLINE"
has_m = "ENABLED"
has_z = "ENABLED"
spatial_ref = path + "WGS1984.prj"
arcpy.CreateFeatureclass_management(
    data_path, lines, geometry_type, "", has_m, has_z, spatial_ref)


fieldPrecision = 9
fieldPrecision2 = 2
filename = data_path + lines

arcpy.AddField_management(filename, 'o_label', "TEXT",
                          "", "", 64, "", "NULLABLE")
arcpy.AddField_management(filename, 'd_label', "TEXT",
                          "", "", 64, "", "NULLABLE")
arcpy.AddField_management(filename, 'total', "LONG",
                          fieldPrecision, "", "", "", "NULLABLE")

coordsList = []
curLine = arcpy.da.InsertCursor(
    filename, ["SHAPE@", 'o_label', 'd_label', 'total'])  # add filed if needed

with open(path + csv_file) as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        startPoint = [float(row[p1_lng_index]), float(row[p1_lat_index])]
        endPoint = [float(row[p2_lng_index]), float(row[p2_lat_index])]
        coordsList.append(startPoint)
        coordsList.append(endPoint)
        lineArray = arcpy.Array()
        lineArray.add(arcpy.Point(startPoint[0], startPoint[1]))
        lineArray.add(arcpy.Point(endPoint[0], endPoint[1]))

        o_label = row[p1_label_index]  # add more vabiables if needed
        d_label = row[p2_label_index]
        vol = int(row[total_index])
        # add filed if needed
        curLine.insertRow([arcpy.Polyline(lineArray), o_label, d_label, vol])
        coordsList = []
f.close()
