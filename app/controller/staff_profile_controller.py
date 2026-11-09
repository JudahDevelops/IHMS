from app.controller.base import BaseController
from app.model.staff_profile import StaffProfile
from app.schema.staff_profile import (
    StaffProfileCreate,
    StaffProfileUpdate,
    StaffProfileResponse,
)
from app.service.staff_profile_service import staff_profile_service

class StaffProfileController(
    BaseController[StaffProfile, StaffProfileCreate, StaffProfileUpdate, StaffProfileResponse]
):
    def __init__(self):
        super().__init__(service=staff_profile_service, model_name="StaffProfile")

staff_profile_controller = StaffProfileController()

