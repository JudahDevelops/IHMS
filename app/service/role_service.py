from app.model.role import Role
from app.schema.role import RoleCreate, RoleUpdate
from app.service.base import BaseService

class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        super().__init__(
            model=Role,
            search_fields=[Role.name, Role.description]
        )

role_service = RoleService()

