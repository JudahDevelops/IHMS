from app.schema.common import (
    MessageResponse,
    DeleteAllResponse,
    PaginatedResponse,
)
from app.schema.role import RoleBase, RoleCreate, RoleUpdate, RoleResponse
from app.schema.user import UserBase, UserCreate, UserUpdate, UserResponse
from app.schema.maintenance_unit import (
    MaintenanceUnitBase,
    MaintenanceUnitCreate,
    MaintenanceUnitUpdate,
    MaintenanceUnitResponse,
)
from app.schema.hostel import HostelBase, HostelCreate, HostelUpdate, HostelResponse
from app.schema.room import RoomBase, RoomCreate, RoomUpdate, RoomResponse
from app.schema.bed_space import BedSpaceBase, BedSpaceCreate, BedSpaceUpdate, BedSpaceResponse
from app.schema.student_profile import (
    StudentProfileBase,
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
)
from app.schema.staff_profile import (
    StaffProfileBase,
    StaffProfileCreate,
    StaffProfileUpdate,
    StaffProfileResponse,
)
from app.schema.academic_session import (
    AcademicSessionBase,
    AcademicSessionCreate,
    AcademicSessionUpdate,
    AcademicSessionResponse,
)
from app.schema.allocation import (
    AllocationBase,
    AllocationCreate,
    AllocationUpdate,
    AllocationResponse,
)
from app.schema.complaint import (
    ComplaintBase,
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
)
from app.schema.complaint_history import (
    ComplaintHistoryBase,
    ComplaintHistoryCreate,
    ComplaintHistoryUpdate,
    ComplaintHistoryResponse,
)
from app.schema.notification_log import (
    NotificationLogBase,
    NotificationLogCreate,
    NotificationLogUpdate,
    NotificationLogResponse,
)
from app.schema.triage_keyword import (
    TriageKeywordBase,
    TriageKeywordCreate,
    TriageKeywordUpdate,
    TriageKeywordResponse,
)
from app.schema.audit_log import (
    AuditLogBase,
    AuditLogCreate,
    AuditLogUpdate,
    AuditLogResponse,
)

__all__ = [
    "MessageResponse",
    "DeleteAllResponse",
    "PaginatedResponse",
    "RoleBase", "RoleCreate", "RoleUpdate", "RoleResponse",
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    "MaintenanceUnitBase", "MaintenanceUnitCreate", "MaintenanceUnitUpdate", "MaintenanceUnitResponse",
    "HostelBase", "HostelCreate", "HostelUpdate", "HostelResponse",
    "RoomBase", "RoomCreate", "RoomUpdate", "RoomResponse",
    "BedSpaceBase", "BedSpaceCreate", "BedSpaceUpdate", "BedSpaceResponse",
    "StudentProfileBase", "StudentProfileCreate", "StudentProfileUpdate", "StudentProfileResponse",
    "StaffProfileBase", "StaffProfileCreate", "StaffProfileUpdate", "StaffProfileResponse",
    "AcademicSessionBase", "AcademicSessionCreate", "AcademicSessionUpdate", "AcademicSessionResponse",
    "AllocationBase", "AllocationCreate", "AllocationUpdate", "AllocationResponse",
    "ComplaintBase", "ComplaintCreate", "ComplaintUpdate", "ComplaintResponse",
    "ComplaintHistoryBase", "ComplaintHistoryCreate", "ComplaintHistoryUpdate", "ComplaintHistoryResponse",
    "NotificationLogBase", "NotificationLogCreate", "NotificationLogUpdate", "NotificationLogResponse",
    "TriageKeywordBase", "TriageKeywordCreate", "TriageKeywordUpdate", "TriageKeywordResponse",
    "AuditLogBase", "AuditLogCreate", "AuditLogUpdate", "AuditLogResponse",
]

