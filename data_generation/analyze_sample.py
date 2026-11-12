import pandas as pd

df = pd.read_csv("data/samples/gps_sample.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

print("===== GPS DATA ANALYSIS =====")

print("\nTotal GPS Records:", len(df))

print("Unique Devices:", df["DeviceID"].nunique())

print("\nLatitude Range:")
print(df["Latitude"].min(), "to", df["Latitude"].max())

print("\nLongitude Range:")
print(df["Longitude"].min(), "to", df["Longitude"].max())

print("\nStart Time:", df["Timestamp"].min())
print("End Time:", df["Timestamp"].max())

print("\nAverage Altitude:", df["Altitude"].mean())

print("\nRecords Per Day:")
print(df.groupby(df["Timestamp"].dt.date).size())

print("\n===== ANALYSIS COMPLETE =====")
