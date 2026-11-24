"""Count dots and distinct people within RADIUS_M of each store, plus overlap."""
import pandas as pd
from common import load_processed, haversine_m

RADIUS_M = 500

df = load_processed()
stores = pd.read_csv("data/stores.csv")

people = {}
for s in stores.itertuples():
    d = haversine_m(df["lat"].to_numpy(), df["lon"].to_numpy(), s.lat, s.lon)
    inside = df[d <= RADIUS_M]
    people[s.store_id] = set(inside["device_id"])
    print(f"Store {s.store_id}: {len(inside):,} dots, {len(people[s.store_id])} distinct people")

if "A" in people and "B" in people:
    both = people["A"] & people["B"]
    print(f"\nPeople seen at BOTH A and B: {len(both)}")
    if people["A"]:
        print(f"= {100 * len(both) / len(people['A']):.1f}% of Store A's people (all hours, rough)")