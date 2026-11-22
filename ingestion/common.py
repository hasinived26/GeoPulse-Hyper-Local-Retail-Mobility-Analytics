
from pathlib import Path
import numpy as np
import pandas as pd

PROCESSED_DIR = Path("data/processed")

def load_processed() -> pd.DataFrame:

    files = sorted(PROCESSED_DIR.glob("*.csv.gz"))
    if not files:
        raise SystemExit("No files in data/processed. Run clean_and_export.py first.")
    return pd.concat(
        (pd.read_csv(f, dtype={"device_id": str}, parse_dates=["ts_local"]) for f in files),
        ignore_index=True,
    )


def haversine_m(lat1, lon1, lat2, lon2):

    r = 6371008.8
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = p2 - p1
    dlam = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlam / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))