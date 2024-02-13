import sys
import math
from pyproj import CRS, Transformer

# Script to calculate base scale for snn-standard tiling scheme where the projection is NOT BASED AT THE EQUATOR, 
# but assumes the the scale growth to be the standard 2x.   
# Extent for this is derived from the projection extent.  BE CAREFUL about using the is extent.
# it is not always correct. This script can be modified to determine the base scale of other projections
# It is a work in progress.  
# Note: thtis is base on tile schema that grow by a factor of 2 and is centered on the equator.
# Note: you will need to know the ellipsode and flattening number from this. 
# 
# TODO:
#  1. Output to JSON and XML
#  2. Make input universal
#  3. Need this guide: https://nsidc.org/data/user-resources/help-center/guide-nsidcs-polar-stereographic-projection
#
# Example to run:
# python3 develop-scheme-arctic-polar-stereo.py 5041 298.2794111

inCRS = CRS(sys.argv[1]) # Tested using EPSG:2193 (WEBMERCATOR)
wgsCRS = CRS(4326)
PPI = 90.1 # Pixels per Inch
TILE_SIZE = [256, 256]
MPU = 0.0254 # Meter per Unit
MPP = 0.00028 # Meters per Pixel
WORLD_CIRCUM = 2 * math.pi * 6378137
FLATTENING = float(sys.argv[2])
MIN_SCALE = 0
MAX_SCALE = 1

wgs_bounds = inCRS.area_of_use.bounds
print(wgs_bounds)
      
# Get bounds in WGS84
transformer = Transformer.from_crs(wgsCRS, inCRS, always_xy=True)
in_bounds = transformer.transform_bounds(*wgs_bounds)
# in_minx = -14440759.350252
# in_maxx =  18440759.350252
# in_miny = -14440759.350252
# in_maxy = 18440759.350252

in_minx = in_bounds[0]
in_maxx = in_bounds[2]
in_miny = in_bounds[1]
in_maxy = in_bounds[3]
print(in_bounds)

# Center point in degrees
center_point = abs((abs(wgs_bounds[3]) + abs(wgs_bounds[1]))/2)
print(f"Center: {center_point}")

# Flattening calculation. Necessary to develop scale factor
# since we are working away from the equator
f = 1/FLATTENING
e2 = (2-f)*f
# e2 = math.sqrt((2*f - f**2))
print(e2)

# Scale Factor for true distance and is estimated as the center lat of the projection.
# The proper formula for local scale factor in ellipsoid Mercator (with true scale at equator)
# is:
#
# k = sqrt( 1 - e^2 * sin^2(phi)) / cos(phi)
#
# where e^2 is the squared eccentricity of the ellipsoid. 
# (Source: John P. Snyder, Map Projections: A Working Manual, 
# #page 44, see http://pubs.er.usgs.gov/usgspubs/pp/pp1395 ) 
# That is, e^2 = (2-f)*f, where f is the flattening. 
deg = math.radians(70)
scale_factor = math.sqrt(1 - (e2) * math.sin(deg)**2) / math.cos(deg)
print(scale_factor)
# H = ((1-e2*math.sin(deg))/(1+e2*math.sin(deg)))**(e2/2)

# t = (math.tan((math.pi/4)-(math.radians(70)/2))) / H

# trytan = math.tan((math.pi/4)-(deg/2))

# m = math.cos(deg) / (math.sqrt(1 - ((e2**2) * math.sin(deg)**2)))

# Calulate Scale X
for zoom in range(MIN_SCALE, MAX_SCALE+1, 1):
    base_width = abs((in_maxx) - (in_minx))
    # print(f"BaseWidth: {base_width}")
    # print(f"Base: {base_width}")
    
    ## CANNOT BE USED FOR POLAR!!!
    # base_scale_x = (
    #     (math.cos(deg * math.radians(math.pi/180)) * math.pi * 2 * (base_width / scale_factor) * PPI) / ((TILE_SIZE[0] * 2**zoom) * MPU)
    #     )
    base_scale_x = (
        ((base_width/ scale_factor) * PPI) / ((TILE_SIZE[0] * 2**zoom) * MPU)
        )
    # Calculate Reso X
    base_reso_x = base_scale_x * MPP
    print(f"Base Scale: {base_scale_x}")
    # print(base_reso_x)
    
    