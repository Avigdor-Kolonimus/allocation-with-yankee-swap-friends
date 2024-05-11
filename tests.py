import unittest

from item import Item
from student import Student
from algo_friendship_bfs import sort_courses_by_friendship, sort_agents_by_friendship, calculate_intersection, get_min_index, find_desired, find_not_desired, agree_exchange, augment_path, calculate_utility

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

    def test_sort_courses_by_friendship(self):
        output = sort_courses_by_friendship([2,3,4], [0,1,2,3,4,5], self.allocation_matrix)
        needed_result = [4, 3, 5, 2, 0, 1]
        self.assertEqual(needed_result, output, 'The sort is wrong.')

    def test_sort_agents_by_friendship(self):
        output = sort_agents_by_friendship(0, self.agents, [1,2,3,4])
        needed_result = [4, 2, 1, 3]
        self.assertEqual(needed_result, output, 'The sort is wrong.')

    def test_calculate_intersection(self):
        output = calculate_intersection(0, self.agents, 6, self.allocation_matrix)
        needed_result = 3
        self.assertEqual(needed_result, output, 'The number of friends is wrong.')

    def test_get_min_index(self):
        output = get_min_index([4,1,0,2,6], 6, self.agents, self.allocation_matrix)
        needed_result = 2
        self.assertEqual(needed_result, output, 'The index is wrong.')

    def test_agree_exchange(self):
        output = agree_exchange(0, 2, self.agents)
        self.assertTrue(output, 'The condition is wrong.')
        output = agree_exchange(0, 5, self.agents)
        self.assertFalse(output, 'The condition is wrong.')

    def test_calculate_utility(self):
        output = calculate_utility(self.agents, self.items)
        needed_result = [6, 6, 6, 6, 6]
        validate = (output & needed_result).all()
        self.assertTrue(validate, 'The utility is wrong.')

    def test_find_desired(self):
        output = find_desired(0, [0,1,2], set([]), self.agents, self.allocation_matrix)
        needed_result = -1
        self.assertEqual(needed_result, output, 'The index [list of yes is empty] is wrong.')

        output = find_desired(0, [0,1,2], set([3,4,5]), self.agents, self.allocation_matrix)
        needed_result = -1
        self.assertEqual(needed_result, output, 'The index [total courses] is wrong.')

    def test_find_not_desired(self):
        output = find_not_desired(0, [0,1], self.agents)
        needed_result = -1
        self.assertEqual(needed_result, output, 'The not_desired_index [bundle < total courses] is wrong.')

        output = find_not_desired(0, [0,1,2,4], self.agents)
        needed_result = 4
        self.assertEqual(needed_result, output, 'The not_desired_index is wrong.')

        output = find_not_desired(0, [0,1,2], self.agents)
        needed_result = 0
        self.assertEqual(needed_result, output, 'The not_desired_index is wrong.')

    # def test_augment_path(self):
    #     output = augment_path(0, [0,1], self.agents)
    #     needed_result = -1
    #     self.assertEqual(needed_result, output, 'The not_desired_index [bundle < total courses] is wrong.')

    #     output = augment_path(0, [0,1,2,4], self.agents)
    #     needed_result = 4
    #     self.assertEqual(needed_result, output, 'The not_desired_index is wrong.')

    #     output = augment_path(0, [0,1,2], self.agents)
    #     needed_result = 0
    #     self.assertEqual(needed_result, output, 'The not_desired_index is wrong.')

if __name__ == '__main__':
    unittest.main()