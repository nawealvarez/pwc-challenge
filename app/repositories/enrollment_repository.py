from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentIn
from sqlalchemy.orm import Session


class EnrollmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, enrollment: EnrollmentIn) -> Enrollment:
        """Create a new enrollment."""
        db_enrollment = Enrollment(**enrollment.dict())
        self.db.add(db_enrollment)
        self.db.commit()
        self.db.refresh(db_enrollment)
        return db_enrollment
    
    def delete(self, enrollment: Enrollment) -> bool:
        """Delete an enrollment."""
        if enrollment:
            enrollment.deleted_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(enrollment)
            return True
        return False

    def get_by_course_and_student(self, course_id: int, student_id: int) -> Enrollment:
        query = self.db.query(Enrollment).filter(Enrollment.deleted_at.is_(None))
        return query.filter_by(student_id=student_id, course_id=course_id).first()