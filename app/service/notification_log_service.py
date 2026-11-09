from app.model.notification_log import NotificationLog
from app.schema.notification_log import NotificationLogCreate, NotificationLogUpdate
from app.service.base import BaseService

class NotificationLogService(BaseService[NotificationLog, NotificationLogCreate, NotificationLogUpdate]):
    def __init__(self):
        super().__init__(
            model=NotificationLog,
            search_fields=[
                NotificationLog.recipient_email,
                NotificationLog.recipient_role,
                NotificationLog.subject,
                NotificationLog.body,
                NotificationLog.event_type,
                NotificationLog.status
            ]
        )

notification_log_service = NotificationLogService()

