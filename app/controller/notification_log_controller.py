from app.controller.base import BaseController
from app.model.notification_log import NotificationLog
from app.schema.notification_log import (
    NotificationLogCreate,
    NotificationLogUpdate,
    NotificationLogResponse,
)
from app.service.notification_log_service import notification_log_service

class NotificationLogController(
    BaseController[NotificationLog, NotificationLogCreate, NotificationLogUpdate, NotificationLogResponse]
):
    def __init__(self):
        super().__init__(service=notification_log_service, model_name="NotificationLog")

notification_log_controller = NotificationLogController()

