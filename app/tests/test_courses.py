# === tests/services/test_course_service.py ===
from datetime import datetime, timezone
from app.models.teacher import Teacher
import pytest
from unittest.mock import MagicMock
from fastapi import Request, HTTPException
from app.services.course_service import CourseService
from app.schemas.course import CourseIn, CourseFilters, CourseOut
from app.schemas.pagination import PaginationParams
from app.models.course import Course

@pytest.fixture
def fake_db():
    return MagicMock()

@pytest.fixture
def fake_request():
    return MagicMock(spec=Request)

@pytest.fixture
def course_service(fake_db):
    return CourseService(fake_db)

def test_get_course_found(course_service, fake_db, fake_request):
    course = Course(id=1, title="Test Course", description="Test Desc", teacher_id=1)
    course_service.course_repo.get_by_id = MagicMock(return_value=course)
    result = course_service.get_course(1, request=fake_request)
    assert result.id == 1

def test_get_course_not_found(course_service, fake_db, fake_request):
    course_service.course_repo.get_by_id = MagicMock(return_value=None)
    with pytest.raises(HTTPException) as e:
        course_service.get_course(99, request=fake_request)
    assert e.value.status_code == 404

def test_create_course_success(course_service, fake_db, fake_request):
    course_data = CourseIn(title="Test", description="Desc", teacher_id=1)
    course_service.teacher_service.get_teacher = MagicMock()
    course_service.course_repo.create = MagicMock(return_value=Course(id=1, **course_data.model_dump()))
    result = course_service.create_course(course_data, request=fake_request)
    assert result.title == "Test"

def test_create_course_error(course_service, fake_db, fake_request):
    course_data = CourseIn(title="Error Course", description="Oops", teacher_id=2)
    course_service.teacher_service.get_teacher = MagicMock()
    course_service.course_repo.create = MagicMock(side_effect=Exception("fail"))
    with pytest.raises(HTTPException) as e:
        course_service.create_course(course_data, request=fake_request)
    assert e.value.status_code == 500

def test_list_courses(course_service, fake_db, fake_request):
    pagination = PaginationParams(page=1, size=10, search=None)
    teacher = Teacher(id=1, name="John Doe", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    mock_result = (1, 1, 1, [CourseOut(id=1, title="A", description="B", teacher_id=1, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), teacher=teacher)])
    course_service.course_repo.get_all = MagicMock(return_value=mock_result)
    response = course_service.list_courses(pagination, filters=None, request=fake_request)
    assert response.total == 1
    assert isinstance(response.items, list)
    assert response.items[0].title == "A"

def test_delete_course_success(course_service, fake_db, fake_request):
    course_service.get_course = MagicMock()
    course_service.course_repo.delete = MagicMock(return_value=True)
    assert course_service.delete_course(1, request=fake_request) is None

def test_delete_course_failure(course_service, fake_db, fake_request):
    course_service.get_course = MagicMock()
    course_service.course_repo.delete = MagicMock(return_value=False)
    with pytest.raises(HTTPException) as e:
        course_service.delete_course(2, request=fake_request)
    assert e.value.status_code == 500

def test_update_course_success(course_service, fake_db, fake_request):
    course_data = CourseIn(title="Updated", description="Updated desc", teacher_id=1)
    course_service.get_course = MagicMock()
    updated_course = Course(id=1, **course_data.model_dump())
    course_service.course_repo.update = MagicMock(return_value=updated_course)
    result = course_service.update_course(1, course_data, request=fake_request)
    assert result.title == "Updated"

def test_update_course_failure(course_service, fake_db, fake_request):
    course_data = CourseIn(title="Fail", description="Fail", teacher_id=1)
    course_service.get_course = MagicMock()
    course_service.course_repo.update = MagicMock(side_effect=Exception("fail"))
    with pytest.raises(HTTPException) as e:
        course_service.update_course(1, course_data, request=fake_request)
    assert e.value.status_code == 500
