from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base


# 3. Модель Exam
class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Связи с другими таблицами
    registrations = relationship("Registration", back_populates="exam")
    results = relationship("Result", back_populates="exam")
    payments = relationship("Payment", back_populates="exam")
    notifications = relationship("Notification", back_populates="exam")
    location = relationship("Location", back_populates="exams")
    organizer = relationship("User", backref="organized_exams")
