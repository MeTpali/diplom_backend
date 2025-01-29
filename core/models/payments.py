from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric,
)
from sqlalchemy.orm import relationship
from .base import Base


# 7. Модель Payment
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False)  # completed/pending
    payment_date = Column(DateTime, nullable=True)

    # Связи
    user = relationship("User", back_populates="payments")
    exam = relationship("Exam", back_populates="payments")
