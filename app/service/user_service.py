from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.model.user import User
from app.model.role import Role
from app.schema.user import UserCreate, UserUpdate
from app.service.base import BaseService

class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(
            model=User,
            search_fields=[
                User.username,
                User.email,
                User.first_name,
                User.last_name,
                User.phone_number
            ]
        )

    def create(self, db: Session, *, obj_in: Union[UserCreate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            data = obj_in.copy()
            role_ids = data.pop("role_ids", [])
        else:
            data = obj_in.model_dump(exclude_unset=True)
            role_ids = data.pop("role_ids", [])

        db_user = User(**data)

        if role_ids:
            roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
            db_user.roles = roles

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        role_ids = update_data.pop("role_ids", None)
        if role_ids is not None:
            roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
            db_obj.roles = roles

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_service = UserService()

