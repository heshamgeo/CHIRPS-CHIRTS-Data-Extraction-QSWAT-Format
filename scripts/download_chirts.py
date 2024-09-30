#Download CHRITS data and extract to QSWAT+ format
import os
import requests
from bs4 import BeautifulSoup

# Define the URL of the CHIRTS data directory
base_url = "https://data.chc.ucsb.edu/products/CHIRTSdaily/v1.0/africa_netcdf_p25/"
output_folder = r"D:/Hesham/WhiteNile/White Nile/Data/CHIRTS_TEMP"  # Set your output directory
os.makedirs(output_folder, exist_ok=True)

# Function to get .nc files from a given directory
def get_nc_files(url):
    print(f"Accessing URL: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # Find all links ending with .nc (NetCDF files)
    files = [url + node.get("href") for node in soup.find_all("a") if node.get("href").endswith(".nc")]
    return files

# Download each .nc file
nc_files = get_nc_files(base_url)
print(f"Found {len(nc_files)} files.")

# Function to download the files
def download_nc_file(url, folder):
    filename = url.split("/")[-1]
    local_path = os.path.join(folder, filename)

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_path}")
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")

# Download all the .nc files found
for file_url in nc_files:
    download_nc_file(file_url, output_folder)

print("Download process completed.")