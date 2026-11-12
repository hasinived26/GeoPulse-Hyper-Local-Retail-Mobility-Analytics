import pandas as pd

df = pd.read_csv("data/samples/gps_sample.csv")

print("----- DATA QUALITY REPORT -----")

print("\nDataset Shape:", df.shape)
print("\nColumn Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

invalid_lat = ~df["Latitude"].between(-90, 90)
print("\nInvalid Latitudes:", invalid_lat.sum())

invalid_lon = ~df["Longitude"].between(-180, 180)
print("Invalid Longitudes:", invalid_lon.sum())

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"], errors="coerce"
)
print("Invalid Timestamps:", df["Timestamp"].isnull().sum())

print("\nTotal Valid Records:",
      len(df) - df["Timestamp"].isnull().sum())

print("\n----- VALIDATION COMPLETE -----")
