from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.teacher import TeacherIn, TeacherOut
from app.services.teacher_service import TeacherService
from app.core.database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=TeacherOut, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherIn, db: Session = Depends(get_db)):
  service = TeacherService(db)
  return service.create_teacher(teacher)

@router.get("/{teacher_id}", response_model=TeacherOut, status_code=status.HTTP_200_OK)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
  service = TeacherService(db)
  return service.get_teacher(teacher_id)

@router.get("/", response_model=List[TeacherOut], status_code=status.HTTP_200_OK)
def list_teachers(
  skip: int = Query(0, description="Number of records to skip"),
  limit: int = Query(100, description="Number of records to return"),
  db: Session = Depends(get_db)
  ):

  service = TeacherService(db)
  return service.list_teachers(skip=skip, limit=limit)

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
  service = TeacherService(db)
  service.delete_teacher(teacher_id)

@router.put("/{teacher_id}", response_model=TeacherOut, status_code=status.HTTP_200_OK)
def update_course(teacher_id: int, course_in: TeacherIn, db: Session = Depends(get_db)):
  service = TeacherService(db)
  return service.update_teacher(teacher_id, course_in)