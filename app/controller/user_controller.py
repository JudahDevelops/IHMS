from app.controller.base import BaseController
from app.model.user import User
from app.schema.user import UserCreate, UserUpdate, UserResponse
from app.service.user_service import user_service

class UserController(BaseController[User, UserCreate, UserUpdate, UserResponse]):
    def __init__(self):
        super().__init__(service=user_service, model_name="User")

user_controller = UserController()

