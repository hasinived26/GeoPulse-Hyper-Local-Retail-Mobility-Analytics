import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/samples/gps_sample.csv")

plt.figure(figsize=(10, 7))

plt.scatter(
    df["Longitude"],
    df["Latitude"],
    s=5,
    alpha=0.6
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("GeoLife GPS Movement - User 000")

plt.grid(True)
plt.tight_layout()

plt.savefig("data/samples/gps_trajectory.png")
plt.show()

print("GPS visualization saved successfully!")
