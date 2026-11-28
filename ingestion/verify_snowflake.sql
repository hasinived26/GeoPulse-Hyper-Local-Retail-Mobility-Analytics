USE WAREHOUSE geopulse_wh;
USE SCHEMA geopulse.raw;

-- 1. Totals: must match check_data.py
SELECT COUNT(*) AS dots, COUNT(DISTINCT device_id) AS people,
       MIN(ts_local) AS first_ts, MAX(ts_local) AS last_ts
FROM pings;

-- 2. Hour-of-day shape: must match check_data.py
SELECT HOUR(ts_local) AS hr, COUNT(*) AS dots FROM pings GROUP BY hr ORDER BY hr;

-- 3. Spatial test: compare with crosscheck_local.py for Store A
SELECT COUNT(*) AS dots, COUNT(DISTINCT device_id) AS people
FROM pings
WHERE ST_DWITHIN(geog, ST_MAKEPOINT(116.331, 39.975), 500);