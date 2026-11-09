from app.model.triage_keyword import TriageKeyword
from app.schema.triage_keyword import TriageKeywordCreate, TriageKeywordUpdate
from app.service.base import BaseService

class TriageKeywordService(BaseService[TriageKeyword, TriageKeywordCreate, TriageKeywordUpdate]):
    def __init__(self):
        super().__init__(
            model=TriageKeyword,
            search_fields=[
                TriageKeyword.keyword,
                TriageKeyword.category,
                TriageKeyword.urgency
            ]
        )

triage_keyword_service = TriageKeywordService()

