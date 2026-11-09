from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class StaffProfile(Base):
    __tablename__ = "staff_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    staff_number = Column(String(50), unique=True, index=True, nullable=False)
    unit_id = Column(Integer, ForeignKey("maintenance_units.id", ondelete="SET NULL"), nullable=True, index=True)
    assigned_hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="SET NULL"), nullable=True, index=True)
    designation = Column(String(100), nullable=True)
    office_location = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="staff_profile")
    maintenance_unit = relationship("MaintenanceUnit", back_populates="staff_members")
    assigned_hostel = relationship("Hostel", back_populates="assigned_staff")
    assigned_complaints = relationship("Complaint", back_populates="assigned_officer")

    def __repr__(self):
        return f"<StaffProfile(id={self.id}, staff_number='{self.staff_number}', designation='{self.designation}')>"
