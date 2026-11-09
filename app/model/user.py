from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), default="", nullable=False)
    last_name = Column(String(50), default="", nullable=False)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    roles = relationship("Role", secondary="user_role", back_populates="users")
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    staff_profile = relationship("StaffProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    allocations_administered = relationship("Allocation", back_populates="allocated_by", foreign_keys="Allocation.allocated_by_user_id")
    history_actions = relationship("ComplaintHistory", back_populates="performed_by", foreign_keys="ComplaintHistory.performed_by_user_id")
    notifications = relationship("NotificationLog", back_populates="recipient_user", foreign_keys="NotificationLog.recipient_user_id")
    audit_logs = relationship("AuditLog", back_populates="user", foreign_keys="AuditLog.user_id")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"