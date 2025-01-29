from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base


# 1. Модель User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # student/organizer
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Связь с другими таблицами
    registrations = relationship("Registration", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    results = relationship("Result", back_populates="user")
