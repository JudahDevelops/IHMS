from app.controller.base import BaseController
from app.model.hostel import Hostel
from app.schema.hostel import HostelCreate, HostelUpdate, HostelResponse
from app.service.hostel_service import hostel_service

class HostelController(BaseController[Hostel, HostelCreate, HostelUpdate, HostelResponse]):
    def __init__(self):
        super().__init__(service=hostel_service, model_name="Hostel")

hostel_controller = HostelController()

