import os
import pandas as pd
import hashlib

def hash_file_content(file_path):
    try:
        df = pd.read_csv(file_path)
        df_string = df.to_string(index=False)
        file_hash = hashlib.md5(df_string.encode()).hexdigest()
        return file_hash
    except Exception as e:
        print(f'Could not read {file_path}: {e}')
        return None

def count_unique_files_by_content(directory):
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    unique_hashes = set()

    for file in csv_files:
        file_path = os.path.join(directory, file)
        file_hash = hash_file_content(file_path)
        if file_hash:
            unique_hashes.add(file_hash)
    
    return len(unique_hashes)

# Example usage:
directory_path = 'C:\\PATH\\TO\\output\\0w\\60_courseLimit_0_weight'
unique_files_count = count_unique_files_by_content(directory_path)
print(f'There are {unique_files_count} unique CSV files based on their content in the folder.')
