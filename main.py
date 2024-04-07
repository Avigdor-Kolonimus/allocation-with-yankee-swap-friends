import argparse
import numpy as np
import pandas as pd

from item import Item
from student import Student
from algo_bfs import bfs_yankee_swap
from algo import yankee_swap, yankee_swap_continue

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

def read_distributions(file_name):
    distributions = []

    try:
        df = pd.read_csv(file_name, sep=",", header=0)
        
        for index, row in df.iterrows():
            item = Item(index, int(row['capacity']))
            array_representation = np.array(row)[:-1] 
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

def main():
    parser = argparse.ArgumentParser(description='Read contents of student, courses, and distributions files.')
    parser.add_argument('-s', '--students', type=str, help='Path to the student file')
    parser.add_argument('-c', '--courses', type=str, help='Path to the courses file')
    parser.add_argument('-d', '--distributions', type=str, help='Path to the distributions file')
    parser.add_argument('-t', '--total_courses', type=int, default=3, help='Total number of courses for student (default: 3)')


    args = parser.parse_args()

    if not (args.students and args.courses and args.distributions):
        parser.error('Please provide paths for all three files.')

    students = read_friendship(args.students, args.total_courses)
    students = read_course_ratings(args.courses, students)
    distributions = read_distributions(args.distributions)


    # print("Students:")
    # for student in students:
    #     print(f"Student ID: {student.student_id}, Friends: {student.get_friends()}, Courses: {student.get_course_ratings()}")
    
    # print("\nDistributions:")
    # for item in distributions:
    #     print(f"Course ID: {item.course_id}, Capacity: {item.capacity}, Distributions: {item.distributions}")
    
    # X, utility = yankee_swap(students, distributions)
    # X, utility = yankee_swap_continue(students, distributions)
    X, utility = bfs_yankee_swap(students, distributions)

    print("\nUtility: ", utility)
    for course_id,item in enumerate(X):
        print(f"Course ID: {course_id}, Capacity: {item[len(item)-1]}, Distributions: {item}")
    
    # for item in distributions:
    #     print(f"Course ID: {item.course_id}, Capacity: {item.capacity}, Distributions: {item.distributions}")
    
if __name__ == "__main__":
    main()
