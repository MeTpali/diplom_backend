from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from .base import Base


# 8. Модель Analytics
class Analytic(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    total_registrations = Column(Integer, nullable=False)
    total_paid = Column(Integer, nullable=False)
    total_unpaid = Column(Integer, nullable=False)
    average_score = Column(Float, nullable=True)
    report_generated_at = Column(DateTime, nullable=True)

    # Связь
    exam = relationship("Exam", backref="analytics")
