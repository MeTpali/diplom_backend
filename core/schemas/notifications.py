from datetime import datetime
from pydantic import Field
from .base import BaseSchema

class NotificationBase(BaseSchema):
    """Base schema for notification data"""
    user_id: int = Field(..., description="ID of the user who will receive the notification")
    exam_id: int | None = Field(None, description="Optional ID of the related exam")
    type: str = Field(..., description="Type of the notification")
    message: str = Field(..., description="Content of the notification message")

class NotificationCreate(NotificationBase):
    """Schema for creating a new notification"""
    pass

class NotificationUpdate(BaseSchema):
    """Schema for updating an existing notification"""
    type: str | None = Field(None, description="New notification type")
    message: str | None = Field(None, description="New notification message")

class NotificationResponse(NotificationBase):
    """Schema for notification response with additional system fields"""
    id: int = Field(..., description="Unique notification ID")
    created_at: datetime = Field(..., description="When the notification was created") 