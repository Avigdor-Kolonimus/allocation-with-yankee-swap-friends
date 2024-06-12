import os
import pandas as pd

def remove_last_column_and_transpose(input_csv, output_csv):
    # Read the input CSV file without headers
    df = pd.read_csv(input_csv, header=None)
    
    # Remove the last column
    df = df.iloc[:, :-1]
    
    # Transpose the DataFrame
    df = df.transpose()
    
    # Write the modified DataFrame to the output CSV file without headers and index
    df.to_csv(output_csv, index=False, header=False)

def process_csv_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            input_csv = os.path.join(input_folder, filename)
            output_csv = os.path.join(output_folder, filename)
            remove_last_column_and_transpose(input_csv, output_csv)

# Example usage
input_folder = 'C:\\Users\\x\\yankee_swap_alg\\output\\0w\\60_courseLimit_0_weight'  # Path to the folder containing input CSV files
output_folder = 'C:\\Users\\x\\yankee_swap_alg\\output\\0w\\60_courseLimit_0_weight_formated'  # Path to the folder where output CSV files will be saved
process_csv_files(input_folder, output_folder)
