from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.model.enums import SemesterEnum

class AcademicSession(Base):
    __tablename__ = "academic_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String(50), nullable=False)
    semester = Column(
        SQLEnum(SemesterEnum, native_enum=False),
        nullable=False,
        default=SemesterEnum.FIRST
    )
    is_current = Column(Boolean, default=False, nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("session_name", "semester", name="uq_session_semester"),
    )

    allocations = relationship("Allocation", back_populates="session")

    def __repr__(self):
        return f"<AcademicSession(id={self.id}, name='{self.session_name}', semester='{self.semester}')>"
