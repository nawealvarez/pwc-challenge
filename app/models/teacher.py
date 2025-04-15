from sqlalchemy import Column, BigInteger, String, DateTime
from app.core.database import Base
from sqlalchemy.orm import relationship

class Teacher(Base):
  __tablename__ = "teachers"
  id = Column(BigInteger, primary_key=True, index=True)
  name = Column(String, nullable=False)
  courses = relationship("Course", back_populates="teacher", cascade="all, delete-orphan")
  created_at = Column(DateTime, nullable=False, default="now()")
  updated_at = Column(DateTime, nullable=False, default="now()")
  deleted_at = Column(DateTime, nullable=True)