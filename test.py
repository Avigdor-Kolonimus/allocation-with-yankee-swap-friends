import unittest
import numpy as np

from item import Item
from student import Student
from algo import Step, get_min_agent, filter_agents, fix_add_allocation, fix_zero_allocation, reshuffle, find_not_desired_course, find_desired_course, sort_courses_by_friendship, calculate_intersection, get_min_index, calculate_utility

class TestAlgoFriendshipDFS(unittest.TestCase):
    def setUp(self):
        item0 = Item(0, 5)
        item0.add_distributions([1,0,0,0,1])
        item1 = Item(0, 5)
        item1.add_distributions([1,1,0,0,0])
        item2 = Item(0, 5)
        item2.add_distributions([1,1,1,0,0])
        item3 = Item(0, 5)
        item3.add_distributions([0,1,1,1,0])
        item4 = Item(0, 5)
        item4.add_distributions([0,0,1,1,1])
        item5 = Item(0, 5)
        item5.add_distributions([0,0,0,1,1])
        self.items = [item0, item1, item2, item3, item4, item5]

        self.allocation_matrix = [
            [1,0,0,0,1,3],
            [1,1,0,0,0,3],
            [1,1,1,0,0,2],
            [0,1,1,1,0,2],
            [0,0,1,1,1,2],
            [0,0,0,1,1,3]]

        student0 = Student(0, 3)
        student0.add_friends([0,2,1,3,0])
        student0.add_courses([1,2,3,0,0,0])
        student1 = Student(1, 3)
        student1.add_friends([0,0,1,2,3])
        student1.add_courses([0,1,2,3,0,0])
        student2 = Student(2, 3)
        student2.add_friends([3,0,0,1,2])
        student2.add_courses([0,0,1,2,3,0])
        student3 = Student(3, 3)
        student3.add_friends([2,3,0,0,1])
        student3.add_courses([0,0,0,3,2,1])
        student4 = Student(4, 3)
        student4.add_friends([0,0,3,0,0])
        student4.add_courses([1,0,0,0,2,3])

        self.agents = [student0, student1, student2, student3, student4]

    def test_calculate_utility(self):
        output = calculate_utility(self.agents, self.items)
        needed_result = [6, 6, 6, 6, 6]
        validate = (output & needed_result).all()
        self.assertTrue(validate, 'The utility is wrong.')

    def test_calculate_intersection(self):
        output = calculate_intersection(0, self.agents, 6, self.allocation_matrix)
        needed_result = 3
        self.assertEqual(needed_result, output, 'The number of friends is wrong.')

    def test_get_min_index_method_1_and_3(self):
        output = get_min_index([4,1,0,2,6], 6, self.agents, self.allocation_matrix, 1)
        needed_result = 2
        self.assertEqual(needed_result, output, 'The index is wrong.')
    
    def test_get_min_index_method_2_and_4(self):
        output = get_min_index([4,0,0,2,6], 6, self.agents, self.allocation_matrix, 4)
        needed_result = 1
        self.assertEqual(needed_result, output, 'The index is wrong.')

    def test_sort_courses_by_friendship(self):
        output = sort_courses_by_friendship([2,3,4], [0,1,2,3,4,5], self.allocation_matrix)
        needed_result = [4, 3, 5, 2, 0, 1]
        self.assertEqual(needed_result, output, 'The sort is wrong.')

    def test_find_desired_course(self):
        output = find_desired_course(self.agents[0], [0,1,2], set([]), self.allocation_matrix, 4)
        needed_result = -1
        self.assertEqual(needed_result, output, 'The index [list of available courses is empty] is wrong.')

        output = find_desired_course(self.agents[0], [0,1,2], set([3,4,5]), self.allocation_matrix, 4)
        needed_result = -1
        self.assertEqual(needed_result, output, 'The index [total courses] is wrong.')

    def test_find_not_desired_course(self):
        output = find_not_desired_course(self.agents[0], [0,1])
        needed_result = -1
        self.assertEqual(needed_result, output, 'The not_desired_index [enrolled_courses < total courses] is wrong.')

        output = find_not_desired_course(self.agents[0], [0,1,2,4])
        needed_result = 4
        self.assertEqual(needed_result, output, 'The not_desired_index is wrong.')

        output = find_not_desired_course(self.agents[0], [0,1,2])
        needed_result = 0
        self.assertEqual(needed_result, output, 'The not_desired_index is wrong.')

    def test_reshuffle(self):
        output = reshuffle([Step(0, -1, 5, -1, True)], self.allocation_matrix, self.agents)
        needed_result = [
            [1,0,0,0,1,3],
            [1,1,0,0,0,3],
            [1,1,1,0,0,2],
            [0,1,1,1,0,2],
            [0,0,1,1,1,2],
            [1,0,0,1,1,2]]
        assert np.array_equal(needed_result, output), 'The reshuffle [from bank] is wrong.'

        output = reshuffle([Step(0, -1, 5, 0, True)], self.allocation_matrix, self.agents)
        needed_result = [
            [0,0,0,0,1,4],
            [1,1,0,0,0,3],
            [1,1,1,0,0,2],
            [0,1,1,1,0,2],
            [0,0,1,1,1,2],
            [1,0,0,1,1,2]]
        assert np.array_equal(needed_result, output), 'The reshuffle [from bank and return to bank] is wrong.'

        output = reshuffle([Step(0, 1, 3, 0, False)], self.allocation_matrix, self.agents)
        needed_result = [
            [0,1,0,0,1,3],
            [1,1,0,0,0,3],
            [1,1,1,0,0,2],
            [1,0,1,1,0,2],
            [0,0,1,1,1,2],
            [0,0,0,1,1,3]]
        
        assert np.array_equal(needed_result, output), 'The reshuffle [between students]  is wrong.'

    def test_fix_zero_allocation(self):
        input_allocation_matrix = np.array(self.allocation_matrix)
        output = fix_zero_allocation(self.agents, len(self.items), input_allocation_matrix)
        needed_result = [
            [1,0,0,0,1,3],
            [1,1,0,0,0,3],
            [1,1,1,0,0,2],
            [0,1,1,1,0,2],
            [0,0,1,1,1,2],
            [0,0,0,1,1,3]]
        
        # Convert lists to numpy arrays for comparison
        output_array = np.array(output)
        needed_result_array = np.array(needed_result)

        # Validate the result using numpy's array comparison
        validate = np.array_equal(output_array, needed_result_array)
        self.assertTrue(validate, 'The zero_allocation is wrong.')

    def test_fix_add_allocation(self):
        input_allocation_matrix = np.array([
            [0,0,0,0,1,2],
            [1,1,0,0,0,1],
            [1,1,1,0,0,0],
            [0,1,1,1,0,0],
            [0,0,1,1,1,0],
            [0,0,0,0,0,3]])
        method = 4
        output = fix_add_allocation(self.agents, len(self.items), method, input_allocation_matrix)
        needed_result = [
            [1,0,0,0,1,1],
            [1,1,0,0,0,1],
            [1,1,1,0,0,0],
            [0,1,1,1,0,0],
            [0,0,1,1,1,0],
            [0,0,0,1,1,1]]
        
        # Convert lists to numpy arrays for comparison
        output_array = np.array(output)
        needed_result_array = np.array(needed_result)

        # Validate the result using numpy's array comparison
        validate = np.array_equal(output_array, needed_result_array)
        self.assertTrue(validate, 'The add_allocation is wrong.')

    def test_filter_agents(self):
        input_allocation_matrix = np.array([
            [0,0,0,0,1,2],
            [1,1,0,0,0,1],
            [1,1,1,0,0,0],
            [0,1,1,1,0,0],
            [0,0,1,1,1,0],
            [0,0,0,0,0,3]])
        output = filter_agents(self.agents, input_allocation_matrix)
        needed_result = [self.agents[0], self.agents[3], self.agents[4]]
        
        # Convert lists to numpy arrays for comparison
        output_array = np.array(output)
        needed_result_array = np.array(needed_result)
        
        # Validate the result using numpy's array comparison
        validate = np.array_equal(output_array, needed_result_array)
        self.assertTrue(validate, 'The filter_agents is wrong.')

    def test_get_min_agent(self):
        input_allocation_matrix = np.array([
            [0,0,0,0,1,2],
            [1,1,0,0,0,1],
            [1,1,1,0,0,0],
            [0,1,1,1,0,0],
            [0,0,1,1,1,0],
            [0,0,0,0,0,3]])
        method = 4
        output = get_min_agent([self.agents[0], self.agents[3], self.agents[4]], self.agents, len(self.items), input_allocation_matrix, method)
        needed_result = self.agents[4]
        
        # Convert lists to numpy arrays for comparison
        output_array = np.array(output)
        needed_result_array = np.array(needed_result)
        
        # Validate the result using numpy's array comparison
        validate = np.array_equal(output_array, needed_result_array)
        self.assertTrue(validate, 'The get_min_agent is wrong.')

if __name__ == '__main__':
    unittest.main()