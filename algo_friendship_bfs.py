from student import Student

def calculate_intersection(i, agents: [Student], num_courses, allocation_matrix):
    num_intersection = 0
    friends = agents[i].get_only_friends()

    for jdash in range(num_courses):
        if allocation_matrix[jdash,i] == 1:
            for index_f in friends:
                if allocation_matrix[jdash,index_f] == 1:
                    num_intersection += 1

    return num_intersection

def get_min_index(utility_vector, num_courses, agents: [Student], allocation_matrix):
    agent_picked = 0
    argmin = 1_000_000
    num_friends = 1_000_000

    for indexI, utility in enumerate(utility_vector):
        if argmin > utility:
            argmin = utility
            agent_picked = indexI
            num_friends = calculate_intersection(indexI, agents, num_courses, allocation_matrix)
        elif argmin == utility:
            tmp_num_friends = calculate_intersection(indexI, agents, num_courses, allocation_matrix)
            if num_friends > tmp_num_friends:
                agent_picked = indexI
                num_friends = tmp_num_friends
    
    return agent_picked
