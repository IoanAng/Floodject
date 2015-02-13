#!/usr/bin/env python


import os
import sys
import subprocess
import numpy
import osgeo
from osgeo import ogr



# Linux
grass7bin_lin = 'grass70'

# add your path to grassdata (the GRASS GIS database) directory
gisbase = '/usr/lib/grass70'

gisdb = os.path.join(os.path.expanduser("~"), "grassdata")

# specify (existing) location and mapset, program has to run once to set these up
location = "WGS_1984" 
mapset   = "test"

#gisbase = 'C:\Program Files (x86)\GRASS GIS 6.4.5svn' # query GRASS 7 itself for its GISBASE
gisbase = '/usr/lib/grass70'

# Set GISBASE environment variable
os.environ['GISBASE'] = gisbase
# the following not needed with trunk
os.environ['PATH'] += os.pathsep + os.path.join(gisbase, 'extrabin')

# define GRASS-Python environment
gpydir = os.path.join(gisbase, "etc", "python")
sys.path.append(gpydir)


# Set GISDBASE environment variable
os.environ['GISDBASE'] = gisdb


def main():
	try:
		# import GRASS Python bindings (see also pygrass)
		import grass.script as gscript
		import grass.script.setup as gsetup
		import random
		from grass.script import raster as grassR
		from osgeo import ogr

		#ask for flood info
		#maxlevel_input = float(input("Please enter the maximum desired water level in meters: "))
		#interval_input = float(input("Please enter the desired flood intervals in meters: "))

		#loop_no = int(maxlevel_input/interval_input)

		#print "With the selected maximum water level of %s and flood level increment of %s, the number of loops is %s " % (maxlevel_input,  interval_input, loop_no)

		#ask for coordinates of the ocean point
		#x_ocean = float(input("Please provide with the X coordinate of the ocean point: "))
		#y_ocean = float(input("Please provide with the Y coordinate of the ocean point: "))
		
		x_ocean = -99662
		
		y_ocean = 158047
		
		create_point(x_ocean, y_ocean)

		print "You have chosen a point with the following coordinates: X %s, Y %s" % (x_ocean, y_ocean)
	
		gsetup.init(gisbase, gisdb, location, mapset)

		outputname = 'output' + str(random.randint(1,100))
		reclassoutput = 'out_recl_' + str(random.randint(1,100))
		useroutput = reclassoutput + str(random.randint(1,100)) + '.tif'
		expressionout = 'out' + str(random.randint(1,100))
			    
		gscript.run_command('r.in.gdal', flags='o', input = 'srtm_35_09.tif', output=outputname)
	
		print "Import done"
		
		gscript.run_command('g.remove', flags='f', type='vector', pattern='ocean*')
	
#		gscript.run_command('r.in.arc', input = 'DTM10_617_68.asc', output=outputname)
	
		print gscript.run_command('r.info', map=outputname)

		gscript.run_command('r.mapcalc', expression= '%s = if(%s = 162, 0, null())' % (expressionout, outputname))
		
		print "Mapcalc done"
		
		gscript.run_command('v.select', ainput='ocean_vector2', binput='ocean_point', output='selected ocean') 

		#gscript.run_command('r.out.gdal', input = expressionout , output = useroutput)
	
		gscript.run_command('r.to.vect', input = expressionout, output = 'ocean_vector2', type = 'area')
		
		print "Vector conversion done"
		
		#Run cleanup
		
		gscript.run_command('g.remove', flags='f', type = 'raster', pattern='out*')
		
		gscript.run_command('g.remove', flags='f', type = 'vector', pattern='ocean*')
	
		print "Removal done"

	except: 
		print "Something does not work"
	
def create_point(x_ocean, y_ocean):
	ocean_point = ogr.Geometry(ogr.wkbPoint)
	ocean_point.AddPoint(x_ocean, y_ocean)
	print ocean_point.ExportToWkt()
	
if __name__ == "__main__":
	main()
