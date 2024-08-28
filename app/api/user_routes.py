# app/api/user_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user as user_schemas, course as course_schemas
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.models import Course as ORMCourse
from app.api.dependencies import get_db, get_current_user

router = APIRouter()

@router.get("/me/", response_model=user_schemas.UserResponse)
def get_current_user_info(db: Session = Depends(get_db), user: user_schemas.User = Depends(get_current_user)):
    user_info = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "courses": []  # Initially an empty list
    }

    userRepository = UserRepository(db)
    subscribed_courses = userRepository.get_user_subscribed_courses(user.id)

    for course_id in subscribed_courses:
        course = db.query(ORMCourse).filter(ORMCourse.id == course_id).first()
        if course:
            user_info["courses"].append(course_schemas.CourseBase(
                id=course.id,
                title=course.title,
                description=course.description,
                category=course.category
            ))
    
    return user_info
