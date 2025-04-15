from pydantic import BaseModel
from datetime import datetime

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    status: str = "active"


class EnrollmentIn(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True 