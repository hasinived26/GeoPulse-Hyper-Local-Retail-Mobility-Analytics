"""Pick Store A and Store B from the data and print the stores.csv contents.
    python ingestion/pick_stores.py --save   # print AND write data/stores.csv
"""
import sys
from pathlib import Path
from common import load_processed, haversine_m

df = load_processed()
df["lat_r"] = df["lat"].round(3)   # ~100 m squares
df["lon_r"] = df["lon"].round(3)

# For each square, count DISTINCT PEOPLE (not dots), busiest first
cells = (df.groupby(["lat_r", "lon_r"])["device_id"].nunique()
           .reset_index(name="people")
           .sort_values("people", ascending=False)
           .reset_index(drop=True))

print("Top 10 squares by distinct people:")
print(cells.head(10).to_string(index=False))

# Store A = busiest square
a = cells.iloc[0]

# Store B = busiest square that is 600-900 m away from A
cells["dist_from_a_m"] = haversine_m(a.lat_r, a.lon_r, cells["lat_r"], cells["lon_r"])
band = cells[cells["dist_from_a_m"].between(600, 900)]
if band.empty:
    raise SystemExit("No busy square 600-900 m from Store A. "
                     "Process more users, or widen the distance range above.")
b = band.iloc[0]

csv_text = (
    "store_id,name,lat,lon\n"
    f"A,Store A,{a.lat_r:.3f},{a.lon_r:.3f}\n"
    f"B,Store B,{b.lat_r:.3f},{b.lon_r:.3f}\n"
)

print(f"\nStore A: {int(a.people)} distinct people pass through.")
print(f"Store B: {int(b.people)} distinct people, {b.dist_from_a_m:.0f} m from Store A.")

if "--save" in sys.argv:
    Path("data").mkdir(exist_ok=True)
    Path("data/stores.csv").write_text(csv_text)
    print("Saved data/stores.csv")