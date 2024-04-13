import os

# Define the directory path
directory = 'C:\\Users\\superup\\yankee_swap_alg\\formatter'
input_directory = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\input'

# Define the format to exclude (e.g., '.txt', '.pdf', etc.)
exclude_format_file = '.txt'  # Change this to your desired format
exclude_format_folder = 'formated'
accumulate_folder = 'accumulate'

# Get all directories in the specified directory
folders = [folder for folder in os.listdir(input_directory) if os.path.isdir(os.path.join(input_directory, folder))]

# Filter out folders with the excluded format
filtered_folders = [folder for folder in folders if not folder.endswith(exclude_format_folder)]

# Filter out folders ending with the exclude_format_file
filtered_folders = [folder for folder in filtered_folders if not os.path.exists(os.path.join(input_directory, folder + exclude_format_file))]

# Print the filtered folders
print(filtered_folders)

# Create duplicate folders with names containing the excluded format within the "formated" folder
for folder in filtered_folders:
    # Create the duplicate folder name
    duplicate_folder_name = folder + "_" + exclude_format_folder
    accumulate_folder_name = folder + "_" + accumulate_folder
    
    # Create the duplicate folder path
    duplicate_folder_path = os.path.join(directory, 'formated', duplicate_folder_name)
    accumulate_folder_path = os.path.join(directory, 'accumulate', accumulate_folder_name)
    
    # Create the duplicate folder
    os.makedirs(duplicate_folder_path)
    os.makedirs(accumulate_folder_path)

print("Duplicate folders created successfully.")