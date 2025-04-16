# === tests/services/test_enrollment_service.py ===
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, Request
from app.services.enrollment_service import EnrollmentService
from app.schemas.enrollment import EnrollmentIn
from app.models.enrollment import Enrollment

@pytest.fixture
def fake_db():
    return MagicMock()

@pytest.fixture
def fake_request():
    return MagicMock(spec=Request)

@pytest.fixture
def enrollment_service(fake_db):
    return EnrollmentService(fake_db)

def test_create_enrollment_success(enrollment_service, fake_request):
    enrollment = EnrollmentIn(student_id=1, course_id=1)
    enrollment_service.student_service.get_student = MagicMock()
    enrollment_service.course_service.create_course = MagicMock()
    enrollment_service.enrollment_repo.get_by_course_and_student = MagicMock(return_value=None)
    enrollment_service.enrollment_repo.create = MagicMock(return_value=Enrollment(id=123))

    result = enrollment_service.create_enrollment(enrollment, request=fake_request)
    assert result.id == 123

def test_create_enrollment_duplicate(enrollment_service, fake_request):
    enrollment = EnrollmentIn(student_id=1, course_id=1)
    enrollment_service.student_service.get_student = MagicMock()
    enrollment_service.course_service.create_course = MagicMock()
    enrollment_service.enrollment_repo.get_by_course_and_student = MagicMock(return_value=True)

    with pytest.raises(HTTPException) as e:
        enrollment_service.create_enrollment(enrollment, request=fake_request)
    assert e.value.status_code == 400

def test_create_enrollment_failure(enrollment_service, fake_request):
    enrollment = EnrollmentIn(student_id=1, course_id=1)
    enrollment_service.student_service.get_student = MagicMock()
    enrollment_service.course_service.create_course = MagicMock()
    enrollment_service.enrollment_repo.get_by_course_and_student = MagicMock(return_value=None)
    enrollment_service.enrollment_repo.create = MagicMock(side_effect=Exception("DB fail"))

    with pytest.raises(HTTPException) as e:
        enrollment_service.create_enrollment(enrollment, request=fake_request)
    assert e.value.status_code == 500

def test_delete_enrollment_success(enrollment_service, fake_request):
    enrollment = EnrollmentIn(student_id=1, course_id=1)
    mock_enrollment = Enrollment(id=42)
    enrollment_service.enrollment_repo.get_by_course_and_student = MagicMock(return_value=mock_enrollment)
    enrollment_service.enrollment_repo.delete = MagicMock(return_value=True)

    assert enrollment_service.delete_enrollment(enrollment, request=fake_request) is None

def test_delete_enrollment_not_found(enrollment_service, fake_request):
    enrollment = EnrollmentIn(student_id=1, course_id=1)
    enrollment_service.enrollment_repo.get_by_course_and_student = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as e:
        enrollment_service.delete_enrollment(enrollment, request=fake_request)
    assert e.value.status_code == 404

def test_delete_enrollment_failure(enrollment_service, fake_request):
    enrollment = EnrollmentIn(student_id=1, course_id=1)
    mock_enrollment = Enrollment(id=42)
    enrollment_service.enrollment_repo.get_by_course_and_student = MagicMock(return_value=mock_enrollment)
    enrollment_service.enrollment_repo.delete = MagicMock(return_value=False)

    with pytest.raises(HTTPException) as e:
        enrollment_service.delete_enrollment(enrollment, request=fake_request)
    assert e.value.status_code == 500