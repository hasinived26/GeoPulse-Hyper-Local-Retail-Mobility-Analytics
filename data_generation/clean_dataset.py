
import pandas as pd
import numpy as np
from pathlib import Path

# Load original GPS sample
df = pd.read_csv("data/samples/gps_sample.csv")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort records trajectory-wise
df = df.sort_values(
    ["TrajectoryID", "Timestamp"]
).reset_index(drop=True)

# Get previous GPS coordinates
prev_lat = df.groupby("TrajectoryID")["Latitude"].shift(1)
prev_lon = df.groupby("TrajectoryID")["Longitude"].shift(1)

# Convert coordinates to radians
lat1 = np.radians(prev_lat)
lon1 = np.radians(prev_lon)
lat2 = np.radians(df["Latitude"])
lon2 = np.radians(df["Longitude"])

# Calculate distance using Haversine formula
dlat = lat2 - lat1
dlon = lon2 - lon1

a = (
    np.sin(dlat / 2) ** 2
    + np.cos(lat1) * np.cos(lat2)
    * np.sin(dlon / 2) ** 2
)

df["Distance_km"] = (
    2 * 6371 * np.arcsin(np.sqrt(a))
)

# Calculate time difference
df["Time_Difference"] = (
    df.groupby("TrajectoryID")["Timestamp"]
    .diff()
    .dt.total_seconds()
)

# Calculate speed
df["Speed_kmh"] = (
    df["Distance_km"] / df["Time_Difference"] * 3600
)

# Flag suspicious records
df["Is_Anomaly"] = df["Speed_kmh"] > 50

# Add record status
df["Record_Status"] = np.where(
    df["Is_Anomaly"],
    "Suspicious",
    np.where(
        df["Speed_kmh"].isna(),
        "Insufficient Data",
        "Normal"
    )
)

# Save cleaned dataset
output_path = Path("data/processed/gps_cleaned.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

# Display summary
print("CLEANED DATASET SUMMARY")
print("-----------------------")

print("Total records:", len(df))
print("\nRecord status:")
print(df["Record_Status"].value_counts())

print("\nSaved successfully to:", output_path)
