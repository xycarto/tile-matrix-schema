import sys
import math
from pyproj import CRS, Transformer
import json
import rasterio as rio

# Script to calculate base scale for standard tiling scheme where the projection is BASED AT THE EQUATOR  
# Extent for this is derived from the projection extent.  BE CAREFUL about using the is extent.
# is is not always correct. This script can be modified to determine the base scale of other projections
# It is a work in progress. This example uses the standard webmercator projection, however, develops 
# a tile matrix schema based on an input extent. A method like this is necessary to get across the
# anti-meridian when creating a tile matrix for EPSG:3857.  Otherwise, things like COG outputs
# are cut off, so we need to tell the processing that the bounding box spans the dateline.
#
# NOTE: this is base on tile schema that grow by a factor of 2 and is centered on the equator.
# NOTE: inut file projection and requested tile projection must match!!!!
#
# TODO:
#  1. Output to JSON and XML
#  2. Make input universal
#
# Example to run:
# python3 develop-scheme-standard.py 3857 "/home/ireese/dragonfly/oceans-data/data/clipped-eez-nztm-20200116090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02_fill_cut_warp.tif"


inCRS = CRS(sys.argv[1]) # Tested using EPSG:3857 (WEBMERCATOR)
inFile = sys.argv[2]
output_json = "/home/ireese/dragonfly/oceans-data/data/quad/WebMercatorQuad-custom.json"
wgsCRS = CRS(4326)
PPI = 90.71428571428571 # Pixels per Inch
TILE_SIZE = [256, 256]
MPU = 0.0254 # Meter per Unit
MPP = 0.00028 # Meters per Pixel
WORLD_CIRCUM = 2 * math.pi * 6378137
MIN_SCALE = 0
MAX_SCALE = 24
LAT = 0

      
# Get bounds in WGS84, transform to input projection units
wgs_bounds = inCRS.area_of_use.bounds
transformer = Transformer.from_crs(wgsCRS, inCRS, always_xy=True)
in_bounds = transformer.transform_bounds(*wgs_bounds)
in_minx = in_bounds[0]
in_maxx = in_bounds[2]
in_miny = in_bounds[1]
in_maxy = in_bounds[3]

# Get bounds from input file
rio_file = rio.open(inFile)
minx = rio_file.bounds[0]
miny = rio_file.bounds[1]
maxx = rio_file.bounds[2]
maxy = rio_file.bounds[3]

# develop header for JSON Matrix file

custom_header = {
   "id": "WebMercatorQuad Custom",
   "title": "Google Maps Compatible for the World",
   "supportedCRS": "http://www.opengis.net/def/crs/EPSG/0/3857",
   "boundingBox": {
    "type": "BoundingBoxType",
    "crs": "https://www.opengis.net/def/crs/EPSG/0/3857",
    "lowerCorner": [maxx, miny],
    "upperCorner": [minx, maxy]
    },
   "orderedAxes": ["X", "Y"],
   "wellKnownScaleSet": "http://www.opengis.net/def/wkss/OGC/1.0/GoogleMapsCompatible",
   "tileMatrices": []
}
json_build = json.loads(json.dumps(custom_header, indent=4))


# Center LAT assumed to be equator
deg = math.radians(LAT)

# Calculate Scale X
# No scale factor required if center assumed to be equator
for zoom in range(MIN_SCALE, MAX_SCALE+1, 1):
    base_width = WORLD_CIRCUM
    scale_x = (
        (math.cos(deg) * (base_width) * PPI) / ((TILE_SIZE[0] * 2**zoom) * MPU)
        )
    # Calculate Reso X
    reso_x = scale_x * MPP
    
    scale_template = {
    "id": f"{zoom}",
    "scaleDenominator": scale_x,
    "cellSize": reso_x,
    "topLeftCorner": [
        minx, maxy
    ],
    "tileWidth": TILE_SIZE[0],
    "tileHeight": TILE_SIZE[1],
    "matrixWidth": 2**zoom,
    "matrixHeight": 2**zoom
    }
    
    json_build["tileMatrices"].append(scale_template)
    
json.dump(json_build, open(output_json, "w"), indent=4)

