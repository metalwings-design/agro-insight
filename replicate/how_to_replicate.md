# Maharashtra Cropping Dynamics Dashboard – Complete Replication Guide

Author: Sanket G.

Purpose: This document provides comprehensive, step-by-step instructions to fully replicate the Maharashtra Cropping Dynamics Dashboard—encompassing all 8 analytical sections—from raw data processing to the deployment of interactive visualizations.

## 1. System Requirements

| Component         | Minimum Specification        |
| Operating System  | Windows 10/11, macOS 11+, or Ubuntu 20.04+ |
| RAM               | 8 GB (16 GB recommended for multi-year state-level raster processing) |
| Storage           | 5 GB available disk space    |
| Python            | 3.9, 3.10, or 3.11           | 

## 2. Required Directory Architecture

Construct the exact structural hierarchy detailed below prior to downloading data layers. The core replication script **(code3_replicate.py)** must sit at the root of this structure:

project_folder/
│
├── code3_replicate.py
├── mhdata.xlsx
├── shrug updated dist mh poly/
│   └── mh_updated.shp
├── core_rivers_state/
│   └── MH_Rivers_Selection.geojson
└── lulc layers/
    ├── MH_lulc_17_18/
    ├── MH_lulc_18_19/
    ├── MH_lulc_19_20/
    ├── MH_lulc_20_21/
    ├── MH_lulc_21_22/
    ├── MH_lulc_22_23/
    ├── MH_lulc_23_24/
    └── MH_lulc_24_25/

## 3. Data Acquisition and Routing Guidelines

Download each source dataset and place them in the corresponding local directory defined in the structure above.

| Data Type | Source / Reference Link | Target Directory Path | Format |
|-----------|--------------------------|----------------------|--------|
| LULC GeoTIFFs | CoRE Stack Layer Spreadsheet | lulc layers/ (Subfolders per year) | .tif |
| District Shapefile | SHRUG Download Portal | shrug updated dist mh poly/ | .shp, .shx, .dbf, .prj |
| Rivers | CoRE Stack Layer Spreadsheet | core_rivers_state/ | .geojson |
| UPAG Statistics | Unified Portal for Agricultural Statistics | Root directory (as mhdata.xlsx) | .xlsx |
| APMC Mandi Coordinates | GitHub Repository | Root directory | .xlsx |

**Links**
LULC GeoTIFFs = https://docs.google.com/spreadsheets/d/1xS5d7vgyjyoqqnmmajKDZBx9qS6GqyAdSbNDR62ot2Y/edit?gid=0#gid=0

Rivers = https://code.earthengine.google.com/?asset=projects/ext-datasets/assets/datasets/River_pan_india

District Shapefile = https://www.devdatalab.org/shrug_download/

upag statistics = https://upag.gov.in/

APMC mandi locations= https://github.com/metalwings-design/apmc-mandi-data-maharashtra

**Note**
Acquired UPAG data and Mandi locations at Maharashtra level is gathered and avaialable in replicate folder in mhdata.xlsx file.

## 4. Dependancy

Generate a local text file named requirements.txt containing the exact library versions pinned below:

streamlit==1.35.0
pandas==2.2.2
numpy==1.26.4
geopandas==0.14.4
rasterio==1.3.10
matplotlib==3.8.4
plotly==5.22.0
scipy==1.13.0
openpyxl==3.1.2
Pillow==10.3.0
shapely==2.0.4
fiona==1.9.6
pyproj==3.6.1
xlsxwriter==3.2.0

Execute the batch installation within your terminal environment:

**pip install -r requirements.txt**

## 5. Execution Pipeline and Script Architecture

**Step 1: Spatial Data Acquisition and District-Level Raster Extraction**
The spatial processing workflow involves the acquisition, preprocessing, and localized clipping of Land Use and Land Cover (LULC) data to establish consistent district-level annual raster layers for Maharashtra from the agricultural years 2017–18 through 2024–25.

Boundary Shapefile Preprocessing: Base administrative boundaries were acquired from the Socioeconomic High-resolution Rural-Urban Geographic Platform (SHRUG). QGIS was utilized to filter and extract the Maharashtra state-level and district-level vector boundaries from the national dataset.

Areal Adjustments: Due to administrative boundary updates, a custom shapefile was generated for Palghar District to account for its bifurcation from Thane District, ensuring spatial topology alignment across all analytical layers.

State-Level Raster Extraction: The standardized Maharashtra state boundary was imported into the Google Earth Engine (GEE) platform as a spatial filter to extract and download the state-level GeoTIFF layers. GEE was used to query and extract the INDIASAT v3 LULC product (covering the 2017 to 2025 temporal range) and the corresponding rivers network layers, adhering to the specifications outlined in the CoRE Stack Layer Documentation.

Zonal Masking and Clipping: The downloaded state-level raster tiles were ingested into QGIS. Using the processed district-level shapefiles as mask layers, the state rasters were clipped to individual administrative boundaries. This process executed an iterative extraction resulting in eight discrete, annual raster layers for each district within the state, formatting the data for subsequent localized spatial analysis.

**Step 2: Temporal Stacking for Aggregated Periods**
To analyze structural shifts while minimizing annual climatic anomalies, the individual annual raster layers are aggregated into two distinct temporal blocks:

Baseline Period: The annual rasters from 2017–18, 2018–19, and 2019–20 are stacked into a multi-layer array.

Recent Period: The annual rasters from 2022–23, 2023–24, and 2024–25 are stacked into a parallel multi-layer array.

Temporal Exclusion: The intervening agricultural years 2020–21 and 2021–22 are explicitly excluded from both blocks to serve as transitional buffer years, establishing a clearer statistical separation between the baseline and recent periods.

**Step 3: Agricultural Statistics and Tabular Data Ingestion (UPAG)**
To validate the spatial analysis, empirical crop production metrics are integrated into the pipeline utilizing data from the Unified Portal for Agricultural Statistics (UPAG).

Data Acquisition: Crop-specific variables—specifically area under cultivation, total production, and yield metrics—are systematically harvested from the UPAG platform. The dataset encompasses records for all primary crops cultivated across the study region.

Dashboard Integration: The tabular data is structured, cleaned, and ingested into the dashboard architecture. This tabular attributes dataset is coupled with the spatial layers to facilitate dual-axis validation and comparative analysis between satellite-derived LULC classifications and official empirical agricultural returns.

**Step 4: Pixel-Wise Modal Filtering**
To generate a representative snapshot for each composite period, a pixel-wise aggregation is applied across the temporal stacks:

For every pixel coordinate within the district geometry, the mode (the most frequently occurring land-use classification value) across the three stacked layers is computed using scipy.stats.mode().

This mathematical aggregation ensures that each pixel in the final baseline layer represents the stable cropping class that appeared most often during the three-year period, mitigating single-year classification noise.

**Step 5: Output Layer Generation**
The final aggregated arrays are written back to disk as standardized spatial files:

The resulting modal layers are saved as GeoTIFF files in separate directories: baseline_mode_2017_20 and recent_mode_2022_25.

These two aggregated modal layers serve as the analytical baseline foundation for all spatial modules in Sections 4 through 8 of the application framework.

**6. Execution Pipeline and Script Architecture**
**Run the Data Preprocessing Engine**
Execute the root python script **code3_replicate.py** to generate output. Execute code in blocks as per sections.

**7. Web Dashboard Initialization**
run following command in terminal.

streamlit run dashboard_app.py