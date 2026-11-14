import pandas as pd

df = pd.read_csv("data/samples/gps_sample.csv")

print("DATASET OVERVIEW")
print("----------------")
print("Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nLatitude Range:")
print(df["Latitude"].min(), "to", df["Latitude"].max())

print("\nLongitude Range:")
print(df["Longitude"].min(), "to", df["Longitude"].max())

print("\nAltitude Range:")
print(df["Altitude"].min(), "to", df["Altitude"].max())

print("\nTimestamp Range:")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
print(df["Timestamp"].min(), "to", df["Timestamp"].max())

print("\nInvalid Coordinates:")
invalid = (
    ~df["Latitude"].between(-90, 90)
    | ~df["Longitude"].between(-180, 180)
)
print(invalid.sum())

print("\nALTITUDE ANALYSIS")

print("Negative altitude records:")
print((df["Altitude"] < 0).sum())

print("\nAltitude above 3000 feet:")
print((df["Altitude"] > 3000).sum())

print("\nAltitude Statistics:")
print(df["Altitude"].describe())
