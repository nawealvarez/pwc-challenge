import logging
from typing import Optional
from app.services.course_service import CourseService
from app.services.student_service import StudentService
from app.utils.logging import log_with_correlation
from sqlalchemy.orm import Session
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.enrollment import EnrollmentIn, EnrollmentOut
from fastapi import HTTPException, status, Request


class EnrollmentService:
  def __init__(self, db: Session):
    self.enrollment_repo = EnrollmentRepository(db)
    self.course_service = CourseService(db)
    self.student_service = StudentService(db)

  def create_enrollment(self, enrollment: EnrollmentIn, request: Optional[Request] = None) -> EnrollmentOut:
    """Enroll a student in a course."""
    log_with_correlation("info", f"Enrolling student {enrollment.student_id} in course {enrollment.course_id}", request)
    self.student_service.get_student(self.db, enrollment.student_id)
    self.course_service.create_course(self.db, enrollment.course_id)

    existing_enrollments = self.enrollment_repo.get_by_course_and_student(self.db, enrollment.course_id, enrollment.student_id)
    if existing_enrollments:
      log_with_correlation("warning", f"Student {enrollment.student_id} already enrolled in course {enrollment.course_id}", request)
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Student already enrolled in this course"
      )
    
    try:
      db_enrollment = self.enrollment_repo.create(self.db, enrollment)
      log_with_correlation("info", f"Enrollment created successfully with ID: {db_enrollment.id}", request)
      return db_enrollment
    except Exception as e:
      log_with_correlation("error", f"Failed to create enrollment: {enrollment.student_id}, {enrollment.course_id}", request)
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred while creating the enrollment"
      )
    
  def delete_enrollment(self, enrollment: EnrollmentIn, request: Optional[Request] = None) -> None:
    """Remove student from course."""
    log_with_correlation("info", f"Removing student {enrollment.student_id} from course {enrollment.course_id}", request)
    existing_enrollment = self.enrollment_repo.get_by_course_and_student(self.db, enrollment.course_id, enrollment.student_id)

    if not existing_enrollment:
      log_with_correlation("warning", f"Enrollment not found for student {enrollment.student_id} in course {enrollment.course_id}", request)
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Enrollment not found"
      )
    
    if not self.enrollment_repo.delete(self.db, existing_enrollment.id):
      log_with_correlation("error", f"Failed to delete enrollment: {existing_enrollment.id}", request)
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred while deleting the enrollment"
      )
    
    log_with_correlation("info", f"Enrollment deleted successfully with ID: {existing_enrollment.id}", request)

