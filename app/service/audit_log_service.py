from app.model.audit_log import AuditLog
from app.schema.audit_log import AuditLogCreate, AuditLogUpdate
from app.service.base import BaseService

class AuditLogService(BaseService[AuditLog, AuditLogCreate, AuditLogUpdate]):
    def __init__(self):
        super().__init__(
            model=AuditLog,
            search_fields=[
                AuditLog.action,
                AuditLog.entity_name,
                AuditLog.ip_address,
                AuditLog.old_values,
                AuditLog.new_values
            ]
        )

audit_log_service = AuditLogService()

