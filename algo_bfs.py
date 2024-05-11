import numpy as np
from queue import Queue

from item import Item
from student import Student

def find_desired(i, bundle, list_of_yes, agents, items):
    agenti = agents[i]
    list_of_yesses = list(list_of_yes.difference(bundle))

    if len(list_of_yesses)==0:
        return -1
    
    if not agenti.need_desired(bundle) and len(bundle)==agenti.get_total_courses():
        return -1
    
    for yes in list_of_yesses:
        if agenti.is_desired(yes):
            return yes
    
    if len(bundle)<agenti.get_total_courses():
        return list_of_yesses[0]
    
    return -1

def find_not_desired(i, bundle, agents):
    agenti = agents[i]
    
    if (len(bundle)+1)<=agenti.get_total_courses():
        return -1
    
    for item in bundle:
        if not agenti.is_desired(item):
            return item
    
    return bundle[0]

def agree_exchange(i, course, agents):
    agenti = agents[i]

    if agenti.is_desired(course):
        return True
    
    return False

def get_distances(i, agents, items, allocation_matrix):
    distances = {}
    previous_agent = {}
    previous_item = {}

    n = len(agents)
    m = len(items)

    q = Queue()
    q.put(-1)

    list_of_yes = set(np.arange(m).flatten())
    
    while(not q.empty()):
        j = q.get()

        if(j == -1):
            bundle = [jdash for jdash in range(m) if allocation_matrix[jdash,i] == 1]

            jprime = find_desired(i, bundle, list_of_yes, agents, items)
            
            while(jprime != -1):
                list_of_yes.remove(jprime)
                
                if(jprime not in distances):
                    previous_item[jprime] = -1
                    previous_agent[jprime] = -1
                    distances[jprime] = 1
                    
                    if(allocation_matrix[jprime,n] != 0):
                        previous_item[jprime] = find_not_desired(i,bundle,agents)
                        return jprime, previous_agent, previous_item
                    
                    q.put(jprime)
                
                jprime = find_desired(i, bundle, list_of_yes, agents, items)
        else:
            for iprime in [idash for idash in range(n) if allocation_matrix[j,idash] == 1]:
                print("Student #",iprime)
                bundle = [jdash for jdash in range(len(items)) if ((allocation_matrix[jdash,iprime] == 1)&(jdash != j))]
                jprime = find_desired(iprime, bundle, list_of_yes, agents, items)
                
                while(jprime != -1):
                    list_of_yes.remove(jprime)
                    
                    if(jprime not in distances):
                        previous_item[jprime] = j
                        previous_agent[jprime] = iprime
                        distances[jprime] = distances[j] + 1
                        
                        print("allocation_matrix[jprime,n]", allocation_matrix[jprime,n], " agree_exchange(iprime, j, agents)", agree_exchange(iprime, j, agents))
                        if(allocation_matrix[jprime,n] != 0 or agree_exchange(iprime, j, agents)):
                            return jprime, previous_agent, previous_item
                        
                        q.put(jprime)
                    
                    jprime = find_desired(iprime, bundle, list_of_yes, agents, items)

    return -1, previous_agent, previous_item

def augment_path(i, item, previous_agent, previous_item, allocation_matrix, agents):
    n = len(agents)

    new_allocation_matrix = np.copy(allocation_matrix)
    item_to_move = item
    agent_to_move_from = n

    # exchange your favorite course with your least favorite one
    if len(previous_agent)<2 and previous_item[item_to_move] != -1:
        new_allocation_matrix[previous_item[item_to_move],i] = 0
        new_allocation_matrix[previous_item[item_to_move],agent_to_move_from] += 1

        new_allocation_matrix[item_to_move,i] = 1
        new_allocation_matrix[item_to_move,agent_to_move_from] -= 1
    else:
        if(previous_agent[item_to_move] != -1):
            new_allocation_matrix[item_to_move,i] = 0
            new_allocation_matrix[item_to_move,agent_to_move_from] += 1

        while(previous_agent[item_to_move] != -1):
            new_allocation_matrix[item_to_move,previous_agent[item_to_move]] = 1
            new_allocation_matrix[item_to_move,agent_to_move_from] -= 1

            agent_to_move_from = previous_agent[item_to_move]
            item_to_move = previous_item[item_to_move]
            

        new_allocation_matrix[item_to_move,i] = 1
        new_allocation_matrix[item_to_move,agent_to_move_from] -= 1

    return new_allocation_matrix

def calculate_utility(agents: [Student], items: [Item]):
    n = len(agents)
    utility = np.zeros(n, dtype=int)

    for indexI, agent in enumerate(agents):
        ratings = agent.get_course_ratings()
        utility[indexI] = sum(ratings[indexJ] for indexJ, item in enumerate(items) if item.distributions[indexI] == 1)

    return utility

def bfs_yankee_swap(agents: [Student], items: [Item]):
    count = 0
    n = len(agents)
    m = len(items)

    #Initialize allocation matrix, players, and utility vector
    allocation_matrix = np.zeros((m,n+1),dtype=int)
    allocation_matrix[:,n] = np.array([int(items[j].capacity) for j in range(m)])
    U = set(np.arange(n).flatten())
    u_vector = np.zeros(n, dtype=int)
    utility_vector = np.zeros(n, dtype=float)

    for indexI, item in enumerate(items):
        sum = 0
        for indexJ, student in enumerate(item.distributions):
            allocation_matrix[indexI,indexJ] = student
            sum += student
        allocation_matrix[indexI,n] = item.capacity - sum

    u_vector = calculate_utility(agents, items)
    for indexI, u in enumerate(u_vector):
        utility_vector[indexI] = float(u)

    while(len(U) != 0):
        count += 1
        print("Iteration: %d" % count, end='\r')

        agent_picked = np.argmin(utility_vector)
        print("agent_picked = ", agent_picked)
        item, previous_agent, previous_item = get_distances(agent_picked, agents, items, allocation_matrix)
        print("item=", item, " previous_agent=",  previous_agent, " previous_item=", previous_item)

        if(item != -1):
            allocation_matrix = augment_path(agent_picked, item, previous_agent, previous_item, allocation_matrix, agents)
            u_vector[agent_picked] += 1
            utility_vector[agent_picked] +=1
        else:
            utility_vector[agent_picked] = 10000*m
            U.remove(agent_picked)

    print("USW:", np.sum(u_vector))

    return allocation_matrix, u_vector