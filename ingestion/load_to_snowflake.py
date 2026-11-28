"""Uploaded  data/processed/*.csv.gz to Snowflake and build raw.pings."""
import os
from pathlib import Path
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    warehouse="GEOPULSE_WH",
    database="GEOPULSE",
    schema="RAW",
)
cur = conn.cursor()
try:
    cur.execute("TRUNCATE TABLE pings_load")
    cur.execute("REMOVE @pings_stage")

    for f in sorted(Path("data/processed").glob("*.csv.gz")):
        path = f.resolve().as_posix()
        cur.execute(f"PUT 'file://{path}' @pings_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE")
        print("uploaded", f.name)

    cur.execute("COPY INTO pings_load FROM @pings_stage")

    # NOTE: ST_MAKEPOINT takes LONGITUDE first, then latitude.
    cur.execute("""
        CREATE OR REPLACE TABLE pings AS
        SELECT device_id, lat, lon, ts_local, ST_MAKEPOINT(lon, lat) AS geog
        FROM pings_load
    """)

    cur.execute("SELECT COUNT(*), COUNT(DISTINCT device_id) FROM pings")
    print("rows, devices in Snowflake:", cur.fetchone())
finally:
    cur.close()
    conn.close()