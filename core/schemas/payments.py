from datetime import datetime
from pydantic import Field
from .base import BaseSchema

class PaymentBase(BaseSchema):
    """Base schema for payment data"""
    user_id: int = Field(..., description="ID of the user making the payment")
    exam_id: int = Field(..., description="ID of the exam being paid for")
    status: str = Field(..., description="Current payment status (pending/completed/failed)")

class PaymentCreate(PaymentBase):
    """Schema for creating a new payment"""
    pass

class PaymentUpdate(BaseSchema):
    """Schema for updating an existing payment"""
    status: str | None = Field(None, description="New payment status")
    payment_date: datetime | None = Field(None, description="Date when payment was processed")

class PaymentResponse(PaymentBase):
    """Schema for payment response with additional system fields"""
    id: int = Field(..., description="Unique payment ID")
    payment_date: datetime | None = Field(None, description="Date when payment was processed") 