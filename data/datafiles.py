# import urllib.request
# import os

# # Create the data directory if it doesn't exist
# os.makedirs("data", exist_ok=True)

# # NOAA PSL URLs for standard monthly mean climate datasets
# datasets = {
#     "temperature": "https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis.derived/surface/air.mon.mean.nc",
#     "precipitation": "https://downloads.psl.noaa.gov/Datasets/cmap/std/precip.mon.mean.nc",
#     "wind_speed": "https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis.derived/surface/wspd.mon.mean.nc"
# }

# print("Downloading NetCDF files... (This might take a minute or two depending on Wi-Fi)")

# for name, url in datasets.items():
#     file_path = f"data/{name}.nc"
#     print(f"Fetching {name} data...")
#     urllib.request.urlretrieve(url, file_path)
#     print(f"✅ Saved to {file_path}")

# print("\nAll files downloaded successfully! You are ready to map.")