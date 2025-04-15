from sqlalchemy import Column, BigInteger, DateTime, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    created_at = Column(DateTime, nullable=False, default="now()")
    updated_at = Column(DateTime, nullable=False, default="now()")
    deleted_at = Column(DateTime, nullable=True)
