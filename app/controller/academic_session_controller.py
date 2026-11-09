from app.controller.base import BaseController
from app.model.academic_session import AcademicSession
from app.schema.academic_session import (
    AcademicSessionCreate,
    AcademicSessionUpdate,
    AcademicSessionResponse,
)
from app.service.academic_session_service import academic_session_service

class AcademicSessionController(
    BaseController[AcademicSession, AcademicSessionCreate, AcademicSessionUpdate, AcademicSessionResponse]
):
    def __init__(self):
        super().__init__(service=academic_session_service, model_name="AcademicSession")

academic_session_controller = AcademicSessionController()

