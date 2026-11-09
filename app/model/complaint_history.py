from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.model.enums import ComplaintActionEnum

class ComplaintHistory(Base):
    __tablename__ = "complaint_history"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(
        SQLEnum(ComplaintActionEnum, native_enum=False),
        nullable=False,
        index=True
    )
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=True)
    from_escalation_level = Column(Integer, nullable=True)
    to_escalation_level = Column(Integer, nullable=True)
    performed_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    complaint = relationship("Complaint", back_populates="history_entries")
    performed_by = relationship("User", back_populates="history_actions")

    def __repr__(self):
        return f"<ComplaintHistory(id={self.id}, complaint_id={self.complaint_id}, action='{self.action_type}')>"
