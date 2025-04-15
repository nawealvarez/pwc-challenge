from pydantic import BaseModel, EmailStr
from datetime import datetime

class TeacherBase(BaseModel):
    name: str

class TeacherIn(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True 