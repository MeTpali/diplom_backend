from datetime import datetime
from .base import BaseSchema

class NotificationBase(BaseSchema):
    user_id: int
    exam_id: int | None = None
    type: str
    message: str

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseSchema):
    type: str | None = None
    message: str | None = None

class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime 