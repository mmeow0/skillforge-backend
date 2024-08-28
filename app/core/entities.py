# app/core/entities.py

class User:
    def __init__(self, id: int, name: str, email: str, hashed_password: str):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password

class Course:
    def __init__(self, id: int, title: str, description: str, category: str, instructor_name: str = None, instructor_image: str = None):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.instructor_name = instructor_name
        self.instructor_image = instructor_image
