import numpy as np
import random as rnd
from queue import Queue
from collections import deque

from item import Item
from student import Student

class Step:
    def __init__(self, student_recipient, student_giver, received_course, given_course, flag_bank=False):
        self.student_recipient = student_recipient
        self.student_giver = student_giver
        self.received_course = received_course
        self.given_course = given_course
        self.flag_bank = flag_bank

def sort_courses_by_friendship(friends, courses, allocation_matrix):
    sorted = [-1] * len(courses)
    value_sorted = [-1] * len(courses)

    for course in courses:
        count_friend = sum(1 for friend in friends if allocation_matrix[course][friend] == 1)
        ind_recorded = course

        for index, value in enumerate(sorted):
            if value == -1:
                sorted[index] = ind_recorded
                value_sorted[index] = count_friend
                break
            elif value_sorted[index] < count_friend:
                sorted[index], ind_recorded = ind_recorded, sorted[index]
                value_sorted[index], count_friend = count_friend, value_sorted[index] 

    return sorted

def sort_courses_by_friendship2(friends, courses, allocation_matrix, student_id):
    sorted = [-1] * len(courses)
    value_sorted = [-1] * len(courses)
    max = 0
    max_list = []

    for course in courses:
        count_friend = sum(1 for friend in friends if allocation_matrix[course][friend] == 1)
        ind_recorded = course
        if max<count_friend and allocation_matrix[course][student_id] == 1:
            max=count_friend

        for index, value in enumerate(sorted):
            if value == -1:
                sorted[index] = ind_recorded
                value_sorted[index] = count_friend
                break
            elif value_sorted[index] < count_friend:
                sorted[index], ind_recorded = ind_recorded, sorted[index]
                value_sorted[index], count_friend = count_friend, value_sorted[index]
    
    for course in courses:
        count_friend = sum(1 for friend in friends if allocation_matrix[course][friend] == 1)
        ind_recorded = course
        if max==count_friend and allocation_matrix[course][student_id] == 1:
            max_list.append(course)

    if len(max_list)>0:
        return max, max_list
    
    return max, sorted

def find_desired_course(agent_picked:Student, enrolled_courses, list_of_available_courses, allocation_matrix, method=1):
    list_of_selection_courses = list(list_of_available_courses.difference(enrolled_courses))
    max = -1
    
    if len(list_of_selection_courses) == 0:
        return -1
    
    if not agent_picked.need_desired(enrolled_courses) and len(enrolled_courses) == agent_picked.get_total_courses():
        return -1
    
    if method == 3 or method == 4:
        max, list_of_selection_courses = sort_courses_by_friendship2(agent_picked.get_only_friends(), list_of_selection_courses, allocation_matrix, agent_picked.get_student_id())
        if max>0:
            return rnd.choice(list_of_selection_courses)
        
    desired_courses = []
    list_of_selection_courses = sort_courses_by_friendship(agent_picked.get_only_friends(), list_of_selection_courses, allocation_matrix)
    for selection_course in list_of_selection_courses:
        if agent_picked.is_desired(selection_course):
            desired_courses.append(selection_course)
    
    if len(desired_courses)>0:
        return rnd.choice(desired_courses)

    return -1

def find_not_desired_course(agent_picked:Student, enrolled_courses): 
    if (len(enrolled_courses)+1) <= agent_picked.get_total_courses():
        return -1
    
    for enrolled_course in enrolled_courses:
        if not agent_picked.is_desired(enrolled_course):
            return enrolled_course
    
    return enrolled_courses[0]

def find_path(agent_picked, agents:[Student], items:[Item], allocation_matrix, method=1):
    path = []
    distances = {}

    num_students = len(agents)
    num_courses = len(items)

    list_of_available_courses = set(np.arange(num_courses).flatten())
    
    q = Queue()
    q.put(-1)

    while(not q.empty()):
        j = q.get()

        if(j == -1):
            enrolled_courses = [course_id for course_id in range(num_courses) if allocation_matrix[course_id, agent_picked] == 1]
            if method == 5:
                enrolled_courses = rnd.shuffle(enrolled_courses)
            selected_course = find_desired_course(agents[agent_picked], enrolled_courses, list_of_available_courses, allocation_matrix, method)
    
            while(selected_course != -1):
                list_of_available_courses.remove(selected_course)
                
                if(selected_course not in distances):
                    distances[selected_course] = 1
                    if(allocation_matrix[selected_course, num_students] != 0):
                        given_course = find_not_desired_course(agents[agent_picked], enrolled_courses)
                        student_giver = -1

                        step = Step(agent_picked, student_giver, selected_course, given_course, True)
                        path.append(step)

                        return selected_course, path
                       
                    q.put(selected_course)
                
            selected_course = find_desired_course(agents[agent_picked], enrolled_courses, list_of_available_courses, allocation_matrix, method)
        else: # Explore neighbors
            registred_students = [student_id for student_id in range(num_students) if allocation_matrix[j, student_id] == 1]
            if method == 5:
                registred_students = rnd.shuffle(registred_students)
            for registred_student in registred_students:
                enrolled_courses = [course_id for course_id in range(num_courses) if ((allocation_matrix[course_id, registred_student] == 1)&(course_id != j))]
                if method == 5:
                    enrolled_courses = rnd.shuffle(enrolled_courses)

                selected_course = find_desired_course(agents[registred_student], enrolled_courses, list_of_available_courses, allocation_matrix, method)

                while(selected_course != -1):
                    list_of_available_courses.remove(selected_course)

                    if(selected_course not in distances):
                        # previous_item[jprime] = j
                        # previous_agent[jprime] = iprime
                        distances[selected_course] = distances[j] + 1

                        if(allocation_matrix[selected_course, num_students] != 0):
                            return jprime, previous_agent, previous_item
                        
                        q.put(selected_course)
                    
                    selected_course = find_desired_course(agents[registred_student], enrolled_courses, list_of_available_courses, allocation_matrix, method)

    return -1, path

def calculate_intersection(agent_id, agents: [Student], num_courses, allocation_matrix):
    num_intersection = 0
    friends = agents[agent_id].get_only_friends()

    for course_id in range(num_courses):
        if allocation_matrix[course_id][agent_id] == 1:
            for index_f in friends:
                if allocation_matrix[course_id][index_f] == 1:
                    num_intersection += 1

    return num_intersection

def get_min_index(utility_vector, num_courses, agents: [Student], allocation_matrix, method):
    argmin = 1_000_000
    num_friends = 1_000_000
    min_agents = []
    min_friendship_agents = []
    

    for agent_id, utility in enumerate(utility_vector):
        if utility < 1_000:
            min_agents.append(agent_id)
        if argmin > utility:
            argmin = utility
            num_friends = calculate_intersection(agent_id, agents, num_courses, allocation_matrix)
            min_agents = []
            min_friendship_agents = []
            min_agents.append(agent_id)
            min_friendship_agents.append(agent_id)
        elif argmin == utility:
            if (method == 2 or method == 4):
                tmp_num_friends = calculate_intersection(agent_id, agents, num_courses, allocation_matrix)
                if num_friends > tmp_num_friends:
                    num_friends = tmp_num_friends
                    min_friendship_agents = []
                    min_friendship_agents.append(agent_id)
                elif num_friends == tmp_num_friends:
                  min_friendship_agents.append(agent_id)
            else:
                min_agents.append(agent_id)
    
    if method == 1 or method == 3: 
        return rnd.choice(min_agents)
    else:
        return rnd.choice(min_friendship_agents)
    

def calculate_utility(agents: [Student], items: [Item]):
    n = len(agents)
    utility = np.zeros(n, dtype=int)

    for indexI, agent in enumerate(agents):
        ratings = agent.get_course_ratings()
        utility[indexI] = sum(ratings[indexJ] for indexJ, item in enumerate(items) if item.distributions[indexI] == 1)

    return utility

def reshuffle(path:[Step], allocation_matrix, agents:[Student]):
    num_students = len(agents)
    new_allocation_matrix = np.copy(allocation_matrix)

    for step in path:
        # receive
        new_allocation_matrix[step.received_course, step.student_recipient] = 1
        if step.flag_bank:
            new_allocation_matrix[step.received_course, num_students] -= 1
        else:
            new_allocation_matrix[step.received_course, step.student_giver] = 0

        # give
        if step.given_course != -1:
            new_allocation_matrix[step.given_course, step.student_recipient] = 0
            if step.student_giver != -1:
                new_allocation_matrix[step.given_course, step.student_giver] = 1
            else:
                new_allocation_matrix[step.given_course, num_students] += 1

    return new_allocation_matrix

def find_path_original(agent_picked, agents:[Student], items:[Item], allocation_matrix, method=1):
    distances = {}
    previous_agent = {}
    previous_course = {}

    num_students = len(agents)
    num_courses = len(items)

    list_of_available_courses = set(np.arange(num_courses).flatten())
    
    q = Queue()
    q.put(-1)

    while(not q.empty()):
        j = q.get()

        if(j == -1):
            enrolled_courses = [course_id for course_id in range(num_courses) if allocation_matrix[course_id, agent_picked] == 1]
            selected_course = find_desired_course(agents[agent_picked], enrolled_courses, list_of_available_courses, allocation_matrix, method)
    
            while(selected_course != -1):
                list_of_available_courses.remove(selected_course)
                
                if(selected_course not in distances):
                    previous_course[selected_course] = -1
                    previous_agent[selected_course] = -1
                    distances[selected_course] = 1

                    if(allocation_matrix[selected_course, num_students] != 0):
                        return selected_course, previous_agent, previous_course
                       
                    q.put(selected_course)
                
                selected_course = find_desired_course(agents[agent_picked], enrolled_courses, list_of_available_courses, allocation_matrix, method)
        else: # Explore neighbors
            registred_students = [student_id for student_id in range(num_students) if allocation_matrix[j, student_id] == 1]
            rnd.shuffle(registred_students)
            for registred_student in registred_students:
            # for registred_student in [student_id for student_id in range(num_students) if allocation_matrix[j, student_id] == 1]:
                enrolled_courses = [course_id for course_id in range(num_courses) if ((allocation_matrix[course_id, registred_student] == 1)&(course_id != j))]
                
                selected_course = find_desired_course(agents[registred_student], enrolled_courses, list_of_available_courses, allocation_matrix, method)

                while(selected_course != -1):
                    list_of_available_courses.remove(selected_course)

                    if(selected_course not in distances):
                        previous_course[selected_course] = j
                        previous_agent[selected_course] = registred_student
                        distances[selected_course] = distances[j] + 1

                        if(allocation_matrix[selected_course, num_students] != 0):
                            return selected_course, previous_agent, previous_course
                        
                        q.put(selected_course)
                    
                    selected_course = find_desired_course(agents[registred_student], enrolled_courses, list_of_available_courses, allocation_matrix, method)

    return -1, previous_agent, previous_course

def augment_path(agent_picked, item, previous_agent, previous_item, allocation_matrix, num_agents):
    new_allocation_matrix = np.copy(allocation_matrix)
    item_to_move = item
    agent_to_move_from = num_agents

    if(previous_agent[item_to_move] != -1):
        new_allocation_matrix[item_to_move, previous_agent[item_to_move]] = 1
        new_allocation_matrix[item_to_move, agent_to_move_from] -= 1

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    while(previous_agent[item_to_move] != -1):
        new_allocation_matrix[item_to_move, previous_agent[item_to_move]] = 1
        new_allocation_matrix[item_to_move, agent_to_move_from] = 0

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    new_allocation_matrix[item_to_move, agent_picked] = 1
    new_allocation_matrix[item_to_move, agent_to_move_from] -= 1

    return new_allocation_matrix

def yankee_swap(agents: [Student], items: [Item], method=1):
    count = 0
    num_agents = len(agents)
    num_courses = len(items)

    #Initialize allocation matrix, players, and utility vector
    allocation_matrix = np.zeros((num_courses, num_agents+1),dtype=int)
    allocation_matrix[:,num_agents] = np.array([int(items[course_id].capacity) for course_id in range(num_courses)])

    U = set(np.arange(num_agents).flatten())
    u_vector = np.zeros(num_agents, dtype=int)
    utility_vector = np.zeros(num_agents, dtype=float)

    for course_id, item in enumerate(items):
        sum = 0
        for student_id, student in enumerate(item.distributions):
            allocation_matrix[course_id, student_id] = student
            sum += student
        allocation_matrix[course_id, num_agents] = item.capacity - sum

    print("First validation")
    validate_allocation(agents, items, allocation_matrix)
    allocation_matrix = fix_zero_allocation(agents, num_courses, allocation_matrix)
    allocation_matrix = fix_allocation(agents, items, allocation_matrix)

    u_vector = calculate_utility(agents, items)
    for indexI, u in enumerate(u_vector):
        utility_vector[indexI] = float(u)

    selected_course = -1
    previous_agent = {}
    previous_course = {}
    rnd.seed(17)
    print("Start")
    while(len(U) != 0):
        count += 1
        print("Iteration: %d" % count, end='\r')

        agent_picked = get_min_index(utility_vector, num_courses, agents, allocation_matrix, method)
        selected_course, previous_agent, previous_course = find_path_original(agent_picked, agents, items, allocation_matrix, method)
        
        if(selected_course != -1):
            allocation_matrix = augment_path(agent_picked, selected_course, previous_agent, previous_course, allocation_matrix, num_agents)
            u_vector[agent_picked] += 1
            utility_vector[agent_picked] +=1
        else:
            utility_vector[agent_picked] = 10000*num_courses
            U.remove(agent_picked)

    allocation_matrix = fix_add_allocation(agents, num_courses, method, allocation_matrix)
    print("Last validation")
    validate_allocation(agents, items, allocation_matrix)

    return allocation_matrix, u_vector

def fix_zero_allocation(agents: [Student], num_courses, allocation_matrix):
    agent_to_move_from = len(agents)
    new_allocation_matrix = np.copy(allocation_matrix)

    for student_id, agenti in enumerate(agents):
        list_for_fix = []
        bundle = [course_id for course_id in range(num_courses) if allocation_matrix[course_id, student_id] == 1]

        for item in bundle:
            if not agenti.is_desired(item):
                list_for_fix.append(item)

        for fix in list_for_fix:
            new_allocation_matrix[fix, student_id] = 0
            new_allocation_matrix[fix, agent_to_move_from] += 1
                
    return new_allocation_matrix

def filter_agents(agents: [Student], allocation_matrix):
    new_agents = []
    for  agent in agents:
        if agent.total_courses != sum(row[agent.student_id] for row in allocation_matrix):
            new_agents.append(agent)

    return new_agents

def get_min_agent(filtered_agents:[Student], agents: [Student], num_courses, allocation_matrix, method):
    agent_picked = filtered_agents[0]
    argmin = sum(row[agent_picked.student_id] for row in allocation_matrix)
    num_friends = calculate_intersection(agent_picked.student_id, agents, num_courses, allocation_matrix)

    for agent in filtered_agents:
        count_enrolled_courses = sum(row[agent.student_id] for row in allocation_matrix)
        if argmin > count_enrolled_courses:
            argmin = count_enrolled_courses
            agent_picked = agent
            num_friends = calculate_intersection(agent.student_id, agents, num_courses, allocation_matrix)
        elif (method == 2 or method == 4) and argmin == count_enrolled_courses:
            tmp_num_friends = calculate_intersection(agent.student_id, agents, num_courses, allocation_matrix)
            if num_friends > tmp_num_friends:
                agent_picked = agent
                num_friends = tmp_num_friends
    
    return agent_picked

def fix_add_allocation(agents: [Student], num_courses, method, allocation_matrix):
    agent_to_move_from = len(agents)
    new_allocation_matrix = np.copy(allocation_matrix)
    filtered_agents = filter_agents(agents, new_allocation_matrix)
    
    while(len(filtered_agents)>0):
        agent = get_min_agent(filtered_agents, agents, num_courses, new_allocation_matrix, method)
        filtered_agents.remove(agent)

        bundle = [course_id for course_id in range(num_courses) if new_allocation_matrix[course_id, agent.student_id] == 1]
        list_for_fix = [course_id for course_id in range(num_courses) if ((new_allocation_matrix[course_id, agent_to_move_from] > 0)&(new_allocation_matrix[course_id, agent.student_id]==0))]
        list_for_fix_1 = []
        list_for_fix_0 = []
        for item in list_for_fix:
            if agent.is_desired(item):
                list_for_fix_1.append(item)
            else:
                list_for_fix_0.append(item)

        if len(bundle) < agent.get_total_courses():
            diff_courses =  agent.get_total_courses() - len(bundle)
            list_for_fix_1 = sort_courses_by_friendship(agent.get_only_friends(), list_for_fix_1, new_allocation_matrix)
            if (diff_courses>0):
                if method == 1 and method == 2:
                    while(diff_courses>0):
                        random_number = rnd.choice(list_for_fix_1)
                        new_allocation_matrix[random_number, agent.student_id] = 1
                        new_allocation_matrix[random_number, agent_to_move_from] -= 1
                        diff_courses-=1
                else:
                    for fix in list_for_fix_1:
                        new_allocation_matrix[fix, agent.student_id] = 1
                        new_allocation_matrix[fix, agent_to_move_from] -= 1
                        diff_courses-=1
                        if (diff_courses==0):
                            break
        
        bundle = [course_id for course_id in range(num_courses) if new_allocation_matrix[course_id, agent.student_id] == 1]
        if len(bundle) < agent.get_total_courses():
            diff_courses =  agent.get_total_courses() - len(bundle)
            list_for_fix_0 = sort_courses_by_friendship(agent.get_only_friends(), list_for_fix_0, new_allocation_matrix)
            
            if (diff_courses>0):
                if method == 1 and method == 2:
                    while(diff_courses>0):
                        random_number = rnd.choice(list_for_fix_0)
                        new_allocation_matrix[random_number, agent.student_id] = 1
                        new_allocation_matrix[random_number, agent_to_move_from] -= 1
                        diff_courses-=1

                else:
                    for fix in list_for_fix_0:
                        new_allocation_matrix[fix, agent.student_id] = 1
                        new_allocation_matrix[fix, agent_to_move_from] -= 1
                        diff_courses-=1
                        if (diff_courses==0):
                            break
           
    return new_allocation_matrix

def validate_allocation(agents: [Student], items: [Item], allocation_matrix):
    # students in course
    for course_id, course in enumerate(items):
        count_student = sum(allocation_matrix[course_id][:-1])
        if count_student > course.capacity:
            print(f"Warning capacity {course.capacity} != {count_student}")
    
    # courses for student
    for student_id, student in enumerate(agents):
        count_course = sum(row[student_id] for row in allocation_matrix)
        if count_course > student.total_courses or count_course!=3:
            print(f"Warning student courses studentID={student_id} {student.total_courses} != {count_course}")

def fix_allocation(agents: [Student], items: [Item], allocation_matrix):
    new_allocation_matrix = np.copy(allocation_matrix)
    # students in course
    for course_id, course in enumerate(items):
        count_student = sum(allocation_matrix[course_id][:-1])
        if count_student > course.capacity:
            new_allocation_matrix[course_id, len(agents)] = 0

    return new_allocation_matrix

def find_not_desired(agent: Student, allocation_matrix):
    not_desired = []

    for selection_course, row in enumerate(allocation_matrix):
        id = agent.student_id
        if row[id] == 1 and not(agent.is_desired(selection_course)):
            not_desired.append(selection_course)

    return not_desired