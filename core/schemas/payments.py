from datetime import datetime
from decimal import Decimal
from .base import BaseSchema

class PaymentBase(BaseSchema):
    user_id: int
    exam_id: int
    amount: Decimal
    status: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseSchema):
    status: str | None = None
    payment_date: datetime | None = None

class PaymentResponse(PaymentBase):
    id: int
    payment_date: datetime | None = None 