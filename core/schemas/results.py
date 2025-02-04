from datetime import datetime
from pydantic import Field
from .base import BaseSchema

class ResultBase(BaseSchema):
    """Base schema for exam result data"""
    user_id: int = Field(..., description="ID of the user who took the exam")
    exam_id: int = Field(..., description="ID of the exam taken")
    score: int = Field(..., description="Exam score (0-100)")
    grade: str = Field(..., description="Letter grade (A/B/C/D/F)")

class ResultCreate(ResultBase):
    """Schema for creating a new exam result"""
    pass

class ResultUpdate(BaseSchema):
    """Schema for updating an existing result"""
    score: int | None = Field(None, description="Updated exam score")
    grade: str | None = Field(None, description="Updated letter grade")

class ResultResponse(ResultBase):
    """Schema for result response with additional system fields"""
    id: int = Field(..., description="Unique result ID")
    released_at: datetime | None = Field(None, description="When the result was released") 