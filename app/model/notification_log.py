from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.model.enums import NotificationEventEnum, DeliveryStatusEnum

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String(100), nullable=False, index=True)
    recipient_role = Column(String(50), nullable=False)
    recipient_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    event_type = Column(
        SQLEnum(NotificationEventEnum, native_enum=False),
        nullable=False,
        index=True
    )
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="SET NULL"), nullable=True, index=True)
    status = Column(
        SQLEnum(DeliveryStatusEnum, native_enum=False),
        nullable=False,
        default=DeliveryStatusEnum.SENT,
        index=True
    )
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    complaint = relationship("Complaint", back_populates="notifications")
    recipient_user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<NotificationLog(id={self.id}, to='{self.recipient_email}', event='{self.event_type}', status='{self.status}')>"
