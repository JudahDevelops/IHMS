from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id", ondelete="CASCADE"), nullable=False, index=True)
    room_number = Column(String(20), nullable=False)
    floor = Column(Integer, default=1, nullable=False)
    capacity = Column(Integer, default=4, nullable=False)
    current_occupancy = Column(Integer, default=0, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("hostel_id", "room_number", name="uq_hostel_room_number"),
    )

    hostel = relationship("Hostel", back_populates="rooms")
    bed_spaces = relationship("BedSpace", back_populates="room", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="room")

    def __repr__(self):
        return f"<Room(id={self.id}, hostel_id={self.hostel_id}, number='{self.room_number}')>"
