# imports
import pandas as pd
import numpy as np
import glob
import os
from pathlib import Path
import re
import time
from tqdm.auto import tqdm
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
stores_gdf.to_pickle("./out_data_full/stores_gdf.pkl")
print("stores_gdf saved as pickle.")

# gps_signals
# read and transform gps signal batches into GeoDataFrames
signals_gdf_list = []
start = time.time()
print("Reading and transforming gps signal csv batches into GeoDataFrames...")
path = "../assignment_data/full_data/"
files_list = glob.glob(path + "*.csv")
for index in tqdm(range(len(files_list))):
    # open a partition/batch of a gps signal as a Pandas DataFrame
    signal = pd.read_csv(path + f"part_{index + 1}.csv")
    # sort by "utc_timestamp" ascending
    signal = signal.sort_values(by=["utc_timestamp"]).reset_index(drop=True)
    # transform utc_timestamp into yyyy-mm-dd (Europe/Berlin timezone)
    signal["utc_timestamp"] = signal["utc_timestamp"].astype(
        "datetime64[ms]").dt.to_period("D")
    # rename "utc_timestamp" to "date"
    signal = signal.rename(columns={"utc_timestamp": "date"})
    # create POINT from lat lon and transform df into gdf
    signal_gdf = gpd.GeoDataFrame(
        signal, geometry=gpd.points_from_xy(signal["lon"], signal["lat"]))
    # append into the signals_list
    signals_gdf_list.append(signal_gdf)
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")

# create spatial joins between stores_gdf and each signal_gdf and concat all spatial joins vertically together
signals_stores_gdf = gpd.GeoDataFrame()
start = time.time()
print("Joining each signal_gdf and stores_gdf and creating a GeoDataFrame...")
for index in tqdm(range(len(signals_gdf_list))):
    signal_gdf = signals_gdf_list[index]
    # spatial join signal_gdf and stores_gdf
    signals_stores = sjoin(signal_gdf, stores_gdf, how="inner")
    # concat/add all spatial joins vertically together
    signals_stores_gdf = pd.concat(
        [signals_stores_gdf, signals_stores], ignore_index=True)
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")

# users
# create unique users by dropping each duplicated device_id from the signals_stores_gdf
users = signals_stores_gdf[["device_id"]].drop_duplicates(
    subset=["device_id"]).reset_index(drop=True)
# sort by device_id ascending
users = users.sort_values(by=["device_id"]).reset_index(drop=True)

# user affinities
# list the files in the user_affinities folder (each file contains device ids)
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
users.to_csv("./out_data_full/users.csv", index=False)

# merge signals_stores_gdf and users (affinities)
start = time.time()
print("Merging signals_stores_gdf and users (affinities)...")
signals_stores_useraff = signals_stores_gdf.merge(
    users, how="inner", on="device_id")
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minute(s).")

# create users_in_stores for visualizing on a map
users_in_stores = signals_stores_useraff[[
    "device_id", "lat", "lon", "date", "store_id", "store_name"]]
users_in_stores.to_csv("./out_data_full/users_in_stores.csv", index=False)
print("users_in_stores saved as csv.")


# 1.b Group the resolved visits by date (yyyy-mm-dd), store_name, and store_id.
# 1.c For each store_id/store_name/date provide the following metric.
# 1.c.i A total number of GPS signals per place_id/date.
# 1.c.ii A total number of unique visitors (i.e. device ids).

# create total number of GPS signals per place_id/date and total number of unique visitors
ssu_total_and_unique = (signals_stores_useraff
                        .groupby(by=["date", "store_name", "store_id"])
                        .agg({"lat": "count", "device_id": "nunique"})
                        .rename(columns={"lat": "total_signals", "device_id": "unique_visits"})
                        .reset_index())

# 1.c.iii A total number of unique visitors belonging to each affinity group.

# total number of unique visitors belonging to each affinity group
start = time.time()
print("Creating total number of unique visitors belonging to each affinity group...")
ssu_unique_aff = (signals_stores_useraff
                  .drop(["lat", "lon", "geometry", "index_right"], axis=1)
                  .drop_duplicates(subset=["date", "store_name", "store_id", "device_id"])
                  .groupby(by=["date", "store_name", "store_id"])
                  # would sum lat, lon and device_id as well what is nonsense!!!
                  .agg(sum)
                  .reset_index()
                  .drop(["device_id"], axis=1))
# delete unnecessary columns
ssu_unique_aff = ssu_unique_aff.drop(
    ["date", "store_name", "store_id"], axis=1)
end = time.time()
dt = end - start
print(f"The above task took {round(dt/60, 2)} minutes.")

# concat the ssu_total_and_unique and ssu_unique_aff
final_df = pd.concat([ssu_total_and_unique, ssu_unique_aff], axis=1)
# save final df as csv
final_df.to_csv("./out_data_full/analysis.csv", index=False)
print("final_df saved as csv.")

end_analysis = time.time()
dt_analysis = end_analysis - start_analysis
print(f"Analysis took {round(dt_analysis/60, 2)} minute(s).")
