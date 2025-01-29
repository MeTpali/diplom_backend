from datetime import datetime
from .base import BaseSchema

class RegistrationBase(BaseSchema):
    user_id: int
    exam_id: int
    status: str
    payment_status: str

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationUpdate(BaseSchema):
    status: str | None = None
    payment_status: str | None = None

class RegistrationResponse(RegistrationBase):
    id: int
    registered_at: datetime 