from app.infrastructure.repositories.course_repository import CourseRepository

class CourseUseCase:

    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    def get_courses(self, skip=0, limit=10):
        return self.course_repository.get_courses(skip, limit)

    def create_course(self, course_data):
        return self.course_repository.create_course(course_data)

    def toggle_course_subscription(self, user_id, course_id):
        return self.course_repository.toggle_course_subscription(user_id, course_id)
    
    def get_courses_with_subscription_info(self, user_id, skip=0, limit=10):
        return self.course_repository.get_courses_with_subscription_info(user_id, skip, limit)
    
    
