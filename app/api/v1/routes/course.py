from app.schemas.pagination import PaginatedResponse, PaginationParams
from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy.orm import Session
from app.schemas.course import CourseIn, CourseOut
from app.services.course_service import CourseService
from app.core.database import get_db
from typing import Optional

router = APIRouter()

@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseIn, db: Session = Depends(get_db), request: Request = None):
    service = CourseService(db)
    return service.create_course(course, request)

@router.get("/{course_id}", response_model=CourseOut, status_code=status.HTTP_200_OK)
def get_course(course_id: int, db: Session = Depends(get_db), request: Request = None):
    service = CourseService(db)
    return service.get_course(course_id, request)

@router.get("/", response_model=PaginatedResponse[CourseOut], status_code=status.HTTP_200_OK)
def list_courses(
    page: int = Query(1, ge=1, description="Current page number"),
    size: int = Query(10, ge=1, le=100, description="Number of records per page"),
    search: Optional[str] = Query(None, description="Search by course name or description"),
    teacher_id: Optional[int] = Query(None, description="Filter by teacher ID"),
    db: Session = Depends(get_db),
    request: Request = None
    ):
    pagination = PaginationParams(page=page, size=size, search=search)
    filters = {}
    if teacher_id:
        filters["teacher_id"] = teacher_id

    service = CourseService(db)
    return service.list_courses(pagination=pagination, filters=filters, request=request)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db), request: Request = None):
    service = CourseService(db)
    service.delete_course(course_id, request)

@router.put("/{course_id}", response_model=CourseOut, status_code=status.HTTP_200_OK)
def update_course(course_id: int, course_in: CourseIn, db: Session = Depends(get_db), request: Request = None):
    service = CourseService(db)
    return service.update_course(course_id, course_in, request)