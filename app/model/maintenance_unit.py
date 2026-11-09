from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class MaintenanceUnit(Base):
    __tablename__ = "maintenance_units"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    email = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    staff_members = relationship("StaffProfile", back_populates="maintenance_unit")
    complaints = relationship("Complaint", back_populates="assigned_unit")

    def __repr__(self):
        return f"<MaintenanceUnit(id={self.id}, code='{self.code}', name='{self.name}')>"
