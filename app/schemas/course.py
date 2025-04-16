from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TypedDict
from app.schemas.teacher import TeacherOut

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseIn(CourseBase):
    teacher_id: int

class CourseFilters(TypedDict, total=False):
    teacher_id: int

class CourseOut(CourseBase):
    id: int
    teacher_id: int
    teacher: TeacherOut
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }