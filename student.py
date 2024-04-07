class Student:
    def __init__(self, student_id, total_courses):
        self.student_id = student_id
        self.friends = []
        self.only_friends = []
        self.course_ratings = []
        self.sorted_indices = []
        self.desired_courses = []
        self.total_courses = total_courses

    def get_student_id(self):
        return self.student_id
    
    def add_friends(self, friends):
        self.friends = friends
        self.only_friends = [index for index, value in enumerate(friends) if value != 0]

    def get_friends(self):
        return self.friends
    
    def get_friend(self, indFriend):
        return self.friends[indFriend]

    def get_only_friends(self):
        return self.only_friends

    def add_courses(self, rating):
        self.course_ratings = rating
        self.sorted_indices = sorted(range(len(rating)), key=lambda k: rating[k])
        
        output = []
        for index,_ in enumerate(rating):
            if rating[index] != 0:
                output.append(index)
        self.desired_courses = output


    def get_course_ratings(self):
        return self.course_ratings
    
    def get_course_rating(self, indCourse):
        return self.course_ratings[indCourse]
    
    def get_sorted_indices(self):
        return self.sorted_indices

    def get_total_courses(self):
        return self.total_courses
    
    def valuation_index(self, bundle, items):   
        slots=set()
        
        for g in bundle:
            if items[g].course_id in self.desired_courses:
                slots.add(items[g].course_id)
        
        return min(len(slots), self.total_courses)
    
    def need_desired(self, bundle):   
        for course in self.desired_courses:
            if course not in bundle:
                return True
        
        return False
    
    def is_desired(self, course):
        if course in self.desired_courses:
            return True
        
        return False