from sqlalchemy.orm import Session
from app.infrastructure.models import User as ORMUser
from app.schemas.user import UserCreate
from app.infrastructure.models import UserCourse as ORMUserCourse

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(ORMUser).filter(ORMUser.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(ORMUser).filter(ORMUser.email == email).first()

    def create_user(self, user: UserCreate):
        db_user = ORMUser(name=user.name, email=user.email, hashed_password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_subscribed_courses(self, user_id: int):
        # Запрашиваем только столбец course_id
        subscribed_courses = (
            self.db.query(ORMUserCourse.course_id)
            .filter(ORMUserCourse.user_id == user_id)
            .all()
        )
        
        # Извлекаем значения course_id из результата запроса
        return {course_id for (course_id,) in subscribed_courses}