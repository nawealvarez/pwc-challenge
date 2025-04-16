# === tests/services/test_student_service.py ===
from datetime import datetime, timezone
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, Request
from app.services.student_service import StudentService
from app.schemas.student import StudentIn, StudentOut
from app.models.student import Student
from app.schemas.pagination import PaginationParams

@pytest.fixture
def fake_db():
    return MagicMock()

@pytest.fixture
def fake_request():
    return MagicMock(spec=Request)

@pytest.fixture
def student_service(fake_db):
    return StudentService(fake_db)

def test_get_student_found(student_service, fake_request):
    student = Student(id=1, name="Alice", email="alice@example.com")
    student_service.repo.get_by_id = MagicMock(return_value=student)
    result = student_service.get_student(1, request=fake_request)
    assert result.id == 1

def test_get_student_not_found(student_service, fake_request):
    student_service.repo.get_by_id = MagicMock(return_value=None)
    with pytest.raises(HTTPException) as e:
        student_service.get_student(99, request=fake_request)
    assert e.value.status_code == 404

def test_create_student_success(student_service, fake_request):
    student_data = StudentIn(name="Bob", email="bob@example.com")
    student_service.repo.create = MagicMock(return_value=Student(id=2, **student_data.model_dump()))
    result = student_service.create_student(student_data, request=fake_request)
    assert result.name == "Bob"

def test_create_student_failure(student_service, fake_request):
    student_data = StudentIn(name="Error", email="error@example.com")
    student_service.repo.create = MagicMock(side_effect=Exception("fail"))
    with pytest.raises(HTTPException) as e:
        student_service.create_student(student_data, request=fake_request)
    assert e.value.status_code == 500

def test_list_students(student_service, fake_request):
    pagination = PaginationParams(page=1, size=10, search=None)
    student = StudentOut(id=1, name="Foo", email="foo@bar.com", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    student_service.repo.get_all = MagicMock(return_value=(1, 1, 1, [student]))
    response = student_service.list_students(pagination, filters=None, request=fake_request)
    assert response.total == 1
    assert response.items[0].name == "Foo"

def test_update_student_success(student_service, fake_request):
    student_data = StudentIn(name="Updated", email="updated@example.com")
    student_service.get_student = MagicMock()
    student_service.repo.update = MagicMock(return_value=Student(id=1, **student_data.model_dump()))
    result = student_service.update_student(1, student_data, request=fake_request)
    assert result.name == "Updated"

def test_update_student_failure(student_service, fake_request):
    student_data = StudentIn(name="Fail", email="fail@example.com")
    student_service.get_student = MagicMock()
    student_service.repo.update = MagicMock(side_effect=Exception("fail"))
    with pytest.raises(HTTPException) as e:
        student_service.update_student(1, student_data, request=fake_request)
    assert e.value.status_code == 500

def test_delete_student_success(student_service, fake_request):
    student_service.get_student = MagicMock()
    student_service.repo.delete = MagicMock(return_value=True)
    assert student_service.delete_student(1, request=fake_request) is None

def test_delete_student_failure(student_service, fake_request):
    student_service.get_student = MagicMock()
    student_service.repo.delete = MagicMock(return_value=False)
    with pytest.raises(HTTPException) as e:
        student_service.delete_student(1, request=fake_request)
    assert e.value.status_code == 500