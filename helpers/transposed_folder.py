import os
import csv

def transpose_csv(input_csv, output_csv):
    # Read the input CSV file
    with open(input_csv, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        data = list(reader)
    
    # Modify the student entries by adding 'A' at the beginning
    modified_data = [data[0]]  # Include the header
    for row in data[1:]:
        modified_row = [f"A{row[0]}"] + row[1:]
        modified_data.append(modified_row)

    # Transpose the data (excluding the header)
    transposed_data = list(zip(*modified_data[1:]))
    
    # Write the transposed data to the output CSV file
    with open(output_csv, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(transposed_data)

def process_csv_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        print(filename)
        if filename.endswith(".csv"):
            input_csv = os.path.join(input_folder, filename)
            output_csv = os.path.join(output_folder, filename)
            print(input_csv, output_csv)
            transpose_csv(input_csv, output_csv)

# Example usage
input_folder = 'C:\\Users\\x\\yankee_swap_alg\\original_input\\0w\\60_courseLimit_0_weight_formated'  # Path to the folder containing input CSV files
output_folder = 'C:\\Users\\x\\yankee_swap_alg\\original_input\\0w\\60_courseLimit_0_weight'  # Path to the folder where output CSV files will be saved
process_csv_files(input_folder, output_folder)
