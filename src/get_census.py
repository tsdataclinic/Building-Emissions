import pandas as pd
import geopandas as geopd

import censusdis
import censusdis.data as ced
import censusdis.maps as cem
from censusdis.states import STATE_MA
from collections import OrderedDict

from censusdis.maps import ShapeReader
import os
import argparse
import areal_interpolation as areal

SHAPEFILE_PATH = "data/shapefiles/cb_2020_36_tract_500k/cb_2020_36_tract_500k.shp"
OUT_DATA_FOLDER = "data/"

YEAR = 2020
DATASET = "acs/acs5"
STATE = censusdis.states.STATE_NY

CENSUS_VARS = {
    "B25014_008E" : "total_renter_units",
    "B25014_011E" : "renter_units_1_1.5_per_room",
    "B25014_012E" : "renter_units_1.5_2_per_room",
    "B25014_013E" : "renter_units_2_plus_per_room",
    "B25014_008E" : "total_renter_units",
    "B25070_007E" : "renters_30_35_pct",
    "B25070_008E" : "renters_35_40_pct",
    "B25070_009E" : "renters_40_50_pct",
    "B25070_010E" : "renters_50_plus_pct",
    "B17001_001E" : "total_population",
    "B17001_002E" : "pop_in_poverty",
    "B03002_004E" : "pop_black",
    "B03002_012E" : "pop_hispanic"
}

census_data = ced.download_detail(
            DATASET,
            YEAR,
            CENSUS_VARS,
            state=STATE,
            tract = "*")
census_data = census_data.rename(CENSUS_VARS, axis = 1)

census_data["GEOID"] = census_data["STATE"] + census_data["COUNTY"] + census_data["TRACT"]
census_data = census_data.drop(["STATE", "COUNTY", "TRACT"], axis = 1)

CDs = geopd.read_file("https://data.cityofnewyork.us/api/geospatial/yfnk-k7r4?method=export&format=GeoJSON")

census_geo = geopd.read_file(SHAPEFILE_PATH)

CD_census = areal.areal_interpolation(census_geo,
                    census_data, 
                    CDs, 
                    "boro_cd", 
                    drop_cols = ["intersection_weight"], crs = "EPSG:2263").reset_index()

CD_census["pct_overcrowding"] = (CD_census["renter_units_1_1.5_per_room"] + 
                                        CD_census["renter_units_1.5_2_per_room"] + 
                                        CD_census["renter_units_2_plus_per_room"]) / CD_census["total_renter_units"]

CD_census["pct_rent_burden"] = (CD_census["renters_30_35_pct"] + 
                                      CD_census["renters_35_40_pct"] + 
                                      CD_census["renters_40_50_pct"] + 
                                      CD_census["renters_50_plus_pct"]) / CD_census["total_renter_units"]


CD_census["pct_severe_rent_burden"] = CD_census["renters_50_plus_pct"] / CD_census["total_renter_units"]
CD_census["pct_black"] = CD_census["pop_black"] / CD_census["total_population"]
CD_census["pct_hispanic"] = CD_census["pop_hispanic"] / CD_census["total_population"]
CD_census["pct_in_poverty"] = CD_census["pop_in_poverty"] / CD_census["total_population"]

CD_census = CD_census.drop(CENSUS_VARS.values(), axis = 1)
CD_census.to_csv("data/CD_census.csv")