from app.controller.base import BaseController
from app.model.role import Role
from app.schema.role import RoleCreate, RoleUpdate, RoleResponse
from app.service.role_service import role_service

class RoleController(BaseController[Role, RoleCreate, RoleUpdate, RoleResponse]):
    def __init__(self):
        super().__init__(service=role_service, model_name="Role")

role_controller = RoleController()

