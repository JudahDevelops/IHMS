from fastapi import APIRouter

from app.route.role import router as role_router
from app.route.user import router as user_router
from app.route.maintenance_unit import router as maintenance_unit_router
from app.route.hostel import router as hostel_router
from app.route.room import router as room_router
from app.route.bed_space import router as bed_space_router
from app.route.student_profile import router as student_profile_router
from app.route.staff_profile import router as staff_profile_router
from app.route.academic_session import router as academic_session_router
from app.route.allocation import router as allocation_router
from app.route.complaint import router as complaint_router
from app.route.complaint_history import router as complaint_history_router
from app.route.notification_log import router as notification_log_router
from app.route.triage_keyword import router as triage_keyword_router
from app.route.audit_log import router as audit_log_router

api_router = APIRouter()

api_router.include_router(role_router)
api_router.include_router(user_router)
api_router.include_router(maintenance_unit_router)
api_router.include_router(hostel_router)
api_router.include_router(room_router)
api_router.include_router(bed_space_router)
api_router.include_router(student_profile_router)
api_router.include_router(staff_profile_router)
api_router.include_router(academic_session_router)
api_router.include_router(allocation_router)
api_router.include_router(complaint_router)
api_router.include_router(complaint_history_router)
api_router.include_router(notification_log_router)
api_router.include_router(triage_keyword_router)
api_router.include_router(audit_log_router)

__all__ = [
    "api_router",
    "role_router",
    "user_router",
    "maintenance_unit_router",
    "hostel_router",
    "room_router",
    "bed_space_router",
    "student_profile_router",
    "staff_profile_router",
    "academic_session_router",
    "allocation_router",
    "complaint_router",
    "complaint_history_router",
    "notification_log_router",
    "triage_keyword_router",
    "audit_log_router",
]

