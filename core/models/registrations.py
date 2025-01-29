from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base


# 4. Модель Registration
class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    status = Column(String, nullable=False)  # registered/cancelled
    payment_status = Column(String, nullable=False)  # paid/unpaid
    registered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Связи
    user = relationship("User", back_populates="registrations")
    exam = relationship("Exam", back_populates="registrations")
