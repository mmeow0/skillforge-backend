from app.infrastructure.repositories.user_repository import UserRepository

class UserUseCase:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data):
        return self.user_repository.create_user(user_data)

    def get_user(self, user_id):
        return self.user_repository.get_user(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)
    
    def get_user_subscribed_courses(self, user_id):
        return self.user_repository.get_user_subscribed_courses(user_id)
    