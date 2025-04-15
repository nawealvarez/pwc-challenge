from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Course(Base):
  __tablename__ = "courses"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  title = Column(String, index=True)
  description = Column(String, nullable=True)
  created_at = Column(String, nullable=False, default="now()")
  updated_at = Column(String, nullable=False, default="now()")
  deleted_at = Column(String, nullable=True)