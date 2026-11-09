from app.model.complaint_history import ComplaintHistory
from app.schema.complaint_history import ComplaintHistoryCreate, ComplaintHistoryUpdate
from app.service.base import BaseService

class ComplaintHistoryService(BaseService[ComplaintHistory, ComplaintHistoryCreate, ComplaintHistoryUpdate]):
    def __init__(self):
        super().__init__(
            model=ComplaintHistory,
            search_fields=[
                ComplaintHistory.action_type,
                ComplaintHistory.from_status,
                ComplaintHistory.to_status,
                ComplaintHistory.notes
            ]
        )

complaint_history_service = ComplaintHistoryService()

