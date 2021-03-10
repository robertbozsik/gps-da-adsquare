# imports
import pandas as pd
import numpy as np
import glob
import os
from pathlib import Path
import re
import time
import pickle
import shapely.wkt
from shapely.geometry import Point, Polygon
import geopandas as gpd
from geopandas.tools import sjoin
from functions import list_from_affinities  # user-defined function
print("Imports done")

start_analysis = time.time()
print("Analysis started...")

# 1. Analyze the store visitation by date and affinity profile of store visitors.
# 1.a Resolve the user visits per store, i.e. filter the GPS signals through polygons.

# stores
stores = pd.read_csv("../assignment_data/stores.csv")
# transform strings to polygons in column "wkt"
stores["wkt"] = stores["wkt"].apply(lambda x: shapely.wkt.loads(x))
# rename "wkt" to "geometry" for the geopandas sjoin
stores = stores.rename(columns={"wkt": "geometry"})
# transform stores into a GeoDataFrame
stores_gdf = gpd.GeoDataFrame(stores)
# save stores_gdf as pickle
stores_gdf.to_pickle("./out_data_sample/stores_gdf.pkl")
print("stores_gdf saved as pickle.")

# gps_signals
# read all gps_signal csv batches
gps_signals = pd.DataFrame()
start = time.time()
print("Reading all gps_signal csv batches...")
for file_name in glob.glob("../assignment_data/sample_data/*.csv"):
    batch = pd.read_csv(file_name)
    gps_signals = pd.concat([gps_signals, batch], ignore_index=True)
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")
# sort by "utc_timestamp" ascending
gps_signals = gps_signals.sort_values(
    by=["utc_timestamp"]).reset_index(drop=True)
# transform utc_timestamp into yyyy-mm-dd
gps_signals["utc_timestamp"] = gps_signals["utc_timestamp"].astype(
    "datetime64[ms]").dt.to_period("D")
# rename "utc_timestamp" to "date"
gps_signals = gps_signals.rename(columns={"utc_timestamp": "date"})
# create POINT from lat lon and transform df into gdf
start = time.time()
print("Creating POINT from lat lon in gps_signals and transforming the df into a gdf...")
gps_signals_gdf = gpd.GeoDataFrame(gps_signals,
                                   geometry=gpd.points_from_xy(gps_signals["lon"], gps_signals["lat"]))
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")

# spatial join gps_signals_gdf and stores_gdf
start = time.time()
print("Joining gps_signals_gdf and stores_gdf...")
gps_sig_and_stores = sjoin(gps_signals_gdf, stores_gdf, how="inner")
# reset index after the inner spatial join
gps_sig_and_stores = gps_sig_and_stores.reset_index(drop=True)
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")

# users
# create unique users by dropping each duplicated device_id
users = gps_signals[["device_id"]].drop_duplicates(subset=["device_id"])
# sort by device_id ascending
users = users.sort_values(by=["device_id"]).reset_index(drop=True)

# user affinities
# list the files in the "affinities" folder
path = os.getcwd()
# go one level upwards compared to the current path
path = f"{str(Path(path).parents[0])}/assignment_data/affinities"
file_names = os.listdir(path)
file_names = sorted(file_names)
# add .csv after the file names (it should be run only once)
if ".csv" not in file_names[0]:
    for index, file_name in enumerate(file_names):
        os.rename(os.path.join(path, file_name), os.path.join(
            path, "".join([file_name, ".csv"])))
# create a dictionary "user_affinities", key: value -> affinity-name: [lists-of-the-affinity-csv]
user_affinities = {}
for file_name in file_names:
    name = file_name.split(".")[0]
    user_affinities[name] = list_from_affinities(name)

# add user affinities to users
for index, key in enumerate(user_affinities.keys()):
    users[key] = np.where(users["device_id"].isin(user_affinities[key]), 1, 0)
# save users as csv
users.to_csv("./out_data_sample/users.csv", index=False)

# merge gps_sig_and_stores and users (affinities)
start = time.time()
print("Merging gps_sig_and_stores and users (affinities)...")
gpssig_stores_useraff = gps_sig_and_stores.merge(
    users, how="inner", on="device_id")
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")

# create users_in_stores for visualization on a map
users_in_stores = gpssig_stores_useraff[[
    "device_id", "lat", "lon", "date", "store_id", "store_name"]]
users_in_stores.to_csv("./out_data_sample/users_in_stores.csv", index=False)
print("users_in_stores saved as csv.")


# 1.b Group the resolved visits by date (yyyy-mm-dd), store_name, and store_id.
# 1.c For each store_id/store_name/date provide the following metric.
# 1.c.i A total number of GPS signals per place_id/date.
# 1.c.ii A total number of unique visitors (i.e. device ids).

# create total number of GPS signals per place_id/date and total number of unique visitors
gsu_total_and_unique = (gpssig_stores_useraff
                        .groupby(by=["date", "store_name", "store_id"])
                        .agg({"lat": "count", "device_id": "nunique"})
                        .rename(columns={"lat": "total_signals", "device_id": "unique_visits"})
                        .reset_index())

# 1.c.iii A total number of unique visitors belonging to each affinity group.

# total number of unique visitors belonging to each affinity group
start = time.time()
print("Creating total number of unique visitors belonging to each affinity group...")
gsu_unique_aff = (gpssig_stores_useraff
                  .drop(["lat", "lon", "geometry", "index_right"], axis=1)
                  .drop_duplicates(subset=["date", "store_name", "store_id", "device_id"])
                  .groupby(by=["date", "store_name", "store_id"])
                  .agg(sum)  # would sum lat, lon and device_id as well!!!
                  .reset_index()
                  .drop(["device_id"], axis=1))
# delete unnecessary columns
gsu_unique_aff = gsu_unique_aff.drop(
    ["date", "store_name", "store_id"], axis=1)
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")

# concat the gsu_total_and_unique and gsu_unique_aff
final_df = pd.concat([gsu_total_and_unique, gsu_unique_aff], axis=1)
# save final df as csv
final_df.to_csv("./out_data_sample/analysis.csv", index=False)
print("final_df saved as csv.")

end_analysis = time.time()
dt_analysis = end_analysis - start_analysis
print(f"Analysis took {round(dt_analysis/60, 2)} minute(s).")
