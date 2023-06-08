import pandas as pd
import geopandas as geopd

import censusdis
import censusdis.data as ced
import censusdis.maps as cem
from censusdis.states import STATE_MA
from collections import OrderedDict

from censusdis.maps import ShapeReader
import os
os.chdir("/content/jupyter/Building-Emissions")

YEAR = 2020
STATE = censusdis.states.STATE_NY

SHAPEFILE_ROOT = os.path.join("data/shapefiles")
if not os.path.isdir(SHAPEFILE_ROOT):
    os.mkdir(SHAPEFILE_ROOT)

reader = ShapeReader(SHAPEFILE_ROOT, YEAR)

cb_by_geo = {}
if YEAR >= 2010:
    for geo in ["tract"]:
        gdf = reader.read_cb_shapefile(STATE, geo)
        cb_by_geo[geo] = gdf