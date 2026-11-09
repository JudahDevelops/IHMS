from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import Base
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.service.base import BaseService

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    def __init__(
        self,
        service: BaseService[ModelType, CreateSchemaType, UpdateSchemaType],
        model_name: str,
    ):
        self.service = service
        self.model_name = model_name

    def get_paginated(
        self,
        db: Session,
        *,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> PaginatedResponse[Any]:
        items, total = self.service.get_multi(
            db,
            page=page,
            page_size=page_size,
            search=search,
            filters=filters,
        )
        return PaginatedResponse.create(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_by_id(self, db: Session, id: Any) -> ModelType:
        obj = self.service.get(db, id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model_name} with id {id} not found",
            )
        return obj

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            return self.service.create(db, obj_in=obj_in)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e.orig) if hasattr(e, 'orig') else str(e)}",
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating {self.model_name}: {str(e)}",
            )

    def update(self, db: Session, *, id: Any, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = self.get_by_id(db, id)
        try:
            return self.service.update(db, db_obj=db_obj, obj_in=obj_in)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e.orig) if hasattr(e, 'orig') else str(e)}",
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating {self.model_name}: {str(e)}",
            )

    def delete(self, db: Session, *, id: Any) -> MessageResponse:
        obj = self.service.delete(db, id=id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model_name} with id {id} not found",
            )
        return MessageResponse(
            message=f"{self.model_name} with id {id} deleted successfully"
        )

    def delete_all(self, db: Session, *, confirm: bool = False) -> DeleteAllResponse:
        if not confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Explicit confirmation required. Pass confirm=true query parameter to delete all {self.model_name} records.",
            )
        try:
            count = self.service.delete_all(db, confirm=confirm)
            return DeleteAllResponse(
                message=f"All {self.model_name} records deleted successfully",
                deleted_count=count,
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting all {self.model_name} records: {str(e)}",
            )

