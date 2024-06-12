import os
import csv

import numpy as np
import pandas as pd

# Define the directory paths
directory_input = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\formated'
directory_output = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\accumulate'

# Define the input file paths
courses_input = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\input\\courses_50.csv'
friendship1_input = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\input\\friendship1_50.csv'
total_output = 'C:\\Users\\superup\\yankee_swap_alg\\formatter\\accumulate\\total_output.csv'

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
        df = pd.read_csv(file_name, sep=",", header=1)
        
        for index, row in df.iterrows():
            array_representation = np.array(row)
            student = Student(index)
            student.add_friends(array_representation)
            students.append(student)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")

    return students

def read_course_ratings(file_name, students):
    try:
        df = pd.read_csv(file_name, sep=",", header=1)
        
        for index, row in df.iterrows():
            array_representation = np.array(row)
            students[index].add_courses(array_representation)

    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")

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

students = read_friendship(friendship1_input)
students = read_course_ratings(courses_input, students)

# Get all directories in the specified directory
folders = [folder for folder in os.listdir(directory_input) if os.path.isdir(os.path.join(directory_input, folder))]

# Iterate over each folder in the "formated" directory
for folder_name in folders:
    print(f"Start folder '{folder_name}'")
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

        accumulate_csv_file_path = os.path.join(directory_output, accumulate_foldername, 'output.csv')
        with open(accumulate_csv_file_path, mode='w', newline='') as csvfile:
            fieldnames = ['name_file', 'total_course_utility', 'total_friends_utility', 'total_utility', 'gini_coef']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            num_csv_files = len(csv_files)
            for csv_file in csv_files:
                gini = 0
                total_utility = 0
                total_course_utility = 0
                total_friends_utility = 0

                csv_file_path = os.path.join(directory_input, folder_name, csv_file)
                df = pd.read_csv(csv_file_path, sep=",", header=None)
        
                allocation = []
                for _, row in df.iterrows():
                    array_representation = np.array(row)[1:] 
                    allocation.append(array_representation)

                for index_student, row in df.iterrows():
                    array_representation = np.array(row)[1:] 
                    utility, friendship_utility = calculate_utility(students, index_student, array_representation, allocation, friendship_weight=1)

                    students[index_student].set_course_utility(utility)
                    students[index_student].set_friends_utility(friendship_utility)
                    students[index_student].set_total_utility(utility+friendship_utility)

                    total_utility += utility + friendship_utility
                    total_course_utility += utility
                    total_friends_utility += friendship_utility

                    # print(f"Student ID '{row['student']}' courses '{array_representation}' utility '{utility}' friendship_utility '{friendship_utility}'")

                gini = gini_coef(students, total_utility)
                gini = round(gini, 2)

                # print(f"total_utility '{total_utility}' total_course_utility '{total_course_utility}' total_friends_utility '{total_friends_utility}' gini_coef '{gini}'")
                row = {
                    'name_file': csv_file, 
                    'total_course_utility': total_course_utility, 
                    'total_friends_utility': total_friends_utility, 
                    'total_utility': total_utility, 
                    'gini_coef': gini
                }
                writer.writerow(row)

                output_row['total_course_utility'] += total_course_utility
                output_row['total_friends_utility'] += total_friends_utility
                output_row['total_utility'] += total_utility
                output_row['gini_coef'] += gini

                # print(csv_file)
            
    
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
    
   