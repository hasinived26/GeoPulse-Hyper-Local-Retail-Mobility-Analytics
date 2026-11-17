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


# HIGH SPEED ANOMALY ANALYSIS

print("\nHIGH SPEED ANOMALIES")

high_speed = df[df["Speed_kmh"] > 50].copy()

print("Records above 50 km/h:", len(high_speed))

print("\nHighest Speed Records:")

print(
    high_speed[
        [
            "TrajectoryID",
            "Latitude",
            "Longitude",
            "Timestamp",
            "Distance_km",
            "Time_Difference",
            "Speed_kmh"
        ]
    ].sort_values(
        by="Speed_kmh",
        ascending=False
    ).head(10)
)


# INSPECT PREVIOUS GPS POINTS

df["Previous_Latitude"] = (
    df.groupby("TrajectoryID")["Latitude"].shift(1)
)

df["Previous_Longitude"] = (
    df.groupby("TrajectoryID")["Longitude"].shift(1)
)

print("\nGPS JUMP INSPECTION")

print(
    high_speed[
        ["TrajectoryID", "Latitude", "Longitude",
         "Speed_kmh"]
    ].merge(
        df[["TrajectoryID", "Latitude", "Longitude",
            "Previous_Latitude", "Previous_Longitude"]],
        on=["TrajectoryID", "Latitude", "Longitude"]
    ).head(10)
)

# INSPECT GPS POINTS AROUND BIGGEST ANOMALY

print("\nGPS POINTS AROUND BIGGEST ANOMALY")

print(
    df.loc[147:153, [
        "TrajectoryID",
        "Latitude",
        "Longitude",
        "Timestamp",
        "Distance_km",
        "Time_Difference",
        "Speed_kmh"
    ]]
)

# SPEED CATEGORY ANALYSIS

print("\nSPEED CATEGORY ANALYSIS")

print("Stationary (0 km/h):",
      (df["Speed_kmh"] == 0).sum())

print("Walking (0-6 km/h):",
      ((df["Speed_kmh"] > 0) &
       (df["Speed_kmh"] <= 6)).sum())

print("Moderate movement (6-20 km/h):",
      ((df["Speed_kmh"] > 6) &
       (df["Speed_kmh"] <= 20)).sum())

print("Fast movement (20-50 km/h):",
      ((df["Speed_kmh"] > 20) &
       (df["Speed_kmh"] <= 50)).sum())

print("Unusually high speed (>50 km/h):",
      (df["Speed_kmh"] > 50).sum())