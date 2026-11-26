"""Laptop-scale GeoPulse logic: 500 m catchment join -> hourly footfall -> cannibalization -> H3 export.
Input dir needs pings.csv.gz (device_id, lat, lon, ping_ts) and stores.csv (store_id, store_name, lat, lon, status)."""
import pathlib
import numpy as np, pandas as pd

RADIUS_M = 500
MORNING = range(6, 9)
H3_RES = 9
R = 6371000.0

def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi, dl = p2 - p1, np.radians(lon2 - lon1)
    h = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(h))

def to_h3(lat, lon):
    try:
        import h3
    except ImportError:
        return None
    f = h3.latlng_to_cell if hasattr(h3, "latlng_to_cell") else h3.geo_to_h3
    return [f(a, b, H3_RES) for a, b in zip(lat, lon)]

def main(data="data", out="output"):
    out = pathlib.Path(out); out.mkdir(exist_ok=True)
    pings = pd.read_csv(f"{data}/pings.csv.gz", parse_dates=["ping_ts"])
    stores = pd.read_csv(f"{data}/stores.csv")
    parts = []
    for s in stores.itertuples():
        d = haversine(pings.lat.values, pings.lon.values, s.lat, s.lon)
        m = d <= RADIUS_M
        h = pings.loc[m].copy(); h["store_id"] = s.store_id; h["dist_m"] = d[m]
        parts.append(h)
    hits = pd.concat(parts, ignore_index=True)
    hits["hour_ts"] = hits.ping_ts.dt.floor("h")
    ff = (hits.groupby(["store_id", "hour_ts"]).device_id.nunique().rename("unique_visitors").reset_index())
    ff["hour_of_day"] = ff.hour_ts.dt.hour
    ff.to_csv(out / "footfall_hourly.csv", index=False)
    profile = ff.groupby(["store_id", "hour_of_day"]).unique_visitors.mean().unstack(0).round(0).fillna(0)
    profile.to_csv(out / "footfall_hour_of_day_profile.csv")
    morning = hits[hits.ping_ts.dt.hour.isin(MORNING)][["store_id", "device_id"]].drop_duplicates()
    sets = {k: set(v.device_id) for k, v in morning.groupby("store_id")}
    rows = []
    for c in stores[stores.status == "candidate"].store_id:
        for e in stores[stores.status == "existing"].store_id:
            a, b = sets.get(e, set()), sets.get(c, set())
            rows.append(dict(candidate=c, existing=e, existing_morning_devices=len(a), shared_devices=len(a & b),
                             pct_of_existing_morning_traffic_intercepted=round(100 * len(a & b) / max(len(a), 1), 1)))
    cannib = pd.DataFrame(rows); cannib.to_csv(out / "cannibalization.csv", index=False)
    hx = to_h3(hits.lat.values, hits.lon.values)
    if hx is not None:
        hits["hex_id"] = hx
        (hits.drop_duplicates(["hex_id", "hour_ts", "device_id"]).groupby(["hex_id", "hour_ts"]).device_id.size()
         .rename("unique_visitors").reset_index().to_csv(out / "hex_footfall.csv", index=False))
    checks = {"no null device/geo": bool(hits[["device_id", "lat", "lon"]].notna().all().all()),
              "all hits within radius": bool((hits.dist_m <= RADIUS_M).all())}
    md = ["# GeoPulse - run summary", "", f"- Pings: {len(pings):,} | devices: {pings.device_id.nunique():,}",
          f"- Catchment hits (<= {RADIUS_M} m): {len(hits):,}", "", "## Cannibalization (morning 06-09h)", "",
          cannib.to_markdown(index=False), "", "## Checks", ""] + [f"- {'PASS' if v else 'FAIL'}: {k}" for k, v in checks.items()]
    (out / "summary.md").write_text("\n".join(md)); print("\n".join(md))

if __name__ == "__main__":
    main()
