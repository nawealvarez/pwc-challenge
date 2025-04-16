from datetime import datetime, timezone
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, Request
from app.services.teacher_service import TeacherService
from app.schemas.teacher import TeacherIn
from app.models.teacher import Teacher
from app.schemas.pagination import PaginationParams

@pytest.fixture
def fake_db():
    return MagicMock()

@pytest.fixture
def fake_request():
    return MagicMock(spec=Request)

@pytest.fixture
def teacher_service(fake_db):
    return TeacherService(fake_db)

def test_get_teacher_found(teacher_service, fake_request):
    teacher = Teacher(id=1, name="Alice Smith")
    teacher_service.repo.get_by_id = MagicMock(return_value=teacher)
    result = teacher_service.get_teacher(1, request=fake_request)
    assert result.id == 1

def test_get_teacher_not_found(teacher_service, fake_request):
    teacher_service.repo.get_by_id = MagicMock(return_value=None)
    with pytest.raises(HTTPException) as e:
        teacher_service.get_teacher(99, request=fake_request)
    assert e.value.status_code == 404

def test_create_teacher_success(teacher_service, fake_request):
    teacher_data = TeacherIn(name="John Doe")
    teacher_service.repo.create = MagicMock(return_value=Teacher(id=2, **teacher_data.model_dump()))
    result = teacher_service.create_teacher(teacher_data, request=fake_request)
    assert result.name == "John Doe"

def test_create_teacher_failure(teacher_service, fake_request):
    teacher_data = TeacherIn(name="Jane Fail")
    teacher_service.repo.create = MagicMock(side_effect=Exception("fail"))
    with pytest.raises(HTTPException) as e:
        teacher_service.create_teacher(teacher_data, request=fake_request)
    assert e.value.status_code == 500

def test_list_teachers(teacher_service, fake_request):
    pagination = PaginationParams(page=1, size=10, search=None)
    teacher = Teacher(id=1, name="Foo Bar", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    teacher_service.repo.get_all = MagicMock(return_value=(1, 1, 1, [teacher]))
    response = teacher_service.list_teachers(pagination, request=fake_request)
    assert response.total == 1
    assert response.items[0].name == "Foo Bar"

def test_update_teacher_success(teacher_service, fake_request):
    teacher_data = TeacherIn(name="Up Dated")
    teacher_service.get_teacher = MagicMock()
    teacher_service.repo.update = MagicMock(return_value=Teacher(id=1, **teacher_data.model_dump()))
    result = teacher_service.update_teacher(1, teacher_data, request=fake_request)
    assert result.name == "Up Dated"

def test_update_teacher_failure(teacher_service, fake_request):
    teacher_data = TeacherIn(name="Boom Fail")
    teacher_service.get_teacher = MagicMock()
    teacher_service.repo.update = MagicMock(side_effect=Exception("fail"))
    with pytest.raises(HTTPException) as e:
        teacher_service.update_teacher(1, teacher_data, request=fake_request)
    assert e.value.status_code == 500

def test_delete_teacher_success(teacher_service, fake_request):
    teacher_service.get_teacher = MagicMock()
    teacher_service.repo.delete = MagicMock(return_value=True)
    assert teacher_service.delete_teacher(1, request=fake_request) is None

def test_delete_teacher_failure(teacher_service, fake_request):
    teacher_service.get_teacher = MagicMock()
    teacher_service.repo.delete = MagicMock(return_value=False)
    with pytest.raises(HTTPException) as e:
        teacher_service.delete_teacher(1, request=fake_request)
    assert e.value.status_code == 500