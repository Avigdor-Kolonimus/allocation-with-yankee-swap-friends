import os
import csv
import argparse
import numpy as np
import pandas as pd

from item import Item
from student import Student
from algo_friendship_bfs import friendship_bfs_yankee_swap

# Define the directory path
directory = 'C:\\Users\\x\\yankee_swap_alg\\original_input\\0w\\60_courseLimit_0_weight'

# Define the output CSV file path
output_csv_folder = 'C:\\Users\\x\\yankee_swap_alg\\output\\0w\\60_courseLimit_0_weight'
original_capacity=60

def read_friendship(file_name, total_courses=3):
    students = []

    try:
        df = pd.read_csv(file_name, sep=",", header=0)
        
        for index, row in df.iterrows():
            array_representation = np.array(row)
            student = Student(index, total_courses)
            student.add_friends(array_representation)
            students.append(student)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")

    return students

def read_distributions(file_name, capacity):
    distributions = []

    try:
        df = pd.read_csv(file_name, sep=",", header=0)
        
        for index, row in df.iterrows():
            item = Item(index, capacity)
            array_representation = np.array(row)[:]
            item.add_distributions(array_representation)
            distributions.append(item)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")

    return distributions

def read_course_ratings(file_name, students):
    try:
        df = pd.read_csv(file_name, sep=",", header=0)
        
        for index, row in df.iterrows():
            array_representation = np.array(row)
            students[index].add_courses(array_representation)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")

    return students

def write_data_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for _, item in enumerate(data):
            writer.writerow(item)

def main():
    parser = argparse.ArgumentParser(description='Read contents of student and courses files.')
    parser.add_argument('-s', '--students', type=str, help='Path to the student file')
    parser.add_argument('-c', '--courses', type=str, help='Path to the courses file')
    parser.add_argument('-t', '--total_courses', type=int, default=3, help='Total number of courses for student (default: 3)')


    args = parser.parse_args()

    if not (args.students and args.courses):
        parser.error('Please provide paths for all two files.')

    # Find all text files in the current folder
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        
    count = 0
    # Print the path of each text file
    for csv_file in csv_files:
        csv_file_path = os.path.join(directory, csv_file)
        
        students = read_friendship(args.students, args.total_courses)
        students = read_course_ratings(args.courses, students)
        distributions = read_distributions(csv_file_path,capacity=original_capacity)

        X, _ = friendship_bfs_yankee_swap(students, distributions)
    
        # Open the CSV file in write mode
        output_csv_file = os.path.join(output_csv_folder, str(count)+'.csv')
        count += 1
        write_data_to_csv(output_csv_file, X)

    
if __name__ == "__main__":
    main()
