from app.controller.base import BaseController
from app.model.triage_keyword import TriageKeyword
from app.schema.triage_keyword import (
    TriageKeywordCreate,
    TriageKeywordUpdate,
    TriageKeywordResponse,
)
from app.service.triage_keyword_service import triage_keyword_service

class TriageKeywordController(
    BaseController[TriageKeyword, TriageKeywordCreate, TriageKeywordUpdate, TriageKeywordResponse]
):
    def __init__(self):
        super().__init__(service=triage_keyword_service, model_name="TriageKeyword")

triage_keyword_controller = TriageKeywordController()

