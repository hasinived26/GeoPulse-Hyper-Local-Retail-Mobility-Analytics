"""Show the busiest ~100 m squares, by dots and by distinct people."""
from common import load_processed

df = load_processed()
df["lat_r"] = df["lat"].round(3)
df["lon_r"] = df["lon"].round(3)
grid = df.groupby(["lat_r", "lon_r"])

print("Top 10 squares by DISTINCT PEOPLE:")
print(grid["device_id"].nunique().sort_values(ascending=False).head(10).to_string())

print("\nTop 10 squares by DOTS (compare, and notice the difference):")
print(grid.size().sort_values(ascending=False).head(10).to_string())