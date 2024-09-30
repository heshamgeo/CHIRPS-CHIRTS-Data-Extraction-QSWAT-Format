
#format CHRIS data to Swat
import os
import rasterio
import geopandas as gpd
import pandas as pd
from datetime import datetime

# Define paths
tif_folder = r"D:/Hesham/WhiteNile/White Nile/Data/CHRIS_PREC"  # Folder containing .tif files
centroids_shapefile_path = r"D:/Hesham/WhiteNile/White Nile/Data/Subbasins_output_QSWAT+/Sim_WhiteN/Sim2/Subbasin_Centroids_WN_Sim2_wgs.shp"  # Path to the centroid shapefile
output_folder = r"D:/Hesham/WhiteNile/White Nile/Data/QSWAT_PCP_CHRIPS"  # Folder to save the output files
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Read the shapefile containing the centroids
centroids_gdf = gpd.read_file(centroids_shapefile_path)

# Prepare metadata storage
metadata = []

# Loop through each centroid and extract precipitation data
for idx, centroid in centroids_gdf.iterrows():
    point_id = idx + 1
    lon, lat = centroid.geometry.x, centroid.geometry.y
    point_name = f"pcp{point_id}"
    elevation = 0  # Placeholder for elevation (set to 0 as requested)

    # Prepare the text file path
    pcp_file_path = os.path.join(output_folder, f"{point_name}.txt")

    # Open the text file for writing precipitation data
    with open(pcp_file_path, 'w') as pcp_file:
        # Write the start date of the data as the first row
        pcp_file.write(f"19830101\n")  # Start date as required by QSWAT+

        # Loop through each .tif file and extract data
        for tif_file in sorted(os.listdir(tif_folder)):
            if tif_file.endswith(".tif"):
                # Extract the date from the filename based on the format "chirps-v2.0.YYYY.MM.DD.tif"
                date_str = tif_file.split('.')[2] + tif_file.split('.')[3] + tif_file.split('.')[4]
                date = datetime.strptime(date_str, "%Y%m%d")

                # Only process data from 19830101 onwards
                if date >= datetime.strptime("19830101", "%Y%m%d"):
                    # Open the .tif file
                    with rasterio.open(os.path.join(tif_folder, tif_file)) as src:
                        # Check if the centroid point is within the raster bounds
                        if src.bounds.left <= lon <= src.bounds.right and src.bounds.bottom <= lat <= src.bounds.top:
                            # Sample the raster at the centroid's location
                            value = list(src.sample([(lon, lat)]))[0][0]
                        else:
                            value = -9999  # Assign a no-data value if the point is outside

                        # Write the value to the text file
                        pcp_file.write(f"{value}\n")

    # Add metadata for this centroid
    metadata.append([point_id, point_name, lat, lon, elevation])

# Create the metadata file
metadata_df = pd.DataFrame(metadata, columns=["ID", "NAME", "LAT", "LONG", "ELEVATION"])
metadata_file_path = os.path.join(output_folder, "metadata.txt")
metadata_df.to_csv(metadata_file_path, index=False)

print(f"Precipitation data extraction and formatting completed. Check the folder: {output_folder}")
