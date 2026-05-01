# agro-insight
Maharashtra District Level Cropping dynamics Dashboard.

## Release 1.0 (2024-05-01)

### First stable release of Maharashtra District Level Cropping Dashboard

**Core functionality:**
- District-wise cropping pattern analysis for Maharashtra state
- Temporal comparison between 2017-2020 and 2022-2025
- Integration of market proximity analysis

**Analysis modules included:**
1. Land use/cover classification
2. Cropping intensity trends
3. Crop combination and dominance patterns
4. Density hotspot detection (top 15% threshold)
5. Market distance statistics
6. Sankey transition diagrams
7. Scatter plots for intensity-distance correlation

**Technical specifications:**
- Platform: Streamlit
- Data source: ISRO Bhuvan LULC 250k
- Processing: Pixel-to-acre conversion (10m resolution)
- Output: Interactive web dashboard

**Known limitations:**
- Mumbai and Mumbai Suburban excluded (no market data)
- Raw raster files not included (exceeds GitHub limits)

**Citation:** 
Your Name (2024). Agro-Insight Dashboard v1.0. https://github.com/yourusername/agro-insight
