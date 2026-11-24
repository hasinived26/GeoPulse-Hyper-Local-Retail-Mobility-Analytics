"""Print basic facts and draw a scatter plot."""
import matplotlib.pyplot as plt
from common import load_processed

df = load_processed()

print("rows:", f"{len(df):,}")
print("devices:", df["device_id"].nunique())
print("time range:", df["ts_local"].min(), "->", df["ts_local"].max())

print("\nDots per hour of day:")
print(df.groupby(df["ts_local"].dt.hour).size().to_string())

sample = df.sample(min(50_000, len(df)), random_state=1)
plt.figure(figsize=(7, 7))
plt.scatter(sample["lon"], sample["lat"], s=1)
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("50,000 random dots")
plt.savefig("docs/scatter.png", dpi=120)
print("\nSaved docs/scatter.png")