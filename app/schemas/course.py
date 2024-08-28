from typing import Optional
from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    instructor_name: Optional[str] = None
    instructor_image: Optional[str] = None

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    category: str
    instructor_name: Optional[str] = None
    instructor_image: Optional[str] = None

    class Config:
        orm_mode = True

class Course(CourseBase):
    id: int
    is_subscribed: Optional[bool] = False

    class Config:
        orm_mode = True

class SubscriptionRequest(BaseModel):
    course_id: int