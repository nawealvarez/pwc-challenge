from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.schemas.course import CourseIn, CourseFilters
from app.models.course import Course
from datetime import datetime, timezone

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, course_id: int) -> Optional[Course]:
        """Get a Course by ID with teacher information."""
        query = self.db.query(Course).options(joinedload(Course.teacher))
        return query.filter(Course.deleted_at.is_(None)).filter(Course.id == course_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, filters: Optional[CourseFilters] = None) -> List[Course]:
        """Get all Courses with teacher information - optional filtering."""
        query = self.db.query(Course).filter(Course.deleted_at.is_(None)).options(joinedload(Course.teacher))
        
        if filters:
            for key, value in filters.items():
                if hasattr(Course, key):
                    query = query.filter(getattr(Course, key) == value)
        
        return query.offset(skip).limit(limit).all()

    def create(self, course: CourseIn) -> Course:
        """Create a new Course."""
        db_course = Course(**course.dict())
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def update(self, course_id: int, course: CourseIn) -> Optional[Course]:
        """Update a Course."""
        db_course = self.get_by_id(course_id)
        if db_course:
            for key, value in course.model_dump().items():
                setattr(db_course, key, value)
            db_course.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(db_course)
        return db_course

    def delete(self, course_id: int) -> bool:
        """Delete a Course."""
        db_course = self.get_by_id(course_id)
        if db_course:
            db_course.deleted_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(db_course)
            return True
        return False

