from datetime import datetime
from typing import Any, Dict, Union
import uuid
from sqlalchemy.orm import Session
from app.model.complaint import Complaint
from app.model.enums import ComplaintUrgencyEnum
from app.schema.complaint import ComplaintCreate, ComplaintUpdate
from app.service.base import BaseService

class ComplaintService(BaseService[Complaint, ComplaintCreate, ComplaintUpdate]):
    def __init__(self):
        super().__init__(
            model=Complaint,
            search_fields=[
                Complaint.complaint_code,
                Complaint.title,
                Complaint.description,
                Complaint.category,
                Complaint.urgency,
                Complaint.status,
                Complaint.resolution_notes
            ]
        )

    def create(self, db: Session, *, obj_in: Union[ComplaintCreate, Dict[str, Any]]) -> Complaint:
        if isinstance(obj_in, dict):
            data = obj_in.copy()
        else:
            data = obj_in.model_dump(exclude_unset=True)

        submitted_at = data.get("submitted_at") or datetime.utcnow()
        data["submitted_at"] = submitted_at

        if not data.get("complaint_code"):
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            short_id = uuid.uuid4().hex[:4].upper()
            data["complaint_code"] = f"CMP-{timestamp}-{short_id}"

        if not data.get("deadline_at"):
            urgency = data.get("urgency", ComplaintUrgencyEnum.NORMAL)
            data["deadline_at"] = Complaint.calculate_deadline(submitted_at, urgency)

        db_obj = Complaint(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

complaint_service = ComplaintService()

