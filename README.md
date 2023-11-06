# Shoreline-Stipples-For-ArcGIS-Pro

Create stipples on the outside of polygon boundaries for an old-time cartographic effect.  Stipples closer to the source polygon will be more dense and as the distance increased the stipple effect is decreased (stipple density decays with distance from polygon).

This tool accepts a polygon feature class and outputs stipples.tif (shoreline stipples) in the user directory. Stipples are created for a user-defined distance and filtered for a better cartographic effect.  The input polygon data must reference a Euclidean coordinate reference system (CRS) like State Plane or UTM.  The input data define the CRS for the project.  All values for the user-defined arguments will reference the CRS units of measurement.

The tool is currently set to overwrite outputs so either comment out that yourself or exercise caution.  Upon execution a file (stipples.tif) will be created in the working directory.




Inputs:

in_fc = the path and file name to the polygon featureclass.

output_location = a working directory to store all temp files and the final output called stipple.tif.

stipple_cell_size = the spatial resolution of the output stipple pixel.

stipple_distance = the distance from the polygon (basically the buffer distance) at which to make stipples.

filter = an integer value used to control the amount of stippling with values from 20 - 50 as good values.


Tested on ArcGIS Pro v3.1.  

This tool is the intellectual property of the Lummi Indian Business Council and released with an open source MIT license.
