import geopandas as gpd

# Define the path to the shapefile containing subbasins
subbasins_shapefile = r"D:/Hesham/WhiteNile/White Nile/Data/Subbasins_output_QSWAT+/Sim_WhiteN/Sim2/WhiteN_UTM_SRTM90msubbasins.shp"  # Replace with your shapefile path
centroids_output_path = r"D:/Hesham/WhiteNile/White Nile/Data/Subbasins_output_QSWAT+/Sim_WhiteN/Sim2/Subbasin_Centroids_WN_Sim2.shp"  # Optional output for centroids

# Load subbasins shapefile
subbasins = gpd.read_file(subbasins_shapefile)

# Calculate centroids
subbasins['centroid'] = subbasins.geometry.centroid

# Create a GeoDataFrame of centroids
centroids_gdf = gpd.GeoDataFrame(subbasins[['centroid']], geometry='centroid', crs=subbasins.crs)
centroids_gdf = centroids_gdf.set_geometry('centroid')

# Save centroids to a shapefile (optional)
centroids_gdf.to_file(centroids_output_path)
print("Centroids calculated and saved.")