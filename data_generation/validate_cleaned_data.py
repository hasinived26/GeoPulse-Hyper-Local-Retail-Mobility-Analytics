import pandas as pd

df = pd.read_csv("data/processed/gps_cleaned.csv")

print("CLEANED DATASET VALIDATION")
print("=" * 40)

print("\n1. Dataset shape:")
print(df.shape)

print("\n2. Columns:")
print(df.columns.tolist())

print("\n3. Missing values:")
print(df.isnull().sum())

print("\n4. Duplicate records:")
print(df.duplicated().sum())

print("\n5. Record status:")
print(df["Record_Status"].value_counts())

print("\n6. Speed statistics:")
print(df["Speed_kmh"].describe())

print("\n7. First five records:")
print(df.head())

invalid_coordinates = df[
    (df["Latitude"] < -90) |
    (df["Latitude"] > 90) |
    (df["Longitude"] < -180) |
    (df["Longitude"] > 180)
]

print("\n8. Invalid coordinates:", len(invalid_coordinates))
print("\nValidation completed!")

gps_columns = [
    "DeviceID",
    "TrajectoryID",
    "Latitude",
    "Longitude",
    "Altitude",
    "Timestamp"
]

print("\n9. Missing values in GPS fields:")
print(df[gps_columns].isnull().sum())