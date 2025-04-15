from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from app.schemas.student import StudentIn
from app.models.student import Student

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Get a student by ID."""
        query = self.db.query(Student)
        return query.filter(Student.deleted_at.is_(None)).filter(Student.id == student_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Student]:
        """Get all students"""
        query = self.db.query(Student).filter(Student.deleted_at.is_(None))
        
        return query.offset(skip).limit(limit).all()

    def create(self, student: StudentIn) -> Student:
        """Create a new student."""
        db_student = Student(**student.dict())
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def update(self, student_id: int, student: StudentIn) -> Optional[Student]:
        """Update a student."""
        db_student = self.get_by_id(student_id)
        if db_student:
            for key, value in student.model_dump().items():
                setattr(db_student, key, value)
            db_student.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(db_student)
        return db_student

    def delete(self, student_id: int) -> bool:
        """Delete a student."""
        db_student = self.get_by_id(student_id)
        if db_student:
            db_student.deleted_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(db_student)
            return True
        return False 