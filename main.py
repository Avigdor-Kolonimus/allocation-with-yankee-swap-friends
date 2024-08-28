import os
import csv
import argparse
import numpy as np

from item import Item
from student import Student
from algo import yankee_swap

# Define the directory path
directory = 'PATH\\TO\\input\\0w\\60_courseLimit_0_weight'

# Define the output CSV file path
output_csv_folder = 'PATH\\TO\\output\\0w\\60_courseLimit_0_weight'

original_capacity = 60
method = 1
flag_friendship = True
flag_course = True
flag_distribution = True
flag_course_limit = False

def read_friendship(file_name, total_courses=3):
    students = []

    try:
        with open(file_name, 'r') as file:
            for line_number, line in enumerate(file, start=0):
                if (flag_friendship and line_number==0):
                    continue
                
                elements = line.strip().split(',')
                array_representation = np.array(elements, dtype=int)
                id = line_number
                if flag_friendship:
                    id -= 1
                student = Student(id, total_courses)
                student.add_friends(array_representation)
                students.append(student)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
        exit()
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")
        exit()

    return students

def read_course_ratings(file_name, students):
    try:
        with open(file_name, 'r') as file:
            for line_number, line in enumerate(file, start=0):
                if (flag_course and line_number==0):
                    continue

                elements = line.strip().split(',')
                array_representation = np.array(elements, dtype=int)
                id = line_number
                if flag_course:
                    id -= 1
                students[id].add_courses(array_representation)
      
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        exit()
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")
        exit()

    return students

def read_distributions(file_name, capacity):
    distributions = []

    try:
        with open(file_name, 'r') as file:
            for line_number, line in enumerate(file, start=0):
                if (flag_distribution and line_number == 0):
                    continue

                elements = line.strip().split(',')
                if flag_course_limit:
                    elements = elements[:-1]
                array_representation = np.array(elements, dtype=int)
                id = line_number
                if flag_distribution:
                    id -= 1
                item = Item(id, capacity)
                item.add_distributions(array_representation)
                distributions.append(item)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
        exit()
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")
        exit()

    return distributions

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
        for i in range(1, 51):
            print("Start work with csv_file: ", csv_file)
            csv_file_path = os.path.join(directory, csv_file)
        
            students = read_friendship(args.students, args.total_courses)
            students = read_course_ratings(args.courses, students)
            distributions = read_distributions(csv_file_path,capacity=original_capacity)

            X, _ = yankee_swap(students, distributions, method)

            # Open the CSV file in write mode
            output_csv_file = os.path.join(output_csv_folder, str(count)+'_'+str(i)+'.csv')
            print("Stop work with csv_file, output csv: ", output_csv_file)
            count += 1
            write_data_to_csv(output_csv_file, X)

    
if __name__ == "__main__":
    main()
