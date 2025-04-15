from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.teacher import TeacherOut

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseIn(CourseBase):
    teacher_id: int

class CourseFilters(BaseModel):
    title: Optional[str] = None
    teacher_id: Optional[int] = None

class CourseOut(CourseBase):
    id: int
    teacher_id: int
    teacher: TeacherOut
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True