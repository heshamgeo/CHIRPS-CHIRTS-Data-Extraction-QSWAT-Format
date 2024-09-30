#Download CRHIS PREC data 

import os
import requests
from bs4 import BeautifulSoup
import gzip
import shutil

# Define the URL of the CHIRPS data directory
base_url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p25/"
# Set the output directory as specified
output_folder = r"D:\Hesham\WhiteNile\White Nile\Data\CHRIS_PREC"
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Function to get the list of subdirectories from the main directory
def get_subdirectories(url):
    print(f"Accessing URL: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # Find all links that are directories (usually ending with a '/')
    subdirectories = [url + node.get("href") for node in soup.find_all("a") if node.get("href").endswith("/")]
    return subdirectories

# Function to get .tif.gz files from a given directory
def get_tif_files(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # Find all links ending with .tif.gz (compressed GeoTIFF files)
    files = [url + node.get("href") for node in soup.find_all("a") if node.get("href").endswith(".tif.gz")]
    return files

# Function to download and optionally decompress .tif.gz files
def download_and_decompress_file(url, folder, decompress=False):
    filename = url.split("/")[-1]
    local_gz_path = os.path.join(folder, filename)

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_gz_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_gz_path}")

        # Decompress the file if needed
        if decompress:
            local_tif_path = local_gz_path.replace('.gz', '')
            with gzip.open(local_gz_path, 'rb') as gz_file:
                with open(local_tif_path, 'wb') as tif_file:
                    shutil.copyfileobj(gz_file, tif_file)
            print(f"Decompressed: {local_tif_path}")
    except Exception as e:
        print(f"Failed to download or decompress {url}. Error: {e}")

# Get the list of year subdirectories
year_directories = get_subdirectories(base_url)

# Filter to include only the years from 1981 to 1997
filtered_year_directories = [d for d in year_directories if any(str(year) in d for year in range(1981, 1998))]

# Check if directories are filtered correctly
print(f"Number of year directories to process (1981-1997): {len(filtered_year_directories)}")
print("Sample of filtered directories:", filtered_year_directories[:3])

# Loop through each year directory and download .tif.gz files
for year_dir in filtered_year_directories:
    # Get the list of .tif.gz files in the current year directory
    tif_files = get_tif_files(year_dir)
    print(f"Found {len(tif_files)} files in {year_dir}")

    # Download and decompress each file
    for file_url in tif_files:
        download_and_decompress_file(file_url, output_folder, decompress=True)

print("Download and decompression process completed.")
