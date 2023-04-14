# Tile Matrix Schema

Repository to contain calculations for a determining map tile schema using custom projections.

## Definition

In short, a map tile matrix is a table of three columns: Zoom Level, Scale Denominator, and Pixel Size.  Theses are used to tell GIS editing software, web clients, and tile renderers the scale and screen pixel size for viewing inthe software.  This matrix is used to to set the framwork for when geospatial data is contained in a pyramid like strcuture e.g. XYZ or TMS.  

The Open Geospatial Consortium defines it as this:

_The OGC Tile Matrix Set standard defines the rules and requirements for a tile matrix set as a way to index space based on a set of regular grids defining a domain (tile matrix) for a limited list of scales in a Coordinate Reference System (CRS) as defined in [OGC 08-015r2] Abstract Specification Topic 2: Spatial Referencing by Coordinates. Each tile matrix is divided into regular tiles. In a tile matrix set, a tile can be univocally identified by a tile column a tile row and a tile matrix identifier. This document presents a data structure defining the properties of the tile matrix set in both UML diagrams and in tabular form._

## Standards

Open Geospatial Consortium (OGC) sets the standards for WMS, WMTS, Tile Map Schemas, etc. 

http://docs.opengeospatial.org/is/17-083r2/17-083r2.html

All attempts have been mad to stick with standard.

In addition, the method for developing "true" scales for custom projections has been brought together from the following information:

- Bing Maps (detemine scale using specific screen resolution): https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system?redirectedfrom=MSDN

- Snippet from metaCRS mailing list: https://lists.osgeo.org/pipermail/metacrs/2009-April/000253.html


## Uses

Having the ability to create our own tile matrix is of particular importance as we move into more online mapping and creating internal services like WMTS.  Having these scripts will allow us to move away from standard web mercator projections and give us the ability to use custom projections.  Some standards, like NZTM2000, are already developed, however no scemas exist for larger regions like espg:3994 which NIWA uses.  Further development of these methods allows us also to focus on more obscure regions, like the polar stereographic, which are currently unavailable in standard web mercator projections.

Map tile schemas are used in:

1. Web mapping: to detemine which scales to display on the screen
2. WMTS (REST) Services
3. Tile rendering
4. Web mapping JSON doucments

## Examples

- NZTM: https://www.linz.govt.nz/data/linz-data-service/guides-and-documentation/nztm2000-map-tile-service-schema

- WebMercator: https://www.linz.govt.nz/data/linz-data-service/guides-and-documentation/wgs-84-web-mercator-tile-scale-set-definition

## This Repo

One script is so far developed to determine the base scale for the NZTM projection.  NZTM map tile schema is well developed and we are making an attempt to recreate the method because it is a non-standard scaling matrix.

The script developed can be used to develop standard (2x) tile matricies for custom projections.

## TODO:

1. Build method for non-standard scaling like NZTM
2. Develop script for standard scaling in custom projection
3. Push results to XML and JSON document format, accoding to OGC standard