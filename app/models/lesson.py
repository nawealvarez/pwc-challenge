from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    duration_minutes = Column(Integer)
    description = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default="now()")
    updated_at = Column(String, nullable=False, default="now()")
    deleted_at = Column(String, nullable=True)
