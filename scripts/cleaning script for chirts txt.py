#Remove --,-- from the txt file if it's there

import os

# Define the path to the folder containing the text files
text_files_folder = r"D:/Hesham/WhiteNile/White Nile/Data/QSWAT_TEMP_CHRITS"

# Function to remove the last line if it contains "--,--"
def clean_last_row(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the last line contains "--,--"
    if lines and lines[-1].strip() == "--,--":
        # Remove the last line
        lines = lines[:-1]

    # Write the cleaned content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Loop through all text files in the folder and clean them
for file_name in os.listdir(text_files_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(text_files_folder, file_name)
        clean_last_row(file_path)

print("All text files cleaned successfully.")