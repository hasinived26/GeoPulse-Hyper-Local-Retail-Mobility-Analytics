
import pandas as pd
import folium
from pathlib import Path

# Load cleaned GPS dataset
df = pd.read_csv("data/processed/gps_cleaned.csv")

# Remove records with invalid coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Calculate map center
center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

# Create interactive map
gps_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles © Esri"
)

# Different colors for different trajectories
colors = ["blue", "red", "green"]

# Plot each trajectory separately
for i, (trajectory_id, group) in enumerate(
    df.groupby("TrajectoryID")
):
    color = colors[i % len(colors)]

    feature_group = folium.FeatureGroup(
        name=f"Trajectory {i+1}"
    )

    for _, row in group.iterrows():

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=3,
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=f"""
            Trajectory: {trajectory_id}<br>
            Latitude: {row['Latitude']}<br>
            Longitude: {row['Longitude']}
            """
        ).add_to(feature_group)

    feature_group.add_to(gps_map)

# Add layer control
folium.LayerControl().add_to(gps_map)

# Save interactive map
output_path = Path(
    "data/processed/visualizations/gps_trajectory_map.html"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

gps_map.save(str(output_path))

print("GPS map created successfully!")
print("Total GPS points:", len(df))
print("Total trajectories:", df["TrajectoryID"].nunique())
print("Saved to:", output_path)
