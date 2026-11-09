from app.model.academic_session import AcademicSession
from app.schema.academic_session import AcademicSessionCreate, AcademicSessionUpdate
from app.service.base import BaseService

class AcademicSessionService(BaseService[AcademicSession, AcademicSessionCreate, AcademicSessionUpdate]):
    def __init__(self):
        super().__init__(
            model=AcademicSession,
            search_fields=[
                AcademicSession.session_name,
                AcademicSession.semester
            ]
        )

academic_session_service = AcademicSessionService()

