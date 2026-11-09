from datetime import datetime, timedelta
from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, ForeignKey,
    Enum as SQLEnum, CheckConstraint, Index
)
from sqlalchemy.orm import relationship
from app.database import Base
from app.model.enums import (
    ComplaintCategoryEnum, ComplaintUrgencyEnum, TriageSourceEnum, ComplaintStatusEnum
)

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_code = Column(String(50), unique=True, index=True, nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
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
    triage_source = Column(
        SQLEnum(TriageSourceEnum, native_enum=False),
        nullable=False,
        default=TriageSourceEnum.KEYWORD
    )
    triage_confidence = Column(Float, nullable=True)
    assigned_unit_id = Column(Integer, ForeignKey("maintenance_units.id", ondelete="RESTRICT"), nullable=False, index=True)
    assigned_officer_id = Column(Integer, ForeignKey("staff_profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    status = Column(
        SQLEnum(ComplaintStatusEnum, native_enum=False),
        nullable=False,
        default=ComplaintStatusEnum.OPEN,
        index=True
    )
    escalation_level = Column(Integer, default=0, nullable=False, index=True)  # 0: None, 1: Warden, 2: Student Affairs
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    deadline_at = Column(DateTime, nullable=False, index=True)
    escalated_to_warden_at = Column(DateTime, nullable=True)
    escalated_to_admin_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True, index=True)
    resolution_notes = Column(Text, nullable=True)
    student_feedback_rating = Column(Integer, nullable=True)
    student_feedback_comment = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("student_feedback_rating IS NULL OR (student_feedback_rating >= 1 AND student_feedback_rating <= 5)", name="chk_feedback_rating"),
        CheckConstraint("escalation_level >= 0 AND escalation_level <= 2", name="chk_escalation_level"),
        Index("ix_complaint_room_category_submitted", "room_id", "category", "submitted_at"),
    )

    student = relationship("StudentProfile", back_populates="complaints")
    room = relationship("Room", back_populates="complaints")
    assigned_unit = relationship("MaintenanceUnit", back_populates="complaints")
    assigned_officer = relationship("StaffProfile", back_populates="assigned_complaints")
    history_entries = relationship(
        "ComplaintHistory",
        back_populates="complaint",
        cascade="all, delete-orphan",
        order_by="ComplaintHistory.created_at"
    )
    notifications = relationship("NotificationLog", back_populates="complaint")

    @classmethod
    def calculate_deadline(cls, submitted_at: datetime, urgency: ComplaintUrgencyEnum) -> datetime:
        """Calculate resolution deadline d based on Table IV in research paper:
        - Urgent: 24 hours
        - Normal: 72 hours
        - Low: 7 days (168 hours)
        """
        if urgency == ComplaintUrgencyEnum.URGENT:
            return submitted_at + timedelta(hours=24)
        elif urgency == ComplaintUrgencyEnum.NORMAL:
            return submitted_at + timedelta(hours=72)
        else:  # LOW
            return submitted_at + timedelta(days=7)

    def __repr__(self):
        return f"<Complaint(code='{self.complaint_code}', cat='{self.category}', urgency='{self.urgency}', status='{self.status}')>"
