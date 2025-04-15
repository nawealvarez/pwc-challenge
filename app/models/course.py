from sqlalchemy import Column, String, Text, DateTime, ForeignKey, BigInteger
from app.core.database import Base
from sqlalchemy.orm import relationship

class Course(Base):
  __tablename__ = "courses"

  id = Column(BigInteger, primary_key=True, index=True)
  title = Column(String, index=True, nullable=False)
  description = Column(Text, nullable=True)
  teacher_id = Column(BigInteger, ForeignKey('teachers.id', ondelete='CASCADE'))
  teacher = relationship("Teacher", back_populates="courses")
  enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
  created_at = Column(DateTime, nullable=False, default="now()")
  updated_at = Column(DateTime, nullable=False, default="now()")
  deleted_at = Column(DateTime, nullable=True)