import streamlit as st
import pandas as pd
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Maharashtra Cropping Dynamics Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants & Paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PLOT_PATHS = {
    'cropping_combined': os.path.join(BASE_PATH, 'plot_1_cropping_combined'),
    'apy_trends': os.path.join(BASE_PATH, 'plot_1.1_apy'),
    'cdf_plots': os.path.join(BASE_PATH, 'plot_1.2_cdf'),
    'intensity_table': os.path.join(BASE_PATH, 'plot_3_table_intensity', 'table_intensity.xlsx'),
    'hotspot_4': os.path.join(BASE_PATH, 'plot_4_value_8'),
    'hotspot_5': os.path.join(BASE_PATH, 'plot_5_value_9'),
    'hotspot_6': os.path.join(BASE_PATH, 'plot_6_value_10'),
    'hotspot_7': os.path.join(BASE_PATH, 'plot_7_value_11'),
    'dist_cover': os.path.join(BASE_PATH, 'plot_8_dist_cover', 'district_cover.xlsx'),
    'dist_hotspot_stats': os.path.join(BASE_PATH, 'plot_9_distance_hotspot', 'distance_hotspot_modified.xlsx'),
    'dist_histo': os.path.join(BASE_PATH, 'plot_10_dist_histo'),
    'color_location': os.path.join(BASE_PATH, 'plot_11_color_by_location'),
    'scatter': os.path.join(BASE_PATH, 'plot_12_scatter'),
    'scatter_stats': os.path.join(BASE_PATH, 'plot_12_scatter_stats'),
    'sankey': os.path.join(BASE_PATH, 'plot_13_sankey'),
    'sankey_stats': os.path.join(BASE_PATH, 'plot_14_sankey_stats', 'sankey_stats.xlsx'),
}

CROPPING_OPTIONS = {
    "Single kharif": "single_kharif",
    "Single non kharif": "single_non_kharif",
    "Double cropping": "double_cropping",
    "Triple cropping": "triple_cropping"
}

# Helper to map crop keys to folder names (handles hyphen vs underscore)
def get_folder_name(crop_key):
    if crop_key == "single_non_kharif":
        return "single_non-kharif"
    return crop_key

# Helper Functions
@st.cache_data
def get_districts():
    """Dynamically populate district list based on files in data directory"""
    try:
        files = os.listdir(PLOT_PATHS['cropping_combined'])
        districts = [f.split('.')[0] for f in files if f.endswith('.jpeg')]
        return sorted(districts)
    except Exception as e:
        st.error(f"Error loading districts: {e}")
        return ["Ahilyanagar"]

@st.cache_data
def load_excel_sheet(file_path, district):
    """Load specific sheet from Excel file"""
    try:
        if os.path.exists(file_path):
            # Using sheet_name as district name.
            # Clean district name just in case
            sheet = district.strip()
            return pd.read_excel(file_path, sheet_name=sheet)
        return None
    except Exception as e:
        return None

def display_about_me():
    """Display About Me information"""
    st.info("### Project By: Sanket G.")
    st.markdown("""
    **Passionate Researcher in field of economics**
    
    Passionate about bridging the gap between raw data and actionable insights. With a strong background in analyzing complex datasets in field of economics, I focus on developing innovative, data-driven solutions to understand real-world economic challenges with keen interest in spatial econometrics.
    
    This project reflects my enthusiasm for exploring the interaction between geospatial market proximity and crop pattern change and contribution to open source project.
    
    **Connect & Explore:**  
    - Blog: [infoaccess.wordpress.com](https://infoaccess.wordpress.com)  
    - GitHub: [metalwings-design](https://github.com/metalwings-design)  
    - LinkedIn: [Sanket G.](https://www.linkedin.com)
    
    **Acknowledgment:**  
    I extend my sincere gratitude to the CoRE Stack team and Professor Aaditeshwar Seth for their invaluable mentorship and technical guidance during the development of this dashboard. Their expertise was instrumental in refining the project’s analytical framework. I am also deeply grateful to the FOSS United Foundation for their generous grant support, which has been vital in enabling this research and continues to foster the growth of open-source contributions within the Indian developer community.
    """)

# Sidebar Navigation
districts = get_districts()

# Initialize session state for district selection and view mode
if 'selected_district' not in st.session_state:
    st.session_state.selected_district = "Hingoli"
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Home"

# Sidebar
st.sidebar.title("Navigation")

# Home button in sidebar
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.view_mode = "Home"
    st.rerun()

selected_district = st.sidebar.selectbox(
    "Select District",
    districts,
    index=districts.index(st.session_state.selected_district) if st.session_state.selected_district in districts else 0
)

# Update session state and switch to analysis mode if district changes
if selected_district != st.session_state.selected_district:
    st.session_state.selected_district = selected_district
    st.session_state.view_mode = "District Analysis"
    st.rerun()

# Main Content Header with Top-Right Button
col_title, col_btn = st.columns([4, 1])

# Conditional Rendering based on view_mode
if st.session_state.view_mode == "Home":
    with col_title:
        st.title("Maharashtra District Level Cropping Dashboard")
    with col_btn:
        if st.button("👤 About Me", key="home_about", use_container_width=True):
            st.session_state.view_mode = "About Me"
            st.rerun()
            
    st.markdown("""
    Welcome,
    Maharashtra district level cropping dashboard provides comprehensive analysis of structural pattern changes across all districts, comparing two time periods: **2017-2020** & **2022-2025**.
    
    ### What this dashboard measures?
    This dashboard measures how cropping patterns have evolved over time, focusing on **4 major cropping types**: 
    - Single Kharif
    - Single Non-Kharif
    - Double Cropping
    - Triple Cropping
    
    It examines the relationship between agricultural intensity and proximity to markets, helping to understand spatial dynamics of crop choices.
    
    ### Understanding sections:
    
    1. **Cropping dynamics (Trend & Composition):** It shows overall cropping intensity change and how different cropping types are distributed across time periods.
    2. **Total Foodgrains APY Trends:** Displays three stacked line plots (Area, Production, Yield) for Total Foodgrains across the analyzed years to show district-level agricultural productivity. (source = UPAG data)
    3. **Distance to market CDF:** Displays Cumulative Distribution Function (CDF) plots for distance to market by cropping type.
    4. **Cropping intensity tables:** Detail numerical table showing contribution of cropping type in district and cropping intensity across period. It will help to understand change in cropping proportion by type across period.
    5. **Density hotspot analysis:** Plot identify area of high concentration for each cropping type. **Red areas** indicate high density cluster where particular cropping pattern is dominant. Four separate plots by cropping types are available for analysis. It also shows river and water bodies, market yard, APMC mandi across all district.
    6. **Area coverage:** table represents total pixel coverage for each cropping type. It shows structural change took place across two time period.
    7. **Distance to market histogram:** It shows distribution of distances from hotspot cluster to nearest markets. It helps to understand whether cropping intensification closer or away from market.
    8. **Hotspot color by distance:** This plot shows hotspot location representing top 15% density hotspots across two time periods. Colors represent distance to market. Green color represent hotspots are closer to market, red color represents hotspots away from market. Includes download option for hotspot distance statistics.
    9. **Scatter plot:** It examine relations between distance to market and cropping intensity.
    10. **Land Use Transition Statistics:** Interactive table and summary metrics showing land use transition between cropping types, including total area changed, stable area, and percentage change across periods based on sankey plot statistics.
    """)

elif st.session_state.view_mode == "About Me":
    with col_title:
        st.title("About the Project")
    with col_btn:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.view_mode = "Home"
            st.rerun()
    
    display_about_me()

elif st.session_state.view_mode == "District Analysis":
    with col_title:
        st.title(f"Maharashtra Cropping Dynamics: {st.session_state.selected_district}")
    with col_btn:
        if st.button("👤 About Me", key="analysis_about", use_container_width=True):
            st.session_state.view_mode = "About Me"
            st.rerun()

    def get_image_path(base_folder, district, subfolder=None):
        """Find image with any common extension"""
        extensions = ['jpeg', 'jpg', 'png']
        for ext in extensions:
            if subfolder:
                path = os.path.join(base_folder, subfolder, f"{district}.{ext}")
            else:
                path = os.path.join(base_folder, f"{district}.{ext}")
            if os.path.exists(path):
                return path
        return None

    # District Data Display
    district = st.session_state.selected_district

    st.divider()

    # 1. Cropping Dynamics (Trend & Composition)
    st.header("1. Cropping Dynamics (Trend & Composition)")
    img_combined = get_image_path(PLOT_PATHS['cropping_combined'], district)
    if img_combined:
        st.image(img_combined, caption=f"Cropping Dynamics - {district}", use_container_width=True)
    else:
        st.warning("Cropping dynamics image not found.")

    st.divider()

    # 2. Total Foodgrains: Area, Production, & Yield Trends
    st.header("2. Total Foodgrains: Area, Production, & Yield Trends")
    img_apy = get_image_path(PLOT_PATHS['apy_trends'], district)
    if img_apy:
        st.image(img_apy, caption=f"Total Foodgrains APY Trends - {district}", use_container_width=True)
    else:
        st.warning("Total Foodgrains APY Trends image not found.")

    st.divider()

    # 3. Distance to market CDF
    st.header("3. Distance to Market CDF")
    img_3 = get_image_path(PLOT_PATHS['cdf_plots'], district)
    if img_3:
        st.image(img_3, caption=f"Distance to Market CDF - {district}", use_container_width=True)
    else:
        st.warning(f"CDF plot for {district} not found.")

    st.divider()

    # 4. Cropping intensity tables (Excel)
    st.header("4. Cropping Intensity Tables")
    df_3 = load_excel_sheet(PLOT_PATHS['intensity_table'], district)
    if df_3 is not None:
        st.dataframe(df_3, hide_index=True, use_container_width=True)
    else:
        st.warning("Intensity table not found.")

    st.divider()

    # 5. Density Hotspots
    st.header("5. Density Hotspots")
    selected_4 = st.radio("Select cropping type (Hotspots):", list(CROPPING_OPTIONS.keys()), horizontal=True, key="radio_4")

    hotspot_map = {
        "Single kharif": PLOT_PATHS['hotspot_4'],
        "Single non kharif": PLOT_PATHS['hotspot_5'],
        "Double cropping": PLOT_PATHS['hotspot_6'],
        "Triple cropping": PLOT_PATHS['hotspot_7']
    }

    img_4 = get_image_path(hotspot_map[selected_4], district)
    if img_4:
        st.image(img_4, caption=f"{selected_4} Hotspots - {district}", use_container_width=True)
    else:
        st.warning(f"Hotspot image for {selected_4} not found.")

    st.divider()

    # 6. Area coverage (pixel) (Excel)
    st.header("6. Area Coverage (Pixel)")
    df_5 = load_excel_sheet(PLOT_PATHS['dist_cover'], district)
    if df_5 is not None:
        st.dataframe(df_5, hide_index=True, use_container_width=True)
    else:
        st.warning("Area coverage data not found.")

    st.divider()

    # 7. Distribution Histograms
    st.header("7. Distribution Histograms")
    selected_6 = st.radio("Select cropping type (Histograms):", list(CROPPING_OPTIONS.keys()), horizontal=True, key="radio_6")
    img_6 = get_image_path(PLOT_PATHS['dist_histo'], district, get_folder_name(CROPPING_OPTIONS[selected_6]))
    if img_6:
        st.image(img_6, use_container_width=True)
    else:
        st.warning(f"Histogram for {selected_6} not found.")

    st.divider()

    # 8. Hotspots Color by Distance
    st.header("8. Hotspots Color by Distance")
    selected_7 = st.radio("Select cropping type (Color by Location):", list(CROPPING_OPTIONS.keys()), horizontal=True, key="radio_7")
    img_7 = get_image_path(PLOT_PATHS['color_location'], district, get_folder_name(CROPPING_OPTIONS[selected_7]))
    if img_7:
        st.image(img_7, use_container_width=True)
        
        # Download District Stats from Section 5's original data
        df_stats = load_excel_sheet(PLOT_PATHS['dist_hotspot_stats'], district)
        if df_stats is not None:
            csv = df_stats.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {district} Hotspot Statistics (CSV)",
                data=csv,
                file_name=f"{district}_hotspot_distance_stats.csv",
                mime="text/csv",
                key="download_hotspot_stats"
            )
    else:
        st.warning(f"Color map for {selected_7} not found.")

    st.divider()

    # 9. Scatter Plots
    st.header("9. Scatter Plots")
    selected_8 = st.radio("Select cropping type (Scatter Plots):", list(CROPPING_OPTIONS.keys()), horizontal=True, key="radio_8")
    img_8 = get_image_path(PLOT_PATHS['scatter'], district, get_folder_name(CROPPING_OPTIONS[selected_8]))
    if img_8:
        st.image(img_8, use_container_width=True)
    else:
        st.warning(f"Scatter plot for {selected_8} not found.")

    # Market Proximity Statistical Analysis
    st.markdown("### Market Proximity Statistical Analysis")
    stats_file = os.path.join(PLOT_PATHS['scatter_stats'], f"{CROPPING_OPTIONS[selected_8]}.xlsx")
    if os.path.exists(stats_file):
        try:
            df_stats = pd.read_excel(stats_file)
            df_district_stats = df_stats[df_stats['District'] == district]
            
            if not df_district_stats.empty:
                stats_text = "═══════════════════════════════════════════════════════════\n"
                stats_text += "Statistical Significance & Trend Analysis\n"
                stats_text += "───────────────────────────────────────────────────────────\n"
                
                # Sort by period to ensure 2017-2020 comes first if possible
                df_district_stats = df_district_stats.sort_values('Period')
                
                for _, row in df_district_stats.iterrows():
                    period = row['Period']
                    p_val = row['P_value']
                    r_sq = row['R_squared']
                    slope = row['Slope']
                    
                    sig = "✓ Significant" if p_val < 0.05 else "✗ Not significant"
                    trend = "(Decreases with distance)" if slope < 0 else "(Increases with distance)"
                    
                    stats_text += f"{period}:\n"
                    stats_text += f"• P-value: {p_val:.4f} {sig}\n"
                    stats_text += f"• R-squared: {r_sq:.2f}\n"
                    stats_text += f"• Slope: {slope:.2f} {trend}\n"
                
                stats_text += "═══════════════════════════════════════════════════════════"
                st.code(stats_text, language='text')
            else:
                st.info(f"No statistical data found for {district} in this category.")
        except Exception as e:
            st.error(f"Error loading statistical data: {e}")
    else:
        st.warning("Statistical analysis files not found.")

    st.divider()

    # 10. Land Use Transition Statistics
    st.header("10. Land Use Transition Statistics")

    # Sankey Plot (HTML)
    sankey_path = os.path.join(PLOT_PATHS['sankey'], f"{district}.html")
    if os.path.exists(sankey_path):
        try:
            with open(sankey_path, 'r', encoding='utf-8') as f:
                html_data = f.read()
                st.components.v1.html(html_data, height=600, scrolling=True)
        except Exception as e:
            st.error(f"Error loading Sankey plot: {e}")
    else:
        st.warning(f"Sankey plot (HTML) for {district} not found.")

    df_9 = load_excel_sheet(PLOT_PATHS['sankey_stats'], district)

    if df_9 is not None:
        # Helper to get value for metrics safely (handles commas and % signs)
        def get_metric_value(metric_name):
            try:
                # Find row where metric contains the name
                mask = df_9['Metric'].str.contains(metric_name, case=False, na=False)
                val_raw = df_9[mask]['Value'].values
                if len(val_raw) > 0:
                    v = str(val_raw[0]).replace(',', '').replace('%', '').strip()
                    return float(v)
            except:
                pass
            return 0.0

        total_area = get_metric_value("Total Area")
        pct_changed = get_metric_value("Percentage Changed")

        # Summary Cards (Total Area and Percentage Changed only)
        c1, c2 = st.columns(2)
        c1.metric("Total Area (Acres)", f"{total_area:,.0f}")
        c2.metric("Percentage Changed (%)", f"{pct_changed:.1f}%")

        # Simple and robust table display
        st.dataframe(
            df_9,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning(f"Transition statistics for {district} not found.")
