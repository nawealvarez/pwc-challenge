from fastapi import APIRouter
from app.api.v1.routes import course, teacher, student

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(course, prefix="/courses", tags=["Courses"])
api_v1_router.include_router(teacher, prefix="/teachers", tags=["Teachers"])
api_v1_router.include_router(student, prefix="/students", tags=["Students"])