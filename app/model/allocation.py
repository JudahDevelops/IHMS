from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.model.enums import AllocationStatusEnum

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    bed_space_id = Column(Integer, ForeignKey("bed_spaces.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("academic_sessions.id", ondelete="RESTRICT"), nullable=False, index=True)
    status = Column(
        SQLEnum(AllocationStatusEnum, native_enum=False),
        nullable=False,
        default=AllocationStatusEnum.ACTIVE,
        index=True
    )
    # Anti-double-allocation marker: populated with bed_space_id ONLY when active.
    # In SQL standard and MySQL/PostgreSQL, NULL != NULL in unique indexes, so inactive records
    # with NULL active_bed_marker are ignored while active ones strictly enforce uniqueness.
    active_bed_marker = Column(Integer, nullable=True)

    # Anti-double-booking marker: populated with f"{student_id}_{session_id}" ONLY when active.
    active_student_session_marker = Column(String(100), nullable=True)

    allocated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    checked_in_at = Column(DateTime, nullable=True)
    checked_out_at = Column(DateTime, nullable=True)
    allocated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint("active_bed_marker", name="uq_active_bed_allocation"),
        UniqueConstraint("active_student_session_marker", name="uq_active_student_session_allocation"),
    )

    student = relationship("StudentProfile", back_populates="allocations")
    bed_space = relationship("BedSpace", back_populates="allocations")
    session = relationship("AcademicSession", back_populates="allocations")
    allocated_by = relationship("User", back_populates="allocations_administered")

    def sync_active_markers(self):
        """Helper to ensure active markers accurately reflect status."""
        if self.status == AllocationStatusEnum.ACTIVE:
            self.active_bed_marker = self.bed_space_id
            self.active_student_session_marker = f"{self.student_id}_{self.session_id}"
        else:
            self.active_bed_marker = None
            self.active_student_session_marker = None

    def __repr__(self):
        return f"<Allocation(id={self.id}, student_id={self.student_id}, bed_id={self.bed_space_id}, status='{self.status}')>"
