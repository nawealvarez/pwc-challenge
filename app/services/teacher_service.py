from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.utils.logging import log_with_correlation
from fastapi import HTTPException, status, Request
from typing import Optional
from app.repositories.teacher_repository import TeacherRepository
from app.schemas.teacher import TeacherIn, TeacherOut

class TeacherService:
    def __init__(self, db):
        self.repo = TeacherRepository(db)

    def get_teacher(self, teacher_id: int, request: Optional[Request] = None) -> TeacherOut:
        """Get a teacher by ID."""
        log_with_correlation("info", f"Fetching teacher with ID: {teacher_id}", request)
        teacher = self.repo.get_by_id(teacher_id)
        if not teacher:
            log_with_correlation("warning", f"Teacher with ID {teacher_id} not found", request)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with id {teacher_id} not found"
            )
        return teacher

    def list_teachers(self, pagination: PaginationParams, request: Optional[Request] = None) -> PaginatedResponse[TeacherOut]:
        """Get all teachers with optional filtering."""
        log_with_correlation("info", f"Fetching teachers with pagination: {pagination.page}, {pagination.size}", request)
        total, total_pages, page, items =  self.repo.get_all(pagination)
        return PaginatedResponse[TeacherOut](
            total=total,
            pages=total_pages,
            page=page,
            size=pagination.size,
            items=[TeacherOut.model_validate(s) for s in items]
        )

    def create_teacher(self, teacher: TeacherIn, request: Optional[Request] = None) -> TeacherOut:
        """Create a new teacher."""
        log_with_correlation("info", f"Creating teacher: {teacher.name}", request)
        
        try:
            db_teacher = self.repo.create(teacher)
            log_with_correlation("info", f"Teacher created successfully with ID: {db_teacher.id}", request)
            return db_teacher
        except Exception as e:
            log_with_correlation("error", f"Failed to create teacher: {teacher.name}", request)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating the teacher"
            )


    def update_teacher(self, teacher_id: int, teacher: TeacherIn, request: Optional[Request] = None) -> TeacherOut:
        """Update a teacher."""
        log_with_correlation("info", f"Updating teacher with ID: {teacher_id}", request)
        
        self.get_teacher(teacher_id)
        
        try:
            updated_teacher = self.repo.update(teacher_id, teacher)
            log_with_correlation("info", f"Teacher updated successfully: {teacher_id}", request)
            return updated_teacher
        except Exception as e:
            log_with_correlation("error", f"Failed to update teacher: {teacher_id}", request)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while updating the teacher"
            )

    def delete_teacher(self, teacher_id: int, request: Optional[Request] = None) -> None:
        """Delete a teacher."""
        log_with_correlation("info", f"Deleting teacher with ID: {teacher_id}", request)
        
        self.get_teacher(teacher_id)
        
        if not self.repo.delete(teacher_id):
            log_with_correlation("error", f"Failed to delete teacher: {teacher_id}", request)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete teacher"
            )
        
        log_with_correlation("info", f"Teacher deleted successfully: {teacher_id}", request)