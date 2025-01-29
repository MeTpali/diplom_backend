from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from .base import Base


# 2. Модель Location
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    # Связь с экзаменами
    exams = relationship("Exam", back_populates="location")
