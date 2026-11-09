from app.controller.base import BaseController
from app.model.bed_space import BedSpace
from app.schema.bed_space import BedSpaceCreate, BedSpaceUpdate, BedSpaceResponse
from app.service.bed_space_service import bed_space_service

class BedSpaceController(BaseController[BedSpace, BedSpaceCreate, BedSpaceUpdate, BedSpaceResponse]):
    def __init__(self):
        super().__init__(service=bed_space_service, model_name="BedSpace")

bed_space_controller = BedSpaceController()

