from app.model.bed_space import BedSpace
from app.schema.bed_space import BedSpaceCreate, BedSpaceUpdate
from app.service.base import BaseService

class BedSpaceService(BaseService[BedSpace, BedSpaceCreate, BedSpaceUpdate]):
    def __init__(self):
        super().__init__(
            model=BedSpace,
            search_fields=[BedSpace.bed_label]
        )

bed_space_service = BedSpaceService()

