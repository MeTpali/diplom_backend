from datetime import datetime
from pydantic import Field
from .base import BaseSchema

class AnalyticBase(BaseSchema):
    """Base schema for exam analytics data"""
    exam_id: int = Field(..., description="ID of the exam these analytics belong to")
    total_registrations: int = Field(..., description="Total number of exam registrations")
    total_paid: int = Field(..., description="Number of paid registrations")
    total_unpaid: int = Field(..., description="Number of unpaid registrations") 
    average_score: float | None = Field(None, description="Average exam score (if results available)")

class AnalyticCreate(AnalyticBase):
    """Schema for creating new analytics record"""
    pass

class AnalyticUpdate(BaseSchema):
    """Schema for updating existing analytics"""
    total_registrations: int | None = Field(None, description="New total registrations count")
    total_paid: int | None = Field(None, description="New count of paid registrations")
    total_unpaid: int | None = Field(None, description="New count of unpaid registrations")
    average_score: float | None = Field(None, description="New average exam score")

class AnalyticResponse(AnalyticBase):
    """Schema for analytics response with additional system fields"""
    id: int = Field(..., description="Unique analytics record ID")
    report_generated_at: datetime | None = Field(None, description="When this analytics report was generated") 