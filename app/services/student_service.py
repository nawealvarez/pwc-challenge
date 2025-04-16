from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.utils.logging import log_with_correlation
from fastapi import HTTPException, status, Request
from typing import Optional
from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentFilters, StudentIn, StudentOut

class StudentService:
  def __init__(self, db):
    self.repo = StudentRepository(db)

  def get_student(self, student_id: int, request: Optional[Request] = None) -> StudentOut:
    """Get a student by ID."""
    log_with_correlation("info", f"Fetching student with ID: {student_id}", request)
    student = self.repo.get_by_id(student_id)
    if not student:
      log_with_correlation("warning", f"Student with ID {student_id} not found", request)
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Student with id {student_id} not found"
      )
    return student

  def list_students(
      self, 
      pagination: PaginationParams, 
      filters: Optional[StudentFilters] = None, 
      request: Optional[Request] = None
    ) -> PaginatedResponse[StudentOut]:
    """Get all students paginated with optional filtering.

    Args:
      pagination: Pagination parameters
        - page: Current page number
        - size: Number of records per page
        - search: Search query
      filters: Optional filters to apply to the query
        - course_id: Filter by Course ID
    """
    log_with_correlation("info", f"Fetching students with pagination: {pagination.page}, {pagination.size}", request)
    total, total_pages, page, items = self.repo.get_all(pagination, filters)
    return PaginatedResponse[StudentOut](
      total=total,
      pages=total_pages,
      page=page,
      size=pagination.size,
      items=[StudentOut.model_validate(s) for s in items]
    )

  def create_student(self, student: StudentIn, request: Optional[Request] = None) -> StudentOut:
    """Create a new student."""
    log_with_correlation("info", f"Creating student: {student.name}", request)
    
    try:
        db_student = self.repo.create(student)
        log_with_correlation("info", f"Student created successfully with ID: {db_student.id}", request)
        return db_student
    except Exception as e:
        log_with_correlation("error", f"Failed to create student: {student.name}", request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the student"
        )


  def update_student(self, student_id: int, student: StudentIn, request: Optional[Request] = None) -> StudentOut:
    """Update a student."""
    log_with_correlation("info", f"Updating student with ID: {student_id}", request)
    
    self.get_student(student_id)
    
    try:
      updated_student = self.repo.update(student_id, student)
      log_with_correlation("info", f"Student updated successfully: {student_id}", request)
      return updated_student
    except Exception as e:
      log_with_correlation("error", f"Failed to update student: {student_id}", request)
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="An unexpected error occurred while updating the student"
      )

  def delete_student(self, student_id: int, request: Optional[Request] = None) -> None:
    """Delete a student."""
    log_with_correlation("info", f"Deleting student with ID: {student_id}", request)
    
    self.get_student(student_id)
    
    if not self.repo.delete(student_id):
      log_with_correlation("error", f"Failed to delete student: {student_id}", request)
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="Failed to delete student"
      )
    log_with_correlation("info", f"Student deleted successfully: {student_id}", request)