from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class BedSpace(Base):
    __tablename__ = "bed_spaces"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    bed_label = Column(String(10), nullable=False)
    is_occupied = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("room_id", "bed_label", name="uq_room_bed_label"),
    )

    room = relationship("Room", back_populates="bed_spaces")
    allocations = relationship("Allocation", back_populates="bed_space")

    def __repr__(self):
        return f"<BedSpace(id={self.id}, room_id={self.room_id}, label='{self.bed_label}')>"
