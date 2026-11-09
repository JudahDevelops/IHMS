import enum

class UserRoleEnum(str, enum.Enum):
    STUDENT = "student"
    MAINTENANCE_OFFICER = "maintenance_officer"
    HALL_WARDEN = "hall_warden"
    ADMINISTRATOR = "administrator"

class HostelGenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    MIXED = "mixed"

class StudentGenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"

class SemesterEnum(str, enum.Enum):
    FIRST = "first"
    SECOND = "second"

class AllocationStatusEnum(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class ComplaintCategoryEnum(str, enum.Enum):
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    CARPENTRY = "carpentry"
    SANITATION = "sanitation"
    OTHER = "other"

class ComplaintUrgencyEnum(str, enum.Enum):
    URGENT = "urgent"   # 24 hours deadline
    NORMAL = "normal"   # 72 hours deadline
    LOW = "low"         # 7 days deadline

class TriageSourceEnum(str, enum.Enum):
    KEYWORD = "keyword"
    JEV_AI = "jev_ai"
    MANUAL = "manual"

class ComplaintStatusEnum(str, enum.Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"

class ComplaintActionEnum(str, enum.Enum):
    CREATED = "created"
    TRIAGED = "triaged"
    ASSIGNED = "assigned"
    STATUS_CHANGED = "status_changed"
    ESCALATED_LEVEL_1 = "escalated_level_1"
    ESCALATED_LEVEL_2 = "escalated_level_2"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"
    FEEDBACK_SUBMITTED = "feedback_submitted"

class NotificationEventEnum(str, enum.Enum):
    ALLOCATION_CONFIRMED = "allocation_confirmed"
    COMPLAINT_LODGED = "complaint_lodged"
    COMPLAINT_ASSIGNED = "complaint_assigned"
    ESCALATION_LEVEL_1 = "escalated_level_1"
    ESCALATION_LEVEL_2 = "escalated_level_2"
    COMPLAINT_RESOLVED = "complaint_resolved"

class DeliveryStatusEnum(str, enum.Enum):
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"
