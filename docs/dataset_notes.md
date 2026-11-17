
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


### Altitude Anomaly Investigation

Unusual altitude records were identified across all three trajectories.

| Trajectory | Negative Altitude | High Altitude |
|---|---:|---:|
| 20081023025304 | 11 | 25 |
| 20081024020959 | 16 | 0 |
| 20081026134407 | 18 | 0 |

Observations:
- 45 records have negative altitude.
- 25 records have altitude above 3000 feet.
- All high-altitude records belong to the first trajectory.
- No records have been deleted or modified.
- Further investigation is required before handling these values.


## Movement Analysis

- Calculated distance between consecutive GPS points.
- Calculated time differences between GPS records.
- Calculated movement speed in km/h.
- Average speed: 8.47 km/h.
- Maximum speed: 218.10 km/h.

### Speed Distribution

- Stationary: 60 records
- Walking: 1,096 records
- Moderate movement: 622 records
- Fast movement: 61 records
- Unusually high speed: 55 records

### Observations

- Identified unusually high GPS speeds.
- Observed sudden coordinate jumps.
- High-speed records require further investigation.
- Original GPS data remains unchanged.
