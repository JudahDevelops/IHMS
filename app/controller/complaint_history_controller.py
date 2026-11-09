from app.controller.base import BaseController
from app.model.complaint_history import ComplaintHistory
from app.schema.complaint_history import (
    ComplaintHistoryCreate,
    ComplaintHistoryUpdate,
    ComplaintHistoryResponse,
)
from app.service.complaint_history_service import complaint_history_service

class ComplaintHistoryController(
    BaseController[ComplaintHistory, ComplaintHistoryCreate, ComplaintHistoryUpdate, ComplaintHistoryResponse]
):
    def __init__(self):
        super().__init__(service=complaint_history_service, model_name="ComplaintHistory")

complaint_history_controller = ComplaintHistoryController()

