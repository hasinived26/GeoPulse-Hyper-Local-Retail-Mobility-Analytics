
import pandas as pd
import folium
from pathlib import Path

# Load cleaned GPS dataset
df = pd.read_csv("data/processed/gps_cleaned.csv")

# Convert anomaly column to boolean
df["Is_Anomaly"] = (
    df["Is_Anomaly"].astype(str).str.lower() == "true"
)

# Remove records with missing coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Calculate map center
center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

# Create map using Esri tiles
gps_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles © Esri"
)

# Colors for each trajectory
colors = ["blue", "green", "purple"]

# Plot each trajectory separately
for i, (trajectory_id, group) in enumerate(
    df.groupby("TrajectoryID")
):

    color = colors[i % len(colors)]

    # Separate normal and suspicious records
    normal_points = group[group["Is_Anomaly"] == False]
    suspicious_points = group[group["Is_Anomaly"] == True]

    # Normal GPS points layer
    normal_layer = folium.FeatureGroup(
        name=f"Trajectory {i+1} - Normal"
    )

    for _, row in normal_points.iterrows():

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=3,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"""
            Type: Normal<br>
            Trajectory: {trajectory_id}<br>
            Speed: {row['Speed_kmh']:.2f} km/h
            """
        ).add_to(normal_layer)

    normal_layer.add_to(gps_map)

    # Suspicious GPS points layer
    suspicious_layer = folium.FeatureGroup(
        name=f"Trajectory {i+1} - Suspicious"
    )

    for _, row in suspicious_points.iterrows():

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=1,
            popup=f"""
            Type: Suspicious<br>
            Trajectory: {trajectory_id}<br>
            Speed: {row['Speed_kmh']:.2f} km/h
            """
        ).add_to(suspicious_layer)

    suspicious_layer.add_to(gps_map)

# Add layer control
folium.LayerControl(collapsed=False).add_to(gps_map)

# Save map
output_path = Path(
    "data/processed/visualizations/gps_anomaly_map.html"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

gps_map.save(str(output_path))

print("GPS anomaly map created successfully!")
print("Total GPS points:", len(df))
print("Normal points:", (~df["Is_Anomaly"]).sum())
print("Suspicious points:", df["Is_Anomaly"].sum())
print("Saved to:", output_path)
