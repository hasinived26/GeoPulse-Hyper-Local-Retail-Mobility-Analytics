import pandas as pd
import numpy as np

df = pd.read_csv("data/samples/gps_sample.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df = df.sort_values(
    by=["TrajectoryID", "Timestamp"]
).reset_index(drop=True)


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    lat1, lon1, lat2, lon2 = np.radians(
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    return 2 * R * np.arcsin(np.sqrt(a))


df["Distance_km"] = df.groupby("TrajectoryID").apply(
    lambda group: pd.Series(
        [np.nan] + [
            calculate_distance(
                group["Latitude"].iloc[i-1],
                group["Longitude"].iloc[i-1],
                group["Latitude"].iloc[i],
                group["Longitude"].iloc[i]
            )
            for i in range(1, len(group))
        ],
        index=group.index
    )
).reset_index(level=0, drop=True)

df["Time_Difference"] = (
    df.groupby("TrajectoryID")["Timestamp"]
    .diff()
    .dt.total_seconds()
)

df["Speed_kmh"] = (
    df["Distance_km"] / df["Time_Difference"] * 3600
)

print(df[[
    "TrajectoryID",
    "Distance_km",
    "Time_Difference",
    "Speed_kmh"
]].head(10))

print("\nMOVEMENT SPEED ANALYSIS")

print("\nSpeed Statistics:")
print(df["Speed_kmh"].describe())

print("\nAverage Speed:")
print(df["Speed_kmh"].mean())

print("\nMaximum Speed:")
print(df["Speed_kmh"].max())