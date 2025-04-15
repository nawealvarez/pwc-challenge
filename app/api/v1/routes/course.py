from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.course import CourseIn, CourseOut
from app.services.course_service import CourseService
from app.core.database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseIn, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.create_course(course)

@router.get("/{course_id}", response_model=CourseOut, status_code=status.HTTP_200_OK)
def get_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/", response_model=List[CourseOut], status_code=status.HTTP_200_OK)
def list_courses(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return"),
    title: Optional[str] = Query(None, description="Filter by course title"),
    teacher_id: Optional[int] = Query(None, description="Filter by teacher ID"),
    db: Session = Depends(get_db)
    ):
    filters = {}
    if title:
        filters["title"] = title
    if teacher_id:
        filters["teacher_id"] = teacher_id

    service = CourseService(db)
    return service.list_courses(skip=skip, limit=limit, filters=filters)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    service.delete_course(course_id)

@router.put("/{course_id}", response_model=CourseOut, status_code=status.HTTP_200_OK)
def update_course(course_id: int, course_in: CourseIn, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.update_course(course_id, course_in)