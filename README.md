# Shoreline-Stipples-For-ArcGIS-Pro

Create stipples on the outside of polygon boundaries for an old-time cartographic effect.  Stipples closer to the source polygon will be more dense and as the distance increased the stipple effect is decreased (stipple density decays with distance from polygon).

This tool accepts a polygon feature class and outputs stipples (shoreline stipples) for a user-defined range of values.  The input data must reference a Euclidean coordinate reference system (CRS) like State Plane or UTM.  The input data define the CRS for the project.  All values for the user-defined arguments will reference the CRS units of measurement.

Inputs:
in_fc = the path and file name to the polygon featureclass.
output_location = a working directory to store all temp files and the final output called stipple.tif.
stipple_cell_size = the spatial resolution of the output stipple pixel.
stipple_distance = the distance from the polygon (basically the buffer distance) at which to make stipples.
filter = an integer value used to control the amount of stippling with values from 20 - 50 as good values.

Tested on ArcGIS Pro v3.1.  The tool will work as a stand-alone in either the arcpro IDLE interpreter, your favorite interpreter, or in the ArcGIS Pro Python window.  For some reason when run in the ArcGIS Pro Python window some processing data are added to the display.  I am unsure why this would be the case since there are no setting to add data to the display but then...That's Pro!

This tool is the intellectual property of the Lummi Indian Business Council and released with an open source MIT license.
