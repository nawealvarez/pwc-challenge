from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.student import StudentIn, StudentOut
from app.services.student_service import StudentService
from app.core.database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentIn, db: Session = Depends(get_db)):
  service = StudentService(db)
  return service.create_student(student)

@router.get("/{student_id}", response_model=StudentOut, status_code=status.HTTP_200_OK)
def get_student(student_id: int, db: Session = Depends(get_db)):
  service = StudentService(db)
  return service.get_student(student_id)


@router.get("/", response_model=List[StudentOut], status_code=status.HTTP_200_OK)
def list_students(
  skip: int = Query(0, description="Number of records to skip"),
  limit: int = Query(100, description="Number of records to return"),
  course_id: Optional[int] = Query(None, description="Filter by Course ID"),
  db: Session = Depends(get_db)
  ):
  filters = {}
  if course_id:
      filters["course_id"] = course_id

  service = StudentService(db)
  return service.list_students(skip=skip, limit=limit, filters=filters)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
  service = StudentService(db)
  service.delete_student(student_id)

@router.put("/{student_id}", response_model=StudentOut, status_code=status.HTTP_200_OK)
def update_course(student_id: int, course_in: StudentIn, db: Session = Depends(get_db)):
  service = StudentService(db)
  return service.update_student(student_id, course_in)