from fastapi import HTTPException, status
from typing import List
import logging

from app.repositories.teacher_repository import TeacherRepository
from app.schemas.teacher import TeacherIn, TeacherOut

# Configure logging
logger = logging.getLogger(__name__)

class TeacherService:
    def __init__(self, db):
        self.repo = TeacherRepository(db)

    def get_teacher(self, teacher_id: int) -> TeacherOut:
        """Get a teacher by ID."""
        logger.info(f"Fetching teacher with ID: {teacher_id}")
        teacher = self.repo.get_by_id(teacher_id)
        if not teacher:
            logger.warning(f"Teacher with ID {teacher_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with id {teacher_id} not found"
            )
        return teacher

    def list_teachers(self, skip: int = 0, limit: int = 100) -> List[TeacherOut]:
        """Get all teachers with optional filtering."""
        logger.info(f"Fetching teachers with skip={skip}, limit={limit}")
        return self.repo.get_all(skip=skip, limit=limit)

    def create_teacher(self, teacher: TeacherIn) -> TeacherOut:
        """Create a new teacher."""
        logger.info(f"Creating teacher: {teacher.name}")
        
        try:
            db_teacher = self.repo.create(teacher.model_dump())
            logger.info(f"Teacher created successfully with ID: {db_teacher.id}")
            return db_teacher
        except Exception as e:
            logger.error(f"Failed to create teacher: {teacher.name}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create teacher. Please check the data provided."
            )


    def update_teacher(self, teacher_id: int, teacher: TeacherIn) -> TeacherOut:
        """Update a teacher."""
        logger.info(f"Updating teacher with ID: {teacher_id}")
        
        self.get_teacher(teacher_id)
        
        try:
            updated_teacher = self.repo.update(teacher_id, teacher)
            logger.info(f"Teacher updated successfully: {teacher_id}")
            return updated_teacher
        except Exception as e:
            logger.error(f"Failed to update teacher: {teacher_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not update teacher. Please check the data provided."
            )

    def delete_teacher(self, teacher_id: int) -> None:
        """Delete a teacher."""
        logger.info(f"Deleting teacher with ID: {teacher_id}")
        
        self.get_teacher(teacher_id)
        
        if not self.repo.delete(teacher_id):
            logger.error(f"Failed to delete teacher: {teacher_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete teacher"
            )
        
        logger.info(f"Teacher deleted successfully: {teacher_id}")