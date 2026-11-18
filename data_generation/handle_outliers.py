
import pandas as pd
from pathlib import Path

# Load GPS sample
df = pd.read_csv("data/samples/gps_sample.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort GPS records
df = df.sort_values(
    ["TrajectoryID", "Timestamp"]
).reset_index(drop=True)

# Calculate distance between consecutive GPS points
def calculate_distance(lat1, lon1, lat2, lon2):
    import numpy as np

    R = 6371

    lat1, lon1, lat2, lon2 = np.radians(
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    return 2 * R * np.arcsin(np.sqrt(a))


# Calculate distance and time difference
df["Distance_km"] = df.groupby("TrajectoryID").apply(
    lambda group: pd.Series(
        [float("nan")] + [
            calculate_distance(
                group["Latitude"].iloc[i-1],
                group["Longitude"].iloc[i-1],
                group["Latitude"].iloc[i],
                group["Longitude"].iloc[i]
            )
            for i in range(1, len(group))
        ],
        index=group.index
    )
).reset_index(level=0, drop=True)

df["Time_Difference"] = (
    df.groupby("TrajectoryID")["Timestamp"]
    .diff()
    .dt.total_seconds()
)

# Calculate speed
df["Speed_kmh"] = (
    df["Distance_km"] / df["Time_Difference"] * 3600
)

# Flag suspicious GPS records
df["Is_Anomaly"] = df["Speed_kmh"] > 50

# Separate suspicious records
suspicious = df[df["Is_Anomaly"]].copy()

# Save suspicious records
output_path = Path("data/samples/gps_suspicious_records.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

suspicious.to_csv(output_path, index=False)

# Display results
print("GPS OUTLIER INVESTIGATION")
print("-------------------------")

print("Total GPS records:", len(df))
print("Suspicious records:", len(suspicious))
print("Normal records:", (~df["Is_Anomaly"]).sum())

print("\nTop 10 suspicious records:")

print(
    suspicious.nlargest(10, "Speed_kmh")[
        ["TrajectoryID", "Timestamp",
         "Latitude", "Longitude", "Speed_kmh"]
    ]
)

print("\nSuspicious records saved successfully!")
