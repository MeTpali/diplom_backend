from datetime import datetime
from pydantic import Field
from .base import BaseSchema

class RegistrationBase(BaseSchema):
    """Base schema for exam registration data"""
    user_id: int = Field(..., description="ID of the user registering for exam")
    exam_id: int = Field(..., description="ID of the exam being registered for")
    status: str = Field(..., description="Registration status (pending/confirmed/cancelled)")
    payment_status: str = Field(..., description="Payment status (paid/unpaid)")

class RegistrationCreate(RegistrationBase):
    """Schema for creating a new registration"""
    pass

class RegistrationUpdate(BaseSchema):
    """Schema for updating an existing registration"""
    status: str | None = Field(None, description="New registration status")
    payment_status: str | None = Field(None, description="New payment status")

class RegistrationResponse(RegistrationBase):
    """Schema for registration response with additional system fields"""
    id: int = Field(..., description="Unique registration ID")
    registration_date: datetime = Field(..., description="When the registration was created") 