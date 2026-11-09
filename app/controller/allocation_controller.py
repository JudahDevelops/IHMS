from app.controller.base import BaseController
from app.model.allocation import Allocation
from app.schema.allocation import (
    AllocationCreate,
    AllocationUpdate,
    AllocationResponse,
)
from app.service.allocation_service import allocation_service

class AllocationController(
    BaseController[Allocation, AllocationCreate, AllocationUpdate, AllocationResponse]
):
    def __init__(self):
        super().__init__(service=allocation_service, model_name="Allocation")

allocation_controller = AllocationController()

