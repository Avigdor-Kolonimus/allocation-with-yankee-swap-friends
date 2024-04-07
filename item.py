class Item:
    def __init__(self, course_id, capacity):
        self.course_id = course_id
        self.capacity = capacity
        self.distributions = []

    def add_distributions(self, distributions):
        self.distributions = distributions

    def get_distributions(self):
        return self.distributions
    
    def get_capacity(self):
        return self.capacity
    
    def get_course_id(self):
        return self.course_id