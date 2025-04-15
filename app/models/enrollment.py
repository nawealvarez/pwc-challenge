from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Enrollment(Base):
  __tablename__ = "enrollments"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  course_id = Column(Integer, ForeignKey("courses.id"))
  created_at = Column(String, nullable=False, default="now()")
  updated_at = Column(String, nullable=False, default="now()")
  deleted_at = Column(String, nullable=True)
