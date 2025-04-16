from app.schemas.enrollment import EnrollmentOut, EnrollmentIn
from app.services.enrollment_service import EnrollmentService
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentIn, db: Session = Depends(get_db), request: Request = None):
    service = EnrollmentService(db)
    return service.create_enrollment(enrollment, request)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment: EnrollmentIn, db: Session = Depends(get_db), request: Request = None):
    service = EnrollmentService(db)
    service.delete_enrollment(enrollment, request)