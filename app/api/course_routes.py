# app/api/course_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.repositories.course_repository import CourseRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.course import CourseCreate, Course, SubscriptionRequest
from app.schemas.user import User
from app.api.dependencies import get_db, get_current_user
from app.use_cases.course_use_cases import CourseUseCase

router = APIRouter()

@router.get("/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course_repo = CourseRepository(db)
    user_repo = UserRepository(db)
    courseUseCase = CourseUseCase(course_repo)
    user_id = user.id
    all_courses = courseUseCase.get_courses_with_subscription_info(user_id, skip=skip, limit=limit)
    subscribed_courses = user_repo.get_user_subscribed_courses(user_id)
    
    return [
        Course(
            id=course.id,
            title=course.title,
            description=course.description,
            category=course.category,
            is_subscribed=course.id in subscribed_courses,
            instructor_name=course.instructor_name,
            instructor_image=course.instructor_image
        )
        for course in all_courses
    ]

@router.post("/subscribe/", response_model=dict)
def toggle_subscription(subscription_request: SubscriptionRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    course_repo = CourseRepository(db)
    course_use_case = CourseUseCase(course_repo)
    result = course_use_case.toggle_course_subscription(user.id, subscription_request.course_id)
    return result

@router.post("/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    course_repo = CourseRepository(db)
    courseUseCase = CourseUseCase(course_repo)
    return courseUseCase.create_course(course)
