
# Maharashtra Cropping Dynamics Dashboard

# : Documentation & Methodology Report

Author: Sanket Gharat, July 2026

## 1. Summary

The Maharashtra Cropping Dynamics Dashboard is a specialized geospatial analytical tool designed to monitor and visualize the structural shifts in agricultural patterns across the state of Maharashtra. By comparing a baseline period (2017-2020) with a recent period (2022-2025), the dashboard provides deep insights into how farmers are adapting to economic incentives, market proximity, and climate variability through agricultural intensification.

## 2. Data Sources and Technical Framework

The foundation of this analysis rests on high-resolution satellite imagery and government-validated datasets. The primary layers include:

- CoRE Stack Layers: Multi-temporal Land Use Land Cover classification imagery was accessed and processed using Google Earth Engine using Python. The imagery has 10-meter resolution and covers two time periods: 2017 to 2025.
- UPAG Data: Official district-level statistics for Area, Production, and Yield were programmatically fetched using Python from UPAG portal. This data v ground-reported figures for agricultural crops.
- APMC Mandi Locations: Geographic coordinates for market yards across Maharashtra were manually traced and validated using Google Earth satellite imagery. Each coordinate was cross-referenced with official APMC records to ensure reliability and accuracy of proximity analysis.

## Mode-Based Temporal Aggregation Method for Structural Change Analysis

For analyzing structural changes in cropping patterns rather than annual fluctuations, this study employs a modal aggregation technique that condenses multiple years of satellite observations into two representative time periods: Baseline Period (2017-2020) and Recent Period (2022-2025)**.**

## Technical Implementation:

**Step 1: Spatial Data Acquisition and District-Level Raster Extraction**

The spatial processing workflow involves the acquisition, preprocessing, and localized clipping of Land Use and Land Cover (LULC) data to establish consistent district-level annual raster layers for Maharashtra from the agricultural years 2017–18 through 2024–25.

**Boundary Shapefile Preprocessing**: Base administrative boundaries were acquired from the Socioeconomic Platform (). QGIS was utilized to filter and extract the Maharashtra state-level and district-level vector boundaries from the national dataset.

Due to recent administrative boundary updates, I have generated a custom shapefile for **Palghar District** to account for its bifurcation from Thane District, ensuring spatial topology alignment across all analytical layers.

**State-Level Raster Extraction**: The standardized Maharashtra state boundary was imported into the Google Earth Engine (GEE) platform as a spatial filter then Maharashtra state level GeoTIFF layers was downloaded for further analysis. Using same method, rivers GeoTIFF layer was extracted. GEE was used to query and extract the INDIASAT v3 LULC product (covering the 2017 to 2025 temporal range) and rivers, adhering to the specifications outlined in the .

**Zonal Masking and Clipping**: The downloaded state-level raster tiles were inserted back into QGIS. Using the processed district-level shapefiles as mask layers, the state rasters were clipped to individual administrative boundaries. This process executed an iterative extraction resulting in eight discrete, annual raster layers for each district within the state, formatting the data for subsequent localized spatial analysis.

**Step 2: Four-Year Stacking for Each Period**
For the baseline period, the annual rasters from 2017-18, 2018-19, and 2019-20 are stacked into a three-layer array. For the recent period, the annual rasters from 2022-23, 2023-24, and 2024-25 are stacked. The years 2020-21 and 2021-22 are excluded as transitional years to create a clearer separation between the two periods.

**Step 3: Agricultural Statistics UPAG** **data acquisition**

To complement the spatial analysis, crop production metrics are integrated into the dashboard utilizing data from the Unified Portal for Agricultural Statistics ().

**Data** **a****cquisition:** Crop-specific variables, specifically area under cultivation, total production, and yield metrics are systematically harvested from the UPAG platform. The dataset contains records for all crops cultivated across the study region.

**Dashboard** **integration****:** The tabular data is structured, cleaned, and ingested into the dashboard architecture. This tabular attribute dataset is coupled with the spatial layers to facilitate dual-axis validation and comparative analysis between satellite-derived LULC classifications and official empirical agricultural returns.

**Step 4: Pixel-Wise Mode Calculation**
For every pixel location within the district boundary, the mode (most frequently occurring value) across the three stacked layers is computed using scipy.stats.mode(). This means each pixel in the final baseline layer represents the cropping class that appeared most often during the three-year period.

**Step 5: Output Generation**
The resulting modal layers are saved as GeoTIFF files in separate folders: baseline_mode_2017_20 and recent_mode_2022_25. These two layers serve as the foundation for all spatial analyses in Sections 4 through 8 of the dashboard.

## Purpose and Justification

This modal aggregation serves three critical purposes:

Removal of Temporal Noise: Single-year anomalies caused by seasonal variability, data errors, or temporary land use changes are filtered out since a pixel must show the same class in at least two of the three years to become the mode.

Identification of Structural Change: By comparing modal layers from two distinct periods, the analysis captures genuine, sustained shifts in farmer behavior rather than year-to-year volatility. A change between periods indicates a lasting transformation in cropping intensity.

Computational Efficiency: Two representative layers replace eight annual layers, significantly reducing processing time for distance calculations, hotspot detection, and transition analysis without sacrificing analytical validity.

## Application in Dashboard Sections

| Section | How Mode Aggregation Applied |
| --- | --- |
| Section 4: CDF Plot | Distance distributions computed from modal layer pixels only |
| Section 5: Density Hotspots | Hexbin aggregation performed on modal layer pixels to identify persistent clusters |
| Section 6: Distance Histograms | Distances calculated from hotspots identified in modal layers |
| Section 7: Color by Distance | Hotspot centroids from modal layers colored by market proximity |
| Section 8: Transition Statistics | Pixel-by-pixel comparison between baseline and recent modal layers |



## 3. Methodology by Section

### Section 1: Total Foodgrains APY Trends

By integrating UPAG data, the dashboard correlates satellite observations with physical yield reports. This triangulation ensures that the observed geospatial intensification is supported by actual production increases.

**Yield Calculation:**

$$
Yield \left(\frac{Kg}{Ha}\right)= \frac{Production (In Lakh Tonnes)}{Area (In Lakh Hectares)}
$$


### 

### Section 2: Crops Production

This section presents crop wise production in lakh tones by years for each district. Data is sourced from UPAG Portal This helps identify which crops (such as Tur, Moong, Urad, or Wheat) are driving the district's agricultural economy across different years. Pre-processed UPAG data is visualized via interactive radio buttons, allowing to see which crops are driving the district's economy.

### Section 3: Cropping Dynamics (Trend & Composition)

This section evaluates the "Agricultural Intensity" of a district. Cropping Intensity is a measure of how many times a single unit of land is used for cultivation within one agricultural year.

**Mathematical Formula for Cropping Intensity (CI):**

$$
CI= \frac{[(1 \times P_single) + (2 \times P_double) + (3 \times P_triple)]}{P_total}
$$


Where:

- P_single = Count of pixels classified as Single Kharif or Single Non-Kharif.
- P_double = Count of pixels classified as Double Cropping.
- P_triple = Count of pixels classified as Triple Cropping.
- P_total = Total count of all cropped pixels in the district boundary.

****

**Section 4: Distance to Market CDF**

The Cumulative Distribution Function plot examines how cropping patterns are distributed across space relative to market infrastructure. For each cropping type, the distance from every cropping pixel to the nearest APMC market is calculated and plotted as a cumulative distribution. The x-axis represents distance to market in kilometers, while the y-axis shows the cumulative percentage of total cropped area. A curve that rises steeply near the origin indicates that most cropping activity occurs close to markets, while a flatter curve suggests crops are located farther away. This analysis helps reveal whether higher intensity cropping types like double and triple cropping tend to be located closer to markets compared to single cropping patterns.

### Section 5: Distance to Market Histogram (Market Accessibility Profiling)

This section provides a statistical "Accessibility Profile" of the district. It quantifies how many of the most productive agricultural clusters are located within specific distance brackets from market infrastructure.

A "Left-Skewed" distribution indicates a "Market-Led" intensification where farming is clustered around infrastructure. A shift in this histogram over time provides empirical evidence of structural economic shifts in the farming landscape.

### Section 6: Hotspots Color by Distance (Spatial Econometric Mapping)

This spatial visualization maps shows heterogeneity of market connectivity across the district geography. By applying a Red-Yellow-Green colors to hotspot centroids, we can physically locate where the "Distance Decay" of agricultural potential is most severe. Hexagons falling within the top 15 percent of pixel density are classified as hotspots were selected for this analysis.

Dark Red hotspots identify zones where agricultural hotspots are away from market yard because of low economic connectivity. Green clusters represent the district's "Efficiency Zones" which are closer to district markets.

**Section 7: Density Hotspot Analysis**

The density hotspot analysis identifies geographic clusters where specific cropping types are most concentrated. The district area is divided into a hexagonal grid with 50 hexagons across the district extent. For each hexagon, the number of pixels belonging to a particular cropping type is counted. Rather than using a fixed pixel threshold that would not work across districts of different sizes, the dashboard employs a relative thresholding method. Hexagons falling within the top 15 percent of pixel density are classified as hotspots. This approach ensures accurate hotspot detection regardless of district size or total agricultural area. Red areas on the map represent the highest density clusters where a particular cropping pattern dominates, helping researchers understand spatial agglomeration patterns.

### Section 8: Land Use Transition Statistics (Sankey Diagram)

The transition analysis tracks individual pixel changes between the two periods. This is visualized via a Sankey Diagram, showing the flow of land from lower-intensity uses to higher-intensity uses.

## Scaling to Other States

The present study and dashboard framework are currently designed at the district level, covering comprehensive spatial and econometric analysis for all districts within Maharashtra state. However, this localized framework possesses high scalability and can be extended into a broader state-level analysis encompassing all states across the country.

By extending the methodology to cover all states, just like the present study covers all districts from Maharashtra state, the scope of the present study will be significantly broadened. This would allow for comparative analysis between different states, providing insights into macro-economic agricultural trends, varying state-level policy impacts, and structural cropping pattern changes on a national scale. The current technical framework—utilizing Streamlit, geospatial plotting, and mode-based temporal aggregation—can naturally scale to accommodate India data sets, paving the way for a more unified national agricultural monitoring tool.


## 4. Conclusion

By quantifying the spatial relationship between market infrastructure and cropping patterns, this dashboard serves as a decision-support system for identifying where infrastructure gaps hinder agricultural potential.
