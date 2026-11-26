"""Convert the teammate's cleaned GeoLife file (data/processed/gps_cleaned.csv) into pipeline input.
Expects: DeviceID, Latitude, Longitude, Timestamp, Is_Anomaly. Drops anomalies, shifts GMT -> local time
(GeoLife is GMT; Beijing = +8h; verify in dataset_notes.md), and picks 3 existing + 1 candidate store from the
densest, well-separated ~500 m grid cells.
Usage: python local_pipeline/geolife_adapter.py --input data/processed/gps_cleaned.csv --out data_geolife
       python -c "from local_pipeline.local_pipeline import main; main('data_geolife','output_geolife')"
"""
import argparse, pathlib
import numpy as np, pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True); ap.add_argument("--out", default="data_geolife")
    ap.add_argument("--tz-shift-hours", type=float, default=8.0)
    ap.add_argument("--min-sep-m", type=float, default=700)
    a = ap.parse_args()
    df = pd.read_csv(a.input, parse_dates=["Timestamp"])
    if "Is_Anomaly" in df:
        df = df[~df["Is_Anomaly"].astype(str).str.lower().eq("true")]
    pings = pd.DataFrame({"device_id": df.DeviceID.astype(str), "lat": df.Latitude, "lon": df.Longitude,
                          "ping_ts": df.Timestamp + pd.Timedelta(hours=a.tz_shift_hours)}).dropna()
    cell = pings.assign(ci=(pings.lat / .005).round().astype(int), cj=(pings.lon / .005).round().astype(int))
    dens = (cell.groupby(["ci", "cj"]).agg(devices=("device_id", "nunique"), n=("lat", "size"),
            lat=("lat", "mean"), lon=("lon", "mean")).sort_values(["devices", "n"], ascending=False).reset_index(drop=True))
    chosen = []
    for r in dens.itertuples():
        if all(np.hypot((r.lat - c.lat) * 111000, (r.lon - c.lon) * 111000 * np.cos(np.radians(r.lat))) >= a.min_sep_m
               for c in chosen):
            chosen.append(r)
        if len(chosen) == 4: break
    if len(chosen) < 4:
        raise SystemExit("Could not find 4 separated dense areas - data too small or too concentrated.")
    ids, status = ["A", "C", "D", "B"], ["existing"] * 3 + ["candidate"]
    stores = pd.DataFrame([(i, f"Store {i}", c.lat, c.lon, s) for i, c, s in zip(ids, chosen, status)],
                          columns=["store_id", "store_name", "lat", "lon", "status"])
    out = pathlib.Path(a.out); out.mkdir(exist_ok=True)
    pings.to_csv(out / "pings.csv.gz", index=False); stores.to_csv(out / "stores.csv", index=False)
    print(f"{len(pings):,} pings, {pings.device_id.nunique()} devices -> {out}\n{stores}")
    if pings.device_id.nunique() < 20:
        print("WARNING: fewer than 20 devices - cannibalization results will not be meaningful.")

if __name__ == "__main__":
    main()
