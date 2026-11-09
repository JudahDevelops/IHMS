from app.controller.base import BaseController
from app.model.complaint import Complaint
from app.schema.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
)
from app.service.complaint_service import complaint_service

class ComplaintController(
    BaseController[Complaint, ComplaintCreate, ComplaintUpdate, ComplaintResponse]
):
    def __init__(self):
        super().__init__(service=complaint_service, model_name="Complaint")

complaint_controller = ComplaintController()

