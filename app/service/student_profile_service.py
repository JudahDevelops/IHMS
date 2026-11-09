from app.model.student_profile import StudentProfile
from app.schema.student_profile import StudentProfileCreate, StudentProfileUpdate
from app.service.base import BaseService

class StudentProfileService(BaseService[StudentProfile, StudentProfileCreate, StudentProfileUpdate]):
    def __init__(self):
        super().__init__(
            model=StudentProfile,
            search_fields=[
                StudentProfile.matric_number,
                StudentProfile.department,
                StudentProfile.faculty,
                StudentProfile.emergency_contact_name,
                StudentProfile.emergency_contact_phone
            ]
        )

student_profile_service = StudentProfileService()

