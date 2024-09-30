#Extract to Swat+ Format

import netCDF4 as nc
import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime, timedelta

# Define paths
tmax_nc_folder = r"D:/Hesham/WhiteNile/White Nile/Data/CHIRTS_TEMP"  # Folder with Tmax and Tmin .nc files
centroids_gdf_path = r"D:/Hesham/WhiteNile/White Nile/Data/Subbasins_output_QSWAT+/Sim_WhiteN/Sim2/Subbasin_Centroids_WN_Sim2_wgs.shp"  # Path to centroids shapefile
output_folder = r"D:/Hesham/WhiteNile/White Nile/Data/QSWAT_TEMP_test"  # Output folder for text files
os.makedirs(output_folder, exist_ok=True)

# Load centroids from the shapefile
centroids_gdf = gpd.read_file(centroids_gdf_path)

# Prepare metadata storage
metadata = []

# Extract data from Tmax and Tmin NetCDF files
for index, centroid in centroids_gdf.iterrows():
    point_id = index + 1
    lon, lat = centroid.geometry.x, centroid.geometry.y
    point_name = f"t{str(point_id).zfill(3)}"  # Naming format: t001, t002, etc.
    elevation = 0  # Placeholder; replace with actual elevation extraction if available

    # Create the file path for the output .txt file
    temp_file_path = os.path.join(output_folder, f"{point_name}.txt")

    # Open the .txt file for writing Tmax and Tmin data
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write("19830101\n")  # Start date as required by QSWAT+

        # Loop through each year and extract Tmax and Tmin values for the centroid
        for year in range(1983, 1998):
            tmax_file = os.path.join(tmax_nc_folder, f"Tmax.{year}.nc")
            tmin_file = os.path.join(tmax_nc_folder, f"Tmin.{year}.nc")

            # Open Tmax and Tmin NetCDF files
            with nc.Dataset(tmax_file) as tmax_ds, nc.Dataset(tmin_file) as tmin_ds:
                times = nc.num2date(tmax_ds.variables['time'][:], tmax_ds.variables['time'].units)

                # Find the closest grid point to the centroid's location
                lat_idx = abs(tmax_ds.variables['latitude'][:] - lat).argmin()
                lon_idx = abs(tmax_ds.variables['longitude'][:] - lon).argmin()

                # Extract Tmax and Tmin values for each time step
                for i, date in enumerate(times):
                    tmax_value = tmax_ds.variables['Tmax'][i, lat_idx, lon_idx]
                    tmin_value = tmin_ds.variables['Tmin'][i, lat_idx, lon_idx]

                    # Format and write the date and temperature values to the file
                    date_str = date.strftime("%Y%m%d")
                    temp_file.write(f"{tmax_value:.2f},{tmin_value:.2f}\n")

    # Append metadata
    metadata.append([point_id, point_name, lat, lon, elevation])

# Save metadata to a .txt file
metadata_df = pd.DataFrame(metadata, columns=["ID", "NAME", "LAT", "LONG", "ELEVATION"])
metadata_file_path = os.path.join(output_folder, "metadata.txt")
metadata_df.to_csv(metadata_file_path, index=False)

print("Temperature data extraction and formatting completed.")