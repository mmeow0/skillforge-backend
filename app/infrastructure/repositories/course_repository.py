from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.infrastructure.models import Course as ORMCourse
from app.infrastructure.models import UserCourse as ORMUserCourse
from app.schemas.course import CourseCreate

class CourseRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_courses(self, skip: int = 0, limit: int = 10):
        return self.db.query(ORMCourse).offset(skip).limit(limit).all()

    def create_course(self, course: CourseCreate):
        db_course = ORMCourse(
            title=course.title,
            description=course.description,
            category=course.category,
            instructor_name=course.instructor_name,
            instructor_image=course.instructor_image
        )
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def toggle_course_subscription(self, user_id: int, course_id: int):
        user_course = self.db.query(ORMUserCourse).filter_by(user_id=user_id, course_id=course_id).first()
        if user_course:
            self.db.delete(user_course)
            self.db.commit()
            return {"message": "Unsubscribed from course"}
        else:
            self.db.add(ORMUserCourse(user_id=user_id, course_id=course_id))
            self.db.commit()
            return {"message": "Subscribed to course"}

    def get_courses_with_subscription_info(self, user_id: int, skip: int = 0, limit: int = 10):
        return (
            self.db.query(ORMCourse)
            .outerjoin(ORMUserCourse, and_(ORMCourse.id == ORMUserCourse.course_id, ORMUserCourse.user_id == user_id))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def delete_course(self, course_id: int):
        course = self.db.query(ORMCourse).filter(ORMCourse.id == course_id).first()
        if course:
            self.db.delete(course)
            self.db.commit()
            return True
        return False
