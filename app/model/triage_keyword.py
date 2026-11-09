from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, UniqueConstraint
from app.database import Base
from app.model.enums import ComplaintCategoryEnum, ComplaintUrgencyEnum

class TriageKeyword(Base):
    __tablename__ = "triage_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(100), nullable=False, index=True)
    category = Column(
        SQLEnum(ComplaintCategoryEnum, native_enum=False),
        nullable=False,
        index=True
    )
    urgency = Column(
        SQLEnum(ComplaintUrgencyEnum, native_enum=False),
        nullable=False,
        index=True
    )
    weight = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("keyword", "category", name="uq_keyword_category"),
    )

    def __repr__(self):
        return f"<TriageKeyword(keyword='{self.keyword}', category='{self.category}', urgency='{self.urgency}')>"
