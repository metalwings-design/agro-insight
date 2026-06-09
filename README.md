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
