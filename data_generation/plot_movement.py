import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/samples/gps_sample.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

plt.figure(figsize=(12, 7))

for trajectory, group in df.groupby("TrajectoryID"):
    group = group.sort_values("Timestamp")

    plt.plot(
        group["Longitude"],
        group["Latitude"],
        marker=".",
        markersize=3,
        linewidth=1,
        label=trajectory
    )

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("GeoLife GPS Movement - User 000")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("data/samples/gps_connected_movement.png")
plt.show()
