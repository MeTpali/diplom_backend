from datetime import datetime
from decimal import Decimal
from .base import BaseSchema

class ExamBase(BaseSchema):
    subject: str
    date: datetime
    cost: Decimal
    location_id: int
    organizer_id: int

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseSchema):
    subject: str | None = None
    date: datetime | None = None
    cost: Decimal | None = None
    location_id: int | None = None

class ExamResponse(ExamBase):
    id: int
    created_at: datetime 