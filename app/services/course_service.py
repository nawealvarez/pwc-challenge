from typing import Optional
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.services.teacher_service import TeacherService
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseIn, CourseFilters, CourseOut

logger = logging.getLogger(__name__)

class CourseService:
    def __init__(self, db: Session):
        self.course_repo = CourseRepository(db)
        self.teacher_repo = TeacherService(db)

    def get_course(self, course_id: int) -> Optional[CourseOut]:
        logger.info(f"Fetching course with ID: {course_id}")
        course = self.course_repo.get_by_id(course_id)
        if not course:
            logger.warning(f"Course with ID {course_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
        return course

    def list_courses(self, pagination: PaginationParams, filters: Optional[CourseFilters] = None) -> PaginatedResponse[CourseOut]:
        """Get all courses with optional filtering.
        Args:
            pagination: Pagination parameters
                - page: Current page number
                - size: Number of records per page
                - search: Search query
            filters: Optional filters to apply to the query
                - teacher_id: Filter by teacher ID
        """
        logger.info(f"Fetching all Courses with pagination: {pagination.page}, {pagination.size}")
        if filters:
            logger.info(f"Applying filters: {filters}")
        total, total_pages, page, items = self.course_repo.get_all(pagination, filters)
        return PaginatedResponse[CourseOut](
            total=total,
            pages=total_pages,
            page=page,
            size=pagination.size,
            items=[CourseOut.from_orm(s) for s in items]
        )

    
    def create_course(self, course: CourseIn) -> CourseOut:
        logger.info(f"Creating course: {course.title}")
        teacher = self.teacher_repo.get_teacher(course.teacher_id)
        
        if not teacher:
            logger.warning(f"Teacher with ID {course.teacher_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with ID {course.teacher_id} not found"
            )
        
        try:
            db_course = self.course_repo.create(course)
            logger.info(f"Course created successfully with ID: {db_course.id}")
            return db_course
        except Exception as e:
            logger.error(f"Failed to create course: {course.title}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create course. Please check the data provided."
            )

    def delete_course(self, course_id: int) -> None:
        logger.info(f"Deleting course with ID: {course_id}")
        self.get_course(course_id)

        if not self.course_repo.delete(course_id):
            logger.error(f"Failed to delete course: {course_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete course"
            )
        logger.info(f"Course deleted successfully: {course_id}")

    def update_course(self, course_id: int, course: CourseIn) -> CourseOut:
        logger.info(f"Updating course with ID: {course_id}")
        self.get_course(course_id)

        try:
            updated_course = self.course_repo.update(course_id, course)
            logger.info(f"Course updated successfully: {course_id}")
            return updated_course
        except Exception as e:
            logger.error(f"Failed to update course: {course_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not update course. Please check the data provided."
            )