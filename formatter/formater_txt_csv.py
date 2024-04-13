import os
import csv

# Define the directory path
directory = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\input'

# Define the output CSV file path
output_csv_folder = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\formated\\50agents_3_formated'

# Define the format to exclude (e.g., '.txt', '.pdf', etc.)
exclude_format_file = '.csv'  # Change this to your desired format
exclude_format_folder = 'formated'

# Get all directories in the specified directory
folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

# Filter out folders with the excluded format
filtered_folders = [folder for folder in folders if not folder.endswith(exclude_format_folder)]

# Filter out folders ending with the exclude_format_file
filtered_folders = [folder for folder in filtered_folders if not os.path.exists(os.path.join(directory, folder + exclude_format_file))]

# Iterate over each folder in the "formated" directory
for folder_name in filtered_folders:
    print(f"Start folder '{folder_name}'")
    folder_path = os.path.join(directory, folder_name)

    # Check if the current item is a directory
    if os.path.isdir(folder_path):
        # Find all text files in the current folder
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        
        count = 0
        # Print the path of each text file
        for txt_file in txt_files:
            txt_file_path = os.path.join(folder_path, txt_file)

            # Open the CSV file in write mode
            output_csv_file = os.path.join(output_csv_folder, str(count)+'.csv')
            count += 1
        
            with open(output_csv_file, 'w', newline='') as csvfile:
                # Define the header of the CSV file
                fieldnames = ['student', 'course_1', 'course_2', 'course_3', 'course_4', 'course_5', 'course_6', 'course_7', 'course_8', 'course_9']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
                # Write the header to the CSV file
                writer.writeheader()

                # Open the text file for reading
                with open(txt_file_path, 'r') as file:
                    # Read each line of the file
                    for line in file:
                        # Split the row by ':'
                        studentID, courses_str = line.split(':')

                        # Convert the data into a dictionary
                        formatted_row = {'student': int(studentID)}
                        for i in range(1, 10):
                            formatted_row[f'course_{i}'] = 0

                        # Split the courses string by ','
                        for course in courses_str.split(','):
                            # Extract the course number
                            course_num = int(course.strip()[1:])  # Remove the 'c' and convert to integer
                            formatted_row[f'course_{course_num}'] = 1
                        
                        # Write the row to the CSV file
                        writer.writerow(formatted_row)

            print(f"CSV file '{output_csv_file}' created successfully.")