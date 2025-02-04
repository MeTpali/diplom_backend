from datetime import datetime
from decimal import Decimal
from pydantic import Field
from .base import BaseSchema

class ExamBase(BaseSchema):
    """Base schema for exam data"""
    subject: str = Field(..., description="Subject of the exam", example="Mathematics")
    date: datetime = Field(..., description="Date and time when exam will be held")
    cost: Decimal = Field(..., description="Cost of the exam", example="99.99")
    location_id: int = Field(..., description="ID of the location where exam will take place")
    organizer_id: int = Field(..., description="ID of the exam organizer")

class ExamCreate(ExamBase):
    """Schema for creating a new exam"""
    pass

class ExamUpdate(BaseSchema):
    """Schema for updating an existing exam"""
    subject: str | None = Field(None, description="New exam subject")
    date: datetime | None = Field(None, description="New exam date and time")
    cost: Decimal | None = Field(None, description="New exam cost")
    location_id: int | None = Field(None, description="New location ID")

class ExamResponse(ExamBase):
    """Schema for exam response with additional system fields"""
    id: int = Field(..., description="Unique exam ID")