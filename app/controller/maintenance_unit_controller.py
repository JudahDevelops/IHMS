from app.controller.base import BaseController
from app.model.maintenance_unit import MaintenanceUnit
from app.schema.maintenance_unit import (
    MaintenanceUnitCreate,
    MaintenanceUnitUpdate,
    MaintenanceUnitResponse,
)
from app.service.maintenance_unit_service import maintenance_unit_service

class MaintenanceUnitController(
    BaseController[MaintenanceUnit, MaintenanceUnitCreate, MaintenanceUnitUpdate, MaintenanceUnitResponse]
):
    def __init__(self):
        super().__init__(service=maintenance_unit_service, model_name="MaintenanceUnit")

maintenance_unit_controller = MaintenanceUnitController()

