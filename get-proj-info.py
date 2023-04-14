import sys
from pyproj import CRS, Transformer
import json
import requests

# python3 get-proj-info.py 3857 https://epsg.io/3857.json

inCRS = CRS(sys.argv[1]) 
epsgio = sys.argv[2]

jsonurl = requests.get(epsgio).json()
print(jsonurl['bbox'])

wgs_bounds = inCRS.area_of_use.bounds
transformer = Transformer.from_crs(CRS(4326), inCRS, always_xy=True)

projected_bounds = transformer.transform_bounds(*wgs_bounds)

print(wgs_bounds)
print(projected_bounds)