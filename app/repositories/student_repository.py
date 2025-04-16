from app.models.enrollment import Enrollment
from app.schemas.pagination import PaginationParams, PaginationResult
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone
from app.schemas.student import StudentFilters, StudentIn
from app.models.student import Student
from app.utils.pagination import paginate_query

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Get a student by ID."""
        query = self.db.query(Student)
        return query.filter(Student.deleted_at.is_(None)).filter(Student.id == student_id).first()

    def get_all(self, pagination: PaginationParams, filters: Optional[StudentFilters] = None) -> PaginationResult[Student]:
        """Get all students"""
        query = self.db.query(Student).filter(Student.deleted_at.is_(None))

        if "course_id" in filters:
            query = query.join(Enrollment).filter(Enrollment.course_id == filters["course_id"])

        return paginate_query(query=query, model=Student, params=pagination, search_fields=["name"])

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