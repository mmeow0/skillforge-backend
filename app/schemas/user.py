from typing import List
from pydantic import BaseModel
from app.schemas.course import CourseBase


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    courses: List[CourseBase] = []


class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    courses: List[CourseBase] = []