from app.api.v1.routes.course import router as course_router
from app.api.v1.routes.teacher import router as teacher_router
from app.api.v1.routes.student import router as student_router
from app.api.v1.routes.enrollment import router as enrollment_router

course = course_router
teacher = teacher_router
student = student_router
enrollment = enrollment_router