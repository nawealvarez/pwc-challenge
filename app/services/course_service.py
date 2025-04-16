from typing import Optional
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.services.teacher_service import TeacherService
from app.utils.logging import log_with_correlation
from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseIn, CourseFilters, CourseOut

class CourseService:
    def __init__(self, db: Session):
        self.course_repo = CourseRepository(db)
        self.teacher_service = TeacherService(db)

    def get_course(self, course_id: int, request: Optional[Request] = None) -> Optional[CourseOut]:
        log_with_correlation("info", f"Fetching course with ID: {course_id}", request)
        course = self.course_repo.get_by_id(course_id)
        if not course:
            log_with_correlation("warning", f"Course with ID {course_id} not found", request)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
        return course

    def list_courses(self, pagination: PaginationParams, filters: Optional[CourseFilters] = None, request: Optional[Request] = None) -> PaginatedResponse[CourseOut]:
        """Get all courses with optional filtering.
        Args:
            pagination: Pagination parameters
                - page: Current page number
                - size: Number of records per page
                - search: Search query
            filters: Optional filters to apply to the query
                - teacher_id: Filter by teacher ID
        """
        log_with_correlation("info", f"Fetching all Courses with pagination: {pagination.page}, {pagination.size}", request)
        if filters:
            log_with_correlation("info", f"Applying filters: {filters}", request)
        total, total_pages, page, items = self.course_repo.get_all(pagination, filters)
        return PaginatedResponse[CourseOut](
            total=total,
            pages=total_pages,
            page=page,
            size=pagination.size,
            items=[CourseOut.model_validate(s) for s in items]
        )

    
    def create_course(self, course: CourseIn, request: Optional[Request] = None) -> CourseOut:
        log_with_correlation("info", f"Creating course: {course.title}", request)
        self.teacher_service.get_teacher(course.teacher_id)
        
        try:
            db_course = self.course_repo.create(course)
            log_with_correlation("info", f"Course created successfully with ID: {db_course.id}", request)
            return db_course
        except Exception as e:
            log_with_correlation("error", f"Failed to create course: {course.title}", request)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating the course"
            )

    def delete_course(self, course_id: int, request: Optional[Request] = None) -> None:
        log_with_correlation("info",f"Deleting course with ID: {course_id}", request)
        self.get_course(course_id)

        if not self.course_repo.delete(course_id):
            log_with_correlation("error", f"Failed to delete course: {course_id}", request)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while deleting the course"
            )
        log_with_correlation("info", f"Course deleted successfully: {course_id}", request)

    def update_course(self, course_id: int, course: CourseIn, request: Optional[Request] = None) -> CourseOut:
        log_with_correlation("info", f"Updating course with ID: {course_id}", request)
        self.get_course(course_id)

        try:
            updated_course = self.course_repo.update(course_id, course)
            log_with_correlation("info", f"Course updated successfully: {course_id}", request)
            return updated_course
        except Exception as e:
            log_with_correlation("error", f"Failed to update course: {course_id}", request)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while updating the course"
            )