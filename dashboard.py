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
BASE_PATH = r'C:\Users\user\Documents\freelance\core foss dashboard'
PLOT_PATHS = {
    'intensity_trend': os.path.join(BASE_PATH, 'plot_1_cropping_intensity_trend'),
    'stack_plot': os.path.join(BASE_PATH, 'plot_2_stack_plot'),
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
    'sankey': os.path.join(BASE_PATH, 'plot_13_sankey'),
    'sankey_stats': os.path.join(BASE_PATH, 'plot_14_sankey_stats', 'sankey_stats.xlsx'),
}

CROPPING_OPTIONS = {
    "Single kharif": "single_kharif",
    "Single non kharif": "single_non-kharif",
    "Double cropping": "double_cropping",
    "Triple cropping": "triple_cropping"
}

# Helper Functions
@st.cache_data
def get_districts():
    """Dynamically populate district list based on files in data directory"""
    try:
        files = os.listdir(PLOT_PATHS['intensity_trend'])
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
    
    1. **Cropping intensity trend:** It shows overall cropping intensity change over time in district.
    2. **Cropping pattern composition:** visual presentation shows how different cropping types by area are distributed across time period.
    3. **Cropping intensity tables:** Detail numerical table showing contribution of cropping type in district and cropping intensity across period. It will help to understand change in cropping proportion by type across period.
    4. **Density hotspot analysis:** Plot identify area of high concentration for each cropping type. **Red areas** indicate high density cluster where particular cropping pattern is dominant. Four separate plots by cropping types are available for analysis. It also shows river and water bodies, market yard, APMC mandi across all district.
    5. **Area coverage:** table represents total pixel coverage for each cropping type. It shows structural change took place across two time period.
    6. **Distance hotspot statistics:** This table shows the distribution of distances from hotspot cluster to nearest market. It also contains statistical data across all 4 cropping types, it shows maximum, minimum, average distance etc. across two time periods.
    7. **Distance to market histogram:** It shows distribution of distances from hotspot cluster to nearest markets. It helps to understand whether cropping intensification closer or away from market.
    8. **Hotspot color by distance:** This plot shows hotspot location representing top 15% density hotspots across two time periods. Colors represent distance to market. Green color represent hotspots are closer to market, red color represents hotspots away from market. Visualization helps to identify spatial patterns to market accessibility.
    9. **Scatter plot:** It examine relations between distance to market and cropping intensity.
    10. **Cropping pattern transition:** Sankey diagram shows interactive flow diagram, it shows how land use transition between cropping types from 2017-2020 to 2022-2025. Thicker flow represent larger area transitioning between pattern.
    11. **Sankey transition statistics:** Table presents numerical breakdown of all transition shown in Sankey diagram including top conversion pathway and percentage change.
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

    # 1. Cropping intensity trend (JPEG)
    st.header("1. Cropping Intensity Trend")
    img_1 = get_image_path(PLOT_PATHS['intensity_trend'], district)
    if img_1:
        st.image(img_1, caption=f"Cropping Intensity Trend - {district}", use_container_width=True)
    else:
        st.warning("Trend image not found.")

    st.divider()

    # 2. Cropping pattern composition (JPEG)
    st.header("2. Cropping Pattern Composition")
    img_2 = get_image_path(PLOT_PATHS['stack_plot'], district)
    if img_2:
        st.image(img_2, caption=f"Cropping Pattern Composition - {district}", use_container_width=True)
    else:
        st.warning("Composition image not found.")

    st.divider()

    # 3. Cropping intensity tables (Excel)
    st.header("3. Cropping Intensity Tables")
    df_3 = load_excel_sheet(PLOT_PATHS['intensity_table'], district)
    if df_3 is not None:
        st.dataframe(df_3, hide_index=True, use_container_width=True)
    else:
        st.warning("Intensity table not found.")

    st.divider()

    # 4. Density Hotspots
    st.header("4. Density Hotspots")
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

    # 5. Area coverage (pixel) (Excel)
    st.header("5. Area Coverage (Pixel)")
    df_5 = load_excel_sheet(PLOT_PATHS['dist_cover'], district)
    if df_5 is not None:
        st.dataframe(df_5, hide_index=True, use_container_width=True)
    else:
        st.warning("Area coverage data not found.")

    st.divider()

    # 6. Distance hotspot statistics (Excel)
    st.header("6. Distance Hotspot Statistics")
    df_6 = load_excel_sheet(PLOT_PATHS['dist_hotspot_stats'], district)
    if df_6 is not None:
        st.dataframe(df_6, hide_index=True, use_container_width=True)
    else:
        st.warning("Distance hotspot statistics not found.")

    st.divider()

    # 7. Distribution Histograms
    st.header("7. Distribution Histograms")
    selected_7 = st.radio("Select cropping type (Histograms):", list(CROPPING_OPTIONS.keys()), horizontal=True, key="radio_7")
    img_7 = get_image_path(PLOT_PATHS['dist_histo'], district, CROPPING_OPTIONS[selected_7])
    if img_7:
        st.image(img_7, use_container_width=True)
    else:
        st.warning(f"Histogram for {selected_7} not found.")

    st.divider()

    # 8. Hotspots color by distance
    st.header("8. Hotspots Color by Distance")
    selected_8 = st.radio("Select cropping type (Color by Location):", list(CROPPING_OPTIONS.keys()), horizontal=True, key="radio_8")
    img_8 = get_image_path(PLOT_PATHS['color_location'], district, CROPPING_OPTIONS[selected_8])
    if img_8:
        st.image(img_8, use_container_width=True)
    else:
        st.warning(f"Color map for {selected_8} not found.")

    st.divider()

    # 9. Scatter plots
    st.header("9. Scatter Plots")
    selected_9 = st.radio("Select cropping type (Scatter Plots):", list(CROPPING_OPTIONS.keys()), horizontal=True, key="radio_9")
    img_9 = get_image_path(PLOT_PATHS['scatter'], district, CROPPING_OPTIONS[selected_9])
    if img_9:
        st.image(img_9, use_container_width=True)
    else:
        st.warning(f"Scatter plot for {selected_9} not found.")

    st.divider()

    # 10. Sankey plot (HTML)
    st.header("10. Sankey Plot")
    sankey_file = os.path.join(PLOT_PATHS['sankey'], f"{district}.html")
    if os.path.exists(sankey_file):
        with open(sankey_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=600, scrolling=True)
    else:
        st.warning("Sankey plot HTML not found.")

    st.divider()

    # 11. Sankey stats (Excel)
    st.header("11. Sankey Statistics")

    # Load Summary Table (Metric and Value columns)
    df_11_summary = load_excel_sheet(PLOT_PATHS['sankey_stats'], district)
    if df_11_summary is not None:
        st.dataframe(df_11_summary, hide_index=True, use_container_width=True)
    else:
        st.warning(f"Sankey statistics for {district} not found.")
