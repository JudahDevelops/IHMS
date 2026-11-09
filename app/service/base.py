from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import or_, String, desc
from sqlalchemy.orm import Session
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], search_fields: Optional[List[Any]] = None):
        """
        Base service with standard CRUD, pagination, and real-time search capabilities.
        :param model: SQLAlchemy model class
        :param search_fields: List of model column attributes to search against in real time
        """
        self.model = model
        self.search_fields = search_fields or []

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Fetch a single record by its primary key ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Any] = None,
    ) -> Tuple[List[ModelType], int]:
        """
        Fetch a paginated list of records with optional real-time search and exact filters.
        Returns a tuple of (items, total_count).
        """
        query = db.query(self.model)

        # 1. Apply Exact Filters
        if filters:
            for field_name, value in filters.items():
                if value is not None and hasattr(self.model, field_name):
                    query = query.filter(getattr(self.model, field_name) == value)

        # 2. Real-Time Search across designated fields
        if search and self.search_fields:
            search_term = f"%{search.strip()}%"
            conditions = []
            for field in self.search_fields:
                conditions.append(field.cast(String).ilike(search_term))
            if conditions:
                query = query.filter(or_(*conditions))

        # 3. Total Count (optimized before pagination offset/limit)
        total = query.count()

        # 4. Ordering (default to id desc if available, else standard)
        if order_by is not None:
            query = query.order_by(order_by)
        elif hasattr(self.model, "id"):
            query = query.order_by(desc(self.model.id))

        # 5. Pagination offset & limit
        skip = max(0, (page - 1) * page_size)
        items = query.offset(skip).limit(page_size).all()

        return items, total

    def create(self, db: Session, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        """Insert a new record into the database."""
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.model_dump(exclude_unset=True)

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """Delete a single record by its primary key ID."""
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def delete_all(self, db: Session, *, confirm: bool = False) -> int:
        """
        Delete all records in the table.
        Requires explicit confirm=True parameter to prevent accidental deletion.
        """
        if not confirm:
            raise ValueError("Explicit confirmation (confirm=True) is required to delete all records.")

        deleted_count = db.query(self.model).delete(synchronize_session=False)
        db.commit()
        return deleted_count

