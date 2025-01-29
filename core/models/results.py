from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from .base import Base


# 6. Модель Result
class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=True)
    grade = Column(String, nullable=True)
    released_at = Column(DateTime, nullable=True)

    # Связи
    exam = relationship("Exam", back_populates="results")
    user = relationship("User", back_populates="results")
