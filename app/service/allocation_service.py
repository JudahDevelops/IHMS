from typing import Any, Dict, Union
from sqlalchemy.orm import Session
from app.model.allocation import Allocation
from app.model.bed_space import BedSpace
from app.model.enums import AllocationStatusEnum
from app.schema.allocation import AllocationCreate, AllocationUpdate
from app.service.base import BaseService

class AllocationService(BaseService[Allocation, AllocationCreate, AllocationUpdate]):
    def __init__(self):
        super().__init__(
            model=Allocation,
            search_fields=[Allocation.notes, Allocation.status]
        )

    def create(self, db: Session, *, obj_in: Union[AllocationCreate, Dict[str, Any]]) -> Allocation:
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.model_dump(exclude_unset=True)

        db_obj = Allocation(**data)
        db_obj.sync_active_markers()

        # Update bed space occupancy if allocation is active
        if db_obj.status == AllocationStatusEnum.ACTIVE:
            bed = db.query(BedSpace).filter(BedSpace.id == db_obj.bed_space_id).first()
            if bed:
                bed.is_occupied = True

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Allocation,
        obj_in: Union[AllocationUpdate, Dict[str, Any]]
    ) -> Allocation:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db_obj.sync_active_markers()

        # Update bed space occupancy based on status
        bed = db.query(BedSpace).filter(BedSpace.id == db_obj.bed_space_id).first()
        if bed:
            bed.is_occupied = (db_obj.status == AllocationStatusEnum.ACTIVE)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

allocation_service = AllocationService()

