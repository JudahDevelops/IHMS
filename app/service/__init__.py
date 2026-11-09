from app.service.base import BaseService
from app.service.role_service import role_service, RoleService
from app.service.user_service import user_service, UserService
from app.service.maintenance_unit_service import maintenance_unit_service, MaintenanceUnitService
from app.service.hostel_service import hostel_service, HostelService
from app.service.room_service import room_service, RoomService
from app.service.bed_space_service import bed_space_service, BedSpaceService
from app.service.student_profile_service import student_profile_service, StudentProfileService
from app.service.staff_profile_service import staff_profile_service, StaffProfileService
from app.service.academic_session_service import academic_session_service, AcademicSessionService
from app.service.allocation_service import allocation_service, AllocationService
from app.service.complaint_service import complaint_service, ComplaintService
from app.service.complaint_history_service import complaint_history_service, ComplaintHistoryService
from app.service.notification_log_service import notification_log_service, NotificationLogService
from app.service.triage_keyword_service import triage_keyword_service, TriageKeywordService
from app.service.audit_log_service import audit_log_service, AuditLogService

__all__ = [
    "BaseService",
    "role_service", "RoleService",
    "user_service", "UserService",
    "maintenance_unit_service", "MaintenanceUnitService",
    "hostel_service", "HostelService",
    "room_service", "RoomService",
    "bed_space_service", "BedSpaceService",
    "student_profile_service", "StudentProfileService",
    "staff_profile_service", "StaffProfileService",
    "academic_session_service", "AcademicSessionService",
    "allocation_service", "AllocationService",
    "complaint_service", "ComplaintService",
    "complaint_history_service", "ComplaintHistoryService",
    "notification_log_service", "NotificationLogService",
    "triage_keyword_service", "TriageKeywordService",
    "audit_log_service", "AuditLogService",
]

