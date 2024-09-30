
# CHIRPS and CHIRTS Data Extraction for SWAT+

This repository contains Python scripts for downloading, processing, and extracting **CHIRPS** precipitation and **CHIRTS** temperature data to be used in **SWAT+** modeling. The data is extracted based on the centroids of subbasins and formatted into the required text format for SWAT+.

## Repository Structure

The repository is organized into two main sections, each representing a different dataset:

### **CHIRPS (Precipitation Data)**
- **01_Download/**: Script to download CHIRPS precipitation `.tif` files from the UCSB Climate Hazards Center website.
- **02_Calculate_Centroid/**: Script to calculate centroids for the subbasins (required for precipitation data extraction).
- **03_Extract_To_SWAT/**: Script to extract precipitation data from the downloaded `.tif` files based on centroid locations and format it for SWAT+.

### **CHIRTS (Temperature Data)**
- **01_Download/**: Script to download CHIRTS temperature `.nc` files (Tmax and Tmin) from the UCSB Climate Hazards Center website.
- **03_Extract_To_SWAT/**: Script to extract Tmax and Tmin data from the `.nc` files based on centroid locations and format it for SWAT+.

## Requirements

To run these scripts, you will need the following dependencies installed on your machine:

- `Python 3.x`
- `geopandas`
- `rasterio`
- `requests`
- `bs4` (BeautifulSoup)
- `netCDF4`
- `pandas`
- `shapely`

You can install all dependencies using `pip`:
```bash
pip install geopandas rasterio requests beautifulsoup4 netCDF4 pandas shapely
```

## CHIRPS Data (Precipitation)

### **1. Downloading CHIRPS Data**

The script `download_chirps.py` downloads the daily CHIRPS `.tif.gz` files from the UCSB Climate Hazards Center. These files are used to extract precipitation data.

#### Steps:
1. Navigate to the `CHIRPS/01_Download/` directory.
2. Update the `output_folder` path in the script to point to the directory where you want to save the downloaded files.
3. Run the script to download the CHIRPS precipitation files:
   ```bash
   python download_chirps.py
   ```

### **2. Calculating Centroids (For Precipitation Data Extraction)**

The centroids are calculated from the subbasin shapefile. The script `calculate_centroid_chirps.py` takes a shapefile of subbasins and calculates the centroids, saving them to a new shapefile.

#### Steps:
1. Navigate to the `CHIRPS/02_Calculate_Centroid/` directory.
2. Update the path to your subbasin shapefile in the script.
3. Run the script to calculate the centroids:
   ```bash
   python calculate_centroid_chirps.py
   ```

### **3. Extracting Precipitation Data to SWAT Format**

The script `extract_to_swat_chirps.py` extracts precipitation data from the `.tif` files based on the calculated centroids and formats it for SWAT+.

#### Steps:
1. Navigate to the `CHIRPS/03_Extract_To_SWAT/` directory.
2. Update the paths for the `tif_folder` (where the precipitation `.tif` files are stored) and the `centroids_shapefile_path`.
3. Run the script to extract precipitation data:
   ```bash
   python extract_to_swat_chirps.py
   ```

Each centroid will generate a `.txt` file containing precipitation data starting from `19830101`.

---

## CHIRTS Data (Temperature)

### **1. Downloading CHIRTS Data**

The script `download_chirts.py` downloads CHIRTS `.nc` files for Tmax and Tmin from the UCSB Climate Hazards Center. These files are used to extract temperature data.

#### Steps:
1. Navigate to the `CHIRTS/01_Download/` directory.
2. Update the `output_folder` path in the script to point to the directory where you want to save the downloaded files.
3. Run the script to download the CHIRTS Tmax and Tmin files:
   ```bash
   python download_chirts.py
   ```

### **2. Extracting Temperature Data to SWAT Format**

The script `extract_to_swat_chirts.py` extracts Tmax and Tmin data from the `.nc` files based on the centroid points and formats it for SWAT+.

#### Steps:
1. Navigate to the `CHIRTS/03_Extract_To_SWAT/` directory.
2. Update the paths for the `nc_folder` (where the `.nc` files are stored) and the `centroids_shapefile_path`.
3. Run the script to extract Tmax and Tmin data:
   ```bash
   python extract_to_swat_chirts.py
   ```

Each centroid will generate a `.txt` file containing Tmax and Tmin data starting from `19830101`.

---

## Metadata Output

For both precipitation and temperature data, a `metadata.txt` file is generated, which contains:
- **ID**: Unique identifier for each centroid.
- **NAME**: Name of the centroid (e.g., `pcp1`, `t001`).
- **LAT**: Latitude of the centroid.
- **LONG**: Longitude of the centroid.
- **ELEVATION**: Elevation (set to 0 for precipitation, not included for temperature).

---

## Additional Information

### File Naming Conventions:
- The output files for each centroid will follow this naming format:
  - Precipitation: `pcp1.txt`, `pcp2.txt`, ...
  - Temperature: `t001.txt`, `t002.txt`, ...
  
- Each `.txt` file will start with the date `19830101`, followed by the data values (precipitation or Tmax/Tmin) for each day.

---

## Contributors
If you have any questions or need assistance, feel free to reach out through the repository's Issues section.

---

### License Agreement

This code is provided as-is without any warranty. The use, modification, distribution, or reproduction of this code is not permitted without prior written permission from the author.

**Conditions for Use:**
- You must contact the author before using this code for any purpose.
- You may not redistribute, modify, or use this code in any form without explicit permission.

**Contact Information:**
- Author: [Your Name]
- Email: [Your Email Address]
- GitHub: [Your GitHub Profile]

By using or accessing this code, you agree to these terms.
---

### Contact Information

Feel free to contact me at [h.elhaddad@wmich.edu] for any questions or further clarifications.
