import pandas as pd
from pathlib import Path

trajectory_folder = Path(
    "data/raw/Geolife Trajectories 1.3/Data/000/Trajectory"
)

columns = [
    "Latitude",
    "Longitude",
    "Unused",
    "Altitude",
    "Date_MATLAB",
    "Date",
    "Time"
]

records = []

files = sorted(trajectory_folder.glob("*.plt"))[:3]

for file in files:
    df = pd.read_csv(
        file,
        skiprows=6,
        header=None,
        names=columns
    )

    df["DeviceID"] = "000"
    df["Timestamp"] = pd.to_datetime(
        df["Date"] + " " + df["Time"]
    )

    records.append(
        df[[
            "DeviceID",
            "Latitude",
            "Longitude",
            "Altitude",
            "Timestamp"
        ]]
    )

sample = pd.concat(records, ignore_index=True)

output_path = Path("data/samples/gps_sample.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

sample.to_csv(output_path, index=False)

print("Sample created successfully!")
print(sample.head())
print("Total records:", len(sample))