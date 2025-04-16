from app.schemas.pagination import PaginationParams, PaginationResult
from app.utils.pagination import paginate_query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone
from app.schemas.teacher import TeacherIn
from app.models.teacher import Teacher

class TeacherRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, teacher_id: int) -> Optional[Teacher]:
        """Get a teacher by ID."""
        query = self.db.query(Teacher)
        return query.filter(Teacher.deleted_at.is_(None)).filter(Teacher.id == teacher_id).first()

    def get_all(self, pagination: PaginationParams) -> PaginationResult[Teacher]:
        """Get all teachers"""
        query = self.db.query(Teacher).filter(Teacher.deleted_at.is_(None))
        
        return paginate_query(query=query, model=Teacher, params=pagination, search_fields=["name"])


    def create(self, teacher: TeacherIn) -> Teacher:
        """Create a new teacher."""
        db_teacher = Teacher(**teacher.model_dump())
        self.db.add(db_teacher)
        self.db.commit()
        self.db.refresh(db_teacher)
        return db_teacher

    def update(self, teacher_id: int, teacher: TeacherIn) -> Optional[Teacher]:
        """Update a teacher."""
        db_teacher = self.get_by_id(teacher_id)
        if db_teacher:
            for key, value in teacher.model_dump().items():
                setattr(db_teacher, key, value)
            db_teacher.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(db_teacher)
        return db_teacher

    def delete(self, teacher_id: int) -> bool:
        """Delete a teacher."""
        db_teacher = self.get_by_id(teacher_id)
        if db_teacher:
            db_teacher.deleted_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(db_teacher)
            return True
        return False 