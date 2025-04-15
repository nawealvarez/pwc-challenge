from fastapi import APIRouter
from app.api.v1.routes import course

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(course, prefix="/courses", tags=["Courses"])