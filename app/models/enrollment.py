from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Enrollment(Base):
  __tablename__ = "enrollments"

  id = Column(BigInteger, primary_key=True, index=True)
  student_id = Column(BigInteger, ForeignKey("students.id", ondelete="CASCADE"))
  course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"))
  student = relationship("Student", back_populates="enrollments")
  course = relationship("Course", back_populates="enrollments")
  created_at = Column(DateTime, nullable=False, default="now()")
  updated_at = Column(DateTime, nullable=False, default="now()")
  deleted_at = Column(DateTime, nullable=True)
