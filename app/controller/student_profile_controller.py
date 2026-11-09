from app.controller.base import BaseController
from app.model.student_profile import StudentProfile
from app.schema.student_profile import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
)
from app.service.student_profile_service import student_profile_service

class StudentProfileController(
    BaseController[StudentProfile, StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse]
):
    def __init__(self):
        super().__init__(service=student_profile_service, model_name="StudentProfile")

student_profile_controller = StudentProfileController()

