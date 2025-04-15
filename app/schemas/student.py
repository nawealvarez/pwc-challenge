from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None

class StudentIn(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True 