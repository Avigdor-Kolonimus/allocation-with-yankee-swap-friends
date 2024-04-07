import random

import numpy as np

from player import Player
from student import Student
from item import Item

def initialize_players(students: [Student]):
    players = []

    for index, student in enumerate(students):
        player = Player(index, student.get_total_courses())
        players.append(player)

    return players

def pick_player(players):
    picked_player = random.choice(players)
    index = players.index(picked_player)

    num_pick = players[index].dec_num_picks()

    return picked_player, num_pick == 0

def pick_min_utility_player(players, students: [Student], items: [Item]):
    min_utility = 999
    picked_player = players[0]
    index_picked_player = 0

    for player_index, player in enumerate(players):
        student = students[player.get_player_id()]
        student_utility = 0

        for course in items:
            student_utility = student_utility + calculate_union_utility(student, course)

        if min_utility <= student_utility:
            picked_player = player.get_player_id()
            min_utility = student_utility
            index_picked_player = player_index

    num_pick = players[index_picked_player].dec_num_picks()

    return picked_player, num_pick == 0

def calculate_utility(students, items):
    utility = 0

    for iIndex, student in enumerate(students):
        ratings = student.get_course_ratings()
        utility += sum(ratings[jIndex] for jIndex, item in enumerate(items) if item.distributions[iIndex] == 1)

    return utility

def find_replacement_c(student_index:int, students: [Student], items: [Item]):
    sorted_indices = students[student_index].get_sorted_indices()
    student_courses = []

    for iIndex, cours in enumerate(items): 
        if cours.distributions[student_index] == 1:
            student_courses.append(iIndex)

    i = 0
    j = len(sorted_indices) - 1
    
    while (i < j):
        max_index = sorted_indices[i]
        min_index = sorted_indices[j]

        if max_index not in student_courses:
            total_students = sum(items[max_index].distributions)
            if total_students < items[max_index].get_capacity():
                while (i < j):
                    if min_index in student_courses:
                        return True, False, max_index, min_index, 0
                    j -= 1
                    min_index = sorted_indices[j]

                return False, False, 0, 0, 0

            wanted_rank = students[student_index].get_course_rating[max_index]
            not_wanted_rank = students[student_index].get_course_rating[min_index]

            if min_index in student_courses and wanted_rank > not_wanted_rank:
                distributions = items[min_index].get_distributions()

                for swap_index, value in enumerate(distributions):
                        if swap_index != student_index and value == 1:
                            if items[max_index].distributions[swap_index] == 0:
                                return False, True, max_index, min_index, swap_index
            else:
                j -= 1
        else:
            i += 1
    
    return False, False, 0, 0, 0

def calculate_friends_utility(only_friends:[int], friends:[int], course: [Item]):
    utility = 0
    distributions = course.get_distributions()
    
    for friend in only_friends:
        if distributions[friend] == 1:
           utility +=  friends[friend]

    return  utility     

def calculate_union_utility(student: Student, course: Item):
    utility = student.get_course_rating(course.get_course_id()) + calculate_friends_utility(student.get_only_friends(), student.get_friends(), course)

    return utility

def calculate_penalty(exchange_course:int, course_index:int, student: Student, items: [Item]):
    student_index = student.get_student_id()
    distributions = items[course_index].distributions
    total_students = sum(distributions)
    if total_students < items[course_index].get_capacity():
        return True, False, 0, -1
    
    min_penalty = 999
    exchange_student = -1
    for swap_index, value in enumerate(distributions):
        if swap_index != student_index and value == 1:
            if items[exchange_course].distributions[swap_index] == 0:
                if min_penalty > student.get_friend(swap_index):
                    exchange_student = swap_index
                    min_penalty = student.get_friend(swap_index)
                    
                    if min_penalty == 0:
                        return False, True, min_penalty, exchange_student
            
    return False, True, min_penalty, exchange_student

def find_replacement_c_f(student_index:int, students: [Student], items: [Item]):
    student_courses = []
    no_student_courses = []
    
    enroll_courses = [0] * len(items)
    no_enroll_courses = [0] * len(items)

    for iIndex, course in enumerate(items): 
        if course.distributions[student_index] == 1:
            student_courses.append(iIndex)
            enroll_courses[iIndex] = calculate_union_utility(students[student_index], items[iIndex])
        else:
            no_enroll_courses[iIndex] = calculate_union_utility(students[student_index], items[iIndex])
            if no_enroll_courses[iIndex] != 0:
                no_student_courses.append(iIndex)

    enroll_course = -1
    no_enroll_course = -1
    exchange_student = -1
    gap = 0
    free_place = False
    is_find = False
    for student_course in student_courses: 
        course_utility = enroll_courses[student_course]
        
        for no_student_course in no_student_courses:
            calculated_free_place, calculated_is_find, penalty, swap_student = calculate_penalty(no_student_course, student_course, students[student_index], items)
            calculated_gap = no_enroll_courses[no_student_course] - penalty
            calculated_gap -= course_utility
            
            if gap < calculated_gap:
                enroll_course = student_course
                no_enroll_course = no_student_course
                exchange_student = swap_student
                gap = calculated_gap
                free_place = calculated_free_place
                is_find = calculated_is_find

    return free_place, is_find, no_enroll_course, enroll_course, exchange_student

def yankee_swap(students: [Student], items: [Item]):
    random.seed(0)
    np.random.seed(0)

    count = 0
    X = items
    players = initialize_players(students)
    
    while len(players)>0:
        count += 1
        # picked_player, remove = pick_player(players)
        picked_player, remove = pick_min_utility_player(players, students, items)
        student_index = picked_player.get_player_id()
        # si = students[picked_player.get_player_id()].get_sorted_indices()
        # print("Sorted indexes: ", si)

        # free_place, is_find, max_index, min_index, swap_index = find_replacement_c(student_index, students, items)
        free_place, is_find, max_index, min_index, swap_index = find_replacement_c_f(student_index, students, items)
        if free_place:
            items[max_index].distributions[student_index] = 1
            items[min_index].distributions[student_index] = 0
        
        if is_find:
            items[max_index].distributions[student_index] = 1
            items[min_index].distributions[student_index] = 0

            items[max_index].distributions[swap_index] = 0
            items[min_index].distributions[swap_index] = 1

        if remove:
            players.remove(picked_player)
        

    print("Summary iterations: ", count)

    utility = calculate_utility(students, X)

    return X, utility

def calculate_penalty_continue(exchange_course:int, course_index:int, student: Student, items: [Item], p_list):
    student_index = student.get_student_id()
    distributions = items[course_index].distributions
    total_students = sum(distributions)
    if total_students <= items[course_index].get_capacity():
        return True, False, 0, -1
    
    min_penalty = 999
    exchange_student = -1
    for swap_index, value in enumerate(distributions):
        if swap_index != student_index and value == 1 and not(p_list.get(swap_index, False)):
            if items[exchange_course].distributions[swap_index] == 0:
                if min_penalty > student.get_friend(swap_index):
                    exchange_student = swap_index
                    min_penalty = student.get_friend(swap_index)
                    
                    if min_penalty == 0:
                        return False, True, min_penalty, exchange_student
            
    return False, True, min_penalty, exchange_student

def find_replacement_c_f_continue(student_index:int, students: [Student], items: [Item], p_list):
    student_courses = []
    no_student_courses = []
    
    enroll_courses = [0] * len(items)
    no_enroll_courses = [0] * len(items)

    for iIndex, course in enumerate(items): 
        if course.distributions[student_index] == 1:
            student_courses.append(iIndex)
            enroll_courses[iIndex] = calculate_union_utility(students[student_index], items[iIndex])
        else:
            no_enroll_courses[iIndex] = calculate_union_utility(students[student_index], items[iIndex])
            if no_enroll_courses[iIndex] != 0:
                no_student_courses.append(iIndex)

    enroll_course = -1
    no_enroll_course = -1
    exchange_student = -1
    gap = 0
    free_place = False
    is_find = False

    for student_course in student_courses: 
        course_utility = enroll_courses[student_course]
        
        for no_student_course in no_student_courses:
            calculated_free_place, calculated_is_find, penalty, swap_student = calculate_penalty_continue(no_student_course, student_course, students[student_index], items, p_list)
            calculated_gap = no_enroll_courses[no_student_course] - penalty
            calculated_gap -= course_utility
            
            if gap < calculated_gap:
                enroll_course = student_course
                no_enroll_course = no_student_course
                exchange_student = swap_student
                gap = calculated_gap
                free_place = calculated_free_place
                is_find = calculated_is_find

    return free_place, is_find, no_enroll_course, enroll_course, exchange_student

def yankee_swap_continue(students: [Student], items: [Item]):
    random.seed(0)
    np.random.seed(0)

    count = 0
    X = items
    players = initialize_players(students)
    pick_player = True
    p_list = {}

    while len(players)>0:
        if pick_player:
            count += 1
            picked_player, remove = pick_min_utility_player(players, students, items)
            student_index = picked_player.get_player_id()
            p_list[student_index] = True

        free_place, is_find, max_index, min_index, swap_index = find_replacement_c_f_continue(student_index, students, items, p_list)
        if free_place:
            items[max_index].distributions[student_index] = 1
            items[min_index].distributions[student_index] = 0
            p_list = {}
            pick_player = True
        
        if is_find:
            items[max_index].distributions[student_index] = 1
            items[min_index].distributions[student_index] = 0

            items[max_index].distributions[swap_index] = 0
            items[min_index].distributions[swap_index] = 1
            p_list[swap_index] = True
            pick_player = False
            student_index = swap_index
        
        if not(free_place) and not(is_find):
            p_list = {}
            pick_player = True

        if remove:
            players.remove(picked_player)
            remove = False
        

    print("Summary iterations: ", count)

    utility = calculate_utility(students, X)

    return X, utility