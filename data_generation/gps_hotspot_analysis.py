
import pandas as pd
import folium
from folium.plugins import HeatMap
from pathlib import Path

# Load cleaned GPS dataset
df = pd.read_csv("data/processed/gps_cleaned.csv")

# Convert anomaly column to boolean
df["Is_Anomaly"] = (
    df["Is_Anomaly"].astype(str).str.lower() == "true"
)

# Keep only normal GPS records
normal_df = df[df["Is_Anomaly"] == False].copy()

# Remove missing coordinates
normal_df = normal_df.dropna(
    subset=["Latitude", "Longitude"]
)

# Calculate map center
center_lat = normal_df["Latitude"].mean()
center_lon = normal_df["Longitude"].mean()

# Create map
hotspot_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles © Esri"
)

# Prepare GPS coordinates for heatmap
heat_data = normal_df[
    ["Latitude", "Longitude"]
].values.tolist()

# Generate heatmap
HeatMap(
    heat_data,
    radius=15,
    blur=20,
    min_opacity=0.3
).add_to(hotspot_map)

# Save heatmap
output_path = Path(
    "data/processed/visualizations/gps_hotspot_map.html"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

hotspot_map.save(str(output_path))

# Display summary
print("GPS HOTSPOT ANALYSIS")
print("=" * 40)

print("Total GPS records:", len(df))
print("Normal GPS records:", len(normal_df))
print("Suspicious records excluded:", df["Is_Anomaly"].sum())

print("\nHeatmap generated successfully!")
print("Saved to:", output_path)
