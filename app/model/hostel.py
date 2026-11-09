from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.model.enums import HostelGenderEnum

class Hostel(Base):
    __tablename__ = "hostels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(20), unique=True, index=True, nullable=False)
    gender_target = Column(
        SQLEnum(HostelGenderEnum, native_enum=False),
        nullable=False,
        default=HostelGenderEnum.MIXED
    )
    description = Column(String(255), nullable=True)
    total_capacity = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    rooms = relationship("Room", back_populates="hostel", cascade="all, delete-orphan")
    assigned_staff = relationship("StaffProfile", back_populates="assigned_hostel")

    def __repr__(self):
        return f"<Hostel(id={self.id}, code='{self.code}', name='{self.name}')>"
