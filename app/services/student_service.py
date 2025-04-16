from app.schemas.pagination import PaginatedResponse, PaginationParams
from fastapi import HTTPException, status
from typing import List, Optional
import logging

from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentFilters, StudentIn, StudentOut

# Configure logging
logger = logging.getLogger(__name__)

class StudentService:
  def __init__(self, db):
    self.repo = StudentRepository(db)

  def get_student(self, student_id: int) -> StudentOut:
    """Get a student by ID."""
    logger.info(f"Fetching student with ID: {student_id}")
    student = self.repo.get_by_id(student_id)
    if not student:
        logger.warning(f"Student with ID {student_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    return student

  def list_students(self, pagination: PaginationParams, filters: Optional[StudentFilters] = None) -> PaginatedResponse[StudentOut]:
    """Get all students with optional filtering."""
    logger.info(f"Fetching students with pagination: {pagination.page}, {pagination.size}")
    total, total_pages, page, items = self.repo.get_all(pagination, filters)
    return PaginatedResponse[StudentOut](
      total=total,
      pages=total_pages,
      page=page,
      size=pagination.size,
      items=[StudentOut.from_orm(s) for s in items]
    )

  def create_student(self, student: StudentIn) -> StudentOut:
    """Create a new student."""
    logger.info(f"Creating student: {student.name}")
    
    try:
        db_student = self.repo.create(student.model_dump())
        logger.info(f"Student created successfully with ID: {db_student.id}")
        return db_student
    except Exception as e:
        logger.error(f"Failed to create student: {student.name}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create student. Please check the data provided."
        )


  def update_student(self, student_id: int, student: StudentIn) -> StudentOut:
    """Update a student."""
    logger.info(f"Updating student with ID: {student_id}")
    
    self.get_student(student_id)
    
    try:
        updated_student = self.repo.update(student_id, student)
        logger.info(f"Student updated successfully: {student_id}")
        return updated_student
    except Exception as e:
        logger.error(f"Failed to update student: {student_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update student. Please check the data provided."
        )

  def delete_student(self, student_id: int) -> None:
    """Delete a student."""
    logger.info(f"Deleting student with ID: {student_id}")
    
    self.get_student(student_id)
    
    if not self.repo.delete(student_id):
        logger.error(f"Failed to delete student: {student_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete student"
        )
    
    logger.info(f"Student deleted successfully: {student_id}")