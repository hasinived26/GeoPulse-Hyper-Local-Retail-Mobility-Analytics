"""Generate mock anonymized mobile pings (device_id, lat, lon, ping_ts) + store locations.
Devices live in 3 zones and commute to a central area; candidate Store B sits on the corridor of one zone.
Usage: python data_gen\generate_pings.py --devices 5000 --days 5 --out data_mock
"""
import argparse, pathlib
import numpy as np, pandas as pd

STORES = pd.DataFrame([
    ("A", "Store A (existing, centre)",      12.9716, 77.5946, "existing"),
    ("C", "Store C (existing, east)",        12.9850, 77.6100, "existing"),
    ("D", "Store D (existing, south-west)",  12.9550, 77.5700, "existing"),
    ("B", "Store B (candidate, 5th St)",     12.9775, 77.6000, "candidate"),
], columns=["store_id", "store_name", "lat", "lon", "status"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--devices", type=int, default=5000)
    ap.add_argument("--days", type=int, default=5)
    ap.add_argument("--start", default="2026-11-02")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="data_mock")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed); D = a.devices
    zones = np.array([[13.000, 77.620], [12.950, 77.565], [12.935, 77.605]])
    z = rng.choice(3, D, p=[0.40, 0.35, 0.25])
    home = zones[z] + rng.normal(0, 0.012, (D, 2))
    work = np.column_stack([rng.normal(12.9716, 0.006, D), rng.normal(77.5946, 0.006, D)])
    ids = np.array([f"dev_{i:07d}" for i in range(D)])
    frames = []
    for d in range(a.days):
        day = pd.Timestamp(a.start) + pd.Timedelta(days=d)
        if day.dayofweek >= 5:
            continue
        present = rng.random(D) < 0.88
        segs = [(np.tile([6.0, 7.0], (D, 1)) + rng.uniform(0, .5, (D, 2)), np.zeros((D, 2)))]
        s = rng.normal(8.0, 0.7, D)[:, None]
        segs.append((s + np.linspace(0, .67, 12)[None, :], np.tile(np.linspace(0, 1, 12), (D, 1))))
        segs.append((np.tile(np.arange(9.5, 17.0, 1.0), (D, 1)) + rng.uniform(0, .4, (D, 8)), np.ones((D, 8))))
        e = rng.normal(17.5, 0.7, D)[:, None]
        segs.append((e + np.linspace(0, .67, 12)[None, :], np.tile(np.linspace(1, 0, 12), (D, 1))))
        segs.append((np.tile([20.0, 22.0], (D, 1)) + rng.uniform(0, .5, (D, 2)), np.zeros((D, 2))))
        for H, F in segs:
            lat = home[:, [0]] + F * (work[:, [0]] - home[:, [0]]) + rng.normal(0, .0003, F.shape)
            lon = home[:, [1]] + F * (work[:, [1]] - home[:, [1]]) + rng.normal(0, .0003, F.shape)
            m = np.broadcast_to(present[:, None], H.shape).ravel()
            frames.append(pd.DataFrame({"device_id": np.repeat(ids, H.shape[1])[m],
                                        "lat": lat.ravel()[m], "lon": lon.ravel()[m],
                                        "ping_ts": day + pd.to_timedelta(H.ravel()[m], unit="h")}))
    pings = pd.concat(frames).sort_values("ping_ts").reset_index(drop=True)
    pings["ping_ts"] = pings["ping_ts"].dt.floor("s")
    out = pathlib.Path(a.out); out.mkdir(exist_ok=True)
    pings.to_csv(out / "pings.csv.gz", index=False); STORES.to_csv(out / "stores.csv", index=False)
    print(f"{len(pings):,} pings, {D:,} devices -> {out}")

if __name__ == "__main__":
    main()
