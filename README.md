# Maharashtra District Level Cropping dynamics Dashboard.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agro-insight.streamlit.app)
## Release 1.0 (2026-05-01)

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

## 📚 How to Cite

If you use this dashboard or data in your research, please cite:

**APA Style:**
> Sanket Gharat (2026). *Maharashtra District Level Cropping Dynamics* (Version 1.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.19953413

**BibTeX:**
```bibtex
@software{agro_insight_2026,
  author = {Sanket Gharat},
  title = {Maharashtra District Level Cropping Dynamics},
  year = {2026},
  doi = {10.5281/zenodo.19953413},
  url = {https://github.com/yourusername/agro-insight},
  version = {1.0},
  license = {GPL-3.0}
}
