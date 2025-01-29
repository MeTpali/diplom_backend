from datetime import datetime
from .base import BaseSchema

class ResultBase(BaseSchema):
    exam_id: int
    user_id: int
    score: float | None = None
    grade: str | None = None

class ResultCreate(ResultBase):
    pass

class ResultUpdate(BaseSchema):
    score: float | None = None
    grade: str | None = None

class ResultResponse(ResultBase):
    id: int
    released_at: datetime | None = None 