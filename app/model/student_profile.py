from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.model.enums import StudentGenderEnum

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    matric_number = Column(String(50), unique=True, index=True, nullable=False)
    gender = Column(SQLEnum(StudentGenderEnum, native_enum=False), nullable=False)
    level = Column(Integer, nullable=False)  # 100, 200, 300, 400, 500, etc.
    department = Column(String(100), nullable=False)
    faculty = Column(String(100), nullable=True)
    fee_cleared = Column(Boolean, default=False, nullable=False)  # Bursary fee clearance check
    fee_cleared_at = Column(DateTime, nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="student_profile")
    allocations = relationship("Allocation", back_populates="student", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="student")

    def __repr__(self):
        return f"<StudentProfile(id={self.id}, matric='{self.matric_number}', level={self.level})>"
