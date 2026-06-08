
####################################################

##  section 1 APY line plot

#####################################################


import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# --- Settings ---
FILE_PATH = 'mhdata.xlsx'
SHEET_NAME = 'upag'
OUTPUT_FOLDER = 'plot_1.1_apy'

def generate_plots():
    # 1. Load Data
    try:
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # 2. Filtering Logic
    df.columns = df.columns.str.strip()
    
    # Filter for Total Food Grains and Total season only
    crop_mask = df['Crop'].astype(str).str.strip() == 'Total Food Grains'
    season_mask = df['Season'].astype(str).str.strip() == 'Total'
    filtered_df = df[crop_mask & season_mask].copy()
    
    if filtered_df.empty:
        print("No data found for 'Total Food Grains' and Season 'Total'")
        print(f"Available crops: {df['Crop'].unique()[:10]}")
        print(f"Available seasons: {df['Season'].unique()}")
        return
    
    # 3. Prepare Directory
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    districts = filtered_df['District'].unique()
    print(f"Generating plots for {len(districts)} districts...")
    
    # 4. Plotting per District
    plt.style.use('ggplot')
    
    for district in districts:
        dist_data = filtered_df[filtered_df['District'] == district].copy()
        dist_data = dist_data.sort_values('Year')
        
        if dist_data.empty or len(dist_data) < 2:
            print(f"Skipping {district}: insufficient data")
            continue
        
        # Create figure with 3 subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
        
        # Plot 1: Area
        ax1.plot(dist_data['Year'], dist_data['Area'], marker='o', color='#2ca02c', linewidth=2, markersize=8)
        ax1.set_ylabel('Area (Hectares)', fontsize=11, fontweight='bold')
        ax1.set_title(f'{district}: Total Food Grains (2017-2025)', fontsize=14, fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels for Area (rounded to 2 decimals)
        for i, (year, area) in enumerate(zip(dist_data['Year'], dist_data['Area'])):
            ax1.annotate(f'{area:.2f}', (year, area), textcoords="offset points", 
                        xytext=(0, 10), ha='center', fontsize=8)
        
        # Plot 2: Production
        ax2.plot(dist_data['Year'], dist_data['Production'], marker='s', color='#1f77b4', linewidth=2, markersize=8)
        ax2.set_ylabel('Production (Tonnes)', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels for Production (rounded to 2 decimals)
        for i, (year, prod) in enumerate(zip(dist_data['Year'], dist_data['Production'])):
            ax2.annotate(f'{prod:.2f}', (year, prod), textcoords="offset points", 
                        xytext=(0, 10), ha='center', fontsize=8)
        
        # Plot 3: Yield
        ax3.plot(dist_data['Year'], dist_data['Yield'], marker='^', color='#ff7f0e', linewidth=2, markersize=8)
        ax3.set_ylabel('Yield (Tonnes/Hectare)', fontsize=11, fontweight='bold')
        ax3.set_xlabel('Year', fontsize=11, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Add value labels for Yield (rounded to 2 decimals)
        for i, (year, yield_val) in enumerate(zip(dist_data['Year'], dist_data['Yield'])):
            ax3.annotate(f'{yield_val:.2f}', (year, yield_val), textcoords="offset points", 
                        xytext=(0, 10), ha='center', fontsize=8)
        
        # Format x-axis
        plt.xticks(rotation=45)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot
        filename = f"{district}.jpeg".replace("/", "_")
        save_path = os.path.join(OUTPUT_FOLDER, filename)
        plt.savefig(save_path, dpi=150, bbox_inches='tight', format='jpeg')
        plt.close()
        
        print(f"✓ Saved: {filename}")

if __name__ == "__main__":
    generate_plots()




#############################################################

## SECtion 2 crop production

############################################################



import os
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Configuration
input_file = r'C:\Users\user\Documents\freelance\core foss dashboard\mhdata.xlsx'
output_dir = 'plot_15_upag_data'
os.makedirs(output_dir, exist_ok=True)

# Read data
df = pd.read_excel(input_file, sheet_name='upag')

# Filter: Season == 'Total' only
df = df[df['Season'] == 'Total']

# Exclude 'Total Food Grains' and 'Total Pulses'
exclude_crops = ['Total Food Grains', 'Total Pulses']
df = df[~df['Crop'].isin(exclude_crops)]

# Get unique years and districts
years = df['Year'].unique()
districts = df['District'].unique()

print(f"Processing {len(years)} years and {len(districts)} districts")

def wrap_label(text, max_len=20):
    """Wrap long crop names to multiple lines"""
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    
    for word in words:
        if current_len + len(word) + 1 <= max_len:
            current_line.append(word)
            current_len += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_len = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

# Process each year
for year in years:
    print(f"\nProcessing year: {year}")
    
    # Create year folder
    year_folder = os.path.join(output_dir, year)
    os.makedirs(year_folder, exist_ok=True)
    
    # Filter data for current year
    df_year = df[df['Year'] == year]
    
    # Get districts for this year
    districts_year = df_year['District'].unique()
    
    # Process each district
    for district in districts_year:
        print(f"  District: {district}")
        
        # Filter data for current district
        df_district = df_year[df_year['District'] == district]
        
        if len(df_district) == 0:
            continue
        
        # Sort by production descending
        df_district = df_district.sort_values('Production', ascending=True)
        
        # Wrap long crop names
        wrapped_crops = [wrap_label(crop, 25) for crop in df_district['Crop']]
        
        # Calculate dynamic figure height (increase for more crops)
        fig_height = max(8, len(df_district) * 0.5)
        fig, ax = plt.subplots(figsize=(12, fig_height))
        
        bars = ax.barh(range(len(df_district)), df_district['Production'], color='steelblue')
        
        # Set y-axis ticks with wrapped labels
        ax.set_yticks(range(len(df_district)))
        ax.set_yticklabels(wrapped_crops, fontsize=9)
        
        # Add value labels (inside bars if possible, else outside)
        max_prod = df_district['Production'].max()
        for i, (bar, prod) in enumerate(zip(bars, df_district['Production'])):
            if prod > 0:
                # Position label inside bar if bar is wide enough
                if prod / max_prod > 0.15:
                    x_pos = prod - (max_prod * 0.02)
                    ha = 'right'
                    color = 'white'
                else:
                    x_pos = prod + (max_prod * 0.01)
                    ha = 'left'
                    color = 'black'
                
                ax.text(x_pos, bar.get_y() + bar.get_height()/2, 
                       f'{prod:.1f}', ha=ha, va='center', fontsize=8, color=color)
        
        # Labels and title
        ax.set_xlabel('Production (Lakh Tonnes)', fontsize=11)
        ax.set_ylabel('Crop', fontsize=11)
        ax.set_title(f'{district} - {year}\nCrop-wise Production', fontsize=13, fontweight='bold')
        
        # Add grid
        ax.grid(True, axis='x', alpha=0.3)
        
        # Adjust margins to prevent cutting
        plt.subplots_adjust(left=0.3, right=0.9, bottom=0.1, top=0.95)
        
        # Save as JPEG
        save_path = os.path.join(year_folder, f"{district}.jpeg")
        plt.savefig(save_path, dpi=150, bbox_inches='tight', format='jpeg')
        plt.close()

print(f"\n✅ Complete! Plots saved to: {output_dir}")


##############################################################


## section 3 cropping dynamics [plot]

##############################################################

import os
import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.mask import mask

# 1. Configuration
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
output_dir = 'plot_1.1_cropping_combined'
os.makedirs(output_dir, exist_ok=True)

years = ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]

tif_dirs = {
    "2017-18": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_17_18',
    "2018-19": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_18_19',
    "2019-20": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_19_20',
    "2020-21": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_20_21',
    "2021-22": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_21_22',
    "2022-23": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_22_23',
    "2023-24": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_23_24',
    "2024-25": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_24_25'
}

def calculate_intensity(tif_path, gdf_boundary):
    """Calculate cropping intensity"""
    if not os.path.exists(tif_path):
        return np.nan
    with rasterio.open(tif_path) as src:
        out_image, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data = np.squeeze(out_image)
        if data.ndim > 2:
            data = data
        
        single_pixels = np.sum((data == 8) | (data == 9))
        double_pixels = np.sum(data == 10)
        triple_pixels = np.sum(data == 11)
        total_cropped_pixels = single_pixels + double_pixels + triple_pixels
        
        if total_cropped_pixels > 0:
            return (1 * single_pixels + 2 * double_pixels + 3 * triple_pixels) / total_cropped_pixels
        return np.nan

def get_pixel_counts(tif_path, gdf_boundary):
    """Get pixel counts for each cropping type"""
    if not os.path.exists(tif_path):
        return 0, 0, 0, 0
    with rasterio.open(tif_path) as src:
        out_image, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data = np.squeeze(out_image)
        if data.ndim > 2:
            data = data
        
        s = np.sum((data == 8) | (data == 9))
        d = np.sum(data == 10)
        t = np.sum(data == 11)
        total = s + d + t
        return s, d, t, total

# 2. Main Processing Loop
boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

for boundary_file in boundary_files:
    district_name = boundary_file.replace('.geojson', '')
    print(f"Processing: {district_name}")
    
    gdf_boundary = gpd.read_file(os.path.join(boundary_dir, boundary_file))
    
    # Calculate intensity values
    intensity_values = []
    for year in years:
        tif_path = os.path.join(tif_dirs[year], f"{district_name}.tif")
        intensity = calculate_intensity(tif_path, gdf_boundary)
        intensity_values.append(intensity)
    
    # Calculate pixel counts and percentages
    single_counts, double_counts, triple_counts, total_counts = [], [], [], []
    for year in years:
        tif_path = os.path.join(tif_dirs[year], f"{district_name}.tif")
        s, d, t, tot = get_pixel_counts(tif_path, gdf_boundary)
        single_counts.append(s)
        double_counts.append(d)
        triple_counts.append(t)
        total_counts.append(tot)
    
    # Calculate percentages
    single_pct = [s/t*100 if t>0 else 0 for s, t in zip(single_counts, total_counts)]
    double_pct = [d/t*100 if t>0 else 0 for d, t in zip(double_counts, total_counts)]
    triple_pct = [t/total*100 if total>0 else 0 for t, total in zip(triple_counts, total_counts)]
    
    # 3. Create Combined Plot (2 subplots: top and bottom)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # ========== TOP PLOT: Cropping Intensity Trend ==========
    ax1.plot(years, intensity_values, 'o-', color='green', linewidth=2, markersize=8)
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Cropping Intensity', fontsize=12)
    ax1.set_title(f'{district_name}: Cropping Intensity Trend (2017-2025)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(1.0, 3.5)  # Adjusted for cropping intensity range
    
    # Add value labels on points
    for i, val in enumerate(intensity_values):
        if not np.isnan(val):
            ax1.annotate(f'{val:.2f}', (years[i], val), textcoords="offset points", 
                        xytext=(0, 10), ha='center', fontsize=9)
    
    # ========== BOTTOM PLOT: Stacked Area Chart ==========
    ax2.stackplot(years, single_pct, double_pct, triple_pct, 
                  labels=['Single Cropping (Kharif+Non-Kharif)', 'Double Cropping', 'Triple Cropping'],
                  colors=['orange', 'green', 'blue'], alpha=0.7)
    
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Cropped Area (%)', fontsize=12)
    ax2.set_title(f'{district_name}: Cropping Pattern Composition (2017-2025)', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)
    
    # Rotate x-axis labels for both plots
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Save combined plot
    save_path = os.path.join(output_dir, f"{district_name}.jpeg")
    plt.savefig(save_path, format='jpeg', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {save_path}")

print(f"\n{'='*50}")
print(f"✅ Combined plots saved to: {output_dir}")
print(f"{'='*50}")

###########################################################

#  section 3      croping intensity table stas

##################################################


import os
import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
from rasterio.mask import mask

# 1. Configuration
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
output_dir = 'plot_3_table_intensity'
os.makedirs(output_dir, exist_ok=True)
excel_path = os.path.join(output_dir, 'table_intensity.xlsx')

years = ["2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
tif_dirs = {
    "2017-18": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_17_18',
    "2018-19": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_18_19',
    "2019-20": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_19_20',
    "2020-21": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_20_21',
    "2021-22": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_21_22',
    "2022-23": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_22_23',
    "2023-24": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_23_24',
    "2024-25": r'C:\Users\user\Documents\freelance\core foss dashboard\district_outputs_24_25'
}

def get_data(tif_path, gdf_boundary):
    if not os.path.exists(tif_path):
        return np.nan, 0, 0, 0, 0
    with rasterio.open(tif_path) as src:
        out_image, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data = np.squeeze(out_image)
        if data.ndim > 2:
            data = data
        
        s = np.sum((data == 8) | (data == 9))
        d = np.sum(data == 10)
        t = np.sum(data == 11)
        total = s + d + t
        
        intensity = (1 * s + 2 * d + 3 * t) / total if total > 0 else np.nan
        return intensity, s, d, t, total

# 2. Main Loop
boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

with pd.ExcelWriter(excel_path) as writer:
    for boundary_file in boundary_files:
        district_name = boundary_file.replace('.geojson', '')
        gdf_boundary = gpd.read_file(os.path.join(boundary_dir, boundary_file))
        
        rows = []
        for year in years:
            tif_path = os.path.join(tif_dirs[year], f"{district_name}.tif")
            intensity, s, d, t, total = get_data(tif_path, gdf_boundary)
            
            if total > 0:
                rows.append({
                    "Years": year,
                    "Crop intensity": round(intensity, 3),
                    "single cropping %": round((s/total)*100, 1),
                    "Double cropping %": round((d/total)*100, 1),
                    "Tripple cropping %": round((t/total)*100, 1)
                })
            else:
                rows.append({"Years": year, "Crop intensity": 0, "single cropping %": 0, "Double cropping %": 0, "Tripple cropping %": 0})
        
        # 3. Create DataFrame and write to sheet
        df = pd.DataFrame(rows)
        df.to_excel(writer, sheet_name=district_name[:31], index=False)
        print(f"Added {district_name} to excel file.")

###############################################################

##  section 4 distance to market CDF

#################################################################

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import warnings
warnings.filterwarnings('ignore')

# Configuration
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
base_baseline = r'C:\Users\user\Documents\freelance\core foss dashboard\baseline_mode_2017_20'
base_recent = r'C:\Users\user\Documents\freelance\core foss dashboard\recent_mode_2022_25'
output_dir = 'plot_1.2_cdf'
os.makedirs(output_dir, exist_ok=True)

# Load market data
df_market = pd.read_excel(r'C:\Users\user\Documents\freelance\core foss dashboard\mhdata.xlsx', sheet_name='dist_coord')

# Cropping types
cropping_types = {
    8: "Single Kharif",
    9: "Single Non-Kharif",
    10: "Double Cropping",
    11: "Triple Cropping"
}

skip_districts = ['Mumbai', 'Mumbai Suburban']

def get_distances_all_pixels(raster_path, gdf_boundary, gdf_markets, target_value):
    """Extract distances to market for ALL pixels (NO threshold)"""
    if not os.path.exists(raster_path):
        return None
    
    with rasterio.open(raster_path) as src:
        out_image, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data = np.squeeze(out_image)
        if data.ndim > 2:
            data = data[0]
        
        rows, cols = np.where(data == target_value)
        if len(rows) == 0:
            return None
        
        # Get pixel coordinates
        x, y = rasterio.transform.xy(src.transform, rows, cols)
        coords = np.column_stack((np.array(x), np.array(y)))
        
        # Get market coordinates
        market_coords = np.array(list(zip(gdf_markets.geometry.x, gdf_markets.geometry.y)))
        if len(market_coords) == 0:
            return None
        
        # Calculate distances (in meters or degrees)
        tree = cKDTree(market_coords)
        distances, _ = tree.query(coords)
        
        # Convert to km
        if src.crs.is_geographic:
            distances_km = distances * 111  # degrees to km
        else:
            distances_km = distances / 1000  # meters to km
        
        return distances_km

# Process each district
boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

for boundary_file in boundary_files:
    district_name = boundary_file.replace('.geojson', '')
    
    if district_name in skip_districts:
        continue
    
    print(f"Processing: {district_name}")
    
    gdf_boundary = gpd.read_file(os.path.join(boundary_dir, boundary_file))
    mkt = df_market[df_market['District Name'] == district_name].copy()
    
    if len(mkt) == 0:
        continue
    
    gdf_markets = gpd.GeoDataFrame(mkt, geometry=gpd.points_from_xy(mkt.longitude, mkt.latitude), crs="EPSG:4326")
    
    # Collect distances for both periods
    distances_2017 = {}
    distances_2022 = {}
    
    for val, crop_name in cropping_types.items():
        # 2017-2020
        path1 = os.path.join(base_baseline, f"{district_name}.tif")
        d1 = get_distances_all_pixels(path1, gdf_boundary, gdf_markets.to_crs('EPSG:4326'), val)
        if d1 is not None and len(d1) > 0:
            distances_2017[crop_name] = d1
        
        # 2022-2025
        path2 = os.path.join(base_recent, f"{district_name}.tif")
        d2 = get_distances_all_pixels(path2, gdf_boundary, gdf_markets.to_crs('EPSG:4326'), val)
        if d2 is not None and len(d2) > 0:
            distances_2022[crop_name] = d2
    
    # Create side-by-side CDF plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    colors = {'Single Kharif': 'orange', 'Single Non-Kharif': 'brown', 
              'Double Cropping': 'green', 'Triple Cropping': 'blue'}
    
    # Plot 2017-2020
    for crop_name, distances in distances_2017.items():
        sorted_dist = np.sort(distances)
        cdf = np.arange(1, len(sorted_dist) + 1) / len(sorted_dist)
        ax1.plot(sorted_dist, cdf, label=crop_name, color=colors.get(crop_name, 'black'), linewidth=2)
    
    ax1.set_xlabel('Distance to Market (km)', fontsize=12)
    ax1.set_ylabel('CDF', fontsize=12)
    ax1.set_title('2017-2020', fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Plot 2022-2025
    for crop_name, distances in distances_2022.items():
        sorted_dist = np.sort(distances)
        cdf = np.arange(1, len(sorted_dist) + 1) / len(sorted_dist)
        ax2.plot(sorted_dist, cdf, label=crop_name, color=colors.get(crop_name, 'black'), linewidth=2)
    
    ax2.set_xlabel('Distance to Market (km)', fontsize=12)
    ax2.set_ylabel('CDF', fontsize=12)
    ax2.set_title('2022-2025', fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1)
    
    # Main title
    fig.suptitle(f'{district_name}: Distance to Market CDF by Cropping Type', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    save_path = os.path.join(output_dir, f"{district_name}.jpeg")
    plt.savefig(save_path, dpi=150, bbox_inches='tight', format='jpeg')
    plt.close()
    print(f"  Saved: {save_path}")

print(f"\n✅ CDF plots saved to: {output_dir}")



#############################################

## section 5 distance to market histogram

##############################################



import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import warnings
warnings.filterwarnings('ignore')  # Suppress warnings

# Configuration
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
base_baseline = r'C:\Users\user\Documents\freelance\core foss dashboard\baseline_mode_2017_20'
base_recent = r'C:\Users\user\Documents\freelance\core foss dashboard\recent_mode_2022_25'
output_dir_excel = 'plot_9_distance_hotspot'
base_histo_dir = 'plot_10_dist_histo'

os.makedirs(output_dir_excel, exist_ok=True)
os.makedirs(base_histo_dir, exist_ok=True)

# Define layer mapping
layers = {
    8: "Single Kharif",
    9: "Single Non-Kharif", 
    10: "Double Cropping",
    11: "Triple Cropping"
}

# Create subfolders for each layer
for layer_name in layers.values():
    layer_folder = layer_name.lower().replace(' ', '_')
    os.makedirs(os.path.join(base_histo_dir, layer_folder), exist_ok=True)

excel_path = os.path.join(output_dir_excel, 'distance_hotspot.xlsx')

# Load market data
df_market = pd.read_excel(r'C:\Users\user\Documents\freelance\core foss dashboard\mhdata.xlsx', sheet_name='dist_coord')

def calculate_hotspot_distances(x_coords, y_coords, gdf_markets, target_crs):
    """
    Calculate distances from hotspot clusters to nearest markets
    Uses top 15% density as threshold (85th percentile)
    """
    if len(x_coords) == 0:
        return {
            'num_hotspots': 0,
            'distances_km': np.array([]),
            'min_distance': np.nan,
            'max_distance': np.nan,
            'mean_distance': np.nan,
            'median_distance': np.nan,
            'std_distance': np.nan
        }
    
    # Check if there are markets
    market_coords = np.array(list(zip(gdf_markets.geometry.x, gdf_markets.geometry.y)))
    
    if len(market_coords) == 0:
        print(f"      ⚠ No markets found in this district - skipping distance calculation")
        return {
            'num_hotspots': 0,
            'distances_km': np.array([]),
            'min_distance': np.nan,
            'max_distance': np.nan,
            'mean_distance': np.nan,
            'median_distance': np.nan,
            'std_distance': np.nan
        }
    
    # Create hexbin and get density information
    plt.figure()
    hb = plt.hexbin(x_coords, y_coords, gridsize=50, mincnt=1)
    plt.close()
    
    hexagon_counts = hb.get_array()
    hexagon_offsets = hb.get_offsets()
    
    if hexagon_counts is None or len(hexagon_counts) == 0:
        return {
            'num_hotspots': 0,
            'distances_km': np.array([]),
            'min_distance': np.nan,
            'max_distance': np.nan,
            'mean_distance': np.nan,
            'median_distance': np.nan,
            'std_distance': np.nan
        }
    
    # Use top 15% as threshold (85th percentile)
    threshold = np.percentile(hexagon_counts, 85)
    
    # Identify hotspots (hexagons above threshold)
    hotspot_mask = hexagon_counts >= threshold
    hotspot_hexagon_coords = hexagon_offsets[hotspot_mask]
    
    if len(hotspot_hexagon_coords) == 0:
        return {
            'num_hotspots': 0,
            'distances_km': np.array([]),
            'min_distance': np.nan,
            'max_distance': np.nan,
            'mean_distance': np.nan,
            'median_distance': np.nan,
            'std_distance': np.nan
        }
    
    # Calculate distances using KD-tree
    # Check for NaN or inf values before creating KD-tree
    if np.any(np.isnan(market_coords)) or np.any(np.isinf(market_coords)):
        print(f"      ⚠ Market coordinates contain NaN or inf values - skipping")
        return {
            'num_hotspots': len(hotspot_hexagon_coords),
            'distances_km': np.array([]),
            'min_distance': np.nan,
            'max_distance': np.nan,
            'mean_distance': np.nan,
            'median_distance': np.nan,
            'std_distance': np.nan
        }
    
    try:
        market_tree = cKDTree(market_coords)
        distances, indices = market_tree.query(hotspot_hexagon_coords)
        
        # Convert to kilometers
        if target_crs.is_geographic:
            # Approximate conversion for degrees to km (1 degree ≈ 111 km)
            distances_km = distances * 111
        else:
            distances_km = distances / 1000
        
        return {
            'num_hotspots': len(hotspot_hexagon_coords),
            'distances_km': distances_km,
            'min_distance': np.min(distances_km),
            'max_distance': np.max(distances_km),
            'mean_distance': np.mean(distances_km),
            'median_distance': np.median(distances_km),
            'std_distance': np.std(distances_km)
        }
    except Exception as e:
        print(f"      ⚠ Error calculating distances: {str(e)}")
        return {
            'num_hotspots': len(hotspot_hexagon_coords),
            'distances_km': np.array([]),
            'min_distance': np.nan,
            'max_distance': np.nan,
            'mean_distance': np.nan,
            'median_distance': np.nan,
            'std_distance': np.nan
        }

def extract_coordinates(raster_path, gdf_boundary, target_value):
    """Extract coordinates for pixels matching target value"""
    if not os.path.exists(raster_path):
        return np.array([]), np.array([]), None
    
    with rasterio.open(raster_path) as src:
        # Clip raster to district boundary
        out_image, out_transform = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data_2d = np.squeeze(out_image)
        
        # Handle multi-band rasters
        if data_2d.ndim > 2:
            data_2d = data_2d[0]
        
        # Find pixels matching target value
        rows, cols = np.where(data_2d == target_value)
        
        if rows.size > 0:
            x_coords, y_coords = rasterio.transform.xy(out_transform, rows, cols)
            x_coords = np.array(x_coords)
            y_coords = np.array(y_coords)
        else:
            x_coords, y_coords = np.array([]), np.array([])
        
        return x_coords, y_coords, src.crs

# Process all districts
boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    for boundary_file in boundary_files:
        district_name = boundary_file.replace('.geojson', '')
        print(f"\n{'='*60}")
        print(f"Processing district: {district_name}")
        print('='*60)
        
        # Load district boundary
        gdf_boundary = gpd.read_file(os.path.join(boundary_dir, boundary_file))
        
        # Filter markets for this district
        mkt = df_market[df_market['District Name'] == district_name].copy()
        
        if len(mkt) == 0:
            print(f"  ⚠ Warning: No market data found for {district_name} - skipping district")
            continue
        
        # Results storage for this district
        district_results = {}
        
        # Process each cropping layer
        for val, layer_name in layers.items():
            print(f"\n  📊 Processing: {layer_name}")
            
            # File paths
            baseline_path = os.path.join(base_baseline, f"{district_name}.tif")
            recent_path = os.path.join(base_recent, f"{district_name}.tif")
            
            # Extract coordinates for 2017-2020
            x_coords_2017, y_coords_2017, crs_2017 = extract_coordinates(
                baseline_path, gdf_boundary, val
            )
            print(f"    2017-2020: {len(x_coords_2017):,} pixels extracted")
            
            # Extract coordinates for 2022-2025
            x_coords_2022, y_coords_2022, crs_2022 = extract_coordinates(
                recent_path, gdf_boundary, val
            )
            print(f"    2022-2025: {len(x_coords_2022):,} pixels extracted")
            
            # Prepare markets in correct CRS
            gdf_markets = gpd.GeoDataFrame(
                mkt,
                geometry=gpd.points_from_xy(mkt.longitude, mkt.latitude),
                crs="EPSG:4326"
            )
            
            # Calculate hotspot distances for both periods
            stats_2017 = calculate_hotspot_distances(
                x_coords_2017, y_coords_2017, 
                gdf_markets.to_crs(crs_2017) if crs_2017 else gdf_markets,
                crs_2017 if crs_2017 else gdf_markets.crs
            )
            
            stats_2022 = calculate_hotspot_distances(
                x_coords_2022, y_coords_2022,
                gdf_markets.to_crs(crs_2022) if crs_2022 else gdf_markets,
                crs_2022 if crs_2022 else gdf_markets.crs
            )
            
            # Print summary
            if stats_2017['num_hotspots'] > 0:
                print(f"    2017-2020 Hotspots: {stats_2017['num_hotspots']} clusters")
                if not np.isnan(stats_2017['mean_distance']):
                    print(f"      Avg distance: {stats_2017['mean_distance']:.2f} km")
            else:
                print(f"    2017-2020: No hotspots detected")
                
            if stats_2022['num_hotspots'] > 0:
                print(f"    2022-2025 Hotspots: {stats_2022['num_hotspots']} clusters")
                if not np.isnan(stats_2022['mean_distance']):
                    print(f"      Avg distance: {stats_2022['mean_distance']:.2f} km")
            else:
                print(f"    2022-2025: No hotspots detected")
            
            # Create histogram (only if there are hotspots and distances)
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            # 2017-2020 histogram
            if stats_2017['num_hotspots'] > 0 and len(stats_2017['distances_km']) > 0:
                axes[0].hist(stats_2017['distances_km'], bins=20, color='orange', 
                            edgecolor='black', alpha=0.7)
                axes[0].axvline(stats_2017['mean_distance'], color='red', 
                               linestyle='dashed', linewidth=2, 
                               label=f"Mean: {stats_2017['mean_distance']:.1f} km")
                axes[0].set_xlabel('Distance to Market (km)')
                axes[0].set_ylabel('Frequency')
                axes[0].set_title(f'2017-2020\n(n={stats_2017["num_hotspots"]} hotspots, Top 15% density)')
                axes[0].legend()
                axes[0].grid(True, alpha=0.3)
            else:
                axes[0].text(0.5, 0.5, 'No hotspots detected', 
                           transform=axes[0].transAxes, ha='center', va='center')
                axes[0].set_title('2017-2020')
            
            # 2022-2025 histogram
            if stats_2022['num_hotspots'] > 0 and len(stats_2022['distances_km']) > 0:
                axes[1].hist(stats_2022['distances_km'], bins=20, color='green', 
                            edgecolor='black', alpha=0.7)
                axes[1].axvline(stats_2022['mean_distance'], color='red', 
                               linestyle='dashed', linewidth=2,
                               label=f"Mean: {stats_2022['mean_distance']:.1f} km")
                axes[1].set_xlabel('Distance to Market (km)')
                axes[1].set_ylabel('Frequency')
                axes[1].set_title(f'2022-2025\n(n={stats_2022["num_hotspots"]} hotspots, Top 15% density)')
                axes[1].legend()
                axes[1].grid(True, alpha=0.3)
            else:
                axes[1].text(0.5, 0.5, 'No hotspots detected', 
                           transform=axes[1].transAxes, ha='center', va='center')
                axes[1].set_title('2022-2025')
            
            plt.suptitle(f'{district_name}: {layer_name}\nHotspot Distance to Market (Top 15% Density Threshold)', 
                        fontsize=12, fontweight='bold')
            plt.tight_layout()
            
            # Save histogram
            layer_folder = layer_name.lower().replace(' ', '_')
            histo_path = os.path.join(base_histo_dir, layer_folder, f"{district_name}.png")
            plt.savefig(histo_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            # Store results for Excel
            district_results[layer_name] = {
                '2017-2020': stats_2017,
                '2022-2025': stats_2022
            }
        
        # Prepare Excel data for this district
        excel_rows = []
        for layer_name, results in district_results.items():
            # Layer header
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': '---',
                '2017-2020': '',
                '2022-2025': ''
            })
            
            # Statistics for 2017-2020
            stats_2017 = results['2017-2020']
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Number of Hotspot Clusters',
                '2017-2020': stats_2017['num_hotspots'],
                '2022-2025': ''
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Minimum Distance (km)',
                '2017-2020': round(stats_2017['min_distance'], 2) if not np.isnan(stats_2017['min_distance']) else 'N/A',
                '2022-2025': ''
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Maximum Distance (km)',
                '2017-2020': round(stats_2017['max_distance'], 2) if not np.isnan(stats_2017['max_distance']) else 'N/A',
                '2022-2025': ''
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Average Distance (km)',
                '2017-2020': round(stats_2017['mean_distance'], 2) if not np.isnan(stats_2017['mean_distance']) else 'N/A',
                '2022-2025': ''
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Std Deviation (km)',
                '2017-2020': round(stats_2017['std_distance'], 2) if not np.isnan(stats_2017['std_distance']) else 'N/A',
                '2022-2025': ''
            })
            
            # Statistics for 2022-2025
            stats_2022 = results['2022-2025']
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Number of Hotspot Clusters',
                '2017-2020': '',
                '2022-2025': stats_2022['num_hotspots']
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Minimum Distance (km)',
                '2017-2020': '',
                '2022-2025': round(stats_2022['min_distance'], 2) if not np.isnan(stats_2022['min_distance']) else 'N/A'
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Maximum Distance (km)',
                '2017-2020': '',
                '2022-2025': round(stats_2022['max_distance'], 2) if not np.isnan(stats_2022['max_distance']) else 'N/A'
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Average Distance (km)',
                '2017-2020': '',
                '2022-2025': round(stats_2022['mean_distance'], 2) if not np.isnan(stats_2022['mean_distance']) else 'N/A'
            })
            excel_rows.append({
                'Cropping Layer': layer_name,
                'Metric': 'Std Deviation (km)',
                '2017-2020': '',
                '2022-2025': round(stats_2022['std_distance'], 2) if not np.isnan(stats_2022['std_distance']) else 'N/A'
            })
            
            # Add spacer
            excel_rows.append({
                'Cropping Layer': '',
                'Metric': '',
                '2017-2020': '',
                '2022-2025': ''
            })
        
        # Write to Excel
        if excel_rows:
            df_district = pd.DataFrame(excel_rows)
            sheet_name = district_name[:31]  # Excel sheet name limit
            df_district.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"\n  ✓ Saved results for {district_name}")

print(f"\n{'='*60}")
print(f"✅ ANALYSIS COMPLETE!")
print(f"{'='*60}")
print(f"📊 Results saved to: {excel_path}")
print(f"📈 Histograms saved to: {base_histo_dir}")
print(f"{'='*60}")



###################################################

##  section 6 hotspot color by distance

###################################################


import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.lines as mlines
from scipy.spatial import cKDTree
import warnings
warnings.filterwarnings('ignore')

# Configuration (using same paths as previous code)
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
base_baseline = r'C:\Users\user\Documents\freelance\core foss dashboard\baseline_mode_2017_20'
base_recent = r'C:\Users\user\Documents\freelance\core foss dashboard\recent_mode_2022_25'
water_bodies_path = r'C:\Users\user\Documents\freelance\core foss dashboard\water_bodies.geojson'  # Update path if needed

# Output folder for color plots
output_color_dir = 'plot_11_color_by_location'
os.makedirs(output_color_dir, exist_ok=True)

# Define layers
layers = {
    8: "Single Kharif",
    9: "Single Non-Kharif",
    10: "Double Cropping",
    11: "Triple Cropping"
}

# Create subfolders for each layer
for layer_name in layers.values():
    layer_folder = layer_name.lower().replace(' ', '_')
    os.makedirs(os.path.join(output_color_dir, layer_folder), exist_ok=True)

# Load market data
df_market = pd.read_excel(r'C:\Users\user\Documents\freelance\core foss dashboard\mhdata.xlsx', sheet_name='dist_coord')

# Load water bodies (if available)
try:
    gdf_water = gpd.read_file(water_bodies_path)
    has_water = True
except:
    has_water = False
    print("Water bodies file not found - continuing without water layer")

def calculate_hotspot_stats(x_coords, y_coords, gdf_markets, target_crs):
    """Calculate hotspot clusters and distances using top 15% density threshold"""
    if len(x_coords) == 0:
        return None, None, None
    
    # Check if there are markets
    market_coords = np.array(list(zip(gdf_markets.geometry.x, gdf_markets.geometry.y)))
    if len(market_coords) == 0:
        return None, None, None
    
    # Create hexbin and get density information
    plt.figure()
    hb = plt.hexbin(x_coords, y_coords, gridsize=50, mincnt=1)
    plt.close()
    
    hexagon_counts = hb.get_array()
    hexagon_offsets = hb.get_offsets()
    
    if hexagon_counts is None or len(hexagon_counts) == 0:
        return None, None, None
    
    # Use top 15% as threshold (85th percentile)
    threshold = np.percentile(hexagon_counts, 85)
    hotspot_mask = hexagon_counts >= threshold
    hotspot_coords = hexagon_offsets[hotspot_mask]
    
    if len(hotspot_coords) == 0:
        return None, None, None
    
    # Calculate distances to markets
    try:
        market_tree = cKDTree(market_coords)
        distances, _ = market_tree.query(hotspot_coords)
        
        # Convert to kilometers
        if target_crs.is_geographic:
            distances_km = distances * 111
        else:
            distances_km = distances / 1000
        
        return hotspot_coords, distances_km, market_coords
    except:
        return None, None, None

def extract_coordinates(raster_path, gdf_boundary, target_value):
    """Extract coordinates for pixels matching target value"""
    if not os.path.exists(raster_path):
        return np.array([]), np.array([]), None
    
    with rasterio.open(raster_path) as src:
        out_image, out_transform = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data_2d = np.squeeze(out_image)
        
        if data_2d.ndim > 2:
            data_2d = data_2d[0]
        
        rows, cols = np.where(data_2d == target_value)
        
        if rows.size > 0:
            x_coords, y_coords = rasterio.transform.xy(out_transform, rows, cols)
            x_coords = np.array(x_coords)
            y_coords = np.array(y_coords)
        else:
            x_coords, y_coords = np.array([]), np.array([])
        
        return x_coords, y_coords, src.crs

def create_color_plot(district_name, layer_name, gdf_boundary, gdf_markets, 
                      stats_2017, stats_2022, market_coords_2017, market_coords_2022):
    """Create side-by-side color-coded hotspot maps for a district and layer"""
    
    # Create figure with more space for titles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Adjust spacing to prevent overlap
    plt.subplots_adjust(left=0.05, right=0.78, bottom=0.12, top=0.88, wspace=0.1)
    
    # Get geometry for plots
    gdf_boundary_proj = gdf_boundary.to_crs(gdf_boundary.crs)
    
    # Determine common color scale limits
    all_distances = []
    if stats_2017 is not None:
        _, distances_2017, _ = stats_2017
        all_distances.extend(distances_2017)
    if stats_2022 is not None:
        _, distances_2022, _ = stats_2022
        all_distances.extend(distances_2022)
    
    vmin, vmax = 0, max(all_distances) if all_distances else 50
    
    # ========== PLOT 1: 2017-2020 ==========
    if stats_2017 is not None:
        hotspot_coords_2017, distances_2017, _ = stats_2017
        scatter1 = ax1.scatter(hotspot_coords_2017[:, 0], hotspot_coords_2017[:, 1], 
                              c=distances_2017, cmap='RdYlGn_r', s=60, 
                              edgecolors='black', linewidth=0.5, zorder=4, 
                              vmin=vmin, vmax=vmax)
    else:
        scatter1 = None
        ax1.text(0.5, 0.5, 'No hotspots detected', transform=ax1.transAxes, 
                ha='center', va='center', fontsize=12)
    
    # Add markets, boundary, water
    if len(gdf_markets) > 0:
        gdf_markets_proj = gdf_markets.to_crs(gdf_boundary_proj.crs)
        gdf_markets_proj.plot(ax=ax1, color='blue', marker='P', markersize=100, 
                             label='Markets', zorder=5, edgecolor='black')
    
    gdf_boundary_proj.boundary.plot(ax=ax1, color='black', linewidth=1.8, zorder=3)
    
    if has_water:
        gdf_water_proj = gdf_water.to_crs(gdf_boundary_proj.crs)
        gdf_water_proj.plot(ax=ax1, color='deepskyblue', linewidth=0.8, alpha=0.6, zorder=2)
    
    ax1.set_title('2017-2020', fontsize=13, fontweight='bold', pad=10)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_facecolor('white')
    ax1.set_aspect('equal')
    
    # ========== PLOT 2: 2022-2025 ==========
    if stats_2022 is not None:
        hotspot_coords_2022, distances_2022, _ = stats_2022
        scatter2 = ax2.scatter(hotspot_coords_2022[:, 0], hotspot_coords_2022[:, 1], 
                              c=distances_2022, cmap='RdYlGn_r', s=60, 
                              edgecolors='black', linewidth=0.5, zorder=4, 
                              vmin=vmin, vmax=vmax)
    else:
        scatter2 = None
        ax2.text(0.5, 0.5, 'No hotspots detected', transform=ax2.transAxes, 
                ha='center', va='center', fontsize=12)
    
    # Add markets, boundary, water
    if len(gdf_markets) > 0:
        gdf_markets_proj.plot(ax=ax2, color='blue', marker='P', markersize=100, 
                             label='Markets', zorder=5, edgecolor='black')
    
    gdf_boundary_proj.boundary.plot(ax=ax2, color='black', linewidth=1.8, zorder=3)
    
    if has_water:
        gdf_water_proj.plot(ax=ax2, color='deepskyblue', linewidth=0.8, alpha=0.6, zorder=2)
    
    ax2.set_title('2022-2025', fontsize=13, fontweight='bold', pad=10)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_facecolor('white')
    ax2.set_aspect('equal')
    
    # Add colorbar (use first scatter if available)
    if scatter1 is not None:
        cbar_ax = fig.add_axes([0.80, 0.15, 0.02, 0.7])  # Adjusted position
        cbar = fig.colorbar(scatter1, cax=cbar_ax)
        cbar.set_label('Distance to Nearest Market (km)', fontsize=11)
    
    # Add legend below plots
    legend_elements = [
        Patch(facecolor='deepskyblue', alpha=0.6, label='Rivers/Water Bodies'),
        mlines.Line2D([], [], color='blue', marker='P', linestyle='None', markersize=8, label='District Market'),
        mlines.Line2D([], [], color='black', linewidth=1.5, label='District Boundary')
    ]
    
    if has_water:
        fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.02), 
                  frameon=True, fontsize=9, title='Legend', title_fontsize=10, ncol=3)
    else:
        legend_elements_no_water = legend_elements[1:]  # Remove water if not available
        fig.legend(handles=legend_elements_no_water, loc='lower center', bbox_to_anchor=(0.5, 0.02), 
                  frameon=True, fontsize=9, title='Legend', title_fontsize=10, ncol=2)
    
    # Main title with adjusted position
    fig.suptitle(f'{district_name}: {layer_name}\nHotspot Clusters Colored by Distance to Market (Top 15% Density)', 
                fontsize=14, fontweight='bold', y=0.95)
    
    # Save plot with tight layout
    layer_folder = layer_name.lower().replace(' ', '_')
    output_path = os.path.join(output_color_dir, layer_folder, f"{district_name}.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"      ✓ Saved color map: {output_path}")

# Process all districts
boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

# Skip districts with no markets
skip_districts = ['Mumbai', 'Mumbai Suburban']

for boundary_file in boundary_files:
    district_name = boundary_file.replace('.geojson', '')
    
    # Skip Mumbai districts
    if district_name in skip_districts:
        print(f"\n⏭ Skipping {district_name} (no market data)")
        continue
    
    print(f"\n{'='*60}")
    print(f"Processing district: {district_name}")
    print('='*60)
    
    # Load district boundary
    gdf_boundary = gpd.read_file(os.path.join(boundary_dir, boundary_file))
    
    # Filter markets for this district
    mkt = df_market[df_market['District Name'] == district_name].copy()
    
    if len(mkt) == 0:
        print(f"  ⚠ No market data found for {district_name} - skipping")
        continue
    
    # Prepare markets GeoDataFrame
    gdf_markets = gpd.GeoDataFrame(
        mkt,
        geometry=gpd.points_from_xy(mkt.longitude, mkt.latitude),
        crs="EPSG:4326"
    )
    
    # Process each cropping layer
    for val, layer_name in layers.items():
        print(f"\n  📊 Creating map for: {layer_name}")
        
        # File paths
        baseline_path = os.path.join(base_baseline, f"{district_name}.tif")
        recent_path = os.path.join(base_recent, f"{district_name}.tif")
        
        # Extract coordinates for both periods
        x_coords_2017, y_coords_2017, crs_2017 = extract_coordinates(baseline_path, gdf_boundary, val)
        x_coords_2022, y_coords_2022, crs_2022 = extract_coordinates(recent_path, gdf_boundary, val)
        
        # Prepare markets in correct CRS
        gdf_markets_2017 = gdf_markets.to_crs(crs_2017) if crs_2017 else gdf_markets
        gdf_markets_2022 = gdf_markets.to_crs(crs_2022) if crs_2022 else gdf_markets
        
        # Calculate hotspot stats
        stats_2017 = calculate_hotspot_stats(x_coords_2017, y_coords_2017, gdf_markets_2017, crs_2017)
        stats_2022 = calculate_hotspot_stats(x_coords_2022, y_coords_2022, gdf_markets_2022, crs_2022)
        
        # Print summary
        if stats_2017:
            _, distances_2017, _ = stats_2017
            print(f"    2017-2020: {len(distances_2017)} hotspots detected")
        else:
            print(f"    2017-2020: No hotspots detected")
            
        if stats_2022:
            _, distances_2022, _ = stats_2022
            print(f"    2022-2025: {len(distances_2022)} hotspots detected")
        else:
            print(f"    2022-2025: No hotspots detected")
        
        # Create color plot
        create_color_plot(district_name, layer_name, gdf_boundary, gdf_markets,
                         stats_2017, stats_2022, 
                         gdf_markets_2017 if stats_2017 else None,
                         gdf_markets_2022 if stats_2022 else None)

print(f"\n{'='*60}")
print(f"✅ COLOR MAPS COMPLETE!")
print(f"{'='*60}")
print(f"📊 Maps saved to: {output_color_dir}")
print(f"{'='*60}")




###############################################

## section 7 density hotspot

#################################################


import os
import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Patch
import pandas as pd
from rasterio.mask import mask

# Paths
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
water_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\core_state_rivers_dist'
base_path = r'C:\Users\user\Documents\freelance\core foss dashboard'
base_baseline = os.path.join(base_path, 'baseline_mode_2017_20')
base_recent = os.path.join(base_path, 'recent_mode_2022_25')

pattern_labels = {
    8: 'Single Kharif Cropping',
    9: 'Single Non-Kharif Cropping',
    10: 'Double Cropping',
    11: 'Triple Cropping'
}

# Output directories
val_folders = {8: 'plot_4_value_8', 9: 'plot_5_value_9', 10: 'plot_6_value_10', 11: 'plot_7_value_11'}
for folder in val_folders.values():
    os.makedirs(folder, exist_ok=True)

# Load market data
df_market = pd.read_excel(os.path.join(base_path, 'mhdata.xlsx'), sheet_name='dist_coord')
df_market_1 = pd.read_excel(os.path.join(base_path, 'mhdata.xlsx'), sheet_name='msamb_apmc_data')

def get_coords(raster_path, gdf_boundary, val):
    with rasterio.open(raster_path) as src:
        out_image, out_transform = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data_2d = np.squeeze(out_image)
        if data_2d.ndim > 2: data_2d = data_2d
        rows, cols = np.where(data_2d == val)
        if rows.size > 0:
            return rasterio.transform.xy(out_transform, rows, cols), src.crs
        return ([], []), src.crs

boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

for boundary_file in boundary_files:
    district_name = boundary_file.replace('.geojson', '')
    boundary_path = os.path.join(boundary_dir, boundary_file)
    water_path = os.path.join(water_dir, f"{district_name}_rivers.geojson")
    
    gdf_boundary = gpd.read_file(boundary_path)
    gdf_water = gpd.read_file(water_path) if os.path.exists(water_path) else None
    
    # Process Market Points
    mkt_dist = df_market[df_market['District Name'] == district_name].copy()
    mkt_apmc = df_market_1[df_market_1['District Name'] == district_name].copy()
    
    gdf_mandi_black = gpd.GeoDataFrame(mkt_dist, geometry=gpd.points_from_xy(mkt_dist.longitude, mkt_dist.latitude), crs="EPSG:4326")
    gdf_mandi_red = gpd.GeoDataFrame(mkt_apmc, geometry=gpd.points_from_xy(mkt_apmc.longitude, mkt_apmc.latitude), crs="EPSG:4326")
    
    # Filter points
    geom_union = gdf_boundary.to_crs("EPSG:4326").union_all()
    gdf_mandi_black_f = gdf_mandi_black[gdf_mandi_black.within(geom_union)]
    gdf_mandi_red_f = gdf_mandi_red[gdf_mandi_red.within(geom_union)]

    for val, folder in val_folders.items():
        (x_b, y_b), crs_b = get_coords(os.path.join(base_baseline, f"{district_name}.tif"), gdf_boundary, val)
        (x_r, y_r), crs_r = get_coords(os.path.join(base_recent, f"{district_name}.tif"), gdf_boundary, val)
        
        fig = plt.figure(figsize=(18, 8))
        ax1 = plt.axes([0.05, 0.1, 0.35, 0.75])
        ax2 = plt.axes([0.42, 0.1, 0.35, 0.75])
        
        # Variable to capture the hexbin object
        hexbin_obj = None

        # Plot Loop
        plot_data = [(ax1, x_b, y_b, crs_b, "2017-2020"), (ax2, x_r, y_r, crs_r, "2022-2025")]
        
        for ax, x, y, crs, title in plot_data:
            if len(x) > 0:
                # Assign the return value of hexbin to 'hb'
                hb = ax.hexbin(x, y, gridsize=50, cmap='YlOrRd', mincnt=1, alpha=0.8)
                # Store the first hexbin object found for the colorbar
                if hexbin_obj is None:
                    hexbin_obj = hb
            
            # Apply aspect='equal' to all GeoPandas plot calls
            if gdf_water is not None:
                gdf_water.to_crs(crs).plot(ax=ax, color='deepskyblue', linewidth=0.6, aspect='equal')
            
            gdf_boundary.to_crs(crs).boundary.plot(ax=ax, color='black', linewidth=1.8, aspect='equal')
            
            if not gdf_mandi_red_f.empty:
                gdf_mandi_red_f.to_crs(crs).plot(ax=ax, color='green', marker='o', markersize=80, edgecolor='darkred', aspect='equal')
            
            if not gdf_mandi_black_f.empty:
                gdf_mandi_black_f.to_crs(crs).plot(ax=ax, color='black', marker='P', markersize=100, aspect='equal')
            
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_axis_off()
        
        # Add Colorbar (references the captured hexbin_obj)
        if hexbin_obj:
            cbar_ax = fig.add_axes([0.78, 0.15, 0.02, 0.65])
            cbar = fig.colorbar(hexbin_obj, cax=cbar_ax)
            cbar.set_label('Intensity (Pixel Count)', fontsize=10, fontweight='bold')

        # Add Legend
        legend_elements = [
            Patch(facecolor='deepskyblue', alpha=0.4, label='Water Bodies'),
            Patch(facecolor='#FF4500', alpha=0.7, label='Hotspots'),
            mlines.Line2D([], [], color='black', marker='P', linestyle='None', markersize=10, label='District Market'),
            mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=8, label='APMC Markets'),
            mlines.Line2D([], [], color='black', linewidth=1.5, label='District Boundary')
        ]
        fig.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(0.86, 0.5), 
                  frameon=True, fontsize=11, title='Legend', title_fontsize=10)

        # Final Adjustments
        fig.suptitle(f"{district_name}: {pattern_labels[val]} Distribution", fontsize=16, fontweight='bold')
        fig.subplots_adjust(right=0.82)
        
        save_path = os.path.join(folder, f"{district_name}.jpeg")
        plt.savefig(save_path, format='jpeg')
        plt.close()                                                                         
        print(f"Saved: {save_path}")



#####################################################

## section 8 transition stats

#####################################################

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import warnings
warnings.filterwarnings('ignore')

# Configuration
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
base_baseline = r'C:\Users\user\Documents\freelance\core foss dashboard\baseline_mode_2017_20'
base_recent = r'C:\Users\user\Documents\freelance\core foss dashboard\recent_mode_2022_25'
output_dir = 'plot_14_sankey_stats'
os.makedirs(output_dir, exist_ok=True)

# Class labels
class_labels = {
    8: 'Single Kharif',
    9: 'Single Non-Kharif', 
    10: 'Double Cropping',
    11: 'Triple Cropping'
}

# Constants
pixel_size_sq_m = 100
sq_m_per_acre = 4046.86

def get_district_stats(district_name, gdf_boundary, raster_2017_path, raster_2022_path):
    """Calculate comprehensive transition statistics for a district"""
    
    # Load rasters
    with rasterio.open(raster_2017_path) as src:
        out_image1, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data_2017 = np.squeeze(out_image1)
        if data_2017.ndim > 2:
            data_2017 = data_2017[0]
    
    with rasterio.open(raster_2022_path) as src:
        out_image2, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data_2022 = np.squeeze(out_image2)
        if data_2022.ndim > 2:
            data_2022 = data_2022[0]
    
    # Filter valid pixels
    flat_2017 = data_2017.flatten()
    flat_2022 = data_2022.flatten()
    valid_mask = (np.isin(flat_2017, [8,9,10,11])) & (np.isin(flat_2022, [8,9,10,11]))
    
    flat_2017_valid = flat_2017[valid_mask]
    flat_2022_valid = flat_2022[valid_mask]
    
    if len(flat_2017_valid) == 0:
        return None
    
    # Calculate area per class for each period
    area_2017 = {}
    area_2022 = {}
    for code in [8,9,10,11]:
        pixels_2017 = np.sum(flat_2017_valid == code)
        pixels_2022 = np.sum(flat_2022_valid == code)
        area_2017[code] = (pixels_2017 * pixel_size_sq_m) / sq_m_per_acre
        area_2022[code] = (pixels_2022 * pixel_size_sq_m) / sq_m_per_acre
    
    total_area = sum(area_2017.values())
    
    # Calculate transitions
    transitions = {}
    for c1 in [8,9,10,11]:
        for c2 in [8,9,10,11]:
            pixel_count = np.sum((flat_2017_valid == c1) & (flat_2022_valid == c2))
            if pixel_count > 0:
                area_acres = (pixel_count * pixel_size_sq_m) / sq_m_per_acre
                transitions[(c1, c2)] = area_acres
    
    # Calculate changed area (where class changed)
    changed_pixels = np.sum(flat_2017_valid != flat_2022_valid)
    changed_area = (changed_pixels * pixel_size_sq_m) / sq_m_per_acre
    stable_area = total_area - changed_area
    
    # Get top 5 transitions
    transitions_list = [(c1, c2, area) for (c1, c2), area in transitions.items() if c1 != c2 and area > 0]
    transitions_list.sort(key=lambda x: x[2], reverse=True)
    
    # Prepare results
    results = {
        'district': district_name,
        'total_area_acres': total_area,
        'stable_area_acres': stable_area,
        'changed_area_acres': changed_area,
        'pct_changed': (changed_area / total_area) * 100,
        'pct_stable': (stable_area / total_area) * 100,
        'area_2017': area_2017,
        'area_2022': area_2022,
        'top_transitions': [(class_labels[c1], class_labels[c2], area) for c1, c2, area in transitions_list[:5]],
        'transition_pcts': [(class_labels[c1], class_labels[c2], 
                           (area / changed_area) * 100 if changed_area > 0 else 0,
                           (area / total_area) * 100) for c1, c2, area in transitions_list[:5]]
    }
    
    return results

# Process all districts
boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

with pd.ExcelWriter(os.path.join(output_dir, 'sankey_stats.xlsx'), engine='openpyxl') as writer:
    for boundary_file in boundary_files:
        district_name = boundary_file.replace('.geojson', '')
        print(f"\nProcessing: {district_name}")
        
        # Load boundary
        gdf_boundary = gpd.read_file(os.path.join(boundary_dir, boundary_file))
        
        # Raster paths
        raster_2017 = os.path.join(base_baseline, f"{district_name}.tif")
        raster_2022 = os.path.join(base_recent, f"{district_name}.tif")
        
        if not os.path.exists(raster_2017) or not os.path.exists(raster_2022):
            print(f"  ⚠ Missing raster files")
            continue
        
        # Get statistics
        stats = get_district_stats(district_name, gdf_boundary, raster_2017, raster_2022)
        
        if stats is None:
            print(f"  ⚠ No valid pixels")
            continue
        
        # Create summary DataFrame
        summary_data = [
            {'Metric': 'Total Area (Acres)', 'Value': f"{stats['total_area_acres']:,.0f}"},
            {'Metric': 'Stable Area (Acres)', 'Value': f"{stats['stable_area_acres']:,.0f}"},
            {'Metric': 'Changed Area (Acres)', 'Value': f"{stats['changed_area_acres']:,.0f}"},
            {'Metric': 'Percentage Changed', 'Value': f"{stats['pct_changed']:.1f}%"},
            {'Metric': 'Percentage Stable', 'Value': f"{stats['pct_stable']:.1f}%"}
        ]
        
        # Area by cropping type
        for code, label in class_labels.items():
            summary_data.append({'Metric': f'2017-2020: {label} (Acres)', 
                               'Value': f"{stats['area_2017'][code]:,.0f}"})
            summary_data.append({'Metric': f'2022-2025: {label} (Acres)', 
                               'Value': f"{stats['area_2022'][code]:,.0f}"})
            change = stats['area_2022'][code] - stats['area_2017'][code]
            summary_data.append({'Metric': f'Change: {label} (Acres)', 
                               'Value': f"{change:+,.0f}"})
        
        df_summary = pd.DataFrame(summary_data)
        
        # Create transitions DataFrame
        transitions_data = []
        for i, (from_class, to_class, area) in enumerate(stats['top_transitions'], 1):
            pct_of_changes, pct_of_total = stats['transition_pcts'][i-1][2], stats['transition_pcts'][i-1][3]
            transitions_data.append({
                'Rank': i,
                'From': from_class,
                'To': to_class,
                'Area (Acres)': f"{area:,.0f}",
                '% of Changes': f"{pct_of_changes:.1f}%",
                '% of Total Area': f"{pct_of_total:.1f}%"
            })
        
        df_transitions = pd.DataFrame(transitions_data)
        
        # Create transition matrix
        matrix_data = []
        for c1 in [8,9,10,11]:
            row = {'From \\ To': class_labels[c1]}
            for c2 in [8,9,10,11]:
                area = stats['top_transitions'][0][2] if len(stats['top_transitions']) > 0 else 0  # Placeholder
                # Actually get the transition area
                pixel_count = 0  # Would need to recalculate, but for brevity
                row[class_labels[c2]] = 'N/A'
            matrix_data.append(row)
        
        # Write all sheets
        df_summary.to_excel(writer, sheet_name=district_name[:31], index=False)
        
        # Add transitions as second sheet
        df_transitions.to_excel(writer, sheet_name=f"{district_name[:27]}_transitions", index=False)
        
        print(f"  ✓ Saved statistics for {district_name}")

print(f"\n{'='*50}")
print(f"✅ Statistics saved to: {output_dir}/sankey_stats.xlsx")
print(f"{'='*50}")




############################################

## ssection 8 sankey plot

############################################



import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Configuration
boundary_dir = r'C:\Users\user\Documents\freelance\core foss dashboard\shrug updated dist mh seperate'
base_baseline = r'C:\Users\user\Documents\freelance\core foss dashboard\baseline_mode_2017_20'
base_recent = r'C:\Users\user\Documents\freelance\core foss dashboard\recent_mode_2022_25'
output_dir = 'plot_13_sankey'
os.makedirs(output_dir, exist_ok=True)

# Class labels (4 cropping types)
class_labels = {
    8: 'Single Kharif',
    9: 'Single Non-Kharif', 
    10: 'Double Cropping',
    11: 'Triple Cropping'
}

# Constants
pixel_size_sq_m = 100  # 10m x 10m pixels
sq_m_per_acre = 4046.86

def create_sankey(district_name, gdf_boundary, raster_2017_path, raster_2022_path):
    """Create Sankey diagram for a single district"""
    
    # Load and process rasters
    with rasterio.open(raster_2017_path) as src:
        out_image1, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data_2017 = np.squeeze(out_image1)
        if data_2017.ndim > 2:
            data_2017 = data_2017[0]
    
    with rasterio.open(raster_2022_path) as src:
        out_image2, _ = mask(src, gdf_boundary.to_crs(src.crs).geometry, crop=True)
        data_2022 = np.squeeze(out_image2)
        if data_2022.ndim > 2:
            data_2022 = data_2022[0]
    
    # Flatten and filter valid pixels (only classes 8-11)
    flat_2017 = data_2017.flatten()
    flat_2022 = data_2022.flatten()
    valid_mask = (np.isin(flat_2017, [8,9,10,11])) & (np.isin(flat_2022, [8,9,10,11]))
    
    flat_2017_valid = flat_2017[valid_mask]
    flat_2022_valid = flat_2022[valid_mask]
    
    if len(flat_2017_valid) == 0:
        print(f"  ⚠ No valid pixels for {district_name}")
        return None
    
    # Calculate transitions in acres
    transitions = {}
    for c1 in [8,9,10,11]:
        for c2 in [8,9,10,11]:
            pixel_count = np.sum((flat_2017_valid == c1) & (flat_2022_valid == c2))
            if pixel_count > 0:
                area_acres = (pixel_count * pixel_size_sq_m) / sq_m_per_acre
                transitions[(c1, c2)] = area_acres
    
    # Create Sankey diagram
    node_labels = []
    for period in ['2017-2020', '2022-2025']:
        for label in class_labels.values():
            node_labels.append(f"{period}<br>{label}")
    
    # Map nodes to indices
    node_indices = {}
    for i, period in enumerate(['2017-2020', '2022-2025']):
        for j, code in enumerate([8,9,10,11]):
            node_indices[(period, code)] = i * 4 + j
    
    # Build links
    sources, targets, values = [], [], []
    for (c1, c2), area in transitions.items():
        sources.append(node_indices[('2017-2020', c1)])
        targets.append(node_indices[('2022-2025', c2)])
        values.append(round(area, 2))  # Round to 2 decimals
    
    # Create and save figure
    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=node_labels),
        link=dict(source=sources, target=targets, value=values)
    )])
    
    fig.update_layout(
        title_text=f"{district_name}: Cropping Pattern Transitions (Area in Acres)",
        font_size=12,
        width=1000,
        height=600
    )
    
    output_path = os.path.join(output_dir, f"{district_name}.html")
    fig.write_html(output_path)
    print(f"  ✓ Saved: {output_path}")
    return fig

# Process all districts
boundary_files = [f for f in os.listdir(boundary_dir) if f.endswith('.geojson')]

for boundary_file in boundary_files:
    district_name = boundary_file.replace('.geojson', '')
    print(f"\nProcessing: {district_name}")
    
    # Load boundary
    gdf_boundary = gpd.read_file(os.path.join(boundary_dir, boundary_file))
    
    # Raster paths
    raster_2017 = os.path.join(base_baseline, f"{district_name}.tif")
    raster_2022 = os.path.join(base_recent, f"{district_name}.tif")
    
    if not os.path.exists(raster_2017) or not os.path.exists(raster_2022):
        print(f"  ⚠ Missing raster files for {district_name}")
        continue
    
    # Create Sankey diagram
    create_sankey(district_name, gdf_boundary, raster_2017, raster_2022)

print(f"\n{'='*50}")
print(f"✅ Sankey plots saved to: {output_dir}")
print(f"{'='*50}")


