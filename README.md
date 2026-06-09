# Maharashtra District Level Cropping Dynamics Dashboard

[Launch Streamlit App](https://agro-insight.streamlit.app)

## Release 1.0 (2026-05-01)

**Core functionality:**
- District-wise cropping pattern analysis for Maharashtra state
- Temporal comparison between 2017-2020 and 2022-2025
- Integration of market proximity analysis

**Analysis modules included:**
1. Total Foodgrains APY Trends
2. Crops production
3. Cropping dynamics (Trend & Composition)
4. Distance to market CDF
5. Distance to market histogram
6. Hotspot color by distance
7. Density hotspot analysis
8. Land Use Transition Statistics

**Known limitations:**
- Mumbai and Mumbai Suburban excluded (no market data)
- Raw raster files not included (exceeds GitHub limits)

---

## Features & Methodology

### 1. Total Foodgrains APY Trends
This module integrates Unified Portal for Agricultural Statistics (UPAG) data to correlate satellite observations with physical yield reports. This triangulation validates observed geospatial intensification against empirical production increases.
It is open-source geospatial and statistical dashboard designed to evaluate agricultural intensity, crop production trends, and market accessibility at the district level. By correlating satellite observations with physical yield data, the platform provides actionable insights into cropping dynamics and spatial econometrics.


#### Yield Calculation Formula
$$\text{Yield} = \frac{\text{Production (Metric Tons)}}{\text{Area (Hectares)}}$$

### 2. Crop Production Analysis
This section displays crop-wise production data (quantified in lakh tonnes) across consecutive fiscal years at the district level, utilizing pre-processed data sourced from the UPAG Portal. 

* **Interactive Elements:** Users can toggle district-level data via interactive radio buttons to isolate specific crops (e.g., Tur, Moong, Urad, Wheat).
* **Analytical Purpose:** Identifies the primary crop varieties driving the district's agricultural economy and tracks output fluctuations over time.

### 3. Cropping Dynamics (Trend & Composition)
This module evaluates district-level **Agricultural Intensity** by calculating Cropping Intensity ($CI$). This metric quantifies the cultivation frequency of a single unit of land within one agricultural year.

#### Mathematical Formula for Cropping Intensity
$$CI = \frac{P_{\text{single}} + (2 \times P_{\text{double}}) + (3 \times P_{\text{triple}})}{P_{\text{total}}} \times 100$$

Where:
* $P_{\text{single}}$: Count of pixels classified as Single Kharif or Single Non-Kharif.
* $P_{\text{double}}$: Count of pixels classified as Double Cropping.
* $P_{\text{triple}}$: Count of pixels classified as Triple Cropping.
* $P_{\text{total}}$: Total count of all cropped pixels within the defined district boundary.

### 4. Distance to Market (CDF Analysis)
The Cumulative Distribution Function (CDF) plot models the spatial distribution of cropping patterns relative to Agricultural Produce Market Committee (APMC) infrastructure.

### 5. Distance to Market Histogram (Market Accessibility Profiling)
This module generates a statistical accessibility profile of the selected district by binning high-density agricultural clusters into specific distance brackets from market infrastructure.

* **Market-Led Intensification:** A left-skewed distribution indicates agricultural intensification is clustered heavily around existing infrastructure.
* **Temporal Tracking:** Longitudinal shifts in the histogram profile over successive years provide empirical evidence of structural economic and logistical shifts within the farming landscape.

### 6. Hotspots Color by Distance (Spatial Econometric Mapping)
A spatial visualization layer mapping the heterogeneity of market connectivity across district geographies. The system applies a Red-Yellow-Green choropleth gradient to hotspot centroids to isolate the distance decay effect on agricultural potential.

| Classification | Vector Layer Criteria | Economic Implication |
| :--- | :--- | :--- |
| **Dark Red Hotspots** | Top 15% pixel density; high distance to market yard | High agricultural productivity constrained by low economic connectivity. |
| **Green Clusters** | Top 15% pixel density; low distance to market yard | **Efficiency Zones** characterized by optimal infrastructural and market access. |

### 7. Density Hotspot Analysis
This component identifies geographic clusters where specific cropping types exhibit high spatial concentration.

* **Grid Specifications:** The district bounding box is tessellated into a hexagonal grid consisting of 50 hexagons across the spatial extent.
* **Relative Thresholding Method:** To maintain cross-district scalability regardless of varying geographic areas, the system employs a relative threshold rather than a fixed pixel count. Hexagons falling within the top 15% of pixel density for a given crop type are classified as active hotspots.
* **Visualization:** High-density clusters are rendered in red to illustrate spatial agglomeration patterns.

### 8. Land Use Transition Statistics (Sankey Diagram)
This module tracks longitudinal, pixel-level land cover transitions between two target periods.

* **Visualization Engine:** A Sankey Diagram maps the directional flow of land allocation.
* **Analytical Purpose:** Quantifies the conversion velocity of land moving from lower-intensity vegetative states to higher-intensity multi-cropping agricultural frameworks.

---

## Repository Structure & Replication Guide

To understand the underlying methodology or to replicate the analysis and automated figures locally, navigate to the `replicate/` directory:

* **`replicate/documentation.docx`**: Contains comprehensive project documentation, theoretical frameworks, and data schema definitions.
* **`replicate/how_it_works.docx`**: A step-by-step technical guide detailing execution requirements and instructions to replicate this project from scratch.
* **`replicate/code3_replicate.py`**: The core execution script. Run this file to ingest the pre-processed data, execute the analytical pipelines, and automatically generate the results, metrics, and plots described below.

---

## Replicating Analysis for Other States

The analytical framework developed for this dashboard is conceptually transferable to any state. However, due to variations in regional data structures and spatial infrastructure, scaling requires localized data preparation. There is no direct automated shortcut; a researcher must manually source and clean the datasets for each target state.

### Required Replication Workflow

To reproduce these analytics and visualizations for a new state, execute the following manual and programmatic steps:

1. **Sourcing Spatial Vector Layers:** * Download the official administrative boundary `.geojson` for the target state and slice/filter it down to the district level.
   * Source regional river network shapefiles/GeoJSONs and clip them to the state's geographic bounding box.

2. **Compiling Attribute Data:**
   * Extract corresponding district-level production statistics (`Area`, `Production`, `Yield`) from the UPAG Portal for the target fiscal years.
   * Compile and clean the APMC mandi location dataset. Ensure all market centroids are accurately geocoded (Latitude/Longitude).

3. **Data Cleaning & String Alignment:**
   * Manually verify that district name strings in the UPAG CSV match the district name attributes inside the `.geojson` properties exactly to prevent null values during joins.

4. **Regenerating Visualizations:**
   * Update the spatial queries and data paths within the processing pipeline (`replicate/code3_replicate.py`) to point to your new localized data vectors to calculate the new distance matrices, CDF curves, and hexagonal density hotspots.

---

## How to Run the Dashboard Locally

Since this application is built entirely on **Streamlit**, it does not require a split frontend/backend architecture (such as npm or uvicorn). The entire dashboard serves directly from the primary Python file.

### Prerequisites
Ensure you have Python 3.9+ installed along with the required spatial and web dependencies listed in `requirements.txt` (including `streamlit`, `geopandas`, `pandas`, `numpy`, and `plotly`).

### Execution Steps

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Launch the Application:**
   ```bash
   streamlit run dashboard.py
   
---

**How to Cite:**

If you use this dashboard or data in your research, please cite:

**BibTeX:**
```bibtex
@software{sanket_g_2026_20089922,
  author       = {Sanket G.},
  title        = {metalwings-design/agro-insight: Maharashtra
                   District Level Cropping Dynamics
                  },
  month        = may,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.1},
  doi          = {10.5281/zenodo.20089922},
  url          = {https://doi.org/10.5281/zenodo.20089922},
}
