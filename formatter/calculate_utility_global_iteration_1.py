import os
import re
import csv

import numpy as np
import pandas as pd

# Define the directory paths
directory_input = 'C:\\Users\\superup\\yankee_swap_2\\formatter\\formated'
directory_output = 'C:\\Users\\superup\\yankee_swap_2\\formatter\\accumulate'

# Define the input file paths
courses_input = 'C:\\Users\\superup\\yankee_swap_2\\formatter\\input\\courses_0_1.csv'
friendship1_input = 'C:\\Users\\superup\\yankee_swap_2\\formatter\\input\\friendship_0_1.csv'
total_output = 'C:\\Users\\superup\\yankee_swap_2\\formatter\\accumulate\\total_output.csv'
global_total_output = 'C:\\Users\\superup\\yankee_swap_2\\formatter\\accumulate\\global_total_output.csv'
fw = 1
flag_friendship = True
flag_course = True
flag_distribution = True
flag_course_limit = True

global_csv_base_0=1
global_csv_base_rnd=0
global_csv_base_dsa_rc=0
global_csv_method=1
exp_num=1


class Student:
    def __init__(self, student_id):
        self.student_id = student_id
        self.friends = []
        self.only_friends = []
        self.course_ratings = []
        self.course_utility = 0
        self.friends_utility = 0
        self.total_utility = 0

    def add_courses(self, rating):
        self.course_ratings = rating

    def add_friends(self, friends):
        self.friends = friends
        self.only_friends = [index for index, value in enumerate(friends) if value != 0]
    
    def get_friend(self, indFriend):
        return self.friends[indFriend]
    
    def get_only_friends(self):
        return self.only_friends
    
    def get_course_rating(self, indCourse):
        return self.course_ratings[indCourse]
    
    def set_course_utility(self, utility):
        self.course_utility = utility
    
    def get_course_utility(self):
        return self.course_utility

    def set_total_utility(self, utility):
        self.total_utility = utility
    
    def get_total_utility(self):
        return self.total_utility

    def set_friends_utility(self, utility):
        self.friends_utility = utility
    
    def get_friends_utility(self):
        return self.friends_utility

def read_friendship(file_name):
    students = []

    try:
        with open(file_name, 'r') as file:
            for line_number, line in enumerate(file, start=0):
                if ( flag_friendship and line_number == 0):
                    continue
                elements = line.strip().split(',')
                array_representation = np.array(elements, dtype=int)
                student = Student(line_number-1)
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
                if (flag_course and line_number == 0):
                    continue
                elements = line.strip().split(',')
                array_representation = np.array(elements, dtype=int)
                students[line_number-1].add_courses(array_representation)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
        exit()
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")
        exit()

    return students

def calculate_friendship_utility(studentI, index_course, allocation, friendship_weight=0):
    friends = studentI.get_only_friends()
    friendship_utility = 0

    for friend in friends:
        friendship_utility += allocation[friend][index_course] * studentI.get_friend(friend) * friendship_weight

    return friendship_utility

def calculate_utility(students, student_id, student_allocation, allocation, friendship_weight=0):
    utility = 0
    friendship_utility = 0

    for index, value in enumerate(student_allocation):
        utility += value * students[student_id].get_course_rating(index)
        # Calculate only desired courses
        # if value==0 or students[student_id].get_course_rating(index)==0:
        #     continue
        if value==0:
            continue
        friendship_utility += calculate_friendship_utility(students[student_id], index, allocation, friendship_weight)

    return utility, friendship_utility

def gini_coef(students, total_cost):
    coef = 0
    mean = 0
    number_of_assigned_variables = len(students)

    mean = total_cost / number_of_assigned_variables

    for i in range(number_of_assigned_variables):
        for j in range(number_of_assigned_variables):
            coef += abs(students[i].get_total_utility() - students[j].get_total_utility())

    coef /= 2 * number_of_assigned_variables ** 2 * mean

    return coef * 100

def extract_course_limit(folder_name):
    # Define the regular expression pattern to match the number before '_courseLimit_'
    pattern = r'(\d+)_courseLimit_'
    
    # Search for the pattern in the folder name
    match = re.search(pattern, folder_name)
    
    if match:
        # Extract the number and convert it to an integer
        return int(match.group(1))
    else:
        # If the pattern is not found, raise an error or handle it as needed
        raise ValueError("courseLimit not found in folder name")
        exit()
    
def write_global_row(total_utility, gini, num_exp, course_limit):
    row ={
        'exp#': num_exp,
        'utility_YS': 0, 
        'utility_YS_order': 0, 
        'utility_YS_course': 0, 
        'utility_YS_both': 0, 
        'gini_YS': 0, 
        'gini_YS_order': 0, 
        'gini_YS_course':0, 
        'gini_YS_both':0, 
        'base_0': global_csv_base_0, 
        'base_rnd': global_csv_base_rnd, 
        'base_DSA_RC': global_csv_base_dsa_rc, 
        'cl_60':0,
        'cl_65':0, 
        'cl_70':0, 
        'cl_75':0, 
        'cl_80':0, 
        'cl_85':0, 
        'cl_90':0, 
        'friendship_w_0':0, 
        'friendship_w_1':0
    }

    # friendship
    if fw==0:
        row['friendship_w_0'] = 1
    else:
        row['friendship_w_1'] = 1

    # method
    match global_csv_method:
        case 1:
            row['utility_YS'] = total_utility
            row['gini_YS'] = gini
        case 2:
            row['utility_YS_order'] = total_utility
            row['gini_YS_order'] = gini
        case 3:
            row['utility_YS_course'] = total_utility
            row['gini_YS_course'] = gini
        case 4:
            row['utility_YS_both'] = total_utility
            row['gini_YS_both'] = gini
    
    # folder
    match course_limit:
        case 60:
            row['cl_60'] = 1
        case 65:
            row['cl_65'] = 1
        case 70:
            row['cl_70'] = 1
        case 75:
            row['cl_75'] = 1
        case 80:
            row['cl_80'] = 1
        case 85:
            row['cl_85'] = 1
        case 90:
            row['cl_90'] = 1

    return row

students = read_friendship(friendship1_input)
students = read_course_ratings(courses_input, students)

# Get all directories in the specified directory
folders = [folder for folder in os.listdir(directory_input) if os.path.isdir(os.path.join(directory_input, folder))]

num_exp = exp_num
# Iterate over each folder in the "formated" directory
for folder_name in folders:
    print(f"Start folder '{folder_name}'")
    course_limit = extract_course_limit(folder_name)
    accumulate_foldername = folder_name.replace("formated", "accumulate")
    folder_path = os.path.join(directory_input, folder_name)

    output_row = {
        'folder_name': folder_name, 
        'total_course_utility': 0, 
        'total_friends_utility': 0, 
        'total_utility': 0, 
        'gini_coef': 0
    }
    num_csv_files = 0

    # Check if the current item is a directory
    if os.path.isdir(folder_path):
        # Find all text files in the current folder
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    
        with open(global_total_output, mode='a', newline='') as csvfile:
            fieldnames = ['exp#', 'utility_YS', 'utility_YS_order', 'utility_YS_course', 'utility_YS_both', 'gini_YS', 'gini_YS_order', 'gini_YS_course', 'gini_YS_both', 'base_0', 'base_rnd', 'base_DSA_RC', 'cl_60',
                          'cl_65', 'cl_70', 'cl_75', 'cl_80', 'cl_85', 'cl_90', 'friendship_w_0', 'friendship_w_1']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
            # If the file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()
            
            num_csv_files = len(csv_files)
            for csv_file in csv_files:
                gini = 0
                total_utility = 0
                total_course_utility = 0
                total_friends_utility = 0

                csv_file_path = os.path.join(directory_input, folder_name, csv_file)
                allocation = []
                with open(csv_file_path, 'r') as file:
                    for line_number, line in enumerate(file, start=0):
                        if (flag_distribution and line_number == 0):
                            continue
                        elements = line.strip().split(',')
                        if (flag_distribution):
                            elements = elements[1:]
                        array_representation = np.array(elements, dtype=int)
                        allocation.append(array_representation)

                with open(csv_file_path, 'r') as file:
                    for line_number, line in enumerate(file, start=0):
                        if (flag_distribution and line_number == 0):
                            continue
                        index_student = line_number - 1
                        elements = line.strip().split(',')
                        if (flag_distribution):
                            elements = elements[1:]
                        array_representation = np.array(elements, dtype=int)
                        utility, friendship_utility = calculate_utility(students, index_student, array_representation, allocation, friendship_weight=fw)

                        students[index_student].set_course_utility(utility)
                        students[index_student].set_friends_utility(friendship_utility)
                        students[index_student].set_total_utility(utility+friendship_utility)

                        total_utility += utility + friendship_utility
                        total_course_utility += utility
                        total_friends_utility += friendship_utility

                gini = gini_coef(students, total_utility)
                gini = round(gini, 2)

                row = write_global_row(total_utility, gini, num_exp, course_limit)
                writer.writerow(row)
                num_exp += 1

                output_row['total_course_utility'] += total_course_utility
                output_row['total_friends_utility'] += total_friends_utility
                output_row['total_utility'] += total_utility
                output_row['gini_coef'] += gini
            
    
    output_row['total_course_utility'] = round(output_row['total_course_utility'] / num_csv_files, 2)
    output_row['total_friends_utility'] = round(output_row['total_friends_utility'] / num_csv_files, 2)
    output_row['total_utility'] = round(output_row['total_utility'] / num_csv_files, 2)
    output_row['gini_coef'] = round(output_row['gini_coef'] / num_csv_files, 2)

    with open(total_output, mode='a', newline='') as file:
        fieldnames = ['folder_name', 'total_course_utility', 'total_friends_utility', 'total_utility', 'gini_coef']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
    
        # If the file is empty, write the header
        if file.tell() == 0:
            writer.writeheader()
        
        writer.writerow(output_row)
    
   