# Read GeoLife .plt files, clean them, write one .csv.gz per user.

import argparse
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw/Geolife Trajectories 1.3/Data")
OUT_DIR = Path("data/processed")

COLS = ["lat", "lon", "zero", "alt_ft", "days", "date", "time"]

# Rough Beijing box. Adjust after looking at the scatter plot.
LAT_MIN, LAT_MAX = 39.7, 40.2
LON_MIN, LON_MAX = 116.1, 116.7


def read_plt(path: Path, device_id: str) -> pd.DataFrame:
    df = pd.read_csv(
        path, skiprows=6, header=None, names=COLS,
        usecols=["lat", "lon", "date", "time"],
    )
    df["device_id"] = device_id  # text, so "000" stays "000"
    df["ts"] = pd.to_datetime(df["date"] + " " + df["time"], errors="coerce")
    return df[["device_id", "lat", "lon", "ts"]]


def clean(df: pd.DataFrame, tz_offset_hours: float) -> pd.DataFrame:
    df = df.dropna(subset=["lat", "lon", "ts"])
    df = df[df["lat"].between(LAT_MIN, LAT_MAX) & df["lon"].between(LON_MIN, LON_MAX)]
    df = df.drop_duplicates(subset=["device_id", "ts"])
    df = df.assign(ts_local=df["ts"] + pd.Timedelta(hours=tz_offset_hours))
    return df[["device_id", "lat", "lon", "ts_local"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=20, help="how many users to process")
    ap.add_argument("--tz-offset", type=float, default=0,
                    help="hours to add to raw timestamps (try 0 first, then 8)")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    user_dirs = sorted(p for p in RAW_DIR.iterdir() if p.is_dir())[: args.users]

    total = 0
    for user_dir in user_dirs:
        device_id = user_dir.name
        files = sorted((user_dir / "Trajectory").glob("*.plt"))
        if not files:
            continue
        raw = pd.concat((read_plt(f, device_id) for f in files), ignore_index=True)
        out = clean(raw, args.tz_offset)
        out.to_csv(OUT_DIR / f"{device_id}.csv.gz", index=False)
        total += len(out)
        print(f"{device_id}: {len(raw):>9,} read -> {len(out):>9,} kept")

    print(f"TOTAL kept: {total:,}")


if __name__ == "__main__":
    main()