import sys
import math
from pyproj import CRS, Transformer

# Script to calculate base scale for standard tiling scheme where the projection is BASED AT THE EQUATOR  
# Extent for this is derived from the projection extent.  BE CAREFUL about using the is extent.
# is is not always correct. This script can be modified to determine the base scale of other projections
# It is a work in progress.  
# Note: thtis is base on tile schema that grow by a factor of 2 and is centered on the equator.
#
# TODO:
#  1. Output to JSON and XML
#  2. Make input universal
#
# Example to run:
# python3 develop-scheme-standard.py 3857


inCRS = CRS(sys.argv[1]) # Tested using EPSG:3857 (WEBMERCATOR)
wgsCRS = CRS(4326)
PPI = 90.71428571428571 # Pixels per Inch
TILE_SIZE = [256, 256]
MPU = 0.0254 # Meter per Unit
MPP = 0.00028 # Meters per Pixel
WORLD_CIRCUM = 2 * math.pi * 6378137
MIN_SCALE = 0
MAX_SCALE = 24

wgs_bounds = inCRS.area_of_use.bounds
      
# Get bounds in WGS84
transformer = Transformer.from_crs(wgsCRS, inCRS, always_xy=True)
in_bounds = transformer.transform_bounds(*wgs_bounds)
in_minx = in_bounds[0]
in_maxx = in_bounds[2]
in_miny = in_bounds[1]
in_maxy = in_bounds[3]

# Center LAT assumed to be equator
deg = math.radians(0)

# Calculate Scale X
# No scale factor required if center assumed to be equator
for zoom in range(MIN_SCALE, MAX_SCALE+1, 1):
    base_width = WORLD_CIRCUM
    base_scale_x = (
        (math.cos(deg) * (base_width) * PPI) / ((TILE_SIZE[0] * 2**zoom) * MPU)
        )
    # Calculate Reso X
    base_reso_x = base_scale_x * MPP
    print(base_scale_x)
    print(base_reso_x)


