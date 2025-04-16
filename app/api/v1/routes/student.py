from app.schemas.pagination import PaginatedResponse, PaginationParams
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.student import StudentIn, StudentOut
from app.services.student_service import StudentService
from app.core.database import get_db
from typing import Optional

router = APIRouter()

@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentIn, db: Session = Depends(get_db)):
  service = StudentService(db)
  return service.create_student(student)

@router.get("/{student_id}", response_model=StudentOut, status_code=status.HTTP_200_OK)
def get_student(student_id: int, db: Session = Depends(get_db)):
  service = StudentService(db)
  return service.get_student(student_id)


@router.get("/", response_model=PaginatedResponse[StudentOut], status_code=status.HTTP_200_OK)
def list_students(
  page: int = Query(1, ge=1, description="Current page number"),
  size: int = Query(10, ge=1, le=100, description="Number of records per page"),
  search: Optional[str] = Query(None, description="Search by student name or email"),
  course_id: Optional[int] = Query(None, description="Filter by Course ID"),
  db: Session = Depends(get_db)
  ):
  pagination = PaginationParams(page=page, size=size, search=search)
  filters = {}
  if course_id:
      filters["course_id"] = course_id

  service = StudentService(db)
  return service.list_students(pagination=pagination, filters=filters)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
  service = StudentService(db)
  service.delete_student(student_id)

@router.put("/{student_id}", response_model=StudentOut, status_code=status.HTTP_200_OK)
def update_course(student_id: int, course_in: StudentIn, db: Session = Depends(get_db)):
  service = StudentService(db)
  return service.update_student(student_id, course_in)