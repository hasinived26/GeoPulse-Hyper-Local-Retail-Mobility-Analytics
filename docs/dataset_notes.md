
# GeoPulse - Dataset Documentation

## Dataset Name
GeoLife GPS Trajectories 1.3

## Source
Microsoft Research Asia

## Dataset Description
The GeoLife dataset contains GPS trajectories
collected from multiple users. It provides
location information with timestamps.

## Original Data Format
The dataset contains .plt files with:
- Latitude
- Longitude
- Altitude
- Date
- Time

## Sample Dataset
Created an initial CSV sample using 3 trajectory
files from user 000.

## Processed Columns
- DeviceID
- Latitude
- Longitude
- Altitude
- Timestamp

## Sample Statistics
Total records: 1897

## Purpose
The dataset will be used to understand movement
patterns and support the development of GeoPulse.


## Data Quality Analysis

- Total records analyzed: 1,897
- Missing values: 0
- Duplicate records: 0
- Invalid GPS coordinates: 0
- Timestamp range: 23 October 2008 to 26 October 2008

### Altitude Analysis

- Minimum altitude: -466 feet
- Maximum altitude: 7,584 feet
- Mean altitude: 245.7 feet
- Median altitude: 120 feet
- Negative altitude records: 45
- Records above 3,000 feet: 25

### Observations

- GPS coordinates are within valid ranges.
- No missing or duplicate records were found.
- Some altitude values require further investigation.
- No records have been removed or modified.
