from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base

Enum = Enum('student', 'teacher')

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(Enum, nullable=False)
    created_at = Column(String, nullable=False, default="now()")
    updated_at = Column(String, nullable=False, default="now()")
    deleted_at = Column(String, nullable=True)
