# Building-Emissions
NYC Building Emissions Analysis

New York City has passed some of the most ambitious regulations on building-related greenhouse gas emissions in the United States. These laws include mandatory reporting standards for certain building owners, requirements to post EnergyStar scores on the outside of covered buildings, and, starting in 2024, fines for building owners that violate certain emissions thresholds. This repository contains analysis related to these policies, with a particular focus on the residential buildings and open data sets.

# Methodology

The analyses in this repository rely on several open datasets. We load each building's EnergyStar rating from a [file](https://raw.githubusercontent.com/NYCDOB/LocalLaw97/gh-pages/data/LL3320220609.json) posted on the [GitHub page](https://github.com/NYCDOB/LocalLaw97) for NYC's department of buildings. We link these records to [NYC's MapPLUTO database](https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page) to learn more about the buildings, including information about which buildings are primarily residential and basic facts about the buildings such as size and age.

We use the geographic coordinates provided by MapPLUTO to identify which of [NYC's community districts](https://data.cityofnewyork.us/City-Government/Community-Districts/yfnk-k7r4) each building falls within. Using data from the US Census's American Community Survey (accessed via the [censusdis](https://github.com/vengroff/censusdis/issues) python package), we calculate interpolated estimates of the demographics within each district. We then calculate the average score, apartment size, and building age in each community district.

With these data assets in place, the [analysis notebook](https://github.com/tsdataclinic/Building-Emissions/blob/main/notebooks/blog_figures.ipynb) calculates the tables and visualizations used in the blog post. 

# Directory Structure

    covid-energy-burden/
    ├── LICENSE
    ├── README.md                     <- The top-level README for developers using this project
    │
    ├── data                          <- Folder where the intermediate data files are stores
        ├── shapefiles                <- Folder containing census shapefiles
        ├── buildings_CD.csv          <- MapPLUTO building level data tagged with each building's community district
        ├── CD_census.csv             <- Census estimates of community district demographics
        ├── CD_building_info          <- Average EnergyStar scores, apartment size, and year build by community district
        └── cd_names.txt              <- Mapping between community district names and id number

    ├── src
        ├── areal_interpolation.py    <- Utility functions used to calculate the demographics of each community district
        ├── get_census.py             <- Script to download census data and create community district estimates
        ├── get_census_geo.py         <- Script to download required census shapefiles
        ├── Neighborhood_scores.ipynb <- Notebook to create CD_building_info.csv and buildings_CD.csv
     
    ├── notebooks
        ├── blog_figures.ipynb       <- Notebook with final data processing and figures
