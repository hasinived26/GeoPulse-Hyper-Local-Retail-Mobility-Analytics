
import pandas as pd
from pathlib import Path

# Load cleaned GPS dataset
df = pd.read_csv("data/processed/gps_cleaned.csv")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Separate valid movement records
valid = df[
    (df["Is_Anomaly"] == False) &
    (df["Distance_km"].notna()) &
    (df["Time_Difference"] > 0)
].copy()

# Summarize each trajectory
summary = df.groupby("TrajectoryID").agg(
    DeviceID=("DeviceID", "first"),
    Total_GPS_Points=("TrajectoryID", "count"),
    Start_Time=("Timestamp", "min"),
    End_Time=("Timestamp", "max")
).reset_index()

# Calculate trajectory duration
summary["Duration_Hours"] = (
    summary["End_Time"] - summary["Start_Time"]
).dt.total_seconds() / 3600

# Calculate valid distance travelled
distance_summary = valid.groupby("TrajectoryID").agg(
    Total_Distance_km=("Distance_km", "sum"),
    Average_Speed_kmh=("Speed_kmh", "mean"),
    Maximum_Speed_kmh=("Speed_kmh", "max")
).reset_index()

# Count suspicious records
anomaly_summary = df.groupby("TrajectoryID").agg(
    Suspicious_Records=("Is_Anomaly", "sum")
).reset_index()

# Combine all summaries
summary = summary.merge(
    distance_summary,
    on="TrajectoryID",
    how="left"
)

summary = summary.merge(
    anomaly_summary,
    on="TrajectoryID",
    how="left"
)

# Save output
output_path = Path("data/processed/trajectory_summary.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

summary.to_csv(output_path, index=False)

# Display results
print("TRAJECTORY SUMMARY")
print("=" * 40)

print("\nTotal trajectories:", len(summary))

print("\nTrajectory-wise analysis:")
print(summary.to_string(index=False))

print("\nSaved successfully to:", output_path)
