import arcpy
import os
import sys
import traceback

try:
    def set_env_settings(stipple_cell_size, in_fc):
        arcpy.AddMessage('Setting environment settings...')
        arcpy.env.overwriteOutput = True
        arcpy.CheckOutExtension('Spatial')
        out_CRS = arcpy.Describe(in_fc).spatialReference
        arcpy.env.outputCoordinateSystem = out_CRS
        arcpy.env.cellSize = str(stipple_cell_size)

    def vanity():
        arcpy.AddMessage('Running Create Shoreline Stipples...')
        arcpy.AddMessage('By Gerry Gabrisch. GISP, Lummi Nation GIS Division...')
        arcpy.AddMessage('Copright 2023 Lummin Indian Business Council - MIT Opensource License...\n')
    
    def build_bins(stipple_distance):
        arcpy.AddMessage('Creating reclass bins...')
        divider = stipple_distance/10
        counter = 10
        bin_distances = []
        while counter >=1:
            #print(stipple_distance)
            bin_distances.append(stipple_distance)
            stipple_distance = stipple_distance- divider
            counter -=1
        bin_distances.append(0)
        bin_distances.reverse()
        return bin_distances
        
    def build_reclass_string(bins):
        arcpy.AddMessage('Create reclassify bins string...')
        starter = 11
        counter = 1
        bin_string = ''
        for item in bins:
            bin_string = bin_string + str(item) + ' ' + str(bins[counter]) + ' '+ str(starter - counter) + '; '
            counter +=1
            if counter == 11:
                bin_string = bin_string[:-2]
                break        
        return bin_string
        
    def build_random_raster_extent(in_fc, stipple_distance):
        '''get the extent of the polygons you want to stipple and add the stipple distance to 
        those values to define the output area...'''
        desc = arcpy.Describe(in_fc)
        xmin = desc.extent.XMin - stipple_distance
        xmax = desc.extent.XMax + stipple_distance
        ymin = desc.extent.YMin - stipple_distance
        ymax = desc.extent.YMax + stipple_distance
        return str(xmin) +" " + str(ymin) +" " + str(xmax) +" " + str(ymax)
    
    def make_buffer(output_location, in_fc, stipple_distance):
        arcpy.AddMessage('Create clipping buffer...')
        buffer_fc = os.path.join(output_location, 'clip_buffer.shp')
        arcpy.analysis.Buffer(in_fc, buffer_fc, str(stipple_distance), "OUTSIDE_ONLY", "ROUND", "ALL", None, 'PLANAR')
        arcpy.env.extent = buffer_fc
        return buffer_fc
        
    def make_random(in_fc, stipple_distance, output_location, stipple_cell_size):
        arcpy.AddMessage('Set processing extent...')
        extent = build_random_raster_extent(in_fc, stipple_distance)
        
        arcpy.AddMessage('Create random raster...')
        #Create a random raster with values from 0 to 1 based on the user defined extent...
        #This produces a random raster with values from 0 to 1
        distribution = "UNIFORM 0.0 1.0"    
        random_ras = "randomraster.tif"
        arcpy.management.CreateRandomRaster(output_location, random_ras, distribution , extent, stipple_cell_size, "DO_NOT_BUILD")
        random_ras = os.path.join(output_location, random_ras)
        return random_ras
        
    def make_distance(in_fc, output_location):
        #create the Euclidan distance raster...
        arcpy.AddMessage('Create Euclidan distance raster...')
        out_Euclid = arcpy.sa.DistanceAccumulation(in_fc)
        out_Euclid_path = os.path.join(output_location, 'euclid_ras.tif')
        out_Euclid.save(out_Euclid_path)
        return out_Euclid_path
        
    def clip_distance(output_location, buffer_fc, out_Euclid_path):
        arcpy.AddMessage('Clip Euclidian distance raster...')
        masked_euclid = os.path.join(output_location, 'masked_euc.tif')
        masked_euc = arcpy.sa.ExtractByMask(out_Euclid_path, buffer_fc)
        masked_euc.save(masked_euclid)
        return masked_euclid
        
    def reclass_euclid(output_location, masked_euclid, bin_string):
        arcpy.AddMessage('Reclassify clipped Euclidean distance raster...')
        out_euc_reclass = arcpy.sa.Reclassify(masked_euclid, "VALUE", bin_string, "NODATA")
        out_reclass_Euclid_path = os.path.join(output_location, 'euclid_reclass.tif')
        out_euc_reclass.save(out_reclass_Euclid_path)
        return out_reclass_Euclid_path
    
    def make_stipple(output_location, out_reclass_Euclid_path, filter):
        arcpy.AddMessage('Creating stipple.tif...')
        random_ras = arcpy.sa.Raster(os.path.join(output_location, "randomraster.tif"))
        out_reclass_Euclid_path = arcpy.sa.Raster(out_reclass_Euclid_path)
        
        stipple_con = arcpy.sa.Con(random_ras <= out_reclass_Euclid_path /filter,1,)
        stipples = os.path.join(output_location, 'stipple.tif')
        stipple_con.save(stipples)        
        return stipples
    def delete_trash(buffer_fc, random_ras, masked_euclid, out_reclass_Euclid_path, out_Euclid_path):
        arcpy.AddMessage('Collecting and deleting garbage...')
        arcpy.management.Delete(buffer_fc)
        arcpy.management.Delete( random_ras)
        arcpy.management.Delete(masked_euclid)
        arcpy.management.Delete(out_reclass_Euclid_path)
        arcpy.management.Delete(out_Euclid_path)
    
    def main(in_fc, output_location, stipple_cell_size, stipple_distance, filter):
        
        vanity()
        set_env_settings(stipple_cell_size, in_fc)
        buffer_fc = make_buffer(output_location, in_fc, stipple_distance)
        random_ras = make_random(in_fc, stipple_distance, output_location, stipple_cell_size)
        out_Euclid_path = make_distance(in_fc, output_location)
        masked_euclid = clip_distance(output_location, buffer_fc, out_Euclid_path)
        bins = build_bins(stipple_distance)
        bin_string = build_reclass_string(bins)
        out_reclass_Euclid_path = reclass_euclid(output_location, masked_euclid, bin_string)
        make_stipple(output_location, out_reclass_Euclid_path, filter)
        print('Finished without error...')
        delete_trash(buffer_fc, random_ras, masked_euclid, out_reclass_Euclid_path, out_Euclid_path)
        
        
    if __name__ == "__main__":

        #this is the polygon data to stipple.  These data set the CRS and should use a Euclidean coordinate reference system.
        in_fc = arcpy.GetParameterAsText(0)
        #This is the working directory for this project.  All outputs are stored here.....
        output_location = arcpy.GetParameterAsText(1)
        #This is the raster cell output size in CRS units of measure.
        stipple_cell_size = int(arcpy.GetParameterAsText(2))
        #This is the mazimum distance to build stipples in the CRS units of measure...
        stipple_distance = int(arcpy.GetParameterAsText(3))
        #Random pixels are filtered using this value.  Values between 30 to 50 seem to work well....
        filter = int(arcpy.GetParameterAsText(4))
        
        main(in_fc, output_location, stipple_cell_size, stipple_distance, filter)
    
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1]))
