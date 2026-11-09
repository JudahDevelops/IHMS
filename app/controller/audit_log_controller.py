from app.controller.base import BaseController
from app.model.audit_log import AuditLog
from app.schema.audit_log import (
    AuditLogCreate,
    AuditLogUpdate,
    AuditLogResponse,
)
from app.service.audit_log_service import audit_log_service

class AuditLogController(
    BaseController[AuditLog, AuditLogCreate, AuditLogUpdate, AuditLogResponse]
):
    def __init__(self):
        super().__init__(service=audit_log_service, model_name="AuditLog")

audit_log_controller = AuditLogController()

