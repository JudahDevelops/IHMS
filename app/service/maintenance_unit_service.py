from app.model.maintenance_unit import MaintenanceUnit
from app.schema.maintenance_unit import MaintenanceUnitCreate, MaintenanceUnitUpdate
from app.service.base import BaseService

class MaintenanceUnitService(BaseService[MaintenanceUnit, MaintenanceUnitCreate, MaintenanceUnitUpdate]):
    def __init__(self):
        super().__init__(
            model=MaintenanceUnit,
            search_fields=[
                MaintenanceUnit.code,
                MaintenanceUnit.name,
                MaintenanceUnit.description,
                MaintenanceUnit.email
            ]
        )

maintenance_unit_service = MaintenanceUnitService()

