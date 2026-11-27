
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load trajectory summary
df = pd.read_csv("data/processed/trajectory_summary.csv")

# Create labels
df["Trajectory_Label"] = [
    f"Trajectory {i+1}" for i in range(len(df))
]

# Create output folder
output_path = Path("data/processed/visualizations")
output_path.mkdir(parents=True, exist_ok=True)


# 1. Total distance comparison
fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    df["Trajectory_Label"],
    df["Total_Distance_km"]
)

ax.bar_label(bars, fmt="%.2f km", padding=4)

ax.set_title("Total Distance by Trajectory")
ax.set_xlabel("Trajectory")
ax.set_ylabel("Distance (km)")

plt.tight_layout()
plt.savefig(output_path / "trajectory_distance.png")
plt.show()


# 2. Duration comparison
fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    df["Trajectory_Label"],
    df["Duration_Hours"]
)

ax.bar_label(bars, fmt="%.2f hrs", padding=4)

ax.set_title("Duration by Trajectory")
ax.set_xlabel("Trajectory")
ax.set_ylabel("Duration (hours)")

plt.tight_layout()
plt.savefig(output_path / "trajectory_duration.png")
plt.show()


# 3. Average speed comparison
fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    df["Trajectory_Label"],
    df["Average_Speed_kmh"]
)

ax.bar_label(bars, fmt="%.2f km/h", padding=4)

ax.set_title("Average Speed by Trajectory")
ax.set_xlabel("Trajectory")
ax.set_ylabel("Average Speed (km/h)")

plt.tight_layout()
plt.savefig(output_path / "trajectory_average_speed.png")
plt.show()


print("All trajectory visualizations created successfully!")
print("Saved in:", output_path)
