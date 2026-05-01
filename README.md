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

**How to Cite:**

If you use this dashboard or data in your research, please cite:

**APA Style:**
Sanket G. (2026). metalwings-design/agro-insight: Maharashtra District Level Cropping Dynamics (v1.0). Zenodo. https://doi.org/10.5281/zenodo.19953413

**BibTeX:**
```bibtex
@software{sanket_g_2026_19953413,
  author       = {Sanket G.},
  title        = {metalwings-design/agro-insight: Maharashtra
                   District Level Cropping Dynamics
                  },
  month        = may,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.19953413},
  url          = {https://doi.org/10.5281/zenodo.19953413},
  swhid        = {swh:1:dir:3a3a0a729a48e91e95b06dba27628f75d9e06577
                   ;origin=https://doi.org/10.5281/zenodo.19953412;vi
                   sit=swh:1:snp:da5af0a9b99d725347e6d43240299f1635d0
                   c458;anchor=swh:1:rel:9ed15ccdb5f1595af3c7bf6abbdc
                   ec11a289ab90;path=metalwings-design-agro-
                   insight-43baf3b
                  },
}
