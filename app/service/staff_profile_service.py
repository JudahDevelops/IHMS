from app.model.staff_profile import StaffProfile
from app.schema.staff_profile import StaffProfileCreate, StaffProfileUpdate
from app.service.base import BaseService

class StaffProfileService(BaseService[StaffProfile, StaffProfileCreate, StaffProfileUpdate]):
    def __init__(self):
        super().__init__(
            model=StaffProfile,
            search_fields=[
                StaffProfile.staff_number,
                StaffProfile.designation,
                StaffProfile.office_location
            ]
        )

staff_profile_service = StaffProfileService()

