from app.model.hostel import Hostel
from app.schema.hostel import HostelCreate, HostelUpdate
from app.service.base import BaseService

class HostelService(BaseService[Hostel, HostelCreate, HostelUpdate]):
    def __init__(self):
        super().__init__(
            model=Hostel,
            search_fields=[
                Hostel.name,
                Hostel.code,
                Hostel.description,
                Hostel.gender_target
            ]
        )

hostel_service = HostelService()

