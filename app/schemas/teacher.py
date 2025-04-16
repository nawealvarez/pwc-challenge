from pydantic import BaseModel
from datetime import datetime

class TeacherBase(BaseModel):
    name: str

class TeacherIn(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    } 