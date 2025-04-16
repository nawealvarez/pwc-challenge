from app.schemas.pagination import PaginatedResponse, PaginationParams
from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy.orm import Session
from app.schemas.teacher import TeacherIn, TeacherOut
from app.services.teacher_service import TeacherService
from app.core.database import get_db
from typing import Optional

router = APIRouter()

@router.post("/", response_model=TeacherOut, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherIn, db: Session = Depends(get_db), request: Request = None):
  service = TeacherService(db)
  return service.create_teacher(teacher, request)

@router.get("/{teacher_id}", response_model=TeacherOut, status_code=status.HTTP_200_OK)
def get_teacher(teacher_id: int, db: Session = Depends(get_db), request: Request = None):
  service = TeacherService(db)
  return service.get_teacher(teacher_id, request)

@router.get("/", response_model=PaginatedResponse[TeacherOut], status_code=status.HTTP_200_OK)
def list_teachers(
  page: int = Query(1, ge=1, description="Current page number"),
  size: int = Query(10, ge=1, le=100, description="Number of records per page"),
  search: Optional[str] = Query(None, description="Search by teacher name"),
  db: Session = Depends(get_db),
  request: Request = None
  ):
  pagination = PaginationParams(page=page, size=size, search=search)

  service = TeacherService(db)
  return service.list_teachers(pagination=pagination, request=request)

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db), request: Request = None):
  service = TeacherService(db)
  service.delete_teacher(teacher_id, request)

@router.put("/{teacher_id}", response_model=TeacherOut, status_code=status.HTTP_200_OK)
def update_teacher(teacher_id: int, teacher: TeacherIn, db: Session = Depends(get_db), request: Request = None):
  service = TeacherService(db)
  return service.update_teacher(teacher_id, teacher, request)