from datetime import datetime
from .base import BaseSchema

class AnalyticBase(BaseSchema):
    exam_id: int
    total_registrations: int
    total_paid: int
    total_unpaid: int
    average_score: float | None = None

class AnalyticCreate(AnalyticBase):
    pass

class AnalyticUpdate(BaseSchema):
    total_registrations: int | None = None
    total_paid: int | None = None
    total_unpaid: int | None = None
    average_score: float | None = None

class AnalyticResponse(AnalyticBase):
    id: int
    report_generated_at: datetime | None = None 