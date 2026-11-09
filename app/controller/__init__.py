from app.controller.base import BaseController
from app.controller.role_controller import role_controller, RoleController
from app.controller.user_controller import user_controller, UserController
from app.controller.maintenance_unit_controller import (
    maintenance_unit_controller,
    MaintenanceUnitController,
)
from app.controller.hostel_controller import hostel_controller, HostelController
from app.controller.room_controller import room_controller, RoomController
from app.controller.bed_space_controller import (
    bed_space_controller,
    BedSpaceController,
)
from app.controller.student_profile_controller import (
    student_profile_controller,
    StudentProfileController,
)
from app.controller.staff_profile_controller import (
    staff_profile_controller,
    StaffProfileController,
)
from app.controller.academic_session_controller import (
    academic_session_controller,
    AcademicSessionController,
)
from app.controller.allocation_controller import (
    allocation_controller,
    AllocationController,
)
from app.controller.complaint_controller import (
    complaint_controller,
    ComplaintController,
)
from app.controller.complaint_history_controller import (
    complaint_history_controller,
    ComplaintHistoryController,
)
from app.controller.notification_log_controller import (
    notification_log_controller,
    NotificationLogController,
)
from app.controller.triage_keyword_controller import (
    triage_keyword_controller,
    TriageKeywordController,
)
from app.controller.audit_log_controller import (
    audit_log_controller,
    AuditLogController,
)

__all__ = [
    "BaseController",
    "role_controller", "RoleController",
    "user_controller", "UserController",
    "maintenance_unit_controller", "MaintenanceUnitController",
    "hostel_controller", "HostelController",
    "room_controller", "RoomController",
    "bed_space_controller", "BedSpaceController",
    "student_profile_controller", "StudentProfileController",
    "staff_profile_controller", "StaffProfileController",
    "academic_session_controller", "AcademicSessionController",
    "allocation_controller", "AllocationController",
    "complaint_controller", "ComplaintController",
    "complaint_history_controller", "ComplaintHistoryController",
    "notification_log_controller", "NotificationLogController",
    "triage_keyword_controller", "TriageKeywordController",
    "audit_log_controller", "AuditLogController",
]

